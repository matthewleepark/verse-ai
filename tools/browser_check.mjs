// End-to-end check of the poster in a real (headless) Microsoft Edge.
//
//   node tools/browser_check.mjs [output-folder]
//
// Build the page first (python visual.py --no-open). This drives web/today.html through
// the Chrome DevTools Protocol: forward/backward transitions, rapid clicks, Today,
// keyboard, Context and Share staying in sync, reduced motion, and a phone layout
// with swipes. Screenshots go to the output folder. Exits 1 if any check fails.

import { spawn } from "node:child_process";
import { existsSync, mkdirSync, mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { pathToFileURL } from "node:url";

const EDGE = [
  "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
  "C:/Program Files/Microsoft/Edge/Application/msedge.exe",
].find(existsSync);
// Headless Edge renders WebGL on the CPU, so draw the sea at low resolution to keep frames
// coming quickly (pass --full to test at full resolution).
const FULL = process.argv.includes("--full");
const PAGE = pathToFileURL(resolve("web/today.html")).href + (FULL ? "" : "?lowres");
process.argv = process.argv.filter((a) => a !== "--full");
const OUT = resolve(process.argv[2] ?? mkdtempSync(join(tmpdir(), "verse-ai-check-")));
const PORT = 9400 + Math.floor(Math.random() * 500);   // avoid clashing with another run
mkdirSync(OUT, { recursive: true });

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const results = [];
function check(name, ok, detail = "") {
  results.push({ name, ok });
  console.log(`${ok ? "PASS" : "FAIL"}  ${name}${detail ? `  (${detail})` : ""}`);
}

// ---------- Start Edge and connect ----------
const browser = spawn(EDGE, [
  "--headless=new", `--remote-debugging-port=${PORT}`,
  `--user-data-dir=${mkdtempSync(join(tmpdir(), "verse-ai-edge-"))}`,
  "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--window-size=1600,900",
  "--no-first-run", "about:blank",
], { stdio: "ignore" });
// Always close the browser, even if a step throws.
process.on("exit", () => browser.kill());
process.on("uncaughtException", (err) => { console.error(err); process.exit(1); });
process.on("unhandledRejection", (err) => { console.error(err); process.exit(1); });

let target;
for (let i = 0; i < 50 && !target; i++) {
  await sleep(200);
  try {
    const list = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
    target = list.find((t) => t.type === "page");
  } catch { /* not up yet */ }
}
if (!target) throw new Error("Edge did not start");

const ws = new WebSocket(target.webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener("open", r, { once: true }));
let nextId = 0;
const pending = new Map();
const pageErrors = [];
ws.addEventListener("message", (msg) => {
  const data = JSON.parse(msg.data);
  if (data.id && pending.has(data.id)) {
    const { resolve: ok, reject } = pending.get(data.id);
    pending.delete(data.id);
    data.error ? reject(new Error(`${data.error.message}`)) : ok(data.result);
  } else if (data.method === "Runtime.exceptionThrown") {
    const message = data.params.exceptionDetails.exception?.description ?? data.params.exceptionDetails.text;
    console.log(`      page error: ${message}`);
    pageErrors.push(message);
  } else if (data.method === "Runtime.consoleAPICalled" && data.params.type === "error") {
    pageErrors.push(data.params.args.map((a) => a.value ?? a.description).join(" "));
  }
});
const send = (method, params = {}) => new Promise((ok, reject) => {
  const id = ++nextId;
  pending.set(id, { resolve: ok, reject });
  ws.send(JSON.stringify({ id, method, params }));
});
async function evaluate(expression) {
  const r = await send("Runtime.evaluate", { expression, awaitPromise: true, returnByValue: true });
  if (r.exceptionDetails) throw new Error(r.exceptionDetails.exception?.description ?? r.exceptionDetails.text);
  return r.result.value;
}
const state = () => evaluate("verseAI.state()");
const verseFor = (o) => evaluate(`verseAI.verseFor(${o})`);
async function shot(name) {
  const { data } = await send("Page.captureScreenshot", { format: "png" });
  writeFileSync(join(OUT, `${name}.png`), Buffer.from(data, "base64"));
}
async function waitFor(expression, ms = 15000) {
  const end = Date.now() + ms;
  while (Date.now() < end) {
    try { if (await evaluate(expression)) return true; } catch { /* page still loading */ }
    await sleep(100);
  }
  throw new Error(`Timed out waiting for: ${expression}`);
}
async function open(url = PAGE) {
  // Go via a blank page so a URL that only differs by #date still reloads.
  await send("Page.navigate", { url: "about:blank" });
  await sleep(100);
  await send("Page.navigate", { url });
  await waitFor("window.verseAI && verseAI.ready");
  await sleep(300);
}
async function click(selector) {
  const box = await evaluate(`(() => { const r = document.querySelector(${JSON.stringify(selector)}).getBoundingClientRect(); return { x: r.x + r.width / 2, y: r.y + r.height / 2 }; })()`);
  // Move there first, as a real mouse would, then press and release.
  await send("Input.dispatchMouseEvent", { type: "mouseMoved", x: box.x, y: box.y });
  for (const type of ["mousePressed", "mouseReleased"]) {
    await send("Input.dispatchMouseEvent", { type, x: box.x, y: box.y, button: "left", clickCount: 1 });
  }
}
const KEYS = { ArrowLeft: 37, ArrowRight: 39, Escape: 27, c: 67, t: 84 };
async function press(key) {
  const code = key.length === 1 ? `Key${key.toUpperCase()}` : key;
  const text = key.length === 1 ? key : undefined;
  await send("Input.dispatchKeyEvent", { type: "keyDown", key, code, windowsVirtualKeyCode: KEYS[key], text });
  await send("Input.dispatchKeyEvent", { type: "keyUp", key, code, windowsVirtualKeyCode: KEYS[key] });
}
const ghostTransform = () => evaluate(`(() => {
  const g = document.querySelector('.heading.ghost');
  const a = g && g.getAnimations()[0];
  return a ? a.effect.getKeyframes().at(-1).transform : null;
})()`);

await send("Page.enable");
await send("Runtime.enable");
await send("Emulation.setDeviceMetricsOverride", { width: 1600, height: 900, deviceScaleFactor: 1, mobile: false });

// ---------- 1. Opening state ----------
await open();
let s = await state();
await shot("01-today");
check("opens on today's verse", s.offset === s.todayOffset, `offset ${s.offset}, today ${s.todayOffset}`);
check("shows the Today badge", s.shownDate.includes("Today"), s.shownDate);
check("caption, title and share text match the verse", s.shownRef === s.ref && s.shownTitle === s.word && s.shareText.includes(s.ref), s.ref);
check("address remembers the day", s.hash === `#${s.iso}`, s.hash);
const startRef = s.ref;

// How smoothly does this (software-rendered) browser draw? Real GPUs are much faster.
const fps = await evaluate("new Promise(r => { let n = 0; const t0 = performance.now(); const f = () => { n++; performance.now() - t0 < 2000 ? requestAnimationFrame(f) : r(n / 2); }; requestAnimationFrame(f); })");
console.log(`(headless Edge draws about ${fps.toFixed(1)} frames per second here)`);
const settled = async () => {
  const t0 = Date.now();
  try {
    await waitFor("verseAI.state().ghosts === 0", 10000);
  } catch (err) {
    console.log("      leftover copies:", JSON.stringify(await evaluate(`[...document.querySelectorAll('.ghost')].map(g => ({
      cls: g.className, anims: g.getAnimations().map(a => [a.playState, Math.round(a.currentTime), a.effect.getTiming().duration, a.pending]) }))`)));
    console.log("      browser clock:", JSON.stringify(await evaluate(`new Promise(r => {
      const t0 = document.timeline.currentTime; let frames = 0;
      const f = () => { frames++; requestAnimationFrame(f); }; requestAnimationFrame(f);
      setTimeout(() => r({ timelineAdvancedMs: Math.round(document.timeline.currentTime - t0), framesIn1s: frames, visibility: document.visibilityState }), 1000);
    })`)));
    throw err;
  }
  return Date.now() - t0;
};

// ---------- 2. Forward ----------
await click("#next");
s = await state();
const next1 = await verseFor(1);
check("next: day changes immediately", s.offset === 1 && s.ref === next1, `${s.ref}`);
check("next: caption and share text already show the new verse", s.shownRef === next1 && s.shareText.includes(next1));
check("next: outgoing title and caption fade out as copies", s.ghosts === 2, `ghosts ${s.ghosts}`);
const fwdTransform = await ghostTransform();
await sleep(120); await shot("02-forward-120ms");
await sleep(260); await shot("03-forward-380ms");
await sleep(320); await shot("04-forward-700ms");
const fwdMs = await settled();
s = await state();
await shot("05-forward-done");
check("next: outgoing copies are cleaned up", s.ghosts === 0, `${fwdMs} ms after the last screenshot`);
check("next: Today badge gone, title updated", !s.shownDate.includes("Today") && s.shownTitle === s.word, s.word);

// ---------- 3. Backward (keyboard) ----------
await press("ArrowLeft");
const backTransform = await ghostTransform();
await sleep(120); await shot("06-back-120ms");
await sleep(260); await shot("07-back-380ms");
await settled();
s = await state();
check("back: returns to the same verse", s.offset === 0 && s.ref === startRef, s.ref);
check("forward and backward use different motion",
  fwdTransform?.includes("scale(1.12)") && backTransform?.includes("scale(0.88)"),
  `forward "${fwdTransform}", back "${backTransform}"`);

// ---------- 4. Rapid clicks ----------
for (let i = 0; i < 6; i++) { await click("#next"); await sleep(30); }
s = await state();
check("rapid clicks: every click counts", s.offset === 6, `offset ${s.offset}`);
check("rapid clicks: never more than one set of outgoing copies", s.ghosts <= 2, `ghosts ${s.ghosts}`);
await settled();
s = await state();
const ref6 = await verseFor(6);
check("rapid clicks: ends on the right verse with no leftovers",
  s.ref === ref6 && s.shownRef === ref6 && s.shownTitle === s.word && s.ghosts === 0, `${s.shownRef}, ghosts ${s.ghosts}`);
await shot("08-after-rapid-clicks");
for (let i = 0; i < 6; i++) { await press("ArrowLeft"); await sleep(30); }
await settled();
s = await state();
check("rapid keys back: ends on today", s.offset === 0 && s.ref === startRef, `offset ${s.offset}`);

// ---------- 5. Today button and editing the address ----------
for (let i = 0; i < 3; i++) { await press("ArrowRight"); await sleep(80); }
await settled();
await click("#today");
await settled();
s = await state();
check("Today returns to the real date", s.offset === s.todayOffset && s.shownDate.includes("Today"), s.shownDate);
const iso3 = await evaluate("isoDate(3)");
await evaluate(`location.hash = '${iso3}'`);
await sleep(300);
s = await state();
check("editing the #date in the address moves to that day", s.offset === 3 && s.ref === (await verseFor(3)), s.iso);
await settled();
await click("#today");
await settled();

// ---------- 6. Context stays in sync ----------
await press("c");
await sleep(500);
s = await state();
check("Context opens on the current verse", s.drawerRef === s.ref, `${s.drawerRef}`);
await press("ArrowRight");
s = await state();
check("Context follows navigation immediately", s.drawerRef === s.ref && s.ref === (await verseFor(1)), `${s.drawerRef}`);
await sleep(1300);
await shot("09-context-open");
const coveredButtons = await evaluate(`[...document.querySelectorAll('.controls > button, #shareBtn')].filter(b => {
  const r = b.getBoundingClientRect(); const hit = document.elementFromPoint(r.x + r.width / 2, r.y + r.height / 2);
  return !(hit === b || b.contains(hit)); }).map(b => b.id)`);
check("with Context open, the day and Share buttons are still clickable", coveredButtons.length === 0, coveredButtons.join(", "));
await press("Escape");
await waitFor("!document.getElementById('drawer').classList.contains('open')", 3000).catch(() => {});
check("Escape closes Context", !(await evaluate("document.getElementById('drawer').classList.contains('open')")));
await sleep(400);

// ---------- 7. Share uses the verse on screen ----------
await press("ArrowRight");
await sleep(1300);
s = await state();
const ref2 = await verseFor(2);
check("share text is the displayed verse", s.ref === ref2 && s.shareText.includes(ref2) && s.shareText.includes(s.shownText), ref2);
const menuVisible = "!document.getElementById('shareMenu').hidden";
await evaluate(`window.__events = []; for (const type of ['pointerdown', 'pointerup', 'click']) document.addEventListener(type, e => __events.push(type + ':' + (e.target.id || e.target.className || e.target.tagName)), true);
  new MutationObserver(() => __events.push('menu ' + (document.getElementById('shareMenu').hidden ? 'closed' : 'opened'))).observe(document.getElementById('shareMenu'), { attributes: true });`);
await click("#shareBtn");
const menuOpen = await waitFor(menuVisible, 5000).catch(() => false);
if (!menuOpen) console.log("      events around the Share click:", (await evaluate("__events")).join(" | "));
await shot("10-share-menu");
await click("#copyVerse");
await waitFor(`document.getElementById('toast').textContent.includes(${JSON.stringify(ref2)})`, 5000).catch(() => {});
const copyToast = await evaluate("document.getElementById('toast').textContent");
check("share menu opens; Copy verse names the displayed verse", menuOpen && copyToast === `Copied ${ref2}`, copyToast);
await click("#shareBtn");
await waitFor(menuVisible, 5000);
await click("#saveImage");
const slug = ref2.replace(/[^A-Za-z0-9]+/g, "-");
await waitFor(`document.getElementById('toast').textContent.startsWith('Saved')`, 10000).catch(() => {});
const saveToast = await evaluate("document.getElementById('toast').textContent");
check("Save image is named for the displayed verse", saveToast.includes(slug), saveToast);
const card = await evaluate("verseAI.shareCard()");
writeFileSync(join(OUT, "11-share-card.png"), Buffer.from(card.split(",")[1], "base64"));

// ---------- 8. Arrow keys leave text fields alone ----------
const before = (await state()).offset;
await evaluate("(() => { const i = document.createElement('input'); i.id = 'probe'; document.body.append(i); i.focus(); })()");
await press("ArrowRight");
await sleep(200);
check("arrow keys don't navigate while typing", (await state()).offset === before);
await evaluate("document.getElementById('probe').remove()");

// ---------- 9. Reopening keeps your place ----------
const iso5 = await evaluate("(() => { const d = new Date(Date.UTC(...DATA.startDate.split('-').map((n, i) => i === 1 ? n - 1 : +n)) + 5 * 86400000); return d.toISOString().slice(0, 10); })()");
await open(`${PAGE}#${iso5}`);
s = await state();
check("reloading with #date reopens that day", s.offset === 5 && s.iso === iso5, s.iso);

// ---------- 10. Reduced motion ----------
await send("Emulation.setEmulatedMedia", { features: [{ name: "prefers-reduced-motion", value: "reduce" }] });
await open();
await click("#next");
await sleep(40);
// Only the verse-change animations (CSS hover/press transitions are checked by the media query).
const rm = await evaluate(`document.getAnimations()
  .filter(a => !(a instanceof CSSTransition) && !(a instanceof CSSAnimation))
  .map(a => ({
    duration: a.effect.getTiming().duration,
    moves: a.effect.getKeyframes().some(k => (k.transform && k.transform !== 'none') || (k.filter && k.filter !== 'none')),
  }))`);
const cssTransition = await evaluate("getComputedStyle(document.querySelector('.controls button')).transitionDuration");
await shot("12-reduced-motion");
await settled();
s = await state();
check("reduced motion: button and drawer transitions are switched off", cssTransition.split(",").every((d) => parseFloat(d) < 0.001), cssTransition);
check("reduced motion: only short fades, no movement",
  rm.length > 0 && rm.every((a) => a.duration <= 200 && !a.moves), JSON.stringify(rm));
check("reduced motion: still navigates and cleans up", s.offset === 1 && s.ghosts === 0);
await send("Emulation.setEmulatedMedia", { features: [] });

// ---------- 11. Phone layout and swipes ----------
await send("Emulation.setDeviceMetricsOverride", { width: 390, height: 844, deviceScaleFactor: 2, mobile: true });
await send("Emulation.setTouchEmulationEnabled", { enabled: true, maxTouchPoints: 5 });
await open();
await shot("13-phone");
const overflow = await evaluate(`[...document.querySelectorAll('.controls button, .caption, .heading')]
  .filter(el => { const r = el.getBoundingClientRect(); return r.left < 0 || r.right > innerWidth + 1; })
  .map(el => el.id || el.className)`);
check("phone: controls, title and caption fit on screen", overflow.length === 0, overflow.join(", "));
const tapTargets = await evaluate(`[...document.querySelectorAll('.controls > button, #shareBtn')]
  .map(b => b.getBoundingClientRect()).every(r => r.height >= 44 && r.width >= 44)`);
check("phone: buttons are at least 44px", tapTargets);
// Each simulated touch gets 15 seconds; a stuck one is reported instead of hanging the run.
const touch = (params) => Promise.race([
  send("Input.dispatchTouchEvent", params),
  sleep(15000).then(() => { throw new Error(`touch event "${params.type}" got no reply in 15 s`); }),
]);
const swipe = async (fromX, toX) => {
  try {
    await touch({ type: "touchStart", touchPoints: [{ x: fromX, y: 560 }] });
    for (let i = 1; i <= 6; i++) {
      await touch({ type: "touchMove", touchPoints: [{ x: fromX + ((toX - fromX) * i) / 6, y: 562 }] });
      await sleep(16);
    }
    await touch({ type: "touchEnd", touchPoints: [] });
  } catch (err) {
    check("phone: simulated swipe was delivered", false, err.message);
  }
};
await swipe(320, 80);
await sleep(200);
s = await state();
check("phone: swipe left goes to the next verse", s.offset === 1, `offset ${s.offset}`);
await sleep(700); await shot("14-phone-after-swipe");
await swipe(80, 320);
await sleep(1300);
s = await state();
check("phone: swipe right goes back", s.offset === 0, `offset ${s.offset}`);

// ---------- 12. A page built yesterday opens on the real today ----------
await send("Emulation.setTouchEmulationEnabled", { enabled: false });
await send("Emulation.setDeviceMetricsOverride", { width: 1600, height: 900, deviceScaleFactor: 1, mobile: false });
const { identifier } = await send("Page.addScriptToEvaluateOnNewDocument", { source: `{
  const RealDate = Date, shift = 86400000;   // pretend the clock is one day later
  globalThis.Date = class extends RealDate { constructor(...a) { a.length ? super(...a) : super(RealDate.now() + shift); } static now() { return RealDate.now() + shift; } };
}` });
await open();
s = await state();
check("a page built yesterday opens on today's verse", s.offset === 1 && s.todayOffset === 1 && s.shownDate.includes("Today") && s.ref === (await verseFor(1)), `${s.iso}, ${s.ref}`);
await send("Page.removeScriptToEvaluateOnNewDocument", { identifier });

check("no errors in the page", pageErrors.length === 0, pageErrors.join(" | "));

ws.close();
browser.kill();
const failed = results.filter((r) => !r.ok).length;
console.log(`\n${results.length - failed}/${results.length} checks passed. Screenshots: ${OUT}`);
process.exit(failed ? 1 : 0);
