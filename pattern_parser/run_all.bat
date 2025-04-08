@echo off
echo Running extractor on all example files...

for %%f in (examples\*.py) do (
    echo Processing %%f
    python extractor\function_info_extractor.py %%f
)

echo Done!
pause
