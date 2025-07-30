@echo off
echo ============================================
echo     PyInstaller Build Script Started
echo ============================================

REM Activate virtual environment
echo [1/5] Activating virtual environment...
call venv\Scripts\activate.bat

REM Create release folder if needed
echo [2/5] Ensuring release folder exists...
if not exist release (
    mkdir release
)

REM Clean old build files
echo [3/5] Cleaning old build and dist folders...
if exist release\build (
    rmdir /s /q release\build
)
if exist release\dist (
    rmdir /s /q release\dist
)

REM Run PyInstaller with your spec file
echo [4/5] Running PyInstaller...
pyinstaller release\main.spec --distpath release\dist --workpath release\build

REM Final message
echo [5/5] Build complete!
echo --------------------------------------------
echo Output EXE is located in: release\dist\
echo --------------------------------------------
pause