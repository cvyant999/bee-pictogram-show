# BEE Pictogram Show

Tokyo-2020-style pictogram performance tool for the BEE 청년부 talent show (Gospel of John: 7 signs, 7 "I am"s, the cross, "feed my sheep").

**Live:** https://cvyant999.github.io/bee-pictogram-show/

## How it works
- A laptop in the front row points its webcam at the performers; the laptop's screen is mirrored to the projector.
- Each scene: the pictogram cue shows top-left over the live camera, countdown bottom-right.
- At 0: shutter + chime, the frame freezes, then a result card (pictogram ⟷ your photo in circles) holds, then the next scene.
- At the end, a gallery of all captures, with a download button.

## Controls
Space pause · → capture now / skip · ← previous · F fullscreen · M mute · Esc menu.
Settings: camera, mirror, seconds per scene (default 15), result-card length, music (Track A / B / A→B / your own file).

## Music
The original Tokyo 2020 pictogram background music was an unreleased commissioned piece. `audio/bgm_A.mp3` and `bgm_B.mp3` are original AI-generated tracks (Google Lyria) in the same quirky techno-pop style.
Shutter/chime sound is synthesized in-browser (no file).

## Run locally
`python3 -m http.server` in this folder → http://localhost:8000 (the camera needs https or localhost).
