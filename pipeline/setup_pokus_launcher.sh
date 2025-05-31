#!/bin/bash

# Set your target base directory
PROJECT_DIR="/home/sgarimella/Projects/PokuStudio/summer-pokus/pipeline/pokus_launcher_gui"

# Create directory structure
mkdir -p "$PROJECT_DIR/launcher"
mkdir -p "$PROJECT_DIR/resources"

# Create empty Python files
touch "$PROJECT_DIR/launcher/__init__.py"
touch "$PROJECT_DIR/launcher/config.py"
touch "$PROJECT_DIR/launcher/launcher.py"
touch "$PROJECT_DIR/launcher/main.py"

# Create README.md
cat > "$PROJECT_DIR/README.md" <<EOF
# Pokus Launcher GUI

A PySide6-based launcher to open WSL, Blender, and Krita for the Summer Pokus animation project.

## Usage

1. Install dependencies:

\`\`\`bash
pip install -r requirements.txt
\`\`\`

2. Run the launcher:

\`\`\`bash
python launcher/main.py
\`\`\`
EOF

# Create requirements.txt
cat > "$PROJECT_DIR/requirements.txt" <<EOF
PySide6>=6.6
EOF

# Create launcher/config.py with default paths
cat > "$PROJECT_DIR/launcher/config.py" <<EOF
# Paths for Pokus Launcher

PROJECT_PATH_WINDOWS = r"C:\\\\Users\\\\sgarimella\\\\dev\\\\summer-pokus"
PROJECT_PATH_WSL = "/home/sgarimella/dev/summer-pokus"

BLENDER_PATH = r"C:\\\\Program Files\\\\Blender Foundation\\\\Blender 3.6\\\\blender.exe"
KRITA_PATH = r"C:\\\\Program Files\\\\Krita (x64)\\\\bin\\\\krita.exe"

WSL_COMMAND = ["wsl.exe", "-d", "Ubuntu", "--cd", PROJECT_PATH_WSL]
EOF

echo "✅ Project created at: $PROJECT_DIR"
