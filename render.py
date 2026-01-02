import sys
import yaml
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML, CSS

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data" 
TEMPLATES_DIR = BASE_DIR / "template"
STYLES_DIR = BASE_DIR / "styles"
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok = True)

print("Initializing renderer...")

# Load YAML resume
filename = input("Enter file name (without extension): ").strip()
filename_ext = filename + ".yaml"

print("Reading file...")

try:
    with open(DATA_DIR / filename_ext, "r") as f:
        content = yaml.safe_load(f)
except Exception as e:
    print(f"Something went wrong. Error msg: {e}")
    sys.exit(1)

# Get HTML template
environment = Environment(loader = FileSystemLoader(TEMPLATES_DIR), 
                          autoescape=select_autoescape(["html", "xml"]))                         
template = environment.get_template("resume.html")

output_HTML = OUTPUT_DIR / (filename + "_easyresume.html")
output_PDF = OUTPUT_DIR / (filename + "_easyresume.pdf")

output_HTML.write_text(
    template.render(content),
    encoding="utf-8"
)

# Convert to PDF (critical: base_url)
HTML(
    filename=str(output_HTML),
    base_url=str(BASE_DIR)
).write_pdf(output_PDF,
            stylesheets = [CSS(filename = str(STYLES_DIR / "style.css"))])

print(f"Resume created at `{output_PDF}`!")
