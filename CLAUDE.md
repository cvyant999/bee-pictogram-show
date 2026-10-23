See DEVELOPING.md for the full guide to this repo (structure, timing constants, build and deploy workflow).

Key rules:
- Edit `show/template.html`, never `show/index.html`. Regenerate index.html with `cd skit && python3 build.py`.
- Scene content lives in `skit/spec.py`. `skit/gen.py` needs `OPENROUTER_API_KEY`.
- Show timing follows the audio clock: `BEAT[k] = 16 + 4k` (with `BEAT[24]=110` and `BEAT[25]=114`), `LEAD=0.4`, `AMEN=118`, fade `124→140`.
- Test locally with `python3 -m http.server 8000` → http://localhost:8000/show/. Pushing to `main` redeploys GitHub Pages.
