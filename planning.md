# Planning Document

This document is a recording of my learning process as I try to learn about project structuring and the engineering process by building this tool.

## How should I set up my repository? 

Sometimes I feel confused about what folders I should be making when starting a project and/or whether I should be formatting my project as a python library. As a rule of thumb, I should be clearly articulating **what** my project actually is before creating my file structures. In particular, is this project something that I expect users to **apply** or to **import and use**.

In this case, I expect the user to have a YAML file that they run my python script on to generate a cleanly formatted resume. This means that they should be importing anything or even really need to open a python file at all. Given this design choice, I can classify this project as building a **tool**, so I don't need to make it into a library.


## Key questions to answer

**Is this a tool or a library?**
- This is a tool. I expect a user to create a YAML file and then use this **tool** to generate a cleanly formatted resume.

**Who is the primary user?**
- I am the primary user. I've been having trouble getting interviews and want to be able to quickly and cleanly create tailored resumes for applications.

**What changes often vs rarely?**
- The YAML file will likely change often. It would be nice to create specific types of resumes for specific roles so I will likely have several YAML files.
- The HTML template file will not change often. Since the HTML file just has the general structure and placeholders, it should not be changing very often and is not a file that would be changed by the end user.
- The CSS file might change if I want to add different resume styles in the future but it will generally stay the same for a given style.

**Can I start with one script?**
- Yes. The script (for now) just needs to read in the YAML, parse the sections into variables, use those variables to dynamically fill in the HTML file, and convert and output the HTML file (with styling) as a pdf.

**What folders map cleanly to concerns?**
- I need a folder to hold the YAML files, a folder to hold the HTML template, and a folder for the CSS styling. I think the script can be in the root directory so that it is easy to call the script on a file.