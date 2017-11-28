; example2.nsi
;
; This script is based on example1.nsi, but it remember the directory, 
; has uninstall support and (optionally) installs start menu shortcuts.
;
; It will install example2.nsi into a directory that the user selects,

;--------------------------------

; The name of the installer
Name "VtiDiscountKeeper"

; The file to write
OutFile "vdk_service_install.exe"

; The default installation directory
InstallDir $PROGRAMFILES\VtiDiscountKeeper
; Registry key to check for directory (so if you install again, it will 
; overwrite the old one automatically)
InstallDirRegKey HKLM "Software\VtiDiscountKeeper" "Install_Dir"

; Request application privileges for Windows Vista
RequestExecutionLevel admin

;--------------------------------

; Pages

Page components
Page directory
Page instfiles

UninstPage uninstConfirm
UninstPage instfiles

;--------------------------------

; The stuff to install
Section "VtiDiscountKeeper (required)"

  SectionIn RO
  
  ; Set output path to the installation directory.
  SetOutPath $INSTDIR

   SimpleSC::StopService "VtiDiscountKeeper" 1 30
  Pop $0 
  SimpleSC::RemoveService "VtiDiscountKeeper"
  Pop $0 
  
  ; Put file there
  File /r "D:\projects\VtiDiscountKeeper Installer\Release\*"
  
  ; Write the installation path into the registry
  WriteRegStr HKLM SOFTWARE\VtiDiscountKeeper "Install_Dir" "$INSTDIR"
  


 
  SimpleSC::InstallService "VtiDiscountKeeper" "VtiDiscountKeeper" "16" "2" "$INSTDIR\VtiDiscountKeeper.exe" "" "" ""
  Pop $0 
  
  SimpleSC::StartService "VtiDiscountKeeper" "" 30
  Pop $0 

SectionEnd



;--------------------------------

