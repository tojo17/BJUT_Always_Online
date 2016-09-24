Set ws = CreateObject("Wscript.Shell")
path = createobject("Scripting.FileSystemObject").GetFile(Wscript.ScriptFullName).ParentFolder.Path
ws.CurrentDirectory = path
ws.run "cmd.exe /c python online.py >> log.txt", vbhide