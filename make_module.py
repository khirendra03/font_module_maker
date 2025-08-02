import os
import font_processor as fp

def main():
    """Main function to run the interactive script."""
    fp.initialize()
    fp.check_and_update_omf_template()

    print("--- Interactive Font Module Script ---")

    # 1. Get Font Path
    font_path = ""
    while True:
        path_input = input("\nEnter the full path to your font file (.ttf, .otf) or zip archive: \n> ")
        font_path = path_input.strip().strip('"\'') # Allow dropping files in terminal
        if os.path.exists(font_path):
            break
        else:
            print("\nError: File not found. Please enter a valid path.")

    # 2. Generate Preview (Optional)
    while True:
        preview_input = input("\nDo you want to generate a font preview image? (y/n): ").lower().strip()
        if preview_input in ['y', 'yes']:
            break
        elif preview_input in ['n', 'no']:
            break
        else:
            print("\nInvalid choice. Please enter y or n.")

    # 4. Create Module
    print(f"\nStarting module creation with the 'OMF' template...")
    try:
        processed_font_list = fp.create_module(font_path)

        # Generate Preview (Optional) - moved here to use processed_font_list
        if preview_input in ['y', 'yes'] and processed_font_list:
            print("\nGenerating font preview...")
            fp.generate_preview(processed_font_list[0])
        elif preview_input in ['y', 'yes'] and not processed_font_list:
            print("\nNote: No fonts were processed, so a preview cannot be generated.")
    except Exception as e:
        print(f"\nError during module creation: {e}")
        print("Please check the font file and try again.")
        processed_font_list = None # Ensure processed_font_list is None on error

    # 5. Clean up
    fp.clear_temp_folders()

if __name__ == "__main__":
    main()