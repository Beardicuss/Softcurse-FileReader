"""
SOFTCURSE FILE READER — v1.0.0
Universal Text File Viewer — Python + pywebview
"""

import os
import sys
import json
import threading
import webview

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

def get_file_ext(path):
    name = os.path.basename(path)
    if '.' in name:
        return name.rsplit('.', 1)[-1].lower()
    return name.lower()


def read_text_file(path):
    """Try reading a file with multiple encodings."""
    encodings = ['utf-8', 'utf-8-sig', 'cp437', 'utf-16', 'latin-1', 'cp1252', 'ascii']
    for enc in encodings:
        try:
            with open(path, 'r', encoding=enc, errors='replace') as f:
                return f.read(), enc
        except Exception:
            continue
    return None, None


def build_file_data(path):
    """Build a dict with file info for the frontend."""
    name = os.path.basename(path)
    ext = get_file_ext(path)
    size = os.path.getsize(path)

    if size > MAX_FILE_SIZE:
        return {
            'name': name, 'path': path, 'ext': ext,
            'content': f'[FILE TOO LARGE — {size // 1048576} MB — Max 50 MB]\n\nUse an external tool to view large files.',
        }

    content, enc = read_text_file(path)
    if content is None:
        return {
            'name': name, 'path': path, 'ext': ext,
            'content': '[BINARY FILE — Cannot display as text]',
        }
    return {'name': name, 'path': path, 'ext': ext, 'content': content}


class SoftcurseAPI:
    """Python API exposed to JavaScript via pywebview."""

    def __init__(self, window_ref):
        self._window = window_ref

    def open_file_dialog(self):
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
        return results[:50]  # limit to 50 files per folder

    def minimize(self):
        self._window.minimize()

    def maximize(self):
        self._window.toggle_fullscreen()

    def close_window(self):
        self._window.destroy()


def get_html_path():
    """Find the UI HTML file whether running frozen or from source."""
    if getattr(sys, 'frozen', False):
        # Running as exe
        base = sys._MEIPASS
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, 'ui.html')


def load_cli_files(window, paths):
    """Load files passed as command-line arguments after the window is ready."""
    import time
    time.sleep(1.2)  # wait for JS to be ready
    for p in paths:
        if os.path.isfile(p):
            fd = build_file_data(p)
            js = f"window.openExternalFile({json.dumps(fd)})"
            window.evaluate_js(js)


def main():
    html_path = get_html_path()
    
    # Create the window first so we can bind the API
    window = webview.create_window(
        title='SOFTCURSE FILE READER v1.0',
        url=f'file:///{html_path}' if sys.platform == 'win32' else html_path,
        width=1280,
        height=800,
        min_size=(800, 560),
        background_color='#020202',
        frameless=True,       # We use custom titlebar
    )

    api = SoftcurseAPI(window)
    window.expose(api.open_file_dialog)
    window.expose(api.open_folder_dialog)
    window.expose(api.minimize)
    window.expose(api.maximize)
    window.expose(api.close_window)

    # Load CLI files after startup
    cli_files = [p for p in sys.argv[1:] if os.path.isfile(p)]
    if cli_files:
        t = threading.Thread(target=load_cli_files, args=(window, cli_files), daemon=True)
        t.start()

    webview.start(debug=False)


if __name__ == '__main__':
    main()
