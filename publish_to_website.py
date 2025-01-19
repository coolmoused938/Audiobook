import os
import markdown
import re

file_name = input("Enter the file name: ")
folder_path = r"D:\OBSIDIAN\NOTES"
md_file_path = os.path.join(folder_path, file_name + ".md")

def generate_toc(md_content):
    toc = []
    headings = re.findall(r"^(#{1,6})\s+(.*)$", md_content, re.MULTILINE)
    for level, heading in headings:
        # Calculate margin-left based on the number of `#` symbols in the heading
        margin_left = len(level)  # This gives the heading level (e.g., 1 for H1, 2 for H2)
        anchor = heading.lower().replace(" ", "-").replace(",", "").replace(".", "")
        toc.append(f'<li style="margin-left: {margin_left}em;"><a href="#{anchor}">{heading}</a></li>')
    if toc:
        return '<ul style="list-style-type: disc; padding-left: 20px;">' + ''.join(toc) + '</ul>'
    return ""

def add_ids_to_headings(md_content):
    def replace_heading(match):
        level, heading = match.groups()
        anchor = heading.lower().replace(" ", "-").replace(",", "").replace(".", "")
        return f'{level} <span id="{anchor}">{heading}</span>'
    
    md_content = re.sub(r"^(#{1,6})\s+(.*)$", replace_heading, md_content, flags=re.MULTILINE)
    return md_content

if os.path.exists(md_file_path):
    with open(md_file_path, "r", encoding="utf-8") as file:
        md_content = file.read()

    # Remove YAML front matter if present
    md_content = re.sub(r"^---.*?^---\s*", "", md_content, flags=re.DOTALL | re.MULTILINE)

    # Generate the table of contents and add IDs to headings
    toc = generate_toc(md_content)
    md_content_with_ids = add_ids_to_headings(md_content)

    # Convert Markdown to HTML
    html_content = markdown.markdown(md_content_with_ids)

    # Inline CSS without minification
    
    css_content = """
body {
    font-family: 'Lexend', sans-serif;
    padding: 20px;
    background-color: #1e1e1e;
    color: white;
    font-size: 1.3rem;
}
h1 {
    color: #f1f1f1;
    font-size: 2em;
}
p {
    line-height: 1.6;
    color: #d1d1d1;
}
a {
    color: #4CAF50;
    text-decoration: none;
}
a:hover {
    text-decoration: underline;
}
pre {
    background-color: #2e2e2e;
    padding: 15px;
    border-radius: 5px;
    color: #d1d1d1;
    font-family: monospace;
    font-size: 1.1rem;
    overflow-x: auto;
}
code {
    color: #ffcc00;
    font-family: monospace;
}
ul {
    list-style-type: disc;
    padding-left: 20px;
}
li {
    margin: 10px 0;
}
#toc {
    margin-bottom: 20px;
    padding: 0;
}
"""

    
    # Define the HTML template with the TOC and final content
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <title>{file_name}</title>
        <link href="https://fonts.googleapis.com/css2?family=Lexend&display=swap" rel="stylesheet">
        <style>
        {css_content}
        </style>
    </head>
    <body>
        <h1>{file_name}</h1>
        <div id="toc">{toc}</div>
        {html_content}
    </body>
    </html>
    """

    # Output HTML file path
    output_html_path = os.path.join(os.getcwd(), file_name + ".html")

    # Save the HTML without minification
    with open(output_html_path, "w", encoding="utf-8") as output_file:
        output_file.write(html_template)

    print(f"Conversion successful! HTML file saved as: {output_html_path}")
else:
    print(f"The file {md_file_path} does not exist.")
