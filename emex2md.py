import os
import glob
import re
from lxml import etree
import html2text
from datetime import datetime

def postprocess_markdown(content_md):
    """
    Postprocess Markdown content to address specific formatting issues.
    """

    # Remove new lines appearing immediately after Bold heading. 
    content_md = re.sub(r'\*\*(.*?)\*\*\n\n', r'**\1**\n', content_md)

    # Remove line break between list items. 
    content_md = re.sub(r'(\s*\*\s.*?)(\n)(?=\s*\*)', r'\1 ', content_md)

    ## Condense more than 2 empty lines into 2 empty lines. 
    content_md = re.sub(r'(\n\s*){3,}', '\n\n', content_md)
    
    return content_md

def generate_timeline(entries, notebook_path):
    with open(os.path.join(notebook_path, 'timeline.md'), 'w', encoding='utf-8') as timeline_file:
        for date in sorted(entries.keys(), reverse=True):
            date_str = datetime.strftime(date, "%d %b %y")
            timeline_file.write(f"### {date_str}\n")
            for note_title, tags in entries[date]:
                tags_str = ', '.join(tags) if tags else ''  # Convert tag list to string
                if tags_str != '':
                    timeline_file.write(f"* [[{note_title}]] - {tags_str}\n")
                else:
                    timeline_file.write(f"* [[{note_title}]]\n")
            timeline_file.write("\n")

def enex_to_md(enex_file_path):
    h = html2text.HTML2Text()
    h.body_width = 0
    
    notebook_name = os.path.splitext(os.path.basename(enex_file_path))[0]
    output_dir = os.path.join(os.getcwd(), "output") 
    os.makedirs(output_dir, exist_ok=True)  

    notebook_path = os.path.join(output_dir, notebook_name)
    notes_path = os.path.join(notebook_path, "notes")
    os.makedirs(notes_path, exist_ok=True)
    
    timeline_entries = {}

    with open(enex_file_path, 'rb') as file:
        tree = etree.parse(file)
    
    for note in tree.xpath('//note'):
        title = note.find('title').text.replace('/', '_').replace('\\', '_')
        content = note.find('content').text
        created = note.find('created').text
        
        # Fetch tags for the current note
        tags = [tag.text for tag in note.xpath('./tag')]
        
        date_created = datetime.strptime(created, "%Y%m%dT%H%M%SZ")
        
        # Store the note title along with its tags in the timeline entries
        if date_created not in timeline_entries:
            timeline_entries[date_created] = []
        timeline_entries[date_created].append((title, tags))
        
        content_md = h.handle(content)
        content_md_processed = postprocess_markdown(content_md)
        
        md_filename = f"{title}.md"
        md_filepath = os.path.join(notes_path, md_filename)
        with open(md_filepath, 'w', encoding='utf-8') as md_file:
            md_file.write(content_md_processed)

    generate_timeline(timeline_entries, notebook_path)

def process_folder(folder_path):
    enex_files = glob.glob(os.path.join(folder_path, '*.enex'))
    for file_path in enex_files:
        print(f"Processing: {file_path}")
        enex_to_md(file_path)
    print("All files processed.")

if __name__ == "__main__":
    enex_folder_path = os.path.join(os.getcwd(), "input") 
    process_folder(enex_folder_path)