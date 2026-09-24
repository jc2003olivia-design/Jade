# Videos

Video editing with the **video-use** skill (`.claude/skills/video-use/`).
Claude transcribes your clips, cuts filler words and dead air, color grades,
adds subtitles, and renders a finished `final.mp4`.

## How to use
1. Make a folder per video, e.g. `07-videos/2026-10-haul/`, and put the raw clips in it
   (or tell Claude which Google Drive folder they're in).
2. Ask Claude: *"edit the clips in 07-videos/2026-10-haul into a 30-second TikTok"*
   or *"inventory these takes and propose a strategy."*
3. Claude proposes a plan, waits for your OK, then renders to `<folder>/edit/final.mp4`.

Video files are not committed to git (too big), see `.gitignore`. Finished
videos get sent to you directly or uploaded to Google Drive.

## Setup each new cloud session
Automatic: `.claude/hooks/session-start.sh` installs ffmpeg and the Python
packages when a cloud session starts, and sets `ELEVENLABS_API_KEY` to a
placeholder (the environment proxy supplies the real key on requests to
api.elevenlabs.io).

## Ideas
- Depop / Poshmark listing videos
- TikTok / Reels hauls and "what sold this week"
- Pop-up market recaps
