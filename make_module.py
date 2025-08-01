
import os
import font_processor as fp

def main():
    """Main function to run the interactive script."""
    fp.initialize()

    print("--- Interactive Font Module Script ---")

    # 1. Get Font Path
    font_path = ""
    while True:
        path_input = input("\nEnter the full path to your font file (.ttf, .otf) or zip archive: \n> ")
        font_path = path_input.strip().strip('\"'') # Allow dropping files in terminal
        if os.path.exists(font_path):
            break
        else:
            print("\nError: File not found. Please enter a valid path.")

    # 2. Choose Template
    template_type = ""
    while True:
        template_input = input("\nChoose a template (1 for OMF, 2 for MFFM): \n1. OMF (Recommended)\n2. MFFM\n> ").strip()
        if template_input == '1':
            template_type = "OMF"
            break
        elif template_input == '2':
            template_type = "MFFM"
            break
        else:
            print("\nInvalid choice. Please enter 1 or 2.")

    # 3. Generate Preview (Optional)
    while True:
        preview_input = input("\nDo you want to generate a font preview image? (y/n): ").lower().strip()
        if preview_input in ['y', 'yes']:
            if font_path.lower().endswith(fp.FONT_EXT):
                fp.generate_preview(font_path)
            else:
                print("\nNote: Preview for zip archives is not currently supported. A preview will not be generated.")
            break
        elif preview_input in ['n', 'no']:
            break
        else:
            print("\nInvalid choice. Please enter y or n.")

    # 4. Create Module
    print(f"\nStarting module creation with the 'OMF' template...")
    fp.create_module(font_path)

    # 5. Clean up
    fp.clear_temp_folders()

if __name__ == "__main__":
    main()
