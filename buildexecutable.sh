#!/bin/bash
source venv/Scripts/activate
[ -d "build" ] && rm -r build
[ -d "dist" ] && rm -r dist
pyinstaller app.spec