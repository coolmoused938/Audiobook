import zipfile
import os
import html2text

def list_html_files(epub_path):
    html_files = []
    
    with zipfile.ZipFile(epub_path, 'r') as epub:
        # List all files in the EPUB
        for file in epub.namelist():
            # Check if the file has a .html extension
            if file.endswith('.html'):
                html_files.append(file)
                
    return html_files

def convert_html_to_md(epub_path, html_files):
    # Create output directory if it doesn't exist
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)

    # Initialize html2text object
    h = html2text.HTML2Text()
    h.body_width = 0  # Set body_width to 0 as requested

    with zipfile.ZipFile(epub_path, 'r') as epub:
        for html_file in html_files:
            # Read the HTML file content
            html_content = epub.read(html_file).decode('utf-8')
            
            # Convert HTML content to Markdown
            markdown_content = h.handle(html_content)

            # Get the base filename without the .html extension
            base_name = os.path.splitext(os.path.basename(html_file))[0]

            # Define the output file path with .md extension
            md_file_path = os.path.join(output_dir, f"{base_name}.md")
            
            # Save the markdown content to a .md file
            with open(md_file_path, 'w', encoding='utf-8') as md_file:
                md_file.write(markdown_content)
            print(f"Converted {html_file} to {md_file_path}")

# Get the EPUB file path from the user
epub_path = input("Enter the path to the EPUB file: ")

# Check if the path exists and is a valid EPUB
if os.path.exists(epub_path) and epub_path.endswith('.epub'):
    html_files = list_html_files(epub_path)
    if html_files:
        convert_html_to_md(epub_path, html_files)
    else:
        print("No HTML files found in the EPUB.")
else:
    print("Invalid path or the file is not an EPUB.")
