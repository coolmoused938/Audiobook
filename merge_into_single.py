import os
import shutil

def merge_md_files(folder_name, output_path):
    # Change to the specified folder
    if not os.path.isdir(folder_name):
        print(f"Folder '{folder_name}' does not exist.")
        return
    
    os.chdir(folder_name)
    
    # List all files in the folder and filter for .md files
    md_files = sorted([f for f in os.listdir() if f.endswith('.md') and f.startswith('Chapter')])
    
    if not md_files:
        print("No markdown files found in the folder.")
        return
    
    # Sort files numerically based on the chapter number
    md_files.sort(key=lambda x: int(x.split()[1].split('.')[0]))
    
    # Ensure output path exists
    os.makedirs(output_path, exist_ok=True)
    
    # Merge content into a single file
    output_file_name = os.path.join(output_path, f"{os.path.basename(folder_name)}.md")
    with open(output_file_name, 'w', encoding='utf-8') as outfile:
        for md_file in md_files:
            with open(md_file, 'r', encoding='utf-8') as infile:
                outfile.write(infile.read() + '\n\n')  # Add some space between chapters
            print(f"Added {md_file} to {output_file_name}")
    
    print(f"All files have been merged into {output_file_name}")
    
    # Delete the folder after merging
    os.chdir('..')  # Move up one directory before deleting
    shutil.rmtree(folder_name)
    print(f"Folder '{folder_name}' has been deleted.")

# Get the folder name from the user
folder_name = input("Enter the folder name containing the markdown files: ")
output_path = "D:\OBSIDIAN\NOTES"
merge_md_files(folder_name, output_path)
