# Build Log, Artifact 2: verse-ai

**Tools:** Claude Code (building), Claude chat (planning)  
**Repo:** https://github.com/matthewleepark/verse-ai  
**Date:** 2026-10-14 to 2026-10-16

- I started by planning a Python command-line app called verse-ai for my school project. The original idea was to get a daily Bible verse about patience, empathy, conflict resolution, or integrity from an online Bible website. I wanted each verse explained in three parts: Universal Wisdom, Historical Context, and Theological Meaning. I also planned an interactive mode with follow-up questions, summaries, and a journal saved as Markdown files. I set up the project files and CLAUDE.md and started with the verse fetcher.
- When I tried to run the project, I found out Python wasn't installed on my computer. I downloaded and installed Python so I could continue building and testing the app.
- I added the three-part verse breakdown, follow-up questions, interactive mode, and journal using the Claude API. Since I didn't have an API key yet, I tested the features using a fake version of Claude to check how the app would behave.
- I decided to include the whole Bible in the NIV instead of getting verses from a website and wanted to pair two verses each day for endless combinations. After looking into copyright, I learned that I couldn't bundle the NIV in the project, so I switched to the Berean Standard Bible, which is public domain. I chose to pair one wisdom verse with a random partner verse.
- I also wanted the app to work offline. I added a local copy of the Bible so the verses could be accessed without an internet connection. I also made the breakdowns save locally so the journal and saved content would still be available offline.
- I prepared the project for my Artifact 2 submission by uploading it to my verse-ai GitHub repository. I also looked into whether the AI features would work outside of testing, how to get an API key, and what options I had if I ran out of credits. I tested the AI connection against a stand-in server and looked into free alternatives.
- I eventually decided to make verse-ai a completely free daily Bible study without any APIs. I removed the AI features and focused on adding a streak tracker, reading history, and a daily reading plan. I also wanted to open the app easily without having to use VS Code, so I added a Desktop shortcut and a Start menu entry.
- I wanted a visual experience with a picture of Jesus that stayed still while the water moved, along with a different Bible verse each day. I used three reference posters to communicate the style I wanted. Instead of copying someone else's design, I used a public-domain 1860 woodcut depicting Jesus catching Peter.
- I changed the daily reading from two verses to one new verse per day. I also wanted the poster to be interactive, so I added a list of 416 verses with no repeats for over a year, clickable water ripples, arrow-key navigation between days, an About panel, and a way to pause the movement.
- I continued refining the design to make the poster fill the entire screen. I wanted comic-book-style waves, a more readable font, bigger buttons at the top, a Context tab instead of About, and more detail about the passage.
- I focused on making the transitions between days feel smoother and more cinematic. I also added a share button and made sure the navigation always matched the verse displayed on the screen. I tested the changes in a real browser and fixed the bugs I found.
- After trying the comic-book style, I decided it didn't fit the message I wanted to communicate. I changed the design to look more like an old engraved Bible, using parchment and traditional scripture-inspired details.
- I then decided to try a darker and more striking design with charcoal, gold, and crimson. I wanted the verse to remain the main focus, with smooth transitions and an option to share the image, while keeping the overall design clean. I planned out the visual direction, implemented the changes, and reviewed the result in a browser.
- During the redesign, I reached my usage limit before finishing everything, so I continued working on the project once my usage reset.
- While testing the Context panel, I noticed that the text could scroll behind the buttons at the top. I took a screenshot of the issue and used it to identify what needed to be fixed.
- I decided that I didn't need to spend more time adjusting the phone layout because I only needed the project to work on desktop computers, including Windows and Mac. I left the additional phone-layout fixes out of scope.
- For the final submission check, I planned to run the tests and app, review CLAUDE.md and .gitignore, finish this build log, and update my portfolio card.

## Changes I made by hand

- Created the verse-ai repository on GitHub.
- Ran the Git commit and push commands myself.
- Tested the poster in my browser and reported the Context panel overlapping the buttons at the top.
- Shared three reference posters to help communicate the visual style I wanted.

## Decisions

1. **Why did you remove the Claude breakdowns and make the app fully offline?**
   - I made the app fully offline because I didn't have usage credits and didn't want the app to depend on them. I wanted something that would work automatically, with or without internet, and would be useful without needing to pay for an API.

2. **Why did you go from a pair of verses each day to one verse?**
   - Having two verses every day felt like too much information to cover. I wanted to focus on one verse at a time so there would be more room to think about the passage and what it means.

3. **Why the Berean Standard Bible?**
   - I switched to the Berean Standard Bible because of copyright restrictions. I needed a translation that I could include in the project without bundling copyrighted text.

4. **Why did the poster go comic → parchment → dark?**
   - The comic style didn't feel professional enough, and it distracted from the message. I tried a more traditional scripture style, then moved toward a darker design because I wanted something more visually striking without taking attention away from the verse.

5. **What did you leave out on purpose?**
   - I left out extra features and distractions that could take the focus away from the Bible passage. I wanted the experience to feel simple, meaningful, and easy to use.

## Issues

- I changed the design several times, going from comic-book style to parchment and then to a dark theme. This took more time and usage than I originally expected.
- I ran out of usage credits partway through the dark redesign, so I had to wait until my usage reset before continuing.
- Claude Code sometimes indicated that a feature was finished when there were still problems. For example, I found the Context panel scrolling behind the top buttons when I tested the app myself, so I reported the issue and had it fixed.
- Some GitHub updates bundled several changes together, so the commit history doesn't show every individual step separately.
- The `.env` rule was removed from `.gitignore` after I removed the AI features. I added the rule back to keep environment files excluded. No `.env` file was ever uploaded to GitHub.
