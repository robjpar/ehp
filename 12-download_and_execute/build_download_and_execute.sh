#!/bin/sh
# pip3 uninstall requests
# pip3 install requests==2.5.1
# chmod 755 build_download_and_execute.sh
# ./build_download_and_execute.sh
wine pyinstaller --onefile --noconsole download_and_execute.py
