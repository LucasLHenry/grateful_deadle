#!/bin/bash

python -m PyQt5.uic.pyuic  ui/input.ui -o ui/input_window.py
python -m PyQt5.uic.pyuic  ui/main_window.ui -o ui/main_window.py