#!/usr/bin/env bash
# Purpose: Text-to-speech for agent voices using OpenAI TTS API
# Author: BBB Project
# Date: 2026-03-24
# Input: Agent name (blacksmith|bookworm|artist|adversary) and text to speak
# Output: Plays audio through speakers

set -euo pipefail

# ── Source API key if not already set ──────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -z "${OPENAI_API_KEY:-}" && -f "$SCRIPT_DIR/.env" ]]; then
    # shellcheck disable=SC1091
    source "$SCRIPT_DIR/.env"
fi

# ── Configuration ──────────────────────────────────────────────────────
OPENAI_API_KEY="${OPENAI_API_KEY:?Error: OPENAI_API_KEY environment variable is not set}"
TTS_MODEL="${TTS_MODEL:-tts-1-hd}"
SPEED="${TTS_SPEED:-1.0}"
AUDIO_DIR="$SCRIPT_DIR/outputs/audio"

# ── Voice mapping (compatible with bash 3) ─────────────────────────────
# Blacksmith (Northern Ontario / Shoresy) → onyx: deep, gruff, masculine
# Bookworm (kind, wholesome, organized)   → nova: warm, clear, friendly
# Artist (florid, poetic, theatrical)     → fable: expressive, British-inflected
# Adversary (passive-aggressive, dry)     → shimmer: cool, poised, cutting
get_voice() {
    case "$1" in
        blacksmith) echo "onyx" ;;
        bookworm)   echo "nova" ;;
        artist)     echo "fable" ;;
        adversary)  echo "shimmer" ;;
        conductor)  echo "alloy" ;;
        *)          return 1 ;;
    esac
}

# ── Usage ──────────────────────────────────────────────────────────────
usage() {
    cat <<EOF
Usage: ./speak.sh <agent> <text>
       echo "text" | ./speak.sh <agent>

Agents: blacksmith, bookworm, artist, adversary, conductor

Options:
  --hd          Use tts-1-hd model (higher quality, slower)
  --speed N     Playback speed 0.25-4.0 (default: 1.0)
  --save        Save audio file but don't play it
  --no-play     Alias for --save

Examples:
  ./speak.sh blacksmith "Oh beauty, she compiled first try, not bad at all eh"
  ./speak.sh adversary "I'm sure that AUC is completely real."
  echo "A visual sonnet emerges" | ./speak.sh artist
  ./speak.sh --hd blacksmith "Big moment here, boys"
EOF
    exit 1
}

# ── Parse flags ────────────────────────────────────────────────────────
SHOULD_PLAY=true

while [[ $# -gt 0 ]]; do
    case "$1" in
        --hd)
            TTS_MODEL="tts-1-hd"
            shift
            ;;
        --speed)
            SPEED="$2"
            shift 2
            ;;
        --save|--no-play)
            SHOULD_PLAY=false
            shift
            ;;
        -h|--help)
            usage
            ;;
        *)
            break
            ;;
    esac
done

# ── Validate agent ────────────────────────────────────────────────────
AGENT="${1:?Error: Agent name required. Use: blacksmith, bookworm, artist, adversary, conductor}"
AGENT=$(echo "$AGENT" | tr '[:upper:]' '[:lower:]')

VOICE=$(get_voice "$AGENT") || {
    echo "Error: Unknown agent '$AGENT'. Use: blacksmith, bookworm, artist, adversary, conductor" >&2
    exit 1
}

# ── Get text ───────────────────────────────────────────────────────────
shift
if [[ $# -gt 0 ]]; then
    TEXT="$*"
elif [[ ! -t 0 ]]; then
    TEXT=$(cat)
else
    echo "Error: No text provided. Pass as argument or pipe via stdin." >&2
    usage
fi

if [[ -z "$TEXT" ]]; then
    echo "Error: Empty text." >&2
    exit 1
fi

# ── Ensure output directory exists ─────────────────────────────────────
mkdir -p "$AUDIO_DIR"

# ── Call OpenAI TTS API ────────────────────────────────────────────────
TIMESTAMP=$(date +%s)
OUTFILE="${AUDIO_DIR}/${AGENT}_${TIMESTAMP}.mp3"

# Escape text for JSON
JSON_TEXT=$(printf '%s' "$TEXT" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')

HTTP_CODE=$(curl -s -w '%{http_code}' -o "$OUTFILE" \
    "https://api.openai.com/v1/audio/speech" \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{
        \"model\": \"$TTS_MODEL\",
        \"input\": $JSON_TEXT,
        \"voice\": \"$VOICE\",
        \"speed\": $SPEED
    }")

if [[ "$HTTP_CODE" != "200" ]]; then
    echo "Error: OpenAI API returned HTTP $HTTP_CODE" >&2
    cat "$OUTFILE" >&2
    rm -f "$OUTFILE"
    exit 1
fi

echo "Audio saved: $OUTFILE (voice=$VOICE, model=$TTS_MODEL)"

# ── Play audio ─────────────────────────────────────────────────────────
if [[ "$SHOULD_PLAY" == true ]]; then
    afplay "$OUTFILE"
fi
