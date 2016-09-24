Set ws = CreateObject("Wscript.Shell")
path = createobject("Scripting.FileSystemObject").GetFile(Wscript.ScriptFullName).ParentFolder.Path
ws.run "daemon.cmd " & chr(34) & path & chr(34),vbhide