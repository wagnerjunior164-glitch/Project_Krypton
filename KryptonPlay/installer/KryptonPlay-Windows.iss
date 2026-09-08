#define AppName "KryptonPlay"
#define AppVersion GetEnv("KRYPTONPLAY_VERSION")
#if AppVersion == ""
  #define AppVersion "0.1.0"
#endif
#define AppPublisher "ProjectKrypton"
#define AppExeName "KryptonPlay.exe"
#define UpdaterExeName "KryptonPlay-Updater.exe"

[Setup]
AppId={{8D4A7B7D-4A7D-4F5C-AF8A-4B5A6A7D9C10}
AppName={#AppName}
AppVersion={#AppVersion}
AppVerName={#AppName} {#AppVersion}
AppPublisher={#AppPublisher}
DefaultDirName={autopf}\KryptonPlay
DefaultGroupName=KryptonPlay
OutputDir=installer-output
OutputBaseFilename=KryptonPlay-Windows-Setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
CloseApplications=yes
CloseApplicationsFilter=KryptonPlay.exe
RestartApplications=yes
UninstallDisplayIcon={app}\{#AppExeName}
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Files]
Source: "..\dist\KryptonPlay.exe"; DestDir: "{app}"; Flags: ignoreversion restartreplace
Source: "..\dist\KryptonPlay-Updater.exe"; DestDir: "{app}"; Flags: ignoreversion restartreplace

[Dirs]
Name: "{app}\data"

[Icons]
Name: "{group}\KryptonPlay"; Filename: "{app}\{#AppExeName}"
Name: "{autodesktop}\KryptonPlay"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na área de trabalho"; GroupDescription: "Atalhos:"

[Run]
Filename: "{app}\{#AppExeName}"; Description: "Iniciar KryptonPlay"; Flags: nowait postinstall skipifsilent runascurrentuser

[UninstallRun]
Filename: "{sys}\taskkill.exe"; Parameters: "/IM KryptonPlay.exe /T /F"; Flags: runhidden waituntilterminated
