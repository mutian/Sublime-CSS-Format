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
				view.line(max(sel.a, sel.b)).b   # line end of last line
			)
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
		code = re.sub(r"\s*([\{\}:;,])\s*", r"\1", code)		# remove \s before and after characters {}:;,
		code = re.sub(r",[\d\s\.\#\+>:]*\{", "{", code)			# remove invalid selector
		code = re.sub(r";\s*;", ";", code)						# remove superfluous ;

		if action != 'compress':
			code = re.sub(r"\/\*\s*([\s\S]+?)\s*\*\/", r"/* \1 */", code)	# add space before and after comment content
			code = re.sub(r"\}\s*(\/\*[\s\S]+?\*\/)\s*", r"}\n\1\n", code)	# add \n before and after outside comment
			code = re.sub(r",(\S)", r", \1", code)							# add space after ,
			code = re.sub(r"([A-Za-z-]):([^;\{]+[;\}])", r"\1: \2", code)	# add space after properties' :
			code = re.sub(r"(http[s]?:) \/\/", r"\1//", code)				# fix space after http[s]:
			code = re.sub(r"\s*!important", r" !important", code)			# add space before !important

		code = actions[action](code)

		code = re.sub(r"(@import[^;]+;)\s*", r"\1\n", code)		# add \n and remove \t after @import
		code = re.sub(r"^\s*(\S+(\s+\S+)*)\s*$", r"\1", code)	# remove superfluous \s
		return code

	def compact_rules(self, code):
		#code = re.sub(r"([^\s])([,\}])([^\n])", r"\1\2\n\3", code)
		#code = re.sub(r"([^\s]),([^\s])", r"\1, \2", code)		# todo: add \n after selectors' ,

		code = re.sub(r"(\S)\{(\S)", r"\1 { \2", code)			# add space and after {
		code = re.sub(r"(\S);([^\}])", r"\1; \2", code)			# add space after ;
		code = re.sub(r"(\S)\}", r"\1 }", code)					# add space before }
		code = re.sub(r"\}", r"}\n", code)						# add \n after }
		#code = re.sub(r"\{([^\{\}])*\}", compact_rules_brace_block, code)	# todo:
		return code

	# def compact_rules_brace_block(matches):
	# 	code = matches[0]
	# 	code = re.sub(r"(\S):(\S)", r"\1: \2", code)
	# 	return code

	def expand_rules(self, code):
		#code = re.sub(r"(\w),([^\{]+\{)", r"\1,\n\2", code)	# todo: add \n after selectors' ,
		#code = re.sub(r"(\{[^\{]+),\s+([^\}]+\})", r"\1,\2", code)

		code = re.sub(r"(\S)\{(\S)", r"\1 {\n\t\2", code)				# add space before { , and add \n\t after {
		code = re.sub(r"(\S);([^\}])", r"\1;\n\t\2", code)				# add \n\t after ;
		code = re.sub(r"\;\s*(\/\*[^\n]*\*\/)\s*", r"; \1\n\t", code)	# fix comment after ;
		code = re.sub(r"([^\}])\s*\}", r"\1\n}", code)					# add \n before }
		code = re.sub(r"\}", r"}\n", code)								# add \n after }
		return code
	
	def compress_rules(self, code):
		code = re.sub(r"\/\*[\s\S]+?\*\/", "", code)		# remove non-empty comments, /**/ maybe a hack
		code = re.sub(r"\s*([\{\}:;,])\s*", r"\1", code)	# remove \s before and after characters {}:;, again
		code = re.sub(r"\s*(!important)", r"\1", code)		# remove space before !important
		return code
