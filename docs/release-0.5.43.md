# zumbra-nes 0.5.43

Audio cleanup hotfix.

## Changes

- Uses a desktop-only cleaned audio drain path.
- Adds a light 3-tap low-pass filter to reduce static/harsh edges.
- Adds tiny chunk-edge softening to reduce pops between SDL queue writes.
- Raises the desktop audio queue guard slightly to reduce starvation without adding large latency.
- Keeps input, settings, F12 quit and Xbox-style gamepad behavior from 0.5.41/0.5.42.
