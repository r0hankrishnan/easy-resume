from __future__ import annotations
from pathlib import Path
from importlib.resources import files, as_file

from playwright.sync_api import sync_playwright
from jinja2 import Environment, FileSystemLoader, select_autoescape

from easy_resume.models import Resume

PACKAGE_DIR = files("easy_resume")
STYLES_DIR = PACKAGE_DIR / "styles"
TEMPLATE_DIR = PACKAGE_DIR / "template"

SECTION_TITLE_MAP = {
    "education": "EDUCATION",
    "experience": "EXPERIENCE",
    "projects": "PROJECTS",
    "skills_inline": "SKILLS"
}

def resume_to_context(resume: Resume) -> dict:
    """Takes in a resume object and converts it to 
    a plain dict to be passed to a template via Jinja2.

    Args:
        resume (Resume): A resume object created from a
        parsed YAML file.

    Returns:
        dict: A plain dict with keys: ["header", "sections"]
        to be passed to an html template via Jinja2
    """
    # Order sections
    sections_by_type = {section.type: section for section in resume.sections}
    ordered_sections_dicts = [sections_by_type[section_type].model_dump() for section_type in resume.meta.section_order]
    
    # Resolve titles
    for section in ordered_sections_dicts:
        if not section["title"]:
            section["title"] = SECTION_TITLE_MAP[section["type"]]
            
    header_dict = resume.header.model_dump()     
    
    return {"header": header_dict,
            "sections": ordered_sections_dicts}
    
def render_html(context: dict, output_path: Path, theme:str) -> None:
    """Takes in a context dict (dict distilled from Resume object),
    adds stylesheet path, renders it into the template html using Jinja, 
    then writes the rendered html to output_path.

    Args:
        context (dict): Context dict of Resume object 
        (created from resume_to_context).
        output_path (Path): Path to write the filled in html file.
        theme (str): Theme name extracted from Resume object's meta attribute.

    """
    with as_file(STYLES_DIR / f"{theme}.css") as theme_path:
        context["stylesheet_path"] = theme_path.resolve().as_uri()
        
    with as_file(TEMPLATE_DIR) as template_dir:
        environment = Environment(
            loader = FileSystemLoader(str(template_dir)),
            autoescape = select_autoescape(["html", "xml"])
        )
        
        template = environment.get_template("resume.html")
        
        with open(output_path, "w", encoding = "utf-8") as f:
            f.write(template.render(context))
    
def html_to_pdf(html_path: Path, output_path: Path) -> None: 
    """Takes a filled in html file and converts it into a styled pdf
    using playwright.

    Args:
        html_path (Path): Path to filled in html file.
        output_path (Path): Path to write pdf output.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        page = browser.new_page()
        page.goto(html_path.resolve().as_uri(), wait_until = "load")
        
        page.pdf(
            path = str(output_path),
            format = "Letter",
            print_background = True,
            scale = 1.0
        )
        
        browser.close()
        
        

    
