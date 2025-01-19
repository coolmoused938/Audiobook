import os
import re
from dotenv import load_dotenv
from google import genai
import itertools

# Load environment variables from .env file
load_dotenv()

# Load all API keys from .env (API-1 to API-10)
API_KEYS = [os.getenv(f'API-{i}') for i in range(1, 11)]

# Create a round-robin iterator for API keys
api_key_cycle = itertools.cycle(API_KEYS)

# Function to load content from a file
def load_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Function to extract chapter content using regex
def extract_chapter_content(content, chapter_name):
    pattern = r'(^|\n)##\s+' + re.escape(chapter_name) + r'\s*(.*?)(?=\n##\s+|$)'
    match = re.search(pattern, content, re.DOTALL)
    return match.group(2).strip() if match else None

# Function to chunk the content into 25 paragraphs
def chunk_text(text, paragraph_limit=25):
    paragraphs = text.split('\n')
    return ['\n'.join(paragraphs[i:i + paragraph_limit]) for i in range(0, len(paragraphs), paragraph_limit)]

# Function to send a request to Gemini API and get simplified content
def simplify_text_with_gemini(text):
    # Get the next API key in the round-robin cycle
    api_key = next(api_key_cycle)
    client = genai.Client(api_key=api_key)
    
    # Multi-line prompt without chunk number
    prompt = f"""
    This text is taken from a book:

    {text}

    Instruction:
    Replace the tough English words with easier alternatives. 
    Do not modify anything else.

    Points to Note: 
    Do not need the list of changes done or any kind of explanation.
    Only give me the output in the prescribed format.

    Output Format: 
    {{OUTPUT}}
    """
    
    try:
        response = client.models.generate_content(model='gemini-2.0-flash-exp', contents=prompt)
        return response.text
    except Exception as e:
        print(f"Error with API key {api_key}: {e}")
        return None

# Function to save content to an output file
def save_output(output_path, content):
    with open(output_path, 'a', encoding='utf-8') as output_file:
        output_file.write(content)

# Function to clean the output file
def clean_output_file(output_path):
    with open(output_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Remove occurrences of {OUTPUT}, {{OUTPUT}}, {, and }
    cleaned_content = re.sub(r'\{\{?OUTPUT\}?\}|\{|\}', '', content)
    
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_content)

# Function to process chapter and send chunks to Gemini API
def process_chapter(file_name, chapter_name, notes_dir):
    md_file_path = os.path.join(notes_dir, f"{file_name}.md")
    
    # Load the content of the markdown file
    content = load_file(md_file_path)
    
    # Extract the chapter content
    chapter_content = extract_chapter_content(content, chapter_name)
    if not chapter_content:
        print(f"Chapter '{chapter_name}' not found in the file.")
        return
    
    # Chunk the extracted content into 25 paragraphs
    chunks = chunk_text(chapter_content)
    total_chunks = len(chunks)
    
    # Add chapter heading to the simplified content
    simplified_content = f"## {chapter_name}\n\n"
    
    # Process each chunk and send to Gemini API
    for index, chunk in enumerate(chunks, start=1):
        print(f"Processing chunk {index}/{total_chunks}...")
        simplified_text = simplify_text_with_gemini(chunk)
        if simplified_text:
            simplified_content += simplified_text + "\n\n"
    
    # Output file path with the simplified content
    output_file_path = os.path.join(notes_dir, f"{file_name} (Simplified).md")
    save_output(output_file_path, simplified_content)

    # Clean the output file after all processing is done
    clean_output_file(output_file_path)

    print(f"Simplified and cleaned content saved to {output_file_path}")

# Main function to ask for user input and start the process
def main():
    file_name = input("Enter the file name (without extension): ").strip()
    chapter_name = input("Enter the chapter name (e.g., Chapter 1): ").strip()
    notes_dir = r"D:\OBSIDIAN\NOTES"
    
    process_chapter(file_name, chapter_name, notes_dir)

if __name__ == "__main__":
    main()
