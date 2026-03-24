#!/bin/bash
# ~/Desktop/bbb-project/start_demo.sh
#
# Opens 5 windows on external display:
#   Left 42%:  VSCode (Conductor) with Claude Code extension
#   Right 54%: 4 iTerm2 windows (Blacksmith, Bookworm, Artist, Adversary)
#              stacked vertically, each spanning the agent area width

CODE="/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code"

# ── External display logical coordinates ──────────────────────────────────────
# LG 4K display: 1920x1080 logical points, positioned above laptop display
DISPLAY_X=-92
DISPLAY_Y=-1080
DISPLAY_WIDTH=1920
DISPLAY_HEIGHT=1080
MENU_BAR=25

# ── Layout geometry ───────────────────────────────────────────────────────────
# VSCode (Conductor): left ~52%  (990px wide on 1920px display)
VSCODE_LEFT=$DISPLAY_X
VSCODE_TOP=$(( DISPLAY_Y + MENU_BAR ))
VSCODE_RIGHT=$(( DISPLAY_X + 990 ))
VSCODE_BOTTOM=$(( DISPLAY_Y + DISPLAY_HEIGHT ))

# Agent windows: right side, 888px wide, stacked vertically
AGENT_LEFT=$(( DISPLAY_X + 993 ))
AGENT_RIGHT=$(( DISPLAY_X + 993 + 888 ))
AGENT_TOP=$(( DISPLAY_Y + MENU_BAR ))
AGENT_BOTTOM=$(( DISPLAY_Y + DISPLAY_HEIGHT ))
USABLE_HEIGHT=$(( AGENT_BOTTOM - AGENT_TOP ))
AGENT_ROW1_TOP=$AGENT_TOP
AGENT_ROW2_TOP=$(( AGENT_TOP + USABLE_HEIGHT / 4 ))
AGENT_ROW3_TOP=$(( AGENT_TOP + USABLE_HEIGHT / 2 ))
AGENT_ROW4_TOP=$(( AGENT_TOP + USABLE_HEIGHT * 3 / 4 ))

# ── Create output directories and empty log files ────────────────────────────
mkdir -p ~/Desktop/bbb-project/outputs/{blacksmith,bookworm,artist,adversary}
touch ~/Desktop/bbb-project/outputs/{blacksmith,bookworm,artist,adversary}/progress.log

# ── 1. Open VSCode as the Conductor ──────────────────────────────────────────
"$CODE" ~/Desktop/bbb-project &
sleep 3

osascript -e "tell application \"Visual Studio Code\" to activate"
sleep 1
# VSCode (Electron) doesn't support AppleScript bounds directly; use System Events
osascript -e "tell application \"System Events\" to tell process \"Code\"
  set position of front window to {$VSCODE_LEFT, $VSCODE_TOP}
  set size of front window to {$(( VSCODE_RIGHT - VSCODE_LEFT )), $(( VSCODE_BOTTOM - VSCODE_TOP ))}
end tell"

sleep 1

# ── 2. Helper: open an iTerm2 window, position it, run tail -f ───────────────
open_agent_window() {
  local NAME="$1"
  local B_LEFT=$2
  local B_TOP=$3
  local B_RIGHT=$4
  local B_BOTTOM=$5
  local COLOR=$6
  local LOG_FILE="$7"

  # Create window and position it
  osascript -e "tell application \"iTerm2\"
    create window with default profile
    delay 0.3
    set bounds of front window to {$B_LEFT, $B_TOP, $B_RIGHT, $B_BOTTOM}
  end tell"

  sleep 0.3

  # Send commands to the new window
  osascript -e "tell application \"iTerm2\"
    tell front window
      tell current session
        write text \"printf '\\\\033[${COLOR}m'; clear; echo '  $NAME'; echo '  ─────────────────────'; echo; tail -f $LOG_FILE\"
      end tell
    end tell
  end tell"
}

# ── 3. Open 4 agent windows stacked vertically ───────────────────────────────
# Row 1: Blacksmith (green)
open_agent_window "⚒  BLACKSMITH" \
  $AGENT_LEFT $AGENT_ROW1_TOP $AGENT_RIGHT $AGENT_ROW2_TOP \
  "32" ~/Desktop/bbb-project/outputs/blacksmith/progress.log
sleep 0.5

# Row 2: Bookworm (blue)
open_agent_window "📚  BOOKWORM" \
  $AGENT_LEFT $AGENT_ROW2_TOP $AGENT_RIGHT $AGENT_ROW3_TOP \
  "34" ~/Desktop/bbb-project/outputs/bookworm/progress.log
sleep 0.5

# Row 3: Artist (magenta)
open_agent_window "🎨  ARTIST" \
  $AGENT_LEFT $AGENT_ROW3_TOP $AGENT_RIGHT $AGENT_ROW4_TOP \
  "35" ~/Desktop/bbb-project/outputs/artist/progress.log
sleep 0.5

# Row 4: Adversary (red)
open_agent_window "⚔  ADVERSARY" \
  $AGENT_LEFT $AGENT_ROW4_TOP $AGENT_RIGHT $AGENT_BOTTOM \
  "31" ~/Desktop/bbb-project/outputs/adversary/progress.log

echo "Demo ready. VSCode (Conductor) on the left, 4 agent monitors on the right."
