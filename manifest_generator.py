import json
import uuid
from pathlib import Path
from typing import Optional

MOD_EXTENSIONS = {".patch_0", ".stream", ".gpu_resources"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg"}


def is_hidden(path: Path) -> bool:
    return path.name.startswith(".")


def has_mod_file(folder: Path) -> bool:
    for child in folder.iterdir():
        if child.is_file() and child.suffix in MOD_EXTENSIONS:
            return True
    return False


def scan_directory(root_path: Path) -> dict:
    tree = {"path": root_path, "name": root_path.name, "folders": [], "has_mod": False}

    if has_mod_file(root_path):
        tree["has_mod"] = True

    for child in sorted(root_path.iterdir()):
        if is_hidden(child):
            continue

        if child.is_dir():
            subtree = scan_directory(child)
            tree["folders"].append(subtree)

    return tree


def process_tree_to_options(tree: dict, root_path: Path) -> list:
    options = []

    for folder in tree.get("folders", []):
        if folder["has_mod"]:
            option = {
                "Name": folder["name"],
                "Image": "",
                "Description": "",
                "Include": [
                    str(folder["path"].relative_to(root_path)).replace("\\", "/")
                ],
            }
            options.append(option)
        else:
            subfolders_with_mod = [f for f in folder.get("folders", []) if f["has_mod"]]
            if subfolders_with_mod:
                sub_options = []
                for sub in subfolders_with_mod:
                    sub_option = {
                        "Name": sub["name"],
                        "Description": "",
                        "Image": "",
                        "Include": [
                            str(sub["path"].relative_to(root_path)).replace("\\", "/")
                        ],
                    }
                    sub_options.append(sub_option)

                option = {
                    "Name": folder["name"],
                    "Image": "",
                    "Description": "",
                    "SubOptions": sub_options,
                    "path": folder["path"],
                }
                options.append(option)

    return options


def find_image_for_option(
    option_name: str, current_dir: Path, root_dir: Path
) -> Optional[str]:
    current_dir = Path(current_dir)

    for img in current_dir.iterdir():
        if img.is_file() and img.suffix.lower() in IMAGE_EXTENSIONS:
            new_name = f"{option_name}{img.suffix}"
            new_path = current_dir / new_name
            if not new_path.exists():
                img.rename(new_path)
            return str(new_path.relative_to(root_dir)).replace("\\", "/")

    option_name_lower = option_name.lower().replace("-", " ").replace("_", " ")

    for img in root_dir.iterdir():
        if img.is_file() and img.suffix.lower() in IMAGE_EXTENSIONS:
            img_name = img.stem.lower().replace("-", " ").replace("_", " ")
            if option_name_lower == img_name:
                return str(img.relative_to(root_dir)).replace("\\", "/")

    return None


def find_icon_path(root_path: Path) -> Optional[str]:
    root_name = root_path.name

    for ext in IMAGE_EXTENSIONS:
        icon_path = root_path / f"icon{ext}"
        if icon_path.exists():
            return f"icon{ext}"

    images = [
        f
        for f in root_path.iterdir()
        if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS
    ]

    if len(images) == 1:
        img = images[0]
        new_name = f"{root_name}{img.suffix}"
        new_path = root_path / new_name
        if not new_path.exists():
            img.rename(new_path)
        return new_name

    for img in root_path.iterdir():
        if img.is_file() and img.suffix.lower() in IMAGE_EXTENSIONS:
            img_name = img.stem.lower().replace("-", " ").replace("_", " ")
            root_name_lower = root_name.lower()
            if root_name_lower in img_name or img_name in root_name_lower:
                return str(img.relative_to(root_path)).replace("\\", "/")

    return None


def generate_manifest(root_path: Path) -> dict:
    root_path = Path(root_path).resolve()

    tree = scan_directory(root_path)
    options = process_tree_to_options(tree, root_path)

    for option in options:
        if "SubOptions" in option:
            mother_dir = option.get("path")
            option["Image"] = (
                find_image_for_option(option["Name"], mother_dir, root_path) or ""
            )
            if "path" in option:
                del option["path"]
            for sub in option["SubOptions"]:
                sub_dir = root_path / sub["Include"][0]
                sub["Image"] = (
                    find_image_for_option(sub["Name"], sub_dir, root_path) or ""
                )
        else:
            opt_dir = root_path / option["Include"][0]
            option["Image"] = (
                find_image_for_option(option["Name"], opt_dir, root_path) or ""
            )

    for option in options:
        if "path" in option:
            del option["path"]

    manifest = {
        "Version": 1,
        "Guid": str(uuid.uuid4()),
        "Name": root_path.name,
        "Description": "",
        "IconPath": find_icon_path(root_path) or "",
        "Options": options,
    }

    return manifest


def main():
    import sys

    target_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()

    manifest = generate_manifest(target_path)

    output_path = target_path / "manifest.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"Manifest generated at: {output_path}")


if __name__ == "__main__":
    main()
