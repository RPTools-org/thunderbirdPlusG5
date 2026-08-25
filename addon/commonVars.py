# commonVars.py is a part of Thunderbird+G5 addon
# This module is common to the appModules, globalPlugin and shutils folders
import speech


class CommonVars:
	def __init__(self):
		# public attributes instead of @property 
		self.logging = False
		# Initial state setup
		self.defaultSpeechMode = speech.getState().speechMode
		self.logger = None
		self.reset()

	def reset(self) -> None:
		"""Resets all internal variables to their default values."""
		self.grouping = None
		self.propertyPage = None
		self.folderTree = None
		self.threadTree = None
		self.threadPane = None
	
	# the getters and setters below are disabled for performance reasons.
	# --- DefaultSpeechMode ---
	# @property
	# def defaultSpeechMode(self):
		# """Getter for the default speech mode."""
		# return self.defaultSpeechMode

	# @defaultSpeechMode.setter
	# def defaultSpeechMode(self, mode) -> None:
		# """Setter for the default speech mode."""
		# self.defaultSpeechMode = mode

	# # --- Logger ---
	# @property
	# def logger(self):
		# """Getter for the  logger."""
		# return self.logger

	# @logger.setter
	# def logger(self, logger) -> None:
		# """Setter for the  logger."""
		# self.logger = logger

	# # --- Grouping ---
	# @property
	# def grouping(self):
		# """Getter for Grouping."""
		# return self.grouping

	# @grouping.setter
	# def grouping(self, value) -> None:
		# """Setter for Grouping."""
		# self.grouping = value

	# # --- PropertyPage ---
	# @property
	# def propertyPage(self):
		# """Getter for PropertyPage."""
		# return self.propertyPage

	# @propertyPage.setter
	# def propertyPage(self, value) -> None:
		# """Setter for PropertyPage."""
		# self.propertyPage = value

	# # --- FolderTree ---
	# @property
	# def folderTree(self):
		# """Getter for FolderTree."""
		# return self.folderTree

	# @folderTree.setter
	# def folderTree(self, value) -> None:
		# """Setter for FolderTree."""
		# self.folderTree = value

	# # --- ThreadTree ---
	# @property
	# def threadTree(self):
		# """Getter for ThreadTree."""
		# return self.threadTree

	# @threadTree.setter
	# def threadTree(self, value) -> None:
		# """Setter for ThreadTree."""
		# self.threadTree = value

	# # --- ThreadPane ---
	# @property
	# def threadPane(self):
		# """Getter for ThreadPane."""
		# return self.threadPane

	# @threadPane.setter
	# def threadPane(self, value) -> None:
		# """Setter for ThreadPane."""
		# self.threadPane = value


# Shared instance to be imported across modules
cv = CommonVars()