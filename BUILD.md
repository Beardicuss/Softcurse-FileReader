# ◆ SOFTCURSE FILE READER — BUILD GUIDE

## Requirements
- Windows 10/11 (for final exe packaging)
- Python 3.10+ (64-bit)
- [Inno Setup 6](https://jrsoftware.org/isinfo.php) (for installer)

---

## Step 1 — Install Python Dependencies

```bash
pip install pywebview pyinstaller
```

On Windows, pywebview uses the built-in **WebView2** (Edge) — no extra install needed on Windows 10+.

---

## Step 2 — Build the Executable

```bash
# From the project root:
pyinstaller softcurse_reader.spec
```

This creates `dist/SoftcurseFileReader/` with the standalone app.

**Test it:**
```bash
dist\SoftcurseFileReader\SoftcurseFileReader.exe
```

---

## Step 3 — Build the Installer EXE

1. Install [Inno Setup 6](https://jrsoftware.org/isdl.php)
2. Open `installer.iss` in Inno Setup
3. Press **Compile** (Ctrl+F9)
4. Find your installer at: `installer_output\SoftcurseFileReader_Setup_v1.0.0.exe`

Or from command line:
```bash
iscc installer.iss
```

---

## Project Structure

```
softcurse-reader/
├── src/
│   ├── main.py          ← Python backend (pywebview API)
│   └── ui.html          ← Full UI (HTML/CSS/JS — SOFTCURSE styled)
├── softcurse_reader.spec ← PyInstaller build config
├── installer.iss         ← Inno Setup installer script
└── BUILD.md              ← This file
```

---

## Features

- **Universal text file support** — 100+ extensions
- **Syntax highlighting** — Python, JS/TS, HTML, CSS, JSON, YAML, XML, SQL, Shell, C/C++, Java, Rust, Go, Ruby, PHP, Lua, and more
- **Multi-tab** interface with file sidebar
- **Drag & drop** file opening
- **Live search** with match highlighting
- **Line numbers** toggle
- **Word wrap** toggle
- **File stats** — lines, chars, size, encoding, type
- **Copy to clipboard**
- **Custom SOFTCURSE UI** — cyberpunk retro-futuristic design
- **Frameless window** with custom titlebar
- **Multiple encoding support** — UTF-8, Latin-1, CP1252
- **CLI support** — `SoftcurseFileReader.exe myfile.py`
- **File association** on install (optional)
- **50 MB file size protection**

---

## Supported File Formats (selected)

| Category | Extensions |
|---|---|
| Plain Text | .txt .text .asc .log .nfo |
| Markdown / Docs | .md .markdown .rst .adoc .tex |
| Web | .html .htm .css .scss .xml |
| Data | .json .yaml .yml .csv .tsv .sql |
| Config | .ini .cfg .conf .toml .env |
| Python | .py .pyw .pyx |
| JavaScript / TS | .js .ts .jsx .tsx .mjs |
| Java / JVM | .java .kt .scala .groovy |
| C family | .c .cpp .h .hpp .cs |
| Systems | .go .rs .zig .nim |
| Scripting | .rb .php .lua .pl .r |
| Shell | .sh .bat .ps1 .fish .zsh |
| + 80 more | ... |

---

*— SOFTCURSE/SYS · FILE READER v1.0.0 · BUILD THE FUTURE OR GET PROCESSED BY IT —*
