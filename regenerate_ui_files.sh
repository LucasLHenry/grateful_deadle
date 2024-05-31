#!/bin/bash

python -m PyQt5.uic.pyuic  ui/input.ui -o input_window.py
python -m PyQt5.uic.pyuic  ui/main_window.ui -o main_window.py