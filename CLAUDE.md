See DEVELOPING.md for the full guide to this repo (structure, timing constants, build and deploy workflow).

Key rules:
- Edit `show/template.html`, never `show/index.html`. Regenerate index.html with `cd skit && python3 build.py`.
- Scene content lives in `skit/spec.py`. `skit/gen.py` needs `OPENROUTER_API_KEY`.
- Show timing follows the audio clock: slide 0 = 등장 repeated, slide i = scene i-1 shown from `DING[i]`; `DING[i] = 16 + 4i` with `DING[24..27]=114,118,122,126` (the 2s gap merged into a 6s slide), pulse then next scene after `GAP=0.35`, `SYNC=0.15` (`[`/`]`), fade `127→137`.
- Pictograms are idealised and use white on indigo only, with no stagehand. Storyboards show props as they really look and draw the stagehand as a grey dashed figure.
- Test locally with `python3 -m http.server 8000` → http://localhost:8000/show/. Pushing to `main` redeploys GitHub Pages.
