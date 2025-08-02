# Interactive Font Module Script

This script provides a fast and easy way to create flashable Magisk font modules directly from your command line. It is designed to be simple, interactive, and self-contained.

You can package a single font file (`.ttf` or `.otf`) or a `.zip` archive containing multiple font styles into a module using the OMF template.

## Features

*   **Interactive CLI:** A user-friendly command-line interface that guides you through every step.
*   **Multiple File Types:** Supports single `.ttf` and `.otf` font files, as well as `.zip` archives.
*   **OMF Template:** Uses the OMF (Oh My Font) template.
*   **Font Preview:** Generate a `.png` image preview for any single font file to see how it looks before creating the module.
*   **Automatic Font Mapping:** When using a zip archive, the script intelligently maps different font weights (like Bold, Italic, Thin, etc.) to their correct places in the template.
*   **Self-Contained:** The project includes the template, so you don't need to download it separately.

## Installation & Usage

### 1. Prerequisites

*   Python 3.x
*   Pip (Python package installer)

### 2. Installation

Clone or download the project, then navigate into the `font-script` directory and install the required Python libraries:

```bash
# Navigate to the project folder
cd /path/to/font-script

# Install dependencies
pip install -r requirements.txt
```

### 3. Running the Script

Once the dependencies are installed, run the main script:

```bash
python make_module.py
```

### 4. The Process

The script will then ask you a series of questions:

1.  **Enter Font Path:** Provide the full, absolute path to your font file or zip archive.
    *   *Tip:* You can often drag and drop the file directly onto your terminal window to paste the full path.
2.  **Generate a Preview:** Choose `y` (yes) if you want to create a `.png` preview image of your font. This is highly recommended for single font files.
    *   *Note:* Preview generation is currently only supported for single `.ttf` or `.otf` files, not for zip archives.

After you answer the questions, the script will process the files and create your flashable Magisk module.

### 5. Get Your Module

The finished `.zip` module will be saved in the **`output`** directory. You can then transfer this file to your phone and flash it using Magisk Manager.

## Usage Example

Here is an example of a session to create a module from a single font file named `MyCoolFont-Regular.ttf`.

```bash
$ python make_module.py
--- Interactive Font Module Script ---

Enter the full path to your font file (.ttf, .otf) or zip archive: 
> /home/user/Downloads/MyCoolFont-Regular.ttf

Do you want to generate a font preview image? (y/n): 
> y

Starting module creation with the 'OMF' template...
Generating preview for MyCoolFont-Regular.ttf...
Preview saved to: preview/MyCoolFont-Regular.png
Processing single font: MyCoolFont-Regular.ttf
Updated module.prop for 'MyCoolFont-Regular'

Module 'MyCoolFont-Regular.zip' created successfully in the 'output' folder!
Cleaning temporary folders...
```

This will create two files:
*   `output/MyCoolFont-Regular.zip` (The flashable Magisk module)
*   `preview/MyCoolFont-Regular.png` (The font preview image)

## Project Structure

```
font-script/
├── make_module.py      # The main interactive script you will run
├── font_processor.py   # The core logic for processing fonts and zips
├── requirements.txt    # A list of the required Python libraries
├── README.md           # This file
├── templates/          # Contains the module templates
│   └── OMF/            # The Oh My Font template
├── output/             # Where the final flashable modules are saved
├── preview/            # Where generated font previews are saved
└── temp_*/             # Temporary folders used during processing (can be ignored)
```