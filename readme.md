# Thunderbird+G5 for Thunderbird >= 115

* Authors: Pierre-Louis Renaud (From Thunderbird 78 to 115) & Cyrille Bougot (TB 102), Daniel Poiraud (From TB 78 to 91), Yannick (TB 45 to 60);
* URL: [thunderbirdPlus add-ons home][4] ;
  [History of changes at RPTools.org][5] ;
  [Contact in French or English][6] ;
* Download [stable version][1]
* Download [Latest version from RPTools.org][3] ;
* NVDA compatibility: 2021.1 and later;
* [Source code on gitHub][2]

## Introduction
Thunderbird+G5 is an add-on for NVDA that significantly increases the efficiency and comfort of using the Thunderbird 115 email client.

It improves your productivity by providing commands that don't exist natively in Thunderbird:

* keyboard shortcuts for direct access to the folder tree, message list and preview pane.
* Seamless navigation between the main window panes using the Tab and escape keys.
* Shortcuts for viewing and copying message list fields and message headers without changing focus.
* Direct access to attachments.
* Shortcuts for consultation and direct access to the addressing fields of the Write window.
* Significantly improved the use of the spell check dialog.
* And many more...

This page documents the keyboard shortcuts offered by Thunderbird+G5.

Most of these keyboard shortcuts are configurable via the NVDA Menu / Preferences / Input Gestures / thunderbirdPlusG5 category for Thunderbird 115

## Main window navigation

Note: The named key (key above Tab) in the remainder of this page designates the key located below Escape, above Tab and to the left of the number 1. Its wording varies depending on the language of the keyboard.

### General shortcuts

* (key above Tab): displays the menu of various add-on commands.
* Shift+(key above Tab): Displays the add-on options menu.
* Control+F1: displays the current page. For some clarification you can [visit version4 documentation][7]
* F8 to show or hide the preview pane: this command is voiced by the add-on.

### Navigating between main window panes
These shortcuts are for the folder tree, message list, and message preview pane.

* control+(key above Tab): One press places the focus in the message list, two presses places the focus in the message list then selects the last message.
* alt+Start: one press selects the current folder in the folder tree, two presses displays a menu allowing you to choose the email account to reach in the tree
* Tab: goes to the next pane, straight away.
* Escape: returns to the previous section, without detour.<br>
Escape also allows you to alternate between the folder tree and the message list.
* Shift+Tab: its native behavior has been preserved in this version.

### Navigating through main window tabs

* Control+Tab with or without the shift key and control+1 to 9: The add-on intercepts tab changes in order to announce their order number and the total number of tabs.
* Control+the first key located to the left of backspace: displays a menu with the list of existing tabs. Press Enter on a menu item to activate the corresponding tab.
* Alt+the first key to the left of backspace: displays the tab context menu. This menu is native to Thunderbird.

Note: The label of the first key to the left of backspace varies depending on the keyboard language.

## Message list
Before announcing a line from the message list, the add-on cleans it up to make it more pleasant to listen to or read. Explore the Shift+(key above Tab) / Options menu options for the main window to adjust them.

If this cleaning slows down navigation in the list too much on your PC, press Shift+(key above Tab) / Deactivations. You can deactivate it there.

Note: The "Unread" and "Reading Status" columns can no longer be announced by ThunderbirdPlus. use the "Status" column instead. The "unread" status is announced and the "read" status is silenced. To delete and add columns, go to the message list then press Shift+Tab. Then use left and right arrow to find "Choose which columns to display".

* Escape in the message list: if a filter is active, it is deactivated and the message list remains selected. Otherwise, this shortcut gives focus to the folder tree.
* NVDA+up arrow in message list:<br>
One press: announces the current line of the message list. The NVDA+Tab shortcut produces the same result but without using this add-on.<br>
Two presses: displays the details of the line in a text window which allows analysis of the line using the keyboard.
* Spacebar, F4, or Alt+down arrow: Reads a clean version of the message from the preview pane, without leaving the message list.
* Alt+up arrow: places the message in the virtual quote browser;
* Windows+down or up arrows: reads the next or previous quote.

Note: This quote / citation browser can be used from the message list, message from the separate reading window, from the compose window and from the spell check dialog.

### Announcing, spelling and copying message list fields

Each row of the list is broken down into several fields corresponding to the columns. You can compare a field to a cell in an Excel spreadsheet.

The shortcuts below can be done without changing focus:

* number 1 to 9 of the row above the letters: with the number corresponding to the row of the column of the message list, the following actions are available:<br>
One press: announces the value of the field. For example, depending on the order of your columns, 1 announces the sender and 2 announces the subject.<br>
Two press : spells the value of the field.<br>
Three presses: copies the value of the field to the clipboard.

Tip: If you use several folders, apply the same column order to all of them, so that a number will always correspond to the same column.

### Announcing and copying headers from the preview pane or separate reading window

* Alt+1 to Alt+6 from the list and the separate reading window:<br>
One press : announces the value of the header,<br>
Two presses : opens an edit box containing the header value. By closing this dialog with Enter, this value is copied to the clipboard, which is very practical for retrieving the email address of a correspondent. <br>
Three presses : opens the context menu of the relevant header. This is a native Thunderbird menu.

### Attachments pane in main window and separate reading window
The following shortcuts allow you to announce attachments, open them, or save them.

* Alt+9 or Alt+page down:<br>
One press: announces the number of attachments and the wording of the button that can be activated to open them;<br>
Two presses: displays the menu of actions available if only one attachment or activates the "Save all" button if several attachments are present.

Remarks :

* the attachments pane of Thunderbird 115 is in regression compared to that of version 102. There is no longer a list of attachments and when there are several attachments, only a "Save all" button is posted.
* When an attachment-related button is selected, the Escape key simulates the Shift+f6 key to return to the previous pane.

### Tag management from the message list
The shortcuts below allow vocal management of tags without having to navigate through the Thunderbird context menu.

* Shift+1 to Shift+9: Adds or removes a tag, with vocalization.
* Shift+0: Removes all tags from the selected message.
* alt+0: Announces all tags in the message.

### Vocalization of shortcuts a, c, j and m of the message list
The announcements are different depending on whether a single or several messages are affected by one of these commands.

* a: archives the selected messages.
* c: marks selected messages as read by date.
* j and Shift+j: Marks selected messages as spam or acceptable.
* m: marks selected messages as read or unread.


### Alternative shortcut for the quick filter bar

* letter f : ergonomic alternative to Control+Shift+K to display or reach the quick filter bar. This shortcut is configurable in the input (or command) gestures dialog.

### Announcement of status bar and quick filter information

* Alt+end or Alt+(second key from left backspace):
From the message list or quick filter bar: announces the total or filtered number of messages, the number of selected messages if there is more than one and the filter expression if a filter has been defined. This information comes from the quick filter bar and no longer from the status bar.<br>
From another tab or window: announces the status bar.
* When the message list receives focus,A hissing sound is heard when fast filtering is active.

### SmartReply: reply to mailing lists with control+R
To respond to certain mailing lists, it is necessary to press Control+Shift+L. To avoid replying to the wrong recipient, press Control+R to reply to the list and Control+r twice to reply privately to the sender of the message.

Note: groups.io is not affected by this feature.

## folder tree

* NVDA+upArrow: announces the selected folder name. NVDA no longer does this on its own.
* Spacebar on unread folder: places focus on the first unread message in the message list.
* enter key or Alt+up arrow on a folder: Displays a menu allowing you to reach another folder at the same tree level. This allows you to use the first letter of folder names. ;
* control+enter or Alt+down arrow on a folder: Displays a menu allowing you to reach an unread folder at the same level.<br>
These menus also include an element allowing you to go back to the parent folder.

Remarks :

The new internal structure of the folder tree no longer allows NVDA add-ons to navigate completely through it at an acceptable speed. This is why these menus only load one level at a time.

In addition, the following 2 dialogs that existed in TBPlus 4 had to be deleted:

* Dialog of Filtered Lists of Accounts and Folders (F12)
* List of folders in the main tree, according to 4 types (F7, NVDA+F7 or Shift+F12)

## Closing windows and tabs

* The Escape key closes the separate message reading window and the composing window. See the relevant options.
* Control+Backspace: also used to close tabs and windows. When editing text, this shortcut deletes the previous word.

## Compose window
The shortcuts in this window concern the addressing fields and the attachments pane.

* Alt+1 to Alt+8:<br>
One press: announces the value of the addressing field or the attachments pane,<br>
Two presses : places the focus on the addressing field or the attachments pane.
* Alt+pageDown: Same as Alt+3 for the attachments pane.
* Notes:<br>
the announcement of the attachments pane with Alt+3 cites a numbered list of file names and their total size,<br>
When the focus is in the attachment list, the escape key returns to the message body.
* Alt+up arrow: places the message being written in the virtual quote / citation browser;
* Windows+vertical arrows: announces the next or previous line in the citation browser; This allows you to listen to the message you are replying to without changing windows.
* Windows+horizontal arrow: goes to the next or previous quote without changing windows.<br>

## Spell check dialog
At the opening of this dialogue,The add-on automatically announces words and their spelling. This can be disabled in the compose window options.

The following shortcuts are available from the replacement word editing area:

* Alt+up arrow: spells the misspelled word and the replacement suggestion.
* Alt+up arrow when double-pressed: announces the sentence in which the misspelled word is found, thanks to the virtual citation browser which automatically initializes in this context.
* Enter: press the "Replace" button, without leaving the editing area.
* Shift+enter: press the "Replace all" button.
* Control+Enter: Press the "Ignore" button.
* Shift+control+Enter: press the "Ignore all" button.
* Alt+Enter: adds the replacement word to the dictionary.


[1]: https://github.com/RPTools-org/thunderbirdPlusG5/releases/download/v2023.10.13/thunderbirdPlusG5-2023.10.13.nvda-addon

[2]: https://github.com/RPTools-org/thunderbirdPlusG5/

[3]: https://www.rptools.org/?p=9514

[4]: https://www.rptools.org/NVDA-Thunderbird/index.html

[5]: https://www.rptools.org/NVDA-Thunderbird/get.php?pg=changes&v=G5&lang=en

[6]: https://www.rptools.org/NVDA-Thunderbird/toContact.html

[7]: https://www.rptools.org/NVDA-Thunderbird/get.php?pg=manual&lang=en
