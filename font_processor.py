import fnmatch
import os
import shutil
import requests
import zipfile
import io
import subprocess
from pyunpack import Archive
from fontTools import ttLib
from fontpreview import FontBanner, FontWall, FontPage

# --- Configuration ---

FONT_EXT = ("ttf", "otf")
ZIP_EXT = ("zip", "7z", "rar")
ORIG_DIR = os.getcwd()

# Template details
TEMPLATE = {
    "dir": "templates/OMF",
    "fonts_dir": "templates/OMF/fonts",
    "all_fonts": [
        "ubl.ttf", "ueb.ttf", "ub.ttf", "usb.ttf", "um.ttf", "ur.ttf", "ul.ttf", "uel.ttf", "ut.ttf",
        "ibl.ttf", "ieb.ttf", "ib.ttf", "isb.ttf", "im.ttf", "ir.ttf", "il.ttf", "iel.ttf", "it.ttf",
        "cbl.ttf", "ceb.ttf", "cb.ttf", "csb.ttf", "cm.ttf", "cr.ttf", "cl.ttf", "cel.ttf", "ct.ttf",
        "dbl.ttf", "deb.ttf", "db.ttf", "dsb.ttf", "dm.ttf", "dr.ttf", "dl.ttf", "del.ttf", "dt.ttf",
        "mbl.ttf", "meb.ttf", "mb.ttf", "msb.ttf", "mm.ttf", "mr.ttf", "ml.ttf", "mel.ttf", "mt.ttf",
        "nbl.ttf", "neb.ttf", "nb.ttf", "nsb.ttf", "nm.ttf", "nr.ttf", "nl.ttf", "nel.ttf", "nt.ttf",
        "sbl.ttf", "seb.ttf", "sb.ttf", "ssb.ttf", "sm.ttf", "sr.ttf", "sl.ttf", "sel.ttf", "st.ttf",
        "tbl.ttf", "teb.ttf", "tb.ttf", "tsb.ttf", "tm.ttf", "tr.ttf", "tl.ttf", "tel.ttf", "tt.ttf",
        "obl.ttf", "oeb.ttf", "ob.ttf", "osb.ttf", "om.ttf", "or.ttf", "ol.ttf", "oel.ttf", "ot.ttf",
        "pbl.ttf", "peb.ttf", "pb.ttf", "psb.ttf", "pm.ttf", "pr.ttf", "pl.ttf", "pel.ttf", "pt.ttf"
    ],
    "single_file": ["Regular.ttf"]
}


def process_fonts_in_dir(fontdir):
    """Processes all fonts in a given directory."""
    fonts_to_process = find("*.ttf", fontdir)
    if not fonts_to_process:
        fonts_to_process = find("*.otf", fontdir)
    
    print(f"Processing {len(fonts_to_process)} fonts...")
    for font_path in fonts_to_process:
        try:
            tt = ttLib.TTFont(font_path)
            # Basic metric adjustments (can be expanded)
            if tt["head"].unitsPerEm == 2048:
                tt["hhea"].ascent = 1900
                tt["OS/2"].sTypoAscender = 1900
                tt["hhea"].descent = -500
                tt["OS/2"].sTypoDescender = -500
            elif tt["head"].unitsPerEm == 1000:
                tt["hhea"].ascent = 900
                tt["OS/2"].sTypoAscender = 900
                tt["hhea"].descent = -270
                tt["OS/2"].sTypoDescender = -270
            
            tt["hhea"].lineGap = 0
            tt["OS/2"].sTypoLineGap = 0
            
            try:
                tt.save(font_path)
                # print(f"  - Fixed metrics for: {os.path.basename(font_path)}")
            except Exception as save_e:
                print(f"Warning: Could not save font {os.path.basename(font_path)}. Reason: {save_e}")
        except ttLib.TTLibError as e:
            print(f"Warning: Could not open font {os.path.basename(font_path)}. It might be corrupted or an unsupported format. Reason: {e}")
        except Exception as e:
            print(f"Warning: An unexpected error occurred while processing font {os.path.basename(font_path)}. Reason: {e}")


def generate_preview(font_path):
    """Generates a preview image for a given font."""
    if not os.path.exists(font_path):
        print(f"Error: Font file not found at '{font_path}'")
        return

    print(f"Generating preview for {os.path.basename(font_path)}...")
    
    filename = os.path.basename(font_path)
    preview_img_path = os.path.join("preview", remove_ext(filename) + ".png")

    try:
        try:
            font_tt = ttLib.TTFont(font_path)
            font_name = short_name(font_tt)[1] or "Font"
        except ttLib.TTLibError as e:
            print(f"Error: Could not open font {os.path.basename(font_path)} for preview. It might be corrupted or an unsupported format. Reason: {e}")
            return
        except Exception as e:
            print(f"Error: An unexpected error occurred while reading font {os.path.basename(font_path)} for preview. Reason: {e}")
            return
        
        try:
            fb = FontBanner(font_path, 'landscape')
            fb.font_text = f'{font_name}\nAa Bb Cc Dd Ee Ff Gg\n1234567890'
            fb.bg_color = (20, 20, 20)
            fb.fg_color = (230, 230, 230)
            fb.set_font_size(80)
            fb.set_text_position('center')
            
            fw = FontWall([fb], 1, mode="horizontal")
            fw.draw(1)
            fw.save(preview_img_path)
            print(f"Preview saved to: {preview_img_path}")
        except Exception as e:
            print(f"Error generating preview image for {os.path.basename(font_path)}: {e}")
            print("Please ensure 'fontpreview' library is correctly installed and has all its dependencies.")
    except Exception as e:
        print(f"An unexpected error occurred during preview generation: {e}")


# --- Utility Functions ---

def extract(file, location):
    """Extracts an archive to a given location."""
    create_dir(location)
    print(f"Extracting {os.path.basename(file)} to {location}...")
    try:
        if file.lower().endswith(".7z"):
            shutil.unpack_archive(file, location)
        else:
            Archive(file).extractall(location)
        print("Extraction successful.")
        return True
    except Exception as e:
        print(f"Error during extraction of {os.path.basename(file)}: {e}")
        print("Please ensure the archive is not corrupted and that you have the necessary tools (e.g., 7zip) installed if it's a .7z file.")
        return False


def find(pattern, path):
    """Finds files matching a pattern in a directory."""
    result = []
    for root, _, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


def find_font(font_list, style):
    """
    Finds a specific font style from a list of font files based on OMF naming conventions.
    It tries to match fonts using several strategies:
    1. Exact match with OMF short name (e.g., 'ur.ttf' matches 'ur').
    2. Partial match with OMF short name within the filename (e.g., 'MyFont-ur.ttf' matches 'ur').
    3. Match with common style names (e.g., 'Regular' for 'ur') using a predefined map.
    4. Fallback to font metadata (full font name, family name, and style names).
    5. As a last resort for 'ur' (Regular), it returns the first available font.
    """
    style_base = remove_ext(style).lower()  # e.g., 'ur' from 'ur.ttf'

    # Predefined mapping for common style names to OMF short names
    common_names_map = {
        "ur": ["regular", "book", "roman"], "ir": ["italic", "oblique"],
        "ub": ["bold"], "ib": ["bolditalic"],
        "ut": ["thin"], "it": ["thinitalic"],
        "ul": ["light"], "il": ["lightitalic"],
        "um": ["medium"], "im": ["mediumitalic"],
        "usb": ["semibold", "demibold"], "isb": ["semibolditalic", "demibolditalic"],
        "ueb": ["extrabold", "ultrabold"], "ieb": ["extrabolditalic", "ultrabolditalic"],
        "ubl": ["black", "heavy"], "ibl": ["blackitalic", "heavyitalic"],
        "ucl": ["condensedlight"], "icl": ["condensedlightitalic"],
        "ucr": ["condensedregular"], "icr": ["condenseditalic"],
        "ucb": ["condensedbold"], "icb": ["condensedbolditalic"],
        "ucbl": ["condensedblack"], "icbl": ["condensedblackitalic"],
        "uml": ["monolight"], "iml": ["monolightitalic"],
        "umr": ["monoregular"], "imr": ["monoitalic"],
        "umb": ["monobold"], "imb": ["monobolditalic"],
        "umbl": ["monoblack"], "imbl": ["monoblackitalic"],
        "sfr": ["serifregular"], "sfi": ["serifitalic"],
        "sfb": ["serifbold"], "sfbi": ["serifbolditalic"],
        "sfbl": ["serifblack"], "sfbl": ["serifblackitalic"],
        "smr": ["serifmonoregular"], "smi": ["serifmonoitalic"],
        "smb": ["serifmonobold"], "smbi": ["serifmonobolditalic"],
    }

    # Helper to normalize font filenames for matching
    def normalize_filename(filename):
        return remove_ext(filename).lower().replace("-", "").replace("_", "")

    # Strategy 1: Exact match with OMF short name (e.g., 'ur.ttf' matches 'ur')
    for font_path in font_list:
        if normalize_filename(os.path.basename(font_path)) == style_base:
            return font_path

    # Strategy 2: Partial match with OMF short name within the filename
    for font_path in font_list:
        if style_base in normalize_filename(os.path.basename(font_path)):
            return font_path

    # Strategy 3: Match with common style names
    if style_base in common_names_map:
        for common_name in common_names_map[style_base]:
            for font_path in font_list:
                if common_name in normalize_filename(os.path.basename(font_path)):
                    return font_path

    # Strategy 4: Fallback to font metadata (full font name, family name, and style names)
    for font_path in font_list:
        try:
            font = ttLib.TTFont(font_path)
            # NameID 4: Full font name
            # NameID 1: Font family name
            # NameID 2: Font Subfamily name (e.g., "Regular", "Bold Italic")
            font_names = [
                record.string.decode('utf-16-be') if b'\x00' in record.string else record.string.decode('latin-1')
                for record in font['name'].names
                if record.nameID in [1, 2, 4]
            ]
            
            for name_str in font_names:
                if style_base in name_str.lower().replace(" ", ""):
                    return font_path
        except ttLib.TTLibError as e:
            print(f"Warning: Could not read font metadata for {os.path.basename(font_path)}. It might be corrupted or an unsupported format. Reason: {e}")
            continue
        except Exception as e:
            print(f"Warning: An unexpected error occurred while reading font metadata for {os.path.basename(font_path)}. Reason: {e}")
            continue

    # Strategy 5: As a last resort for 'ur' (Regular), return the first available font
    if style_base == "ur":
        for font_path in font_list:
            if "regular" in normalize_filename(os.path.basename(font_path)) or "book" in normalize_filename(os.path.basename(font_path)):
                return font_path
        if font_list:
            return font_list[0]

    return None


def short_name(font):
    """Gets the short name from a font's names table."""
    name = ""
    family = ""
    for record in font['name'].names:
        try:
            if b'\x00' in record.string:
                name_str = record.string.decode('utf-16-be')
            else:
                name_str = record.string.decode('latin-1')
            
            if record.nameID == 4 and not name: # Full font name
                name = name_str
            elif record.nameID == 1 and not family: # Font family
                family = name_str
            if name and family:
                break
        except:
            continue
    return (name, family)


def paste_to_template(flist, dest_dir):
    """Copies found fonts to the template directory."""
    print("Copying fonts to template...")
    for font_style, font_path in flist:
        if font_path:
            dest_path = os.path.join(dest_dir, font_style + ".ttf")
            try:
                if os.path.exists(font_path):
                    shutil.copy(font_path, dest_path)
                    # print(f"  - Copied {os.path.basename(font_path)} to {os.path.basename(dest_path)}")
            except IOError as e:
                print(f"Error copying {os.path.basename(font_path)} to {os.path.basename(dest_path)}: {e}")
                raise Exception(f"Failed to copy font file: {os.path.basename(font_path)}")

    # Fill missing fonts with regular
    regular_font_path = return_font(flist, "ur")
    if not regular_font_path:
        # If no regular, use the first available font
        for _, fp in flist:
            if fp:
                regular_font_path = fp
                break
    
    if regular_font_path:
        for font_style, font_path in flist:
            if not font_path:
                dest_path = os.path.join(dest_dir, font_style + ".ttf")
                try:
                    shutil.copy(regular_font_path, dest_path)
                    # print(f"  - Filled missing {font_style} with {os.path.basename(regular_font_path)}")
                except IOError as e:
                    print(f"Error copying {os.path.basename(regular_font_path)} to {os.path.basename(dest_path)}: {e}")
                    raise Exception(f"Failed to fill missing font: {os.path.basename(regular_font_path)}")


def def_orig_flist(all_fonts):
    """Creates the initial font list structure."""
    return [[remove_ext(i), False] for i in all_fonts]

def return_font(array, value):
    """Returns a font path from the list based on style."""
    for style, path in array:
        if style == value:
            return path
    return None

def remove_ext(file_with_ext):
    """Removes the extension from a filename."""
    return os.path.splitext(file_with_ext)[0]


def create_dir(folder):
    """Creates a directory if it doesn't exist."""
    if not os.path.exists(folder):
        os.makedirs(folder)


def wipe_files(path_to_folder):
    """Deletes all files and subdirectories in a folder."""
    if not os.path.exists(path_to_folder):
        return
    for filename in os.listdir(path_to_folder):
        file_path = os.path.join(path_to_folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

def initialize():
    """Initializes the script environment."""
    print("Initializing...")
    create_dir("output")
    create_dir("preview")
    create_dir("temp_font_dir")
    wipe_files(TEMPLATE["fonts_dir"])
    wipe_files("temp_font_dir")

def check_and_update_omf_template():
    """Checks for a new OMF template version and updates if available."""
    local_version = ""
    remote_version = ""
    
    # Read local version
    local_module_prop_path = os.path.join(TEMPLATE["dir"], "module.prop")
    if os.path.exists(local_module_prop_path):
        with open(local_module_prop_path, "r") as f:
            for line in f:
                if line.startswith("omfversion="):
                    local_version = line.split("=")[1].strip()
                    break
    
    print(f"Local OMF template version: {local_version if local_version else 'Not found'}")

    # Fetch remote version
    remote_module_prop_url = "https://gitlab.com/nongthaihoang/omftemplate/-/raw/master/module.prop?ref_type=heads"
    temp_clone_dir = "temp_omf_clone"
    remote_version = ""

    try:
        response = requests.get(remote_module_prop_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        for line in response.text.splitlines():
            if line.startswith("omfversion="):
                remote_version = line.split("=")[1].strip()
                break
        print(f"Remote OMF template version: {remote_version if remote_version else 'Not found'}")

        if remote_version and (not local_version or remote_version > local_version):
            print("New OMF template version available. Updating...")
            # Remove old template
            if os.path.exists(TEMPLATE["dir"]):
                shutil.rmtree(TEMPLATE["dir"])
                print("Old OMF template removed.")

            # Clone the repository and copy new template
            print(f"Cloning omftemplate to {temp_clone_dir}...")
            try:
                subprocess.run(['git', 'clone', 'https://gitlab.com/nongthaihoang/omftemplate.git', temp_clone_dir], check=True, capture_output=True, text=True)
            except subprocess.CalledProcessError as e:
                print(f"Error cloning repository: {e.stderr}")
                return
            
            # Copy new template from cloned repo
            shutil.copytree(temp_clone_dir, TEMPLATE["dir"], dirs_exist_ok=True) # Use dirs_exist_ok for Python 3.8+
            print("OMF template updated successfully.")
        else:
            print("OMF template is up to date.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching remote OMF template version: {e}")
    except Exception as e:
        print(f"Error during OMF template update: {e}")
    finally:
        # Clean up the cloned repository
        if os.path.exists(temp_clone_dir):
            shutil.rmtree(temp_clone_dir)
            print("Cleaned up temporary clone directory.")

def clear_temp_folders():
    """Clears temporary folders."""
    print("Cleaning up temporary files...")
    wipe_files("temp_font_dir")

def create_module(font_path):
    """Creates the Magisk font module."""
    temp_font_dir = "temp_font_dir"
    font_list = []

    if font_path.lower().endswith(ZIP_EXT):
        if not extract(font_path, temp_font_dir):
            raise Exception("Failed to extract font archive.")
        font_list = find("*.ttf", temp_font_dir)
        if not font_list:
            font_list = find("*.otf", temp_font_dir)
    elif font_path.lower().endswith(FONT_EXT):
        font_list = [font_path]
    else:
        print(f"Error: Unsupported file type for: {font_path}")
        return

    if not font_list:
        print("Error: No font files found in the provided path.")
        return

    print(f"Found {len(font_list)} font file(s).")
    flist = def_orig_flist(TEMPLATE["all_fonts"])
    
    for i, (style, _) in enumerate(flist):
        found_font = find_font(font_list, style)
        if found_font:
            flist[i][1] = found_font

    wipe_files(TEMPLATE["fonts_dir"])
    paste_to_template(flist, TEMPLATE["fonts_dir"])

    process_fonts_in_dir(TEMPLATE["fonts_dir"])

    try:
        font_family_name = short_name(ttLib.TTFont(font_list[0]))[1]
        if not font_family_name or font_family_name.isspace():
            font_family_name = remove_ext(os.path.basename(font_list[0]))
    except Exception:
        font_family_name = remove_ext(os.path.basename(font_list[0]))

    output_filename_base = os.path.join("output", f"OMF_{font_family_name.replace(' ', '')}")
    
    try:
        print(f"\nPackaging module to: {output_filename_base}.zip")
        shutil.make_archive(output_filename_base, 'zip', TEMPLATE["dir"])
        print("\nModule created successfully!")
    except Exception as e:
        raise Exception(f"Failed to package module: {e}")
    return font_list