#!/bin/bash
# Double-click (Mac) to run the show without internet. Keep this window open during the show.
cd "$(dirname "$0")"
PORT=8765
(sleep 1; open "http://localhost:$PORT/") &
python3 -m http.server $PORT
