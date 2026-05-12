#!/bin/bash
# Kill only the Flask and React server processes
pkill -f "venv/bin/python.*app.py" 2>/dev/null
pkill -f "react-scripts start" 2>/dev/null
sleep 1

# Start Flask in background
/Users/sophie/Projects/ffnToAO3/venv/bin/python /Users/sophie/Projects/ffnToAO3/app.py &

# Start React dev server
cd /Users/sophie/Projects/ffnToAO3/display && npm start
