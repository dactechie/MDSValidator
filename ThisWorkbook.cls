VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "ThisWorkbook"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = True
Option Explicit

Sub Call_Python_Function()
Attribute Call_Python_Function.VB_ProcData.VB_Invoke_Func = "e\n14"
   
   Dim source_file As String
   'do_pre_cleanup
   
   source_file = Range("source_file").Value
   
   Application.ScreenUpdating = False
   
   RunPython ("import xwin; xwin.fetch_validation_results('" + source_file + "')")
   
   Application.ScreenUpdating = True
   
End Sub


Sub do_pre_cleanup()
    ' if loaded sheet exists, delete/rename it.
End Sub
