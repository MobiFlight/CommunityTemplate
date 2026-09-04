import shutil
import os
import re
from pathlib import Path

def find_custom_source_folder():
    """Find the custom_source_folder value from platformio.ini files"""
    # Get script directory (not current working directory)
    script_dir = Path(__file__).parent.resolve()

    # Search for *_platformio.ini files recursively
    ini_files = list(script_dir.glob("**/*_platformio.ini"))

    if not ini_files:
        raise FileNotFoundError(f"No *_platformio.ini file found in {script_dir} or its subdirectories")

    # Parse the first one found
    ini_file = ini_files[0]
    print(f"Found platformio.ini: {ini_file}")

    with open(ini_file, 'r') as f:
        content = f.read()
        # Look for custom_source_folder (e.g. Template)
        match = re.search(r'custom_source_folder\s*=\s*(\S+)', content)
        if match and not match.group(1).startswith('${'):
            return match.group(1)

    raise ValueError("custom_source_folder not found in platformio.ini")

def find_community_project_name():
    """Find the custom_community_project value from platformio.ini files"""
    # Get script directory (not current working directory)
    script_dir = Path(__file__).parent.resolve()

    # Search for *_platformio.ini files recursively
    ini_files = list(script_dir.glob("**/*_platformio.ini"))

    if not ini_files:
        raise FileNotFoundError(f"No *_platformio.ini file found in {script_dir} or its subdirectories")

    # Parse the first one found
    ini_file = ini_files[0]
    print(f"Found platformio.ini: {ini_file}")

    with open(ini_file, 'r') as f:
        content = f.read()
        # Look for custom_community_project e.g. "YourProject" in the template
        match = re.search(r'custom_community_project\s*=\s*(\S+)', content)
        if match and not match.group(1).startswith('${'):
            return match.group(1)

    raise ValueError("custom_community_project not found in platformio.ini")

try:
    # Auto-discover the project folder name
    project_folder = find_custom_source_folder()
    print(f"Project folder: {project_folder}")

    # Auto-discover the community project name (for destination folder)
    community_project_name = find_community_project_name()
    print(f"Community project name: {community_project_name}")

    # Get the script directory (works regardless of where the script is executed from)
    script_dir = Path(__file__).parent.resolve()
    source_dir = script_dir / project_folder / "Community"

    print(f"Script directory: {script_dir}")
    print(f"Source directory: {source_dir}")
    print(f"Source exists: {source_dir.exists()}")

    if not source_dir.exists():
        raise FileNotFoundError(f"Community folder not found at {source_dir}")

    # Destination directory (using USERPROFILE environment variable)
    # Assumes standard install location. We'll notify the user if not found.
    ##########################################
    # NON STANDARD MF INSTALL? EDIT LINE BELOW
    ##########################################
    dest_dir = Path.home() / "AppData" / "Local" / "MobiFlight" / "MobiFlight Connector" / "Community" / community_project_name

    print(f"Destination directory: {dest_dir}")

    # Create destination directory if it doesn't exist
    # Check if MobiFlight Community folder exists
    community_base = dest_dir.parent
    if not community_base.exists():
      raise FileNotFoundError(f"MobiFlight Community folder not found at: {community_base}\nPlease verify MobiFlight Connector is installed at the standard location or update script.")

    # Create the project-specific folder
    dest_dir.mkdir(exist_ok=True)
    print(f"Destination created/verified")

    # Copy all contents from source to destination, overwriting existing files
    shutil.copytree(source_dir, dest_dir, dirs_exist_ok=True)

    print(f"\033[92mSuccessfully copied contents from {source_dir} to {dest_dir}\033[0m")

    # Check if _build folder exists and copy firmware files
    build_firmware_dir = script_dir / "_build" / project_folder / "Community" / "firmware"
    if build_firmware_dir.exists():
        dest_firmware_dir = dest_dir / "firmware"
        dest_firmware_dir.mkdir(exist_ok=True)

        # Copy firmware files from _build to MobiFlight Community
        for firmware_file in build_firmware_dir.glob("*"):
            if firmware_file.is_file():
                shutil.copy2(firmware_file, dest_firmware_dir)
                print(f"\033[92mCopied firmware: {firmware_file.name}\033[0m")
    else:
        print(f"\033[93mWarning: Build firmware folder not found at {build_firmware_dir}\033[0m")
        print(f"\033[93mRun a PlatformIO build first to generate firmware files\033[0m")

except Exception as e:
    print(f"\033[91m*********Error: {e}\033[0m")
    import traceback
    traceback.print_exc()
