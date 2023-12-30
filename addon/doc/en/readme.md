# Thunderbird+G5 for Thunderbird >= 115

* Authors: Pierre-Louis Renaud (From Thunderbird 78 to 115) & Cyrille Bougot (TB 102), Daniel Poiraud (From TB 78 to 91), Yannick (TB 45 to 60);
* URL: [thunderbird+ G5 and G4 add-ons home page][4] ;
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

Most of these keyboard shortcuts are configurable via the NVDA Menu / Preferences / Input Gestures / Thunderbird+G5 (TB >= 115) category. 

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
* Alt+c: displays the accounts menu then the folders menu of the chosen account. Since version 2312.14, supports the "unified folders" mode of the folder tree.
* Control+Alt+c: displays the accounts menu then the unread folders menu for the chosen account. (2023.11.15)<br>
Note: these last two shortcuts can be modified or swapped via the Input Gestures dialog.
* alt+Home : one press selects the current folder in the folder tree, two presses displays a menu allowing you to choose the email account to reach in the tree
* Control+Alt+Home : Same but for folders with unread messages. (2023.10.31)
* Tab: goes to the next pane, straight away.
* Escape: returns to the previous PANE, without detour.<br>
Escape also allows you to alternate between the folder tree and the message list.
* Shift+Tab: its native behavior has been preserved in this version.

### Navigating through main window tabs

* Control+Tab with or without the shift key and control+1 to 9: The add-on intercepts tab changes in order to announce their order number and the total number of tabs.
* Control+the first key located to the left of backspace: displays a menu with the list of existing tabs. Press Enter on a menu item to activate the corresponding tab.
* Alt+the first key to the left of backspace: displays the tab context menu. This menu is native to Thunderbird.

Note: The label of the first key to the left of backspace varies depending on the keyboard language.

## Message list

<!-- begin 2023.11.10 -->

### Custom vocalization of rows (2023.11.10)

This custom mode, disabled by default, allows more comfortable listening to lines in the message list.

However, it has some disadvantages:

* It is not compatible with the card view of the message list. To return to the table view, go to the message list, press Shift+Tab to the "Message list options" button, press Enter and in the context menu, check "Table view".
* On slower PCs, it may cause a noticeable slowdown in navigation with the arrows in the message list.
* If you press down arrow on the last line, it will not be announced.

You can activate this mode by pressing shift+ key above Tab and selecting the "Main window options" item in the menu then checking the "Message list: custom vocalization of rows" option.

This submenu also contains other customization options that only work if custom vocalization is enabled.
<br>
Remark :

Some users are experiencing a problem with blank lines in normal mode. If you are in this case, activate "Message list: force filling of rows if always blank" option.

But ideally, this problem should be solved by creating a new user profile in Thunderbird, which involves reconfiguring email accounts.

#### Tip for custom vocalization of rows

You can use the two columns "Reading Status" and "Status" together to combine their respective advantages:

* The "Reading Status" column announces "unread" when you press the letter m to reverse the reading status.
* The "Status" column announces the statuses "New", "Replied" and "Transferred".
* The add-on will ensure that "Unread" is only announced once and that "Read" is never announced.

<br>
also read the section [Choice and order of columns](#cols)

### Message list shortcuts

<!-- end 2023.10.31 -->

* Escape in the message list: if a filter is active, it is deactivated and the message list remains selected. Otherwise, this shortcut gives focus to the folder tree.
* NVDA+up arrow or NVDA+l (laptop) in message list:<br>
One press: announces the current line of the message list. The NVDA+Tab shortcut produces the same result but without using this add-on.<br>
Two presses: displays the details of the line in a text window which allows analysis of the line using the keyboard.
* Control+right arrow in messages grouped by conversation : selects the last message in the conversation. This is first expanded if it is collapsed. (2312.14.00)
* Control+left arrow in messages grouped by conversations : selects the first message in the conversation. This is first expanded if it is collapsed.<br>These last two shortcuts need the "Total" column to work.
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
The following shortcuts allow you to announce attachments or select one in the list.

* Alt+9 or Alt+Page Down :<br>
One press: announces the number of attachments and the names of all attachments.<br>If Thunderbird does not automatically display the attachments pane, the add-on will do so and Thunderbird will select the first attachment.<br>
Two presses :<br>
If there is only one attachment, move the focus to it then display its context menu. (2312.18.00)<br>
If multiple attachments, select the first attachment in the list. (2312.18.00)

### Tag management from the message list
The shortcuts below allow vocal management of tags without having to navigate through the Thunderbird context menu.

* Shift+1 to Shift+9: Adds or removes a tag, with vocalization.
* Shift+0: Removes all tags from the selected message.
* alt+0: Announces all tags in the message.

### Vocalization of shortcuts a, c, j and m of the message list
From version 2023.11.10, these marking shortcuts are no longer vocalized by the add-on. NVDA immediately announces the change in content of the line concerned.

### Quick message filtering (2023.11.10)

letter f: ergonomic alternative to Control+Shift+k to display or reach the quick filter bar. This shortcut is configurable in the command gestures dialog.
<br>Note: The focus must be in a non-empty message list. Press Escape to deactivate the active filter.

To directly access the filtering results from the keyword input  field, press down arrow.

When a filter is active, a sound resembling hissing is played each time the message list gains focus. This is especially useful when you switch windows or tabs and then return to the message list later.

If this sound bothers you, you have two options:

1. Open the Shift+(key above Tab) menu and in the Deactivations submenu, check the option:<br>
List messages: Don't play a sound when the list is filtered and gets focus.
2. Open the Shift+menu (key above Tab) then press Enter on the item: Open sounds folder.
<br>This folder will open in File Explorer,
<br>There you will find the filter.wav file.
<br> You can replace this file with another as long as your file has the same name: filter.wav.
<br>When done, restart NVDA.

<!-- end 2023.10.31 -->

### Announcement of status bar and quick filter information

* Alt+end or Alt+(second key from left backspace):
From the message list or quick filter bar: announces the total or filtered number of messages, the number of selected messages if there is more than one and the filter expression if a filter has been defined. This information comes from the quick filter bar and no longer from the status bar.<br>
From another tab or window: announces the status bar.
* When the message list receives focus,A hissing sound is heard when fast filtering is active.

### SmartReply: reply to mailing lists with control+R
To respond to certain mailing lists, it is necessary to press Control+Shift+L. To avoid replying to the wrong recipient, press Control+R to reply to the list and Control+r twice to reply privately to the sender of the message.

Note: groups.io is not affected by this feature.

<!-- Don't remove nor translate the following tag --><a name="cols">

<!-- begin 2023.10.31 -->

### Choice and order of columns (2023.10.31)

This procedure is native to Thunderbird 115 but it is explained here because it is poorly documented.

* Press Shift+tab from the message list to move to the list of column headers.
* Use the left and right arrows to select a column.
* When you reach the special column "Choose columns to display", press enter on it.
* In the menu, check or uncheck columns then press Escape to close this menu. As a reminder, it is recommended to uncheck the "Reading Status" column and check the "Status" column.
* Back in the list of column headers, press left arrow to a column to move.
* Then press Alt+left or right arrow to place it in the desired location. This will be correctly vocalized.
* Repeat these operations to move other columns.
* When column arranging is complete, press Tab to return to the message list.

<!-- begin 2023.10.31 -->

## folder tree: quick navigation (2023.10.31)

Some commands display a menu containing folders in the tree structure to allow navigation by initial letters. For performance reasons, the script does not display subfolders of collapsed branches.

Additionally, if the name of an account or folder ends with a hyphen, it will not be included in the unread folders menu.

It is therefore advisable to exclude accounts and folders by closing little-used branches or by renaming accounts to add a hyphen to the end of their name.

<br>
Since version 2312.14.00, "Unified Folders" mode is supported. In this mode, all account names must contain the @ character. To rename an account, select it in the tree, press the Applications key then press Settings in the context menu. Then tab to the "Account Name" field.

### Folder tree Shortcuts

* NVDA+up arrowor NVDA+l (laptop) : announces the name of the selected folder. NVDA no longer does this on its own.
* Space on unread folder:  sets  focus on the first unread message in the message list.
* Enter or Alt+up arrow: displays a menu of all folders in the account to which the selected folder belongs.
* Control+Enter or Alt+down arrow: displays a menu of unread folders for the account to which the selected folder belongs.
<br>In both cases, the last menu item displays the accounts menu. You can press the spacebar to choose an account from there.
* Shift+Enter: displays a menu containing all accounts and folders in the tree.
* Shift+Control+Enter: displays a menu containing all unread accounts and folders in the tree.

Remarks :

For these last two commands, some time will pass before the menu is displayed because the script must go through the entire tree to build the menu.

Instead, use one of these two little tips:

1. Press Alt+Home twice quickly to display the accounts menu,
<br>Choose an account then press Enter.<br>A new menu containing the folders for this account will open and you can use a letter to activate one.
2. Press Control+Alt+Home twice quickly to display the accounts menu with unread folders,
<br>Choose an account then press Enter.
<br>A new menu containing the unread folders of this account will open and you can use a letter to activate one.

<!-- end 2023.10.31 -->

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
* Alt+Enter: adds the word declared as misspelled to the dictionary.

## External complements

### Extension Start With inbox for Thunderbird 115 (2023.10.31)1

When Thunderbird starts, this extension automatically selects:

* the “Incoming Mail” folder of the account of your choice in the folder tree.
* The last message in the incoming mail folder of the chosen account.
* The first unread message in the incoming mail folder of the chosen account.

Facility :

* in Thunderbird, open the “Tools” menu then validate on: Add-ons and themes;
* On the Module Manager page, place yourself in the search box. In navigation mode, you can press the letter e to reach it quickly;
* write: Start with Inbox then press Enter;
* manually select the "Start with inbox :: Search :: Modules for Thunderbird" tab for example. then press the 3 key or quotation mark until you reach the level 3 title titled by the name of the module you searched for;
* With the down arrow, scroll down to the "Add to Thunderbird" link then press Enter on it;
* Follow the procedure then restart Thunderbird;
* If everything went well, Thunderbird will open on the main tab and give focus to the message list;


Set Start with Inbox options:

* Return to the "Add-ons Manager" tab;
* If necessary, leave the search field to place yourself in navigation mode;
* Press key 3 as many times as necessary to reach the level 3 title entitled "Start with Inbox in the list of installed modules;
* Then validate on the button: Module options. This opens a new tab titled: Start with Inbox, Settings;
* Set the options then restart Thunderbird.


[1]: https://github.com/RPTools-org/thunderbirdPlusG5/releases/download/v2311.24.00/thunderbirdPlusG5-2311.24.00.nvda-addon

[2]: https://github.com/RPTools-org/thunderbirdPlusG5/

[3]: https://www.rptools.org/?p=9514

[4]: https://www.rptools.org/NVDA-Thunderbird/index.html

[5]: https://www.rptools.org/NVDA-Thunderbird/get.php?pg=changes&v=G5&lang=en

[6]: https://www.rptools.org/NVDA-Thunderbird/toContact.html

[7]: https://www.rptools.org/NVDA-Thunderbird/get.php?pg=manual&lang=en
