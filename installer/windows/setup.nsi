; installer/setup.nsi
Name "irshelper"
OutFile "irshelper-setup.exe"
InstallDir "$PROGRAMFILES\irshelper"
SetOutPath $INSTDIR

Section "Install"
    File "dist\irshelper.exe"
    CreateShortCut "$DESKTOP\irshelper.lnk" "$INSTDIR\irshelper.exe"
SectionEnd

Section "Uninstall"
    Delete "$INSTDIR\irshelper.exe"
    Delete "$DESKTOP\irshelper.lnk"
    RMDir $INSTDIR
SectionEnd