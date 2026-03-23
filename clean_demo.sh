#!/bin/bash
# ~/Desktop/bbb-project/clean_demo.sh
#
# Resets the demo to a clean state by removing all agent-generated outputs.
# Run this before start_demo.sh to simulate a fresh session.

echo "Cleaning demo outputs..."

# Remove entire output, data, and src directories
rm -rf ~/Desktop/bbb-project/outputs/
echo "  Removed outputs/"
rm -rf ~/Desktop/bbb-project/src/
echo "  Removed src/"
rm -rf ~/Desktop/bbb-project/data/
echo "  Removed data/"

echo "Demo reset complete. Ready for a fresh run."
