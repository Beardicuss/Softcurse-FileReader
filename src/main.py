"""
SOFTCURSE FILE READER — v1.0.0
Universal Text File Viewer & Editor — Python + pywebview
"""

import os
import sys
import json
import threading

try:
    import webview
except ImportError:
    webview = None

# ── SUPPORTED EXTENSIONS ──
TEXT_EXTENSIONS = {
    # Plain text
    'txt', 'text', 'asc', 'ans', '1st', 'bbs', 'nfo', 'diz',
    # Markup / Web
    'html', 'htm', 'xhtml', 'xml', 'xsd', 'xsl', 'xslt',
    'md', 'markdown', 'rst', 'adoc', 'asciidoc',
    'json', 'jsonc', 'json5', 'rss', 'atom',
    # Data
    'csv', 'tsv', 'dif', 'tab',
    # Word processing / docs
    'rtf', 'wpd', 'pages',
    # Scientific
    'tex', 'ltx', 'bib', 'bibtex',
    # Config
    'ini', 'cfg', 'conf', 'config', 'properties',
    'yaml', 'yml', 'toml', 'env', 'envrc',
    'log', 'logs',
    # Ebook
    'epub', 'fb2',
    # Source — Python
    'py', 'pyw', 'pyx', 'pxd', 'pxi',
    # Source — JavaScript / TypeScript
    'js', 'mjs', 'cjs', 'ts', 'tsx', 'jsx',
    # Source — Web
    'css', 'scss', 'sass', 'less', 'styl',
    'asp', 'aspx', 'jsp', 'jspx', 'php', 'php3', 'php4', 'php5', 'phtml',
    # Source — Java/JVM
    'java', 'class', 'kt', 'kts', 'scala', 'groovy', 'clj', 'cljs',
    # Source — C family
    'c', 'cc', 'cpp', 'cxx', 'h', 'hh', 'hpp', 'hxx',
    'cs', 'm', 'mm',
    # Source — Systems
    'go', 'rs', 'zig', 'nim', 'odin',
    # Source — Scripting
    'rb', 'rake', 'gemspec',
    'lua', 'pl', 'pm', 'pod',
    'r', 'rmd',
    'jl', 'mat', 'sql',
    # Source — Shell
    'sh', 'bash', 'zsh', 'fish', 'csh', 'tcsh', 'ksh',
    'bat', 'cmd', 'ps1', 'psm1', 'psd1',
    'vbs', 'vba', 'ahk',
    # Source — Functional / Other
    'hs', 'lhs', 'ml', 'mli', 'elm', 'ex', 'exs', 'erl', 'hrl',
    'dart', 'swift', 'coffee', 'ls',
    # Data science / ML
    'ipynb',
    # Makefile / build
    'makefile', 'mk', 'cmake', 'gradle', 'sbt', 'bazel', 'BUILD',
    # Docker / infra
    'dockerfile', 'tf', 'tfvars', 'hcl',
    # Git
    'gitignore', 'gitconfig', 'gitattributes',
    # Misc
    'svg', 'graphql', 'gql', 'proto', 'thrift', 'avsc', 'avdl',
    'patch', 'diff', 'license', 'readme', 'changelog', 'authors',
    '602', 'bean', 'bna', 'abw', 'awp', 'awt', 'aww', 'zabw',
}

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB
MAX_HEX_BYTES = 256 * 1024        # 256 KB limit for hex view generation


def get_file_ext(path):
    name = os.path.basename(path)
    if '.' in name:
        return name.rsplit('.', 1)[-1].lower()
    return name.lower()


def is_binary_data(sample_bytes):
    """Check if byte sample appears to be binary data."""
    if not sample_bytes:
        return False
    if b'\x00' in sample_bytes:
        return True
    text_chars = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})
    non_text = sum(1 for b in sample_bytes if b not in text_chars)
    return (non_text / len(sample_bytes)) > 0.30


HEX_LOOKUP = [f'{b:02X}' for b in range(256)]
ASCII_LOOKUP = [chr(b) if 32 <= b <= 126 else '.' for b in range(256)]

def generate_hex_dump(data_bytes):
    """Format raw bytes into a canonical hex dump string (optimized with lookups)."""
    lines = []
    length = len(data_bytes)
    for i in range(0, length, 16):
        chunk = data_bytes[i:i + 16]
        left = ' '.join(HEX_LOOKUP[b] for b in chunk[:8])
        right = ' '.join(HEX_LOOKUP[b] for b in chunk[8:])
        hex_part = f'{left:<23}  {right:<23}'
        ascii_part = ''.join(ASCII_LOOKUP[b] for b in chunk)
        lines.append(f'{i:08X}  {hex_part:<48}  |{ascii_part}|')
    return '\n'.join(lines)


def read_text_file(path):
    """Try reading a file with multiple encodings starting with UTF-8 fast-path."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read(), 'utf-8'
    except UnicodeDecodeError:
        pass
    except Exception:
        return None, None

    encodings = ['utf-8-sig', 'cp437', 'utf-16', 'latin-1', 'cp1252', 'ascii']
    for enc in encodings:
        try:
            with open(path, 'r', encoding=enc, errors='replace') as f:
                return f.read(), enc
        except Exception:
            continue
    return None, None


def write_file_content(path, content, encoding='utf-8'):
    """Save text content to file at specified path."""
    try:
        with open(path, 'w', encoding=encoding, errors='replace') as f:
            f.write(content)
        return True, "File saved successfully."
    except Exception as e:
        return False, str(e)


def create_new_file_data(filename='Untitled.txt'):
    """Generate default file data dictionary for new blank documents."""
    return {
        'name': filename,
        'path': filename,
        'ext': get_file_ext(filename),
        'size': 0,
        'encoding': 'UTF-8',
        'is_binary': False,
        'content': '',
        'hex_dump': '',
    }


def build_file_data(path):
    """Build a dict with file info for the frontend."""
    name = os.path.basename(path)
    ext = get_file_ext(path)
    size = os.path.getsize(path)

    if size > MAX_FILE_SIZE:
        return {
            'name': name,
            'path': path,
            'ext': ext,
            'size': size,
            'encoding': 'N/A',
            'is_binary': False,
            'content': f'[FILE TOO LARGE — {size // 1048576} MB — Max limit 50 MB]\n\nUse an external tool to view large files.',
            'hex_dump': '',
        }

    try:
        with open(path, 'rb') as f:
            raw_sample = f.read(8192)
            f.seek(0)
            full_raw = f.read(MAX_HEX_BYTES)
    except Exception as e:
        return {
            'name': name,
            'path': path,
            'ext': ext,
            'size': size,
            'encoding': 'N/A',
            'is_binary': False,
            'content': f'[ERROR READING FILE: {e}]',
            'hex_dump': '',
        }

    is_bin = is_binary_data(raw_sample)
    hex_dump = generate_hex_dump(full_raw)
    if len(full_raw) < size:
        hex_dump += f'\n\n[HEX VIEW TRUNCATED AT {MAX_HEX_BYTES // 1024} KB — FILE SIZE: {size} BYTES]'

    if is_bin:
        return {
            'name': name,
            'path': path,
            'ext': ext,
            'size': size,
            'encoding': 'BINARY',
            'is_binary': True,
            'content': f'[BINARY FILE — Displaying Hex View]\n\n{hex_dump}',
            'hex_dump': hex_dump,
        }

    content, enc = read_text_file(path)
    if content is None:
        return {
            'name': name,
            'path': path,
            'ext': ext,
            'size': size,
            'encoding': 'BINARY',
            'is_binary': True,
            'content': f'[BINARY FILE — Cannot display as text]\n\n{hex_dump}',
            'hex_dump': hex_dump,
        }

    return {
        'name': name,
        'path': path,
        'ext': ext,
        'size': size,
        'encoding': enc.upper() if enc else 'UTF-8',
        'is_binary': False,
        'content': content,
        'hex_dump': hex_dump,
    }


class SoftcurseAPI:
    """Python API exposed to JavaScript via pywebview."""

    def __init__(self, window_ref):
        self._window = window_ref

    def create_new_file(self, filename='Untitled.txt'):
        return create_new_file_data(filename)

    def reload_file(self, path):
        if path and os.path.exists(path):
            return build_file_data(path)
        return None

    def open_file_dialog(self):
        if not webview or not self._window:
            return []
        file_types = (
            'Text Files (*.txt;*.md;*.py;*.js;*.ts;*.html;*.css;*.json;*.xml;*.yaml;*.yml;*.csv;*.tsv;*.sql;*.sh;*.bat;*.java;*.c;*.cpp;*.h;*.rs;*.go;*.rb;*.php;*.lua;*.r;*.ini;*.cfg;*.conf;*.log;*.tex;*.rst;*.adoc;*.env;*.toml;*.graphql;*.proto;*.diff;*.patch)',
            'All Files (*.*)',
        )
        paths = self._window.create_file_dialog(
            webview.OPEN_DIALOG,
            allow_multiple=True,
            file_types=file_types,
        )
        if not paths:
            return []
        results = []
        for p in paths:
            fd = build_file_data(p)
            results.append(fd)
        return results

    def open_folder_dialog(self):
        if not webview or not self._window:
            return []
        paths = self._window.create_file_dialog(webview.FOLDER_DIALOG)
        if not paths:
            return []
        folder = paths[0]
        results = []
        try:
            entries = sorted(os.listdir(folder))
            for entry in entries:
                full = os.path.join(folder, entry)
                if os.path.isfile(full):
                    ext = get_file_ext(full)
                    if ext in TEXT_EXTENSIONS or not os.path.splitext(entry)[1]:
                        fd = build_file_data(full)
                        results.append(fd)
        except Exception as e:
            print(f'Folder read error: {e}')
        return results[:50]

    def save_file(self, path, content):
        """Save content back to existing file path."""
        if not path or not os.path.exists(path):
            return self.save_file_as_dialog(content, os.path.basename(path or 'untitled.txt'))
        success, msg = write_file_content(path, content)
        if success:
            return build_file_data(path)
        return {'error': msg}

    def save_file_as_dialog(self, content, default_name='untitled.txt'):
        """Open Save As dialog and save file."""
        if not webview or not self._window:
            return {'error': 'Window not available'}
        save_path = self._window.create_file_dialog(
            webview.SAVE_DIALOG,
            save_filename=default_name,
        )
        if not save_path:
            return {'cancelled': True}
        path = save_path[0] if isinstance(save_path, (list, tuple)) else save_path
        success, msg = write_file_content(path, content)
        if success:
            return build_file_data(path)
        return {'error': msg}

    def minimize(self):
        if self._window:
            self._window.minimize()

    def maximize(self):
        if self._window:
            self._window.toggle_fullscreen()

    def close_window(self):
        if self._window:
            self._window.destroy()


def get_html_path():
    if getattr(sys, 'frozen', False):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, 'ui.html')


def load_cli_files(window, paths):
    import time
    time.sleep(1.2)
    for p in paths:
        if os.path.isfile(p):
            fd = build_file_data(p)
            js = f"window.openExternalFile({json.dumps(fd)})"
            window.evaluate_js(js)


def main():
    if not webview:
        print("Error: pywebview is not installed.")
        sys.exit(1)

    html_path = get_html_path()
    
    window = webview.create_window(
        title='SOFTCURSE FILE READER & EDITOR v1.0',
        url=f'file:///{html_path}' if sys.platform == 'win32' else html_path,
        width=1280,
        height=800,
        min_size=(800, 560),
        background_color='#020202',
        frameless=True,
    )

    api = SoftcurseAPI(window)
    window.expose(api.create_new_file)
    window.expose(api.reload_file)
    window.expose(api.open_file_dialog)
    window.expose(api.open_folder_dialog)
    window.expose(api.save_file)
    window.expose(api.save_file_as_dialog)
    window.expose(api.minimize)
    window.expose(api.maximize)
    window.expose(api.close_window)

    cli_files = [p for p in sys.argv[1:] if os.path.isfile(p)]
    if cli_files:
        t = threading.Thread(target=load_cli_files, args=(window, cli_files), daemon=True)
        t.start()

    webview.start(debug=False)


if __name__ == '__main__':
    main()
