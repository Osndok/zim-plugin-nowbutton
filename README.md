# zim-plugin-nowbutton
Super-easy way to make a timestamped log entries in the Zim wiki's Journal with the click of a button.

Zim is a personal desktop wiki. This is NOT zim, but a plugin therefore that manifests itself as a single button in the toolbar.

When this new button is clicked, the following happens:
* If the current day's journal page does not exist, it is created.
* The window is navigated to today's journal page.
* The page's text has the time appended to it (e.g. "\n04:52pm - ")
* The cursor is placed at the end of that new line, ready to type "what's happening now".

To install this plugin, place the "py" file at "$HOME/.local/share/zim/plugins", and [re]start Zim.

Configuration
-------------

If you tend to make log entries past midnight, this is the number of hours past midnight that
will be considered "the same day" (for purposes of selecting the journal page). To be most
effective, it should be the time that you are "most surely asleep". Small for early risers, larger
for night-owls. For example, a value of '4' would imply that the new day/page starts at '4am'.