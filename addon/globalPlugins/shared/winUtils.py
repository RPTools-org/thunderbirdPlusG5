# winUtils :Windows additional functions from  ThunderbirdPlusG5 add-on
import winKernel
import ctypes
from tones import beep
from api import copyToClip
import winUser
from . import user32

class processEntry32W(ctypes.Structure):
	_fields_ = [
		("dwSize",ctypes.wintypes.DWORD),
		("cntUsage", ctypes.wintypes.DWORD),
		("th32ProcessID", ctypes.wintypes.DWORD),
		("th32DefaultHeapID", ctypes.wintypes.DWORD),
		("th32ModuleID",ctypes.wintypes.DWORD),
		("cntThreads",ctypes.wintypes.DWORD),
		("th32ParentProcessID",ctypes.wintypes.DWORD),
		("pcPriClassBase",ctypes.c_long),
		("dwFlags",ctypes.wintypes.DWORD),
		("szExeFile", ctypes.c_wchar * 260)
	]

def getProcessIDFromExe(exeName):
	FSnapshotHandle = winKernel.kernel32.CreateToolhelp32Snapshot (2,0)
	FProcessEntry32 = processEntry32W()
	FProcessEntry32.dwSize = ctypes.sizeof(processEntry32W)
	ContinueLoop = winKernel.kernel32.Process32FirstW(FSnapshotHandle, ctypes.byref(FProcessEntry32))
	pID = 0
	while ContinueLoop:
		if exeName == FProcessEntry32.szExeFile :
			pID = FProcessEntry32.th32ProcessID
			break
		ContinueLoop = winKernel.kernel32.Process32NextW(FSnapshotHandle, ctypes.byref(FProcessEntry32))
	winKernel.kernel32.CloseHandle(FSnapshotHandle)
	return pID

	
def findWindowFromExeName(processName) : # returns hWnd or 0
	processID = getProcessIDFromExe(processName)
	if processID == 0 : return 0
	hwndList = user32.enumWindows()
	dbg = "Window list\n"
	for hwnd in hwndList :
		# dbg += "hwnd {}, title : {}, PID {}".format(hwnd, winUser.getWindowText(hwnd), str(winUser.getWindowThreadProcessID(hwnd)))  + "\n"
		if winUser.getWindowThreadProcessID(hwnd)[0] == processID :
			return hwnd
	# copyToClip(dbg)
	return 0
