#!/bin/bash
cd "$(dirname "$0")"
python3 -m pip install --user pywebview pygame
python3 ps3_adapter.py
