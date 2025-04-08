@echo off
echo Running extractor on all example files...

REM Run the main extractor script that already processes all files
python extractor\function_info_extractor.py

echo All files processed. Check the outputs folder.
pause
