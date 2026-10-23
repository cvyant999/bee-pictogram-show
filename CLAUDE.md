See DEVELOPING.md for the full guide to this repo (structure, timing constants, build and deploy workflow).

Key rules:
- Edit `show/template.html`, never `show/index.html`. Regenerate index.html with `cd skit && python3 build.py`.
- Scene content lives in `skit/spec.py`. `skit/gen.py` needs `OPENROUTER_API_KEY`.
- Show timing follows the audio clock: `DING[k] = 16 + 4k` (with `DING[24]=110`, `DING[25]=114`, `DING[26]=118`), pulse then next scene after `GAP=0.35`, `SYNC=0.15` (`[`/`]`), fade `124→140`.
- Pictograms are idealised and use white on indigo only, with no stagehand. Storyboards show props as they really look and draw the stagehand as a grey dashed figure.
- Test locally with `python3 -m http.server 8000` → http://localhost:8000/show/. Pushing to `main` redeploys GitHub Pages.
