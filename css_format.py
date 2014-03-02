import sublime, sublime_plugin, sys, os

if sys.version_info < (3, 0):
	# ST2, Python 2.6
	from libs.cssformatter import format_code
else:
	# ST3, Python 3.3
	from .libs.cssformatter import format_code


class CssFormatCommand(sublime_plugin.TextCommand):

	def run(self, edit, action='compact'):
		view = self.view

		if view.is_loading():
			sublime.status_message('Waiting for loading.')
			return False

		selection = view.sel()[0]
		if len(selection) > 0:
			self.format_selection(edit, action)
		else:
			self.format_whole_file(edit, action)

	def format_selection(self, edit, action):
		view = self.view
		regions = []

		for sel in view.sel():
			region = sublime.Region(
				view.line(min(sel.a, sel.b)).a,  # line start of first line
				view.line(max(sel.a, sel.b)).b   # line end of last line
			)
			code = view.substr(region)
			code = format_code(code, action)
			#view.sel().clear()
			view.replace(edit, region, code)

	def format_whole_file(self, edit, action):
		view = self.view
		region = sublime.Region(0, view.size())
		code = view.substr(region)
		code = format_code(code, action)
		view.replace(edit, region, code)

	def is_visible(self):
		view = self.view
		file_name = view.file_name()
		syntax_path = view.settings().get('syntax')
		css_family = ['css', 'sass', 'scss', 'less']
		suffix = ''
		syntax = ''
		
		if file_name != None: # file exists, pull syntax type from extension
			suffix = os.path.splitext(file_name)[1][1:]
		if syntax_path != None:
			syntax = os.path.splitext(syntax_path)[0].split('/')[-1].lower()
		return suffix in css_family or syntax in css_family
