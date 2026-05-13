## [0.0.2] - 2026-05-13
### Added
- Proper repository structure
- New YAML schema with Pydantic validation
- Modular reusable logic
- Html macros for composable sections

### Notes
I tried to use weasyprint instead but the outputs just were not up to par. I also did find out about RenderCV which is a much more mature version of this project that uses YAML > Typst > PDF. Given the fact that RenderCV is a more mature and built out version of this project, this will likely be the last update for this tool, unless a novel use/need arises.

### Fixed
- Syntax + formatting
- Incomplete html templates

---

## [0.0.1] - 2026-01-06
### Added
- Basic functionality
- Playwright-based PDF generation
- `input()`-based file I/O

### Notes
This is an extremely rough implementation of the idea. v0.0.2 will be a significant refactor exploring better rendering methods and creating a packagable repository. 

### Fixed
- N/A