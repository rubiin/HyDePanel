#!/bin/bash

# Take a screenshot and perform OCR
ocr_text=$(grimblast --freeze save area - | tesseract -l eng - - 2>/dev/null)

# Check if OCR was successful
if [[ -n "$ocr_text" ]]; then
    echo -n "$ocr_text" | wl-copy
    notify-send -a "Tsumiki" "OCR Success" "Text Copied to Clipboard"
else
    notify-send -a "Tsumiki" "OCR Failed" "No text recognized or operation failed"
fi
