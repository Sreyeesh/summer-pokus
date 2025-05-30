from krita import Krita
import os
import re
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QMessageBox

# === CONFIGURATION ===
BASE_PATH = r"\\wsl$\Ubuntu\home\sgarimella\projects\summer_pokus\assets\characters"

# === HELPERS ===
def get_input(prompt, default=""):
    text, ok = QInputDialog.getText(None, "Save Character File", prompt, QLineEdit.Normal, default)
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

# === MAIN FUNCTION ===
def save_character_file():
    app = Krita.instance()
    doc = app.activeDocument()

    if doc is None:
        QMessageBox.warning(None, "No Document", "❌ No active document to save.")
        return

    # Ask for character name
    name, ok = get_input("Character name (e.g. poku):", "poku")
    if not ok or not name:
        return

    # Build folder + file name
    char_path = os.path.join(BASE_PATH, name)
    os.makedirs(char_path, exist_ok=True)

    base_name = f"spk_chr_{name}_turnaround"
    version = get_next_version(char_path, base_name)
    file_name = f"{base_name}_v{version}.kra"
    full_path = os.path.join(char_path, file_name)

    # Save the document
    doc.setFileName(full_path)
    doc.save()

    QMessageBox.information(None, "Save Successful", f"✅ Saved as:\n{full_path}")

# === RUN ===
save_character_file()
