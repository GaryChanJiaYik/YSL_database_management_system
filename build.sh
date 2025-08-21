echo "============================================"
echo "    PyInstaller Build Script Started"
echo "============================================"

# Step 1: Activate virtual environment
echo "[1/5] Activating virtual environment..."
source venv/bin/activate

# Step 2: Ensure release folder exists
echo "[2/5] Ensuring release folder exists..."
mkdir -p release

# Step 3: Clean old build and dist folders
echo "[3/5] Cleaning old build and dist folders..."
rm -rf release/build
rm -rf release/dist

# Step 4: Run PyInstaller with your spec file
echo "[4/5] Running PyInstaller..."
pyinstaller release/main_macos.spec --distpath release/dist --workpath release/build

# Step 5: Final message
echo "[5/5] Build complete!"
echo "--------------------------------------------"
echo "Output executable is located in: release/dist/"
echo "--------------------------------------------"