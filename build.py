#!/usr/bin/env python3
"""
Automated Build Script for iApp M3UI F-Droid Store
Validates project files, packages iApp .iyu and .myu sources into a importable .iapp release zip,
and generates SHA-256 build checksums.
"""

import os
import json
import zipfile
import hashlib
import re
import xml.etree.ElementTree as ET

BUILD_DIR = "dist"
OUTPUT_IAPP = os.path.join(BUILD_DIR, "FDroid_M3_Store.iapp")

def validate_files():
    print("=== [1/3] Validating Source Files ===")

    # 1. Validate src/config.json
    config_path = "src/config.json"
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    print(f" [✓] {config_path} valid JSON.")
    assert config["defaultRepo"]["fingerprint"] == "43238D512C1E5EB2D6569F4A3AFBF5523418B82E0A3ED1552770ABB9A9C9CCAB"

    # 2. Validate .iyu XML Layout files
    for root, dirs, files in os.walk("src/views"):
        for file in files:
            if file.endswith(".iyu"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                xml_part = re.sub(r'<code_iyu>.*?</code_iyu>', '', content, flags=re.DOTALL).strip()
                ET.fromstring(xml_part)
                print(f" [✓] {filepath} XML layout valid.")

    # 3. Validate .myu modules
    for myu in ["src/m3ui/m3ui.myu", "src/fdroid/fdroid.myu"]:
        assert os.path.exists(myu) and os.path.getsize(myu) > 100
        print(f" [✓] {myu} script module valid.")

def package_iapp():
    print("\n=== [2/3] Packaging iApp Release (.iapp) ===")
    os.makedirs(BUILD_DIR, exist_ok=True)

    with zipfile.ZipFile(OUTPUT_IAPP, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk("src"):
            for file in files:
                filepath = os.path.join(root, file)
                # Map src/views/*.iyu to iyu/ directory structure
                if "/views/" in filepath and file.endswith(".iyu"):
                    arcname = os.path.join("iyu", file)
                # Map src/fdroid/ and src/m3ui/ .myu files to myu/ directory
                elif file.endswith(".myu"):
                    arcname = os.path.join("myu", file)
                else:
                    arcname = os.path.join("res", os.path.relpath(filepath, "src"))

                zipf.write(filepath, arcname)
                print(f" Added: {filepath} -> {arcname}")

    print(f" Successfully packaged iApp project: {OUTPUT_IAPP}")

def generate_checksum():
    print("\n=== [3/3] Generating Build Checksum ===")
    sha256 = hashlib.sha256()
    with open(OUTPUT_IAPP, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    digest = sha256.hexdigest().upper()
    print(f" Build File: {OUTPUT_IAPP}")
    print(f" SHA-256 Checksum: {digest}")

    with open(os.path.join(BUILD_DIR, "BUILD_SHA256.txt"), "w", encoding="utf-8") as f:
        f.write(f"{digest}  FDroid_M3_Store.iapp\n")

if __name__ == "__main__":
    validate_files()
    package_iapp()
    generate_checksum()
    print("\n Automated Build Completed Successfully!")
