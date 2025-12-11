#!/bin/bash
if [[ ${OSTYPE} == 'msys' ]]; then
  source .venv/Scripts/activate
else
  source .venv/bin/activate
fi
py UnitTestLauncher.py
