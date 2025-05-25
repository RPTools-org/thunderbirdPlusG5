import ctypes
from ctypes import wintypes

# Define the Windows API functions prototypes
user32 = ctypes.WinDLL('user32', use_last_error=True)

# Functions to list and get the text text
EnumWindows = user32.EnumWindows
EnumWindows.argtypes = [
	ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM),
	wintypes.LPARAM
]
EnumWindows.restype = wintypes.BOOL

IsWindowVisible = user32.IsWindowVisible
IsWindowVisible.argtypes = [wintypes.HWND]
IsWindowVisible.restype = wintypes.BOOL

GetWindowTextLengthW = user32.GetWindowTextLengthW
GetWindowTextLengthW.argtypes = [wintypes.HWND]
GetWindowTextLengthW.restype = wintypes.INT

GetWindowTextW = user32.GetWindowTextW
GetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPWSTR, wintypes.INT]
GetWindowTextW.restype = wintypes.INT

def findWindowByPartialTitle(partial_title):
	"""
	Search windows whose title contains the specified word or sentence
	Args:
		partial_title (str): The word or sentence to look for in the title of the window.

	Returns:
		list: A list of handles (hwnd) of the visible windows found.
	"""
	found_windows = []

	@ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
	def enum_windows_callback(hwnd, lParam):
		if IsWindowVisible(hwnd):
			length = GetWindowTextLengthW(hwnd)
			if length > 0: # S'il y a un titre
				buffer = ctypes.create_unicode_buffer(length + 1)
				GetWindowTextW(hwnd, buffer, length + 1)
				title = buffer.value
				if partial_title.lower() in title.lower():
					found_windows.append(hwnd)
		return True # Continuer l'énumération

	EnumWindows(enum_windows_callback, 0)
	return found_windows

