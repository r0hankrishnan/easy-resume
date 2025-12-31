import yaml
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data" 
TEMPLATES_DIR = BASE_DIR / "template"
STYLES_DIR = BASE_DIR / "styles"
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok = True)

print("Initializing renderer...")

# Load YAML resume
filename = "example.yaml"
with open(DATA_DIR / filename, "r") as f:
    content = yaml.safe_load(f)
    
print(content)
print(content["education"])
print(content["experience"])

    
# Get HTML template
environment = Environment(loader = FileSystemLoader(TEMPLATES_DIR))
template = environment.get_template("resume.html")

print(template)

print(template.render(content))

# Output HTML
output_filename = "output.html"
with open(OUTPUT_DIR / output_filename, "w") as file:
    file.write(template.render(content))
