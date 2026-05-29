import os
import re
from bs4 import BeautifulSoup

# Paths
base_dir = r"D:\EZ_REPO\BNB PROJECT"
html_file = os.path.join(base_dir, "BnB_Program_Design_Report.html")
content_dir = os.path.join(base_dir, "content")
template_file = os.path.join(base_dir, "report_template.html")
build_script = os.path.join(base_dir, "build_report.py")

if not os.path.exists(content_dir):
    os.makedirs(content_dir)

# Section Mapping
section_mapping = [
    ("vision", "01_vision.md"),
    ("philosophy", "02_philosophy.md"),
    ("structure", "03_structure.md"),
    ("curriculum", "04_curriculum.md"),
    ("programs", "05_programs.md"),
    ("summer", "06_summer.md"),
    ("timeline", "07_timeline.md"),
    ("content", "08_content.md"),
    ("assessment", "09_assessment.md"),
    ("pedagogical", "10_pedagogy.md"),
    ("strategic", "11_strategic.md"),
    ("location", "12_location.md")
]

# Read HTML
with open(html_file, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# Extract Sections
for i, (section_id, filename) in enumerate(section_mapping, 1):
    section = soup.find("section", id=section_id)
    if section:
        # Extract inner HTML
        inner_html = "".join([str(child) for child in section.contents])
        # Save to file
        with open(os.path.join(content_dir, filename), "w", encoding="utf-8") as f_out:
            f_out.write(inner_html.strip())
        
        # Replace in soup with marker
        marker = soup.new_string(f"{{{{ SECTION_{i:02d} }}}}")
        section.clear()
        section.append(marker)

# Add Update Button to Sidebar
nav = soup.find("nav")
if nav:
    # Create the button HTML
    btn_html = '''
    <div style="padding: 18px 18px 6px;">
        <button onclick="alert('To sync changes:\\n1. Edit the .md files in the content/ folder\\n2. Run \\'python build_report.py\\' in your terminal')" 
                style="background: #b5724a; color: white; border: none; border-radius: 5px; padding: 8px 12px; cursor: pointer; font-size: 0.75rem; width: 100%; font-weight: bold;">
            🔄 Update Report
        </button>
    </div>
    '''
    btn_soup = BeautifulSoup(btn_html, "html.parser")
    nav.insert(0, btn_soup)

# Save Template
# We use a custom string replacement for markers to ensure they are not escaped by prettify
template_html = soup.prettify()

with open(template_file, "w", encoding="utf-8") as f_tpl:
    f_tpl.write(template_html)

# Create Build Script
build_script_content = r'''import os

# Paths
base_dir = os.path.dirname(os.path.abspath(__file__))
template_file = os.path.join(base_dir, "report_template.html")
content_dir = os.path.join(base_dir, "content")
output_file = os.path.join(base_dir, "BnB_Program_Design_Report.html")

sections = [
    "01_vision.md", "02_philosophy.md", "03_structure.md", 
    "04_curriculum.md", "05_programs.md", "06_summer.md", 
    "07_timeline.md", "08_content.md", "09_assessment.md", 
    "10_pedagogy.md", "11_strategic.md", "12_location.md"
]

def build():
    if not os.path.exists(template_file):
        print(f"Error: Template file not found at {template_file}")
        return

    with open(template_file, "r", encoding="utf-8") as f:
        html = f.read()

    for i, filename in enumerate(sections, 1):
        file_path = os.path.join(content_dir, filename)
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f_in:
                content = f_in.read()
                # Use regex to find and replace the marker to handle potential whitespace from prettify
                pattern = re.compile(rf"\{{\{{\s*SECTION_{i:02d}\s*\}}\}}")
                html = pattern.sub(content, html)
        else:
            print(f"Warning: Content file {filename} not found.")

    with open(output_file, "w", encoding="utf-8") as f_out:
        f_out.write(html)
    
    print(f"Success! Report updated at {output_file}")

if __name__ == "__main__":
    build()
'''

with open(build_script, "w", encoding="utf-8") as f_build:
    f_build.write(build_script_content)

print("Modularization complete!")
