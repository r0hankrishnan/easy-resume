from __future__ import annotations
from pathlib import Path
import argparse
import sys

from pydantic import ValidationError
import yaml

from easy_resume.models import Resume
from easy_resume.render import resume_to_context, render_html, html_to_pdf

def main():
    parser = argparse.ArgumentParser(description = "Generate a resume PDF from a YAML file")
    parser.add_argument("file", help = "Path to your YAML file.")
    parser.add_argument("--output", help = "Output directory (defaults to same directory as input)", default = None)
    args = parser.parse_args()
    
    yaml_path = Path(args.file)
    filename = yaml_path.stem
    
    output_dir = Path(args.output) if args.output else yaml_path.parent
    output_dir.mkdir(exist_ok = True, parents = True)
    
    output_html_path = output_dir / f"{filename}.html"
    output_pdf_path = output_dir / f"{filename}.pdf"

    try:
        with open(yaml_path, "r") as f:
            content = yaml.safe_load(f)
    except Exception as e:
        print(f"There was a problem in loading your YAML file: {e}")
        sys.exit(1)
    
    try:
        resume = Resume.model_validate(content)
    except ValidationError as e:
        print(f"Invalid resume format:\n{e}")
        sys.exit(1)
    
    theme = resume.meta.theme
    context = resume_to_context(resume = resume)
    
    render_html(context = context, output_path = output_html_path, theme = theme)
    
    html_to_pdf(html_path = output_html_path, output_path = output_pdf_path)

    print("succeeded")
    
if __name__ == "__main__":
    main()