import re
import os

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
