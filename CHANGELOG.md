# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-04-08

### Added
- **Aesthetic Overhaul:** Implemented the "SOFTCURSE/SYS v3.0 OMEGA" design system.
- **Cyber Cursor:** Custom animated SVG "Cyber S" cursor with smooth triangular scaling and logic for hover/click states.
- **Rich Text Rendering:** High-fidelity support for ANSI escape codes (colors, bold, background) and system emojis.
- **Legacy Support:** Added `CP437` and `UTF-16` encoding support for `.nfo`, `.ans`, and local log files.
- **Navigation:** Multi-tab file viewer with real-time stats (size, line count).
- **GitHub Health:** Integrated comprehensive community health documentation (README, CONTRIBUTING, CoC, Security, Issue/PR templates).
- **Setup Script:** Inno Setup configuration for automated Windows installation and file associations.

### Changed
- Increased base font size to 16px across the editor for better visibility.
- Improved word-wrapping logic to preserve table formatting in text files.
- Updated build configuration (`softcurse_reader.spec`) to include assets and icons.

### Fixed
- Resolved `TypeError` in `pywebview` window creation (removed `easy_resize` parameter).
- Patched universal cursor override to ensure custom cursor visibility on all elements.
