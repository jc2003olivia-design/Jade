#!/bin/bash
# Installs what the video-use skill needs (ffmpeg + Python deps) in cloud sessions.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

if ! command -v ffmpeg >/dev/null 2>&1; then
  apt-get update -qq
  DEBIAN_FRONTEND=noninteractive apt-get install -y -qq ffmpeg >/dev/null
fi

pip install -q --root-user-action=ignore requests librosa matplotlib pillow numpy reportlab

# The environment proxy injects the real ElevenLabs key on api.elevenlabs.io.
# transcribe.py only needs the variable to be non-empty.
if [ -z "${ELEVENLABS_API_KEY:-}" ] && [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  echo 'export ELEVENLABS_API_KEY=injected-by-proxy' >> "$CLAUDE_ENV_FILE"
fi
