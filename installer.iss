; SOFTCURSE FILE READER — Inno Setup Installer Script
; Compile with Inno Setup 6+: iscc installer.iss
; Produces: SoftcurseFileReader_Setup_v1.0.0.exe

#define AppName       "SOFTCURSE File Reader"
#define AppVersion    "1.0.0"
#define AppPublisher  "SOFTCURSE/SYS"
#define AppExeName    "SoftcurseFileReader.exe"
#define AppURL        "https://github.com/softcurse"
#define BuildDir      "dist\SoftcurseFileReader"

[Setup]
AppId={{8F3A2C1D-4B7E-4F92-B0A8-3D6C9E2F1A50}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL={#AppURL}
AppSupportURL={#AppURL}
AppUpdatesURL={#AppURL}
DefaultDirName={autopf}\SoftcurseFileReader
DefaultGroupName={#AppName}
AllowNoIcons=yes
LicenseFile=LICENSE
OutputDir=installer_output
OutputBaseFilename=SoftcurseFileReader_Setup_v{#AppVersion}
SetupIconFile=src\assets\file_reader.ico
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
UninstallDisplayIcon={app}\{#AppExeName}
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"
Name: "fileassoc";   Description: "Associate common text file extensions"; GroupDescription: "File Associations"

[Files]
Source: "{#BuildDir}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}"
Name: "{group}\Uninstall {#AppName}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon

[Registry]
; File associations (common text formats)
Tasks: fileassoc; Root: HKCU; Subkey: "Software\Classes\.txt\OpenWithProgids"; ValueType: string; ValueName: "SoftcurseFileReader.txt"; ValueData: ""
Tasks: fileassoc; Root: HKCU; Subkey: "Software\Classes\.md\OpenWithProgids";  ValueType: string; ValueName: "SoftcurseFileReader.md";  ValueData: ""
Tasks: fileassoc; Root: HKCU; Subkey: "Software\Classes\.py\OpenWithProgids";  ValueType: string; ValueName: "SoftcurseFileReader.py";  ValueData: ""
Tasks: fileassoc; Root: HKCU; Subkey: "Software\Classes\.js\OpenWithProgids";  ValueType: string; ValueName: "SoftcurseFileReader.js";  ValueData: ""
Tasks: fileassoc; Root: HKCU; Subkey: "Software\Classes\.json\OpenWithProgids"; ValueType: string; ValueName: "SoftcurseFileReader.json"; ValueData: ""
Tasks: fileassoc; Root: HKCU; Subkey: "Software\Classes\.yaml\OpenWithProgids"; ValueType: string; ValueName: "SoftcurseFileReader.yaml"; ValueData: ""
Tasks: fileassoc; Root: HKCU; Subkey: "Software\Classes\.yml\OpenWithProgids";  ValueType: string; ValueName: "SoftcurseFileReader.yml";  ValueData: ""
Tasks: fileassoc; Root: HKCU; Subkey: "Software\Classes\.log\OpenWithProgids";  ValueType: string; ValueName: "SoftcurseFileReader.log";  ValueData: ""
Tasks: fileassoc; Root: HKCU; Subkey: "Software\Classes\.csv\OpenWithProgids";  ValueType: string; ValueName: "SoftcurseFileReader.csv";  ValueData: ""
Tasks: fileassoc; Root: HKCU; Subkey: "Software\Classes\.xml\OpenWithProgids";  ValueType: string; ValueName: "SoftcurseFileReader.xml";  ValueData: ""
Tasks: fileassoc; Root: HKCU; Subkey: "Software\Classes\.html\OpenWithProgids"; ValueType: string; ValueName: "SoftcurseFileReader.html"; ValueData: ""
Tasks: fileassoc; Root: HKCU; Subkey: "Software\Classes\.css\OpenWithProgids";  ValueType: string; ValueName: "SoftcurseFileReader.css";  ValueData: ""
Tasks: fileassoc; Root: HKCU; Subkey: "Software\Classes\.ini\OpenWithProgids";  ValueType: string; ValueName: "SoftcurseFileReader.ini";  ValueData: ""
Tasks: fileassoc; Root: HKCU; Subkey: "Software\Classes\.conf\OpenWithProgids"; ValueType: string; ValueName: "SoftcurseFileReader.conf"; ValueData: ""
Tasks: fileassoc; Root: HKCU; Subkey: "Software\Classes\.sh\OpenWithProgids";   ValueType: string; ValueName: "SoftcurseFileReader.sh";   ValueData: ""
Tasks: fileassoc; Root: HKCU; Subkey: "Software\Classes\.bat\OpenWithProgids";  ValueType: string; ValueName: "SoftcurseFileReader.bat";  ValueData: ""
Tasks: fileassoc; Root: HKCU; Subkey: "Software\Classes\.sql\OpenWithProgids";  ValueType: string; ValueName: "SoftcurseFileReader.sql";  ValueData: ""
Tasks: fileassoc; Root: HKCU; Subkey: "Software\Classes\.ts\OpenWithProgids";   ValueType: string; ValueName: "SoftcurseFileReader.ts";   ValueData: ""

; ProgID
Tasks: fileassoc; Root: HKCU; Subkey: "Software\Classes\SoftcurseFileReader"; ValueType: string; ValueData: "Text File"
Tasks: fileassoc; Root: HKCU; Subkey: "Software\Classes\SoftcurseFileReader\shell\open\command"; ValueType: string; ValueData: """{app}\{#AppExeName}"" ""%1"""

[Run]
Filename: "{app}\{#AppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(AppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"
