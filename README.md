# Font Module Script

This script helps you create custom Magisk font modules easily.

## Table of Contents
- [Installation](#installation)
- [How to Create Your Own Module](#how-to-create-your-own-module)
- [FAQs & Troubleshooting](#faqs--troubleshooting)
- [Supported Android Versions](#supported-android-versions)
- [Safety Disclaimer](#safety-disclaimer)

## Installation

To use this script, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-repo/font-script.git
    cd font-script
    ```
    (Replace `https://github.com/your-repo/font-script.git` with the actual repository URL)

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## How to Create Your Own Module

1.  **Run the script:**
    ```bash
    python make_module.py
    ```

2.  **Follow the prompts:** The script will guide you through the process, asking for:
    *   The path to your font file (`.ttf`, `.otf`) or a `.zip` archive containing fonts.
    *   Your preferred module template (OMF or MFFM).
    *   Whether to generate a font preview image.

3.  **Module Output:** The final Magisk module `.zip` will be saved in the `output/` folder.

## FAQs & Troubleshooting

*   **Q: My module isn't applying. What should I do?**
    *   A: Ensure your font files are valid. Check the Magisk logs for errors.
*   **Q: Can I use multiple font files?**
    *   A: Yes, you can provide a `.zip` file containing multiple font files. The script will process them accordingly.

## Supported Android Versions

This script aims to create modules compatible with Android 10 and above, leveraging Magisk's module system. Compatibility may vary based on specific ROMs and Magisk versions.

## Safety Disclaimer

*   **Use at your own risk:** Modifying system fonts can lead to boot loops or system instability if not done correctly. Always have a backup of your device.
*   **Magisk:** This script relies on Magisk for module installation. Ensure you have a working Magisk installation.
*   **Font Licensing:** Respect font licenses when creating and distributing modules.
