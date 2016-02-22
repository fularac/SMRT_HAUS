Dim WinScriptHost
Set WinScriptHost = CreateObject("WScript.Shell")
WinScriptHost.Run Chr(34) & "C:\Users\Chris\Desktop\fun\PC-MediaCenter\Listen.bat" & Chr(34), 0
Set WinScriptHost = Nothing