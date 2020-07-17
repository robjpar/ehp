#!/bin/sh
# chmod 755 build_backdoor-linux.sh
# ./build_backdoor-linux.sh
pyinstaller --onefile --noconsole backdoor.py
