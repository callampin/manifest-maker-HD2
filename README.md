# 🛡️ Helldivers 2 Manifest Generator

<p align="center">
  <a href="https://www.nexusmods.com/profile/Ka1ser0/mods" target="_blank">
    <img src="https://img.shields.io/badge/Shout%20out%20to%20my%20g-Kaiser-ff69b4?style=flat-square" alt="Shout out to my g Kaiser">
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.7%2B-blue?style=flat-square&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/Helldivers%202-Community-orange?style=flat-square" alt="Helldivers 2">
</p>

> Automate the creation of `manifest.json` files for Helldivers 2 mods with ease. Compatible with HD2 Arsenal mod manager and HD2 Mod Manager.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔍 **Auto-Detection** | Scans folder hierarchy to detect mod files (`.patch_0`, `.stream`, `.gpu_resources`) |
| 📂 **SubOption Support** | Automatically groups subfolders with mods as categories |
| 🖼️ **Smart Image Matching** | Intelligently assigns images to options based on naming conventions |
| ✏️ **Auto-Rename Images** | Automatically renames images to match folder names (no need to manually rename!) |
| 🌐 **OS-Agnostic** | Uses forward slashes (`/`) in output JSON for cross-platform compatibility |
| 🔑 **UUID Generation** | Automatically generates unique GUIDs for each manifest |

---

## 📋 Requirements

- **Python 3.7+** (Windows 11 includes Python via Microsoft Store)
- **No external dependencies** — uses only Python standard library

---

## 🚀 Installation

```powershell
# Clone the repository
git clone https://github.com/callampin/manifest-maker-HD2.git
cd manifest-maker
```

> **Tip:** On Windows 11, you can also install Python from the Microsoft Store or [python.org](https://python.org).

---

## 💻 Usage

### Basic Usage

Simply download the script file `manifest_generator.py`, place it in your mod's root folder, then:

1. Right-click on an empty space inside your mod's folder
2. Select "Open in Terminal"
3. Type: `python manifest_generator.py`
4. Press Enter

This will generate `manifest.json` in your mod's folder.

### Specify a Mod Directory

```powershell
python manifest_generator.py "C:\Path\To\Your\Mod"
```

### Command Line Options

| Argument | Description |
|----------|-------------|
| *(none)* | Uses current working directory |
| `<path>` | Path to mod root folder |

---

## 🧠 How It Works

### Mod File Detection

The script identifies installable options by looking for these file extensions:

```
.patch_0    .stream    .gpu_resources
```

> If a folder contains at least one of these files, it's considered an installable option.

### SubOptions (Categories)

If a folder **does not** contain mod files but has **subfolders** that do, the parent folder becomes a category with SubOptions.

### Image Detection

The script uses the following heuristics:

1. **IconPath (Main Icon)**
   - First looks for `icon.png` or `icon.jpg` in the root
   - If there's only one image in the root folder, automatically renames it to match the project name
   - Falls back to finding any image that matches the root folder name

2. **Option Images**
   - First searches inside the option's own folder
   - Automatically renames found images to match the folder name exactly (case-sensitive)
   - If not found in the option folder, searches the root folder for an image with a similar name (exact match only)

> **Tip:** You don't need to manually rename your images! The script handles this automatically. Just put any image in your folders and it will be renamed to match the folder name.

---

## 📄 Output Format

```json
{
  "Version": 1,
  "Guid": "uuid-generated-automatically",
  "Name": "Mod Folder Name",
  "Description": "",
  "IconPath": "icon.png",
  "Options": [
    {
      "Name": "Option Name",
      "Image": "option_image.png",
      "Description": "",
      "Include": ["path/to/option"]
    },
    {
      "Name": "Category Name",
      "Image": "category_image.png",
      "Description": "",
      "SubOptions": [
        {
          "Name": "SubOption 1",
          "Description": "",
          "Image": "sub_image.png",
          "Include": ["Category/SubOption1"]
        }
      ]
    }
  ]
}
```

---

## 📁 Example

**Input folder structure:**

```
My_HD2_Mod/
├── icon.png
├── Armor_Set_1/
│   ├── image.png
│   └── heavy_armor.patch_0
└── Weapons/
    ├── Assault_Rifle/
    │   └── rifle.patch_0
    └── Shotgun/
        └── shotgun.stream
```

**Running:**
```powershell
python manifest_generator.py My_HD2_Mod
```

**Generated output:**

```json
{
  "Version": 1,
  "Guid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "Name": "My_HD2_Mod",
  "Description": "",
  "IconPath": "icon.png",
  "Options": [
    {
      "Name": "Armor_Set_1",
      "Image": "Armor_Set_1/image.png",
      "Description": "",
      "Include": ["Armor_Set_1"]
    },
    {
      "Name": "Weapons",
      "Image": "",
      "Description": "",
      "SubOptions": [
        {
          "Name": "Assault_Rifle",
          "Description": "",
          "Image": "",
          "Include": ["Weapons/Assault_Rifle"]
        },
        {
          "Name": "Shotgun",
          "Description": "",
          "Image": "",
          "Include": ["Weapons/Shotgun"]
        }
      ]
    }
  ]
}
```

---

## 🔧 Troubleshooting

### ❌ "python" command not found
```powershell
# Use python3 instead
python3 manifest_generator.py
```

Or ensure Python is in your Windows PATH.

### ❌ No options detected
Make sure your mod folders contain at least one of these file types:
- `.patch_0`
- `.stream`
- `.gpu_resources`

### ❌ Images not being found
- The script automatically renames images to match folder names — no manual renaming needed!
- Supported formats: `.png`, `.jpg`, `.jpeg`
- If you have multiple images in an option folder, only one will be used

---

## 📝 License

This project is licensed under the **MIT License**.

---

<p align="center">
  <sub>Made with ❤️ for the Helldivers 2 modding community</sub>
</p>
