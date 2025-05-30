from krita import Krita
import os
import re
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QMessageBox

# === CONFIGURATION ===
BASE_PATH = r"\\wsl$\Ubuntu\home\sgarimella\projects\summer_pokus\assets\characters"
DOC_WIDTH = 3000
DOC_HEIGHT = 2000
DOC_DPI = 300

# === HELPERS ===
def get_input(prompt, default=""):
    text, ok = QInputDialog.getText(None, "Character Setup", prompt, QLineEdit.Normal, default)
    return text.strip().lower(), ok

def get_next_version(path, base_name):
    if not os.path.exists(path):
        return "001"

    files = [
        f for f in os.listdir(path)
        if f.startswith(base_name)
        and re.fullmatch(rf"{re.escape(base_name)}_v\d{{3}}\.kra", f)
        and not f.endswith(".kra~")
        and not f.startswith(".")
        and os.path.isfile(os.path.join(path, f))
    ]

    versions = [
        int(re.search(r'_v(\d{3})\.kra$', f).group(1))
        for f in files if re.search(r'_v(\d{3})\.kra$', f)
    ]

    next_version = max(versions, default=0) + 1
    return str(next_version).zfill(3)

def create_layer(name, parent, doc):
    layer = doc.createNode(name, "paintLayer")
    parent.addChildNode(layer, None)
    return layer

def create_group(name, parent, doc):
    group = doc.createGroupLayer(name)
    parent.addChildNode(group, None)
    return group

# === MAIN FUNCTION ===
def setup_character_turnaround_file():
    app = Krita.instance()

    # Step 1: Prompt for character name
    name, ok = get_input("Character name (e.g. poku):", "poku")
    if not ok or not name:
        return

    # Step 2: Set folder and base filename
    char_path = os.path.join(BASE_PATH, name)
    os.makedirs(char_path, exist_ok=True)

    base_name = f"spk_chr_{name}_turnaround"
    version = get_next_version(char_path, base_name)
    file_name = f"{base_name}_v{version}.kra"
    full_path = os.path.join(char_path, file_name)

    # Step 3: Create and open document
    doc = app.createDocument(DOC_WIDTH, DOC_HEIGHT, base_name, "RGBA", "U8", "", DOC_DPI)
    app.activeWindow().addView(doc)
    doc.saveAs(full_path)

    # Step 4: Build animation-friendly structure
    root = doc.rootNode()
    view_names = ["Front_TPose", "Side", "3Quarter", "Back"]
    layer_names = [
        "Sketch_Rough",
        "Line_Clean",
        "Fill_BaseColor",
        "Fill_Shadow",
        "Notes"
    ]

    for view in view_names:
        group = create_group(f"Turnaround_{view}", root, doc)
        for lname in layer_names:
            create_layer(lname, group, doc)

    # Step 5: Global layers
    create_layer("Reference_Images", root, doc)
    create_layer("Color_Palette", root, doc)
    create_layer("Design_Notes", root, doc)

    doc.refreshProjection()
    QMessageBox.information(None, "Setup Complete", f"✅ File created and saved:\n{full_path}")

# === RUN ===
setup_character_turnaround_file()
