#!/bin/bash
# OLED-like settings for IPS monitor
# Applies gamma, contrast, and night color settings on boot

# Wait for display to be ready
sleep 2

# Apply gamma via xrandr (works on XWayland)
xrandr --output HDMI-A-1 --gamma 0.88:0.88:0.88 --brightness 1.0 2>/dev/null

# Start vibrantLinux in background if not running
if ! pgrep -x vibrantLinux > /dev/null; then
    vibrantLinux &
fi
