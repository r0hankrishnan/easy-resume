import sys
import yaml
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data" 
TEMPLATES_DIR = BASE_DIR / "template"
STYLES_DIR = BASE_DIR / "styles"
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok = True)

def html_to_pdf(html_path: Path, output_pdf: Path):
    html_path = html_path.resolve()
    output_pdf = output_pdf.resolve()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        page.goto(html_path.as_uri(), wait_until="load")

        page.pdf(
            path=str(output_pdf),
            format="Letter",
            print_background=True,
            scale=1.0
        )

        browser.close()
        

if __name__ == "__main__":
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
    with open(output_HTML, "w", encoding="utf-8") as f:
        f.write(template.render(content))
        
    output_PDF = OUTPUT_DIR / (filename + "_easyresume.pdf")

    html_to_pdf(
    html_path=output_HTML,
    output_pdf=output_PDF
    )

    print(f"Resume created at `{output_PDF}`!")