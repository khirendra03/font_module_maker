
import fnmatch
import os
import shutil
from pyunpack import Archive
from py7zr import unpack_7zarchive
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
    "all_fonts": ["Regular.ttf","Light.ttf","ExtraLight.ttf","SemiBold.ttf","Medium.ttf","Black.ttf","Bold.ttf","BlackItalic.ttf","BoldItalic.ttf","ExtraLightItalic.ttf","ThinItalic.ttf","Thin.ttf", "SemiBoldItalic.ttf","MediumItalic.ttf","Italic.ttf","LightItalic.ttf","ExtraBold.ttf","ExtraBoldItalic.ttf",'Condensed-Regular.ttf', 'Condensed-Light.ttf', 'Condensed-ExtraLight.ttf', 'Condensed-SemiBold.ttf', 'Condensed-Medium.ttf', 'Condensed-Black.ttf', 'Condensed-Bold.ttf', 'Condensed-BlackItalic.ttf', 'Condensed-BoldItalic.ttf', 'Condensed-ExtraLightItalic.ttf', 'Condensed-ThinItalic.ttf', 'Condensed-Thin.ttf', 'Condensed-SemiBoldItalic.ttf', 'Condensed-MediumItalic.ttf', 'Condensed-Italic.ttf', 'Condensed-LightItalic.ttf', 'Condensed-ExtraBold.ttf', 'Condensed-ExtraBoldItalic.ttf'],
    "single_file": ["Regular.ttf"]
}
    
    print(f"Updated module.prop for '{fname}'")


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
            
            tt.save(font_path)
            # print(f"  - Fixed metrics for: {os.path.basename(font_path)}")
        except Exception as e:
            print(f"Warning: Could not process font {os.path.basename(font_path)}. Reason: {e}")


def generate_preview(font_path):
    """Generates a preview image for a given font."""
    if not os.path.exists(font_path):
        print(f"Error: Font file not found at '{font_path}'")
        return

    print(f"Generating preview for {os.path.basename(font_path)}...")
    clear_temp_folders()
    
    filename = os.path.basename(font_path)
    preview_img_path = os.path.join("preview", remove_ext(filename) + ".png")

    try:
        font_name = short_name(ttLib.TTFont(font_path))[1] or "Font"
        
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
        print(f"Error generating preview: {e}")


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
    except Exception as e:
        print(f"Error during extraction: {e}")


def find(pattern, path):
    """Finds files matching a pattern in a directory."""
    result = []
    for root, _, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


def find_font(font_list, style, filename=""):
    """Finds a specific font style from a list of font files."""
    # This is a simplified version of the original find_font logic
    style = style.lower()
    
    # First pass: strict filename matching
    for font_path in font_list:
        font_filename = remove_ext(os.path.basename(font_path)).lower()
        if style in font_filename.replace("-", "").replace("_", ""):
            return font_path

    # Second pass: check font metadata
    for font_path in font_list:
        try:
            font_name = short_name(ttLib.TTFont(font_path))[0].lower()
            if style in font_name:
                return font_path
        except:
            continue
            
    # Fallback for regular
    if style == "regular":
        for font_path in font_list:
            font_filename = remove_ext(os.path.basename(font_path)).lower()
            if "regular" in font_filename or "book" in font_filename:
                 return font_path
        return font_list[0] # Return the first font as a last resort

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
            if os.path.exists(font_path):
                shutil.copy(font_path, dest_path)
                # print(f"  - Copied {os.path.basename(font_path)} to {os.path.basename(dest_path)}")

    # Fill missing fonts with regular
    regular_font_path = return_font(flist, "Regular")
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
                shutil.copy(regular_font_path, dest_path)
                # print(f"  - Filled missing {font_style} with {os.path.basename(regular_font_path)}")


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
