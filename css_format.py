import sublime, sublime_plugin, re

class CssFormatCommand(sublime_plugin.TextCommand):
	def run(self, edit, action='compact'):
		view = self.view

		if view.is_loading():
			sublime.status_message("Waiting for loading.")
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
				view.line(max(sel.a, sel.b)).b)  # line end of last line
			code = view.substr(region)
			code = self.process_rules(code, action)
			#view.sel().clear()
			view.replace(edit, region, code)

	def format_whole_file(self, edit, action):
		view = self.view
		region = sublime.Region(0, view.size())
		code = view.substr(region)
		code = self.process_rules(code, action)
		view.replace(edit, region, code)

	def process_rules(self, code, action):
		actions = {
			'compact'	: self.compact_rules,
			'expand'	: self.expand_rules,
			'compress'	: self.compress_rules
		}
		code = re.sub(r"\s*([\{\}:;,])\s*", r"\1", code)
		code = re.sub(r",[\s\.\#\d]*\{", "{", code)
		code = re.sub(r";\s*;", ";", code)
		code = actions[action](code)
		code = re.sub(r"^\s*(\S+(\s+\S+)*)\s*$", r"\1", code)
		return code

	def compact_rules(self, code):
		code = re.sub(r"([^\s])\}([^\n])", r"\1}\n\2", code)
		return code

	def expand_rules(self, code):
		code = re.sub(r"([^\s]),([,\s\.\#\w])\{", r"\1,\n\2{", code)
		code = re.sub(r"([^\s])\{([^\s])", r"\1 {\n\t\2", code)
		code = re.sub(r"([^\s]);([^\s\}])", r"\1;\n\t\2", code)
		code = re.sub(r"([^\s])\}([^\n]*)", r"\1\n}\n\2", code)
		return code
		
	def compress_rules(self, code):
		code = re.sub(r"\/\*(.|\n)*?\*\/", "", code)
		return code
