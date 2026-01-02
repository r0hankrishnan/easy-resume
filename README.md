# Easy Resume

This tool allows you to write out your resume using YAML and then use python to create a properly formatted pdf of your resume. The goal of this project is to allow for rapid editing and tailoring of resumes without having to deal with Word formatting.

The current implementation uses `playwright` to ensure the custom CSS styling is properly reflected in the rendered PDF. While this does add some weight to the overall program, it is the most robust way to ensure formatting consistency. A potential next approach would be to use YAML -> LaTeX -> PDF instead of YAML -> HTML -> PDF with a python translator. 