# Build Log, Artifact 2: verse-ai

Tools: Claude Code (building), Claude chat (planning). Repo: https://github.com/matthewleepark/verse-ai. Date: 2026-10-14 to 2026-10-16

- I asked Claude Code to build a Python command-line app called verse-ai for a school project. It would get a daily Bible verse about patience, empathy, conflict resolution or integrity from an online Bible website, explain it in three parts (Universal Wisdom, Historical Context, Theological Meaning), and have an interactive mode for follow-up questions, a summary, and a journal saved as Markdown files. I asked it to set up the project files and a CLAUDE.md, and to start with the verse fetcher.
- Claude Code set up the project and wrote the verse fetcher. Python wasn't installed on my computer, so it couldn't run the code yet.
- I said "do it for me." Claude Code installed Python, then built the three-part breakdown and the follow-up questions using the Claude API, plus the interactive mode and the journal. It tested everything with a fake version of Claude, since I didn't have an API key.
- I asked to load the whole Bible in the NIV instead of using the website, and to pair two verses each day for endless combinations. Claude Code explained that the NIV is copyrighted and can't be bundled, so I chose the Berean Standard Bible, which is public domain. I picked "a wisdom verse plus a random partner verse" for the pairing.
- I asked for it to work offline as well. Claude Code saved the Bible on my computer and made the AI breakdowns save locally, so verses and the journal work without internet.
- I asked how to put it on GitHub for my Artifact 2 submission. Claude Code uploaded it to my verse-ai repo.
- I asked whether it would really work, how to get an API key, and what to do without credits. Claude Code checked the AI part against a stand-in server, explained how to get a key, and suggested free options.
- I asked to make it a free daily Bible study with no APIs. I chose to remove the AI completely and to add a streak, history, and a daily reading plan. I also asked for an easy way to open it without VS Code, so Claude Code added a Desktop icon and a Start menu entry.
- I asked for a picture of Jesus that stays still while the water moves, showing a verse each day. I shared three reference posters. Claude Code used a public-domain 1860 woodcut of Jesus catching Peter, because my reference images were other people's designs.
- I asked to stop pairing verses and show just one new verse each day, and to make it interactive. Claude Code wrote a list of 416 verses (no repeats for over a year) and added clicking the water for ripples, arrow keys to change the day, an About panel, and pausing.
- I asked for the poster to fill the whole screen, with comic-book style waves, a more readable font, a Context tab instead of About, bigger buttons at the top, and more detail.
- I gave Claude Code detailed instructions for smooth, cinematic transitions between days, along with a share button and navigation that always matches the verse on screen. It built and tested them in a real browser and fixed bugs it found along the way.
- I said I didn't like the comic style and asked for a scripture style. Claude Code changed it to an old engraved-Bible look on parchment.
- I asked for a more stunning look: a dark theme with charcoal, gold, and crimson, the verse as the main focus, smooth transitions, and a share image, while keeping it clean. Claude Code planned the design, built it, and had it reviewed in a browser.
- I hit my usage limit partway through, then told Claude Code to continue once it reset.
- I found a bug where text in the Context panel scrolled behind the buttons at the top and sent a screenshot. Claude Code fixed it.
- I decided the phone layout didn't need more work and only desktop (Windows or Mac) mattered, so the phone fixes were left out.
- I asked Claude Code to check the project for submission: run the tests and the app, check CLAUDE.md and .gitignore, write this log, and update my portfolio card.

## Changes I made by hand

- Created the verse-ai repo on GitHub.
- Ran the commit and push commands myself.
- Tested the poster in my browser and reported the Context panel overlapping the buttons.
- Shared three reference posters for the poster style.

## Decisions

1. Why did you remove the Claude breakdowns and make the app fully offline?
   - I made the app fully offline because I don't have usage credits and can't rely on them. Keeping it offline, so it works automatically with or without internet, felt like the best way to learn and be efficient.
2. Why did you go from a pair of verses each day to one verse?
   - Pairing verses each day felt overwhelming, with a lot of information to cover. Having one verse leaves room for more ideas and thoughts about that passage.
3. Why the Berean Standard Bible?
   - I had to use the Berean Standard Bible because of copyright.
4. Why did the poster go comic → parchment → dark?
   - The comic style felt a little unprofessional, and the message didn't really come through.
5. What did you leave out on purpose?
   - I left out any distractions that could take the focus away from the passage.

## Issues

- I changed the design many times (comic, then parchment, then dark), which used up a lot of usage and time.
- I ran out of usage credits partway through the dark design, and the work had to wait until it reset.
- Claude Code sometimes thought something was done when it wasn't, like the Context panel bug I found myself. I had to test it and tell it what to fix.
- Some saves to GitHub bundled several changes together, so the history doesn't show every step on its own.
- The .env rule was dropped from .gitignore when the AI was removed, so I added it back. No .env file was ever uploaded.
