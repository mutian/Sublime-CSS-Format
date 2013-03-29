import sublime, sublime_plugin, re

class CssFormatCommand(sublime_plugin.TextCommand):
	def run(self, edit, action='compact'):
		view = self.view
		region = sublime.Region(0, view.size())
		code = view.substr(region)

		code = re.sub(r"\s*([\{\}:;,])\s*", r"\1", code)
		code = re.sub(r",[\s\.\#\d]*{", "{", code)
		code = re.sub(r";\s*;", ";", code)
		code = self.rules(code, action)
		code = re.sub(r"^\s*(\S+(\s+\S+)*)\s*$", r"\1", code)

		view.replace(edit, region, code)

	def rules(self, code, action):
		actions = {
			'compact': self.compact,
			'expand': self.expand,
			'compress': self.compress
		}
		code = actions[action](code)
		return code

	def compact(self, code):
		code = re.sub(r"([^\s])([,\}])([^\n])", r"\1\2\n\3", code)
		return code

	def expand(self, code):
		code = re.sub(r"([^\s]),([^\n])", r"\1,\n\2", code)
		code = re.sub(r"([^\s])\{([^\s])", r"\1 {\n\t\2", code)
		code = re.sub(r"([^\s]);([^\s\}])", r"\1;\n\t\2", code)
		code = re.sub(r"([^\s])\}([^\n]*)", r"\1\n}\n\2", code)
		return code
		
	def compress(self, code):
		code = re.sub(r"\/\*(.|\n)*?\*\/", "", code)
		return code
