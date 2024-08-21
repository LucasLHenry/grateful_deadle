#!/bin/bash
python -m PyQt5.uic.pyuic ui/input.ui -o ui/input_window.py
python -m PyQt5.uic.pyuic ui/main_window.ui -o ui/main_window.py
python -m PyQt5.uic.pyuic ui/error.ui -o ui/error_window.py

# CWD=$(pwd)
# cd ../ui
# python -m PyQt5.uic.pyuic input.ui -o ui/input_window.py
# python -m PyQt5.uic.pyuic main_window.ui -o ui/main_window.py
# cd "${CWD}"