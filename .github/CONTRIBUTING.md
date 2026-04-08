# Contributing to SOFTCURSE/SYS

Welcome, runner. Thank you for your interest in enhancing the SOFTCURSE File Reader. 
Whether you're fixing a formatting bug, expanding our syntax highlighting engine, or pushing the UI aesthetic further into the void, your contributions are highly valued. 

By participating here, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## Ways to Contribute
- **Bug Reports:** Did the app crash? Did an ANSI escape code fail to render? Let us know.
- **Feature Requests:** Suggest new language support or UI toggles.
- **Code & Design:** Submit Pull Requests to improve the logic in Python or the visuals in Vanilla CSS.
- **Documentation:** Improve this documentation, our `BUILD.md` file, or inline comments.

## Reporting Bugs
Check if the issue already exists in the tracker. If not, open a new issue using the assigned template. Please include:
- Steps to reproduce the bug.
- Expected vs. actual behavior.
- Your OS, Python version, and any relevant error stack traces from the console.

## Suggesting Features
For large architectural changes, please open a GitHub Discussion first to see if the maintainers align with the vision. For smaller tweaks (like adding `.toml` to the syntax highlighter), simply open an Issue or PR.

## Development Setup
The project requires Python 3.12+ and runs natively on Windows.

1. **Fork & Clone**
   ```bash
   git clone https://github.com/softcurse/softcurse-reader.git
   cd softcurse-reader
   ```
2. **Install Dependencies**
   ```bash
   py -m pip install pywebview pyinstaller
   ```
3. **Run Locally**
   Execute the backend which will automatically launch the Chromium-based UI thread:
   ```bash
   py src/main.py
   ```

## Making Changes
### Branch Naming Convention
Please branch off `main` using the following format:
- `feat/description`
- `fix/description`
- `docs/description`

### Commit Conventions
We follow [Conventional Commits](https://www.conventionalcommits.org/).
- `feat: added support for rendering Markdown tables`
- `fix: parsing error for specific CP437 block characters`
- `style: updated cursor SVG path scaling`

### Testing and Linting
Ensure no syntax errors exist in your Python code and that vanilla JS stays clean. Since we rely on standard library features as much as possible, manual interface testing is highly encouraged. Check that drag & drop and file loading works after your edits.

## Submitting a Pull Request
1. Ensure your code works identically frozen (via PyInstaller) and unfrozen (via Python).
2. Validate that `ui.html` remains self-contained relative to the bundled `assets` directory.
3. Fill out the PR template carefully.
4. Maintainers will review the PR, typically within 48-72 hours. Expect professional, constructive feedback.

## Getting Help
If you are stuck building the project or testing Inno Setup parameters, reach out via email at softcursesystems@gmail.com or visit [softcurse-website.pages.dev](https://softcurse-website.pages.dev/).

Welcome to the system.
