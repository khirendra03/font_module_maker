import os
import font_processor as fp

def main():
    """
    Main function to run the interactive script for creating Magisk font modules.
    It guides the user through selecting a font file, generating a preview,
    and creating the module.
    """
    # Initialize the environment (create necessary directories, wipe old files)
    fp.initialize()
    # Check and update the OMF template to the latest version from GitLab
    fp.check_and_update_omf_template()

    print("--- Interactive Font Module Script ---")

    # Step 1: Get the path to the user's font file or zip archive
    font_path = ""
    while True:
        path_input = input("\nEnter the full path to your font file (.ttf, .otf) or zip archive: \n> ")
        # Remove leading/trailing whitespace and quotes for easier input (e.g., drag-and-drop)
        font_path = path_input.strip().strip('"\'')
        if os.path.exists(font_path):
            break
        else:
            print("\nError: File not found. Please enter a valid path.")

    # Step 2: Ask user if they want to generate a font preview image
    preview_input = ""
    while True:
        preview_input = input("\nDo you want to generate a font preview image? (y/n): ").lower().strip()
        if preview_input in ['y', 'yes'] or preview_input in ['n', 'no']:
            break
        else:
            print("\nInvalid choice. Please enter y or n.")

    # Step 3: Create the Magisk font module
    print(f"\nStarting module creation with the 'OMF' template...")
    processed_font_list = None # Initialize to None
    try:
        # Call the core function to create the module. This function returns a list of processed fonts.
        processed_font_list = fp.create_module(font_path)

        # If preview was requested and fonts were successfully processed, generate the preview
        if preview_input in ['y', 'yes'] and processed_font_list:
            print("\nGenerating font preview...")
            # Use the first processed font for preview generation
            fp.generate_preview(processed_font_list[0])
        elif preview_input in ['y', 'yes'] and not processed_font_list:
            print("\nNote: No fonts were processed, so a preview cannot be generated.")
    except Exception as e:
        # Catch any exceptions during module creation and provide user feedback
        print(f"\nError during module creation: {e}")
        print("Please check the font file and try again.")
        processed_font_list = None # Ensure processed_font_list is None on error

    # Step 4: Clean up temporary folders used during the process
    fp.clear_temp_folders()

if __name__ == "__main__":
    main()