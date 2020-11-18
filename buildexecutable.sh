#!/bin/bash
source venv/Scripts/activate
rm -r build
rm -r dist
pyinstaller app.spec