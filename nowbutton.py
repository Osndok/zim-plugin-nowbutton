#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# nowbutton.py
#
# A Zim plugin that jumps to today's journal entry, and appends the current *time* to the end of the file.
# This makes it nearly trivial to keep a log with tighter-than-one-day granularity.
#
# Skeleton and basic operation of this script was DERIVED from zim 'quicknote' and 'tasklist' plugins.
#
from time import strftime
import gtk


from datetime import datetime, timedelta
from datetime import date as dateclass

# TODO: kern out unneccesary imports
from zim.plugins import PluginClass, WindowExtension, extends
from zim.actions import action

import logging

logger = logging.getLogger('zim.plugins.nowbutton')

class NowButtonPlugin(PluginClass):

	plugin_info = {
		'name': _('Now Button'), # T: plugin name
		'description': _('''\
This plugin provides an easy toolbar option to append the current time to today's journal entry and
focus that page. Note that it is easy to get back to where you were due to Zim\'s built-in back-tracking
buttons.
'''), # T: plugin description
		'author': 'Robert Hailey',
		'help': 'Plugins:NowButton',
	}
	plugin_preferences = (
		('hours_past_midnight', 'int', _('Hours past Midnight'), 4, (0, 12)),
	)


@extends('MainWindow')
class MainWindowExtension(WindowExtension):

	uimanager_xml = '''
		<ui>
			<menubar name='menubar'>
				<menu action='tools_menu'>
					<placeholder name='plugin_items'>
						<menuitem action='now_button_clicked'/>
					</placeholder>
				</menu>
			</menubar>
			<toolbar name='toolbar'>
				<placeholder name='tools'>
					<toolitem action='now_button_clicked'/>
				</placeholder>
			</toolbar>
		</ui>
	'''

	def __init__(self, plugin, window):
		WindowExtension.__init__(self, plugin, window)

	@action(
		_('Log Entry'),
		stock=gtk.STOCK_JUMP_TO,
		readonly=True,
		accelerator = '<Control><Shift>E'
	) # T: menu item
	def now_button_clicked(self):

		calendar_config=self.plugin.config.get_config_dict('<profile>/preferences.conf')['CalendarPlugin'];
		calendar_namespace=calendar_config['namespace'];

		offset_time=datetime.today()-timedelta(hours=self.plugin.preferences['hours_past_midnight'])

		name=str(calendar_namespace.child(offset_time.strftime('%Y:%m:%d')));

		text = '\n' + strftime('%I:%M%p - ').lower();

		ui = self.window.ui
		try:
			#v0.65
			path=ui.notebook.resolve_path(name);
		except AttributeError:
			#v0.66
			path=ui.notebook.pages.lookup_from_user_input(name);

		page=ui.notebook.get_page(path);

		#ui.append_text_to_page(path, text)

		if not page.exists():
			parsetree = ui.notebook.get_template(page)
			page.set_parsetree(parsetree)

		page.parse('wiki', text, append=True) # FIXME format hard coded ??? (this FIXME was copied from gui.__init__)
		ui.present(path)
		ui.notebook.store_page(page);

		# Move the cursor to the end of the line that was just appended...
		textBuffer = self.window.pageview.view.get_buffer();
		i = textBuffer.get_end_iter();
		i.backward_visible_cursor_positions(1);
		textBuffer.place_cursor(i);

		# and finally... scroll the window all the way to the bottom.
		self.window.pageview.scroll_cursor_on_screen();

	def on_notebook_changed(self):
		return None



