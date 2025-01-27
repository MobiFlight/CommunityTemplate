#
#   This renaming script is based on the excellent work from ccrawford
#   All credits are going to him!!
#
#   His original repo can be found under https://github.com/ccrawford/MobiFlight-Custom-Device-Setup/
#   And on Discord see: https://discord.com/channels/608690978081210392/1331350567754403840
#
#   Some slight adaptions has been made to reflect the latest status of the repo.
#   New Device Name and author are asked from the python script
#   Just start it by 'python renaming.py' into the terminal window
#


import os
import shutil
import sys
import fileinput
from pathlib import Path

def replace_in_file(file_path, replacements):
    """Replace all keys in `replacements` with their values in the given file."""
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    for old, new in replacements.items():
        content = content.replace(old, new)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)


def rename_files_and_directories(base_path, replacements):
    """Recursively rename files and directories based on replacements."""
    for root, dirs, files in os.walk(base_path, topdown=False):
        # Rename files
        for name in files:
            old_path = Path(root) / name
            new_name = name
            for old, new in replacements.items():
                new_name = new_name.replace(old, new)
            new_path = Path(root) / new_name
            old_path.rename(new_path)

        # Rename directories
        for name in dirs:
            old_path = Path(root) / name
            new_name = name
            for old, new in replacements.items():
                new_name = new_name.replace(old, new)
            new_path = Path(root) / new_name
            old_path.rename(new_path)


def main():
    # get the new device name
    device_name = input("Enter the name of your device: ")
    # get the new prefix
    prefix = input("Enter your author name: ")
    # get statement from user to rename everything
    print(F"Device will be renamed to: " + device_name)
    print(F"Author will be renamed to: " + prefix)
    response = input("Do you want to rename it? (y/N): ").strip().lower()
    if response != "y":
        print("Operation canceled.")
        sys.exit(1)

    # Locate the 'Template' folder
    template_folder = Path("Template")

    # Rename the Template folder to DEVICE_NAME
    new_device_path = Path(device_name)
    if new_device_path.exists():
        print(f"Device folder '{new_device_path}' already exists.")
        response = input("Do you want to overwrite it? (y/N): ").strip().lower()
        if response != "y":
            print("Operation canceled.")
            sys.exit(1)
        shutil.rmtree(new_device_path)  # Remove the existing directory

    # Perform the rename
    template_folder.rename(new_device_path)

    # Continue with renaming files and updating contents within the renamed folder
    rename_files_and_directories(new_device_path, {
        "MyCustomClass.cpp": f"{device_name}.cpp",
        "MyCustomClass.h": f"{device_name}.h",
        "MyCustomDevice_platformio.ini": f"{device_name}_platformio.ini",
    })

    replacements = {
        "MyCustomClass": device_name,
        "Mobiflight Template": f"{prefix} {device_name}",
        "mobiflight_template": f"{prefix.lower()}_{device_name.lower()}",
        "Template": device_name,
        "YourProject": device_name,
        "MOBIFLIGHT_TEMPLATE": device_name,
        "env_template": f"env_{device_name}",
        "YourProject": f"{prefix}_{device_name}"
    }

    # Update content in relevant files
    for file_path in new_device_path.rglob("*.cpp"):
        replace_in_file(file_path, replacements)

    for file_path in new_device_path.rglob("*.h"):
        replace_in_file(file_path, replacements)

    for file_path in new_device_path.rglob("*_platformio.ini"):
        replace_in_file(file_path, replacements)

    # Update Community boards and devices
    community_path = new_device_path / "Community"
    for file_path in community_path.glob("boards/*.json"):
        replace_in_file(file_path, {
            "mobiflight_template": f"{prefix.lower()}_{device_name.lower()}",
            "Mobiflight Template": f"{prefix} {device_name}",
            "MOBIFLIGHT_TEMPLATE": device_name,
        })

    for file_path in community_path.glob("devices/*.json"):
        replace_in_file(file_path, {
            "MOBIFLIGHT_TEMPLATE": device_name,
            "Mobiflight": prefix,
            "template": device_name,
        })

    # Rename JSON files in boards and devices
    rename_files_and_directories(community_path / "boards", {
        "mobiflight_template": f"{prefix}_{device_name}",
    })
    rename_files_and_directories(community_path / "devices", {
        "mobiflight_template": f"{prefix}_{device_name}",
    })

if __name__ == "__main__":
    main()
