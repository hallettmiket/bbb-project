#!/bin/bash
# ~/Desktop/bbb-project/start_demo.sh

SESSION="bbb-demo"


# External display logical coordinates (AppleScript uses points, not pixels)
# LG 4K display: 1920x1080 logical points, positioned above laptop display
DISPLAY_X=-92
DISPLAY_Y=-1080
DISPLAY_WIDTH=1920
DISPLAY_HEIGHT=1080
MENU_BAR=25

# Pre-compute bounds (AppleScript can't do bash arithmetic)
BOUNDS_LEFT=$DISPLAY_X
BOUNDS_TOP=$(( DISPLAY_Y + MENU_BAR ))
BOUNDS_RIGHT=$(( DISPLAY_X + DISPLAY_WIDTH ))
BOUNDS_BOTTOM=$(( DISPLAY_Y + DISPLAY_HEIGHT ))

# Open iTerm2 window on external display, full width, nearly full height
osascript <<EOF
tell application "iTerm2"
  activate
  set newWindow to (create window with default profile)
  tell newWindow
    set bounds to {$BOUNDS_LEFT, $BOUNDS_TOP, $BOUNDS_RIGHT, $BOUNDS_BOTTOM}
  end tell
end tell
EOF

sleep 0.5

# Set font size in a separate AppleScript call
osascript <<'EOF'
tell application "iTerm2"
  tell current window
    tell current session
      set font size to 18
    end tell
  end tell
end tell
EOF

sleep 0.5

# ── 2. Kill any old session cleanly and wait for server to settle ────────────
tmux kill-server 2>/dev/null
sleep 1

# ── 3. Create session ────────────────────────────────────────────────────────
tmux new-session -d -s $SESSION -x 220 -y 52
sleep 0.5

# Enable mouse mode so selection respects pane boundaries
tmux set-option -t $SESSION mouse on
tmux set-option -t $SESSION @pane-is-vim 0


# ── 4. Send tmux attach to the new iTerm2 window ────────────────────────────
osascript <<EOF
tell application "iTerm2"
  tell current window
    tell current session
      write text "cd ~/Desktop/bbb-project && tmux attach -t $SESSION"
    end tell
  end tell
end tell
EOF

sleep 1

# ── 4. Build layout: conductor top, 4 equal columns below ───────────────────
tmux split-window -v -t $SESSION:0 -p 60
tmux split-window -h -t $SESSION:0.1 -p 75
tmux split-window -h -t $SESSION:0.2 -p 67
tmux split-window -h -t $SESSION:0.3 -p 50

# ── 5. Pane border style ─────────────────────────────────────────────────────
tmux set-option -t $SESSION pane-border-status top
tmux set-option -t $SESSION pane-border-style "fg=colour240"
tmux set-option -t $SESSION pane-active-border-style "fg=colour255,bold"

# ── 6. Name panes with embedded colors in the title ─────────────────────────
tmux select-pane -t $SESSION:0.0 -T "#[fg=colour255,bold]🎼  CONDUCTOR#[default]"
tmux select-pane -t $SESSION:0.1 -T "#[fg=colour35,bold]⚒  BLACKSMITH#[default]"
tmux select-pane -t $SESSION:0.2 -T "#[fg=colour33,bold]📚  BOOKWORM#[default]"
tmux select-pane -t $SESSION:0.3 -T "#[fg=colour135,bold]🎨  ARTIST#[default]"
tmux select-pane -t $SESSION:0.4 -T "#[fg=colour196,bold]⚔  ADVERSARY#[default]"

tmux set-option -t $SESSION pane-border-format " #{pane_title} "

# ── CRITICAL: disable automatic renaming so Claude Code can't overwrite titles
tmux set-option -t $SESSION allow-rename off
tmux set-option -t $SESSION automatic-rename off

# ── 7. Per-pane border colors (tmux 3.4+) ────────────────────────────────────
TMUX_VER=$(tmux -V | awk '{print $2}')
if awk "BEGIN {exit !($TMUX_VER >= 3.4)}"; then
  tmux select-pane -t $SESSION:0.1 -P "fg=colour35"
  tmux select-pane -t $SESSION:0.2 -P "fg=colour33"
  tmux select-pane -t $SESSION:0.3 -P "fg=colour135"
  tmux select-pane -t $SESSION:0.4 -P "fg=colour196"
fi

# ── 8. Colored zsh prompts ───────────────────────────────────────────────────
cat > /tmp/ps1_conductor.sh <<'EOF'
export PROMPT='%F{245}[conductor]%f $ '
EOF
cat > /tmp/ps1_blacksmith.sh <<'EOF'
export PROMPT='%F{35}[blacksmith]%f $ '
EOF
cat > /tmp/ps1_bookworm.sh <<'EOF'
export PROMPT='%F{33}[bookworm]%f $ '
EOF
cat > /tmp/ps1_artist.sh <<'EOF'
export PROMPT='%F{135}[artist]%f $ '
EOF
cat > /tmp/ps1_adversary.sh <<'EOF'
export PROMPT='%F{196}[adversary]%f $ '
EOF

tmux send-keys -t $SESSION:0.0 "source /tmp/ps1_conductor.sh && clear"  Enter
tmux send-keys -t $SESSION:0.1 "source /tmp/ps1_blacksmith.sh && clear" Enter
tmux send-keys -t $SESSION:0.2 "source /tmp/ps1_bookworm.sh && clear"   Enter
tmux send-keys -t $SESSION:0.3 "source /tmp/ps1_artist.sh && clear"     Enter
tmux send-keys -t $SESSION:0.4 "source /tmp/ps1_adversary.sh && clear"  Enter

# ── 9. Launch watch in agent panes, claude --model opus in conductor ──────────
sleep 1

# Create output directories so watch doesn't show errors immediately
mkdir -p ~/Desktop/bbb-project/outputs/blacksmith
mkdir -p ~/Desktop/bbb-project/outputs/bookworm
mkdir -p ~/Desktop/bbb-project/outputs/artist
mkdir -p ~/Desktop/bbb-project/outputs/adversary

# Create empty log files so tail doesn't error before agents start writing
touch ~/Desktop/bbb-project/outputs/blacksmith/progress.log
touch ~/Desktop/bbb-project/outputs/bookworm/progress.log
touch ~/Desktop/bbb-project/outputs/artist/progress.log
touch ~/Desktop/bbb-project/outputs/adversary/progress.log

# Each agent pane tails its own live log
tmux send-keys -t $SESSION:0.1 "tail -f ~/Desktop/bbb-project/outputs/blacksmith/progress.log" Enter
tmux send-keys -t $SESSION:0.2 "tail -f ~/Desktop/bbb-project/outputs/bookworm/progress.log" Enter
tmux send-keys -t $SESSION:0.3 "tail -f ~/Desktop/bbb-project/outputs/artist/progress.log" Enter
tmux send-keys -t $SESSION:0.4 "tail -f ~/Desktop/bbb-project/outputs/adversary/progress.log" Enter

# Conductor runs claude with opus
sleep 1
tmux send-keys -t $SESSION:0.0 "cd ~/Desktop/bbb-project && claude --model opus" Enter

# Re-assert pane titles after Claude Code starts
sleep 4

tmux select-pane -t $SESSION:0.0 -T "#[fg=colour255,bold]🎼  CONDUCTOR#[default]"
tmux select-pane -t $SESSION:0.1 -T "#[fg=colour35,bold]⚒  BLACKSMITH#[default]"
tmux select-pane -t $SESSION:0.2 -T "#[fg=colour33,bold]📚  BOOKWORM#[default]"
tmux select-pane -t $SESSION:0.3 -T "#[fg=colour135,bold]🎨  ARTIST#[default]"
tmux select-pane -t $SESSION:0.4 -T "#[fg=colour196,bold]⚔  ADVERSARY#[default]"

# ── 10. Attach ───────────────────────────────────────────────────────────────
tmux select-pane -t $SESSION:0.0
tmux attach -t $SESSION
