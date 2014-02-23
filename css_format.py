import sublime, sublime_plugin, re, os

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
		actFuns = {
			'compact'	: self.compact_rules,
			'expand'	: self.expand_rules,
			'compress'	: self.compress_rules
		}
		code = re.sub(r'\s*([\{\}:;,])\s*', r'\1', code)		# remove \s before and after characters {}:;,
		code = re.sub(r',[\d\s\.\#\+>:]*\{', '{', code)			# remove invalid selector
		code = re.sub(r';\s*;', ';', code)						# remove superfluous ;

		if action != 'compress':
			code = re.sub(r'\/\*\s*([\s\S]+?)\s*\*\/', r'/* \1 */', code)	# add space before and after comment content
			code = re.sub(r'\}\s*(\/\*[\s\S]+?\*\/)\s*', r'}\n\1\n', code)	# add \n before and after outside comment
			code = self.comma_rules(code)									# add space or \n after ,
			code = re.sub(r'([A-Za-z-]):([^;\{]+[;\}])', r'\1: \2', code)	# add space after properties' :
			code = re.sub(r'(http[s]?:) \/\/', r'\1//', code)				# fix space after http[s]:
			code = re.sub(r'\s*!important', ' !important', code)			# add space before !important

		code = actFuns[action](code)
		code = re.sub(r'(@import[^;]+;)\s*', r'\1\n', code)				# add \n after @import
		code = re.sub(r'^\s*(\S+(\s+\S+)*)\s*$', r'\1', code)			# trim
		return code

	def compact_rules(self, code):
		code = re.sub(r'(\S)\{(\S)', r'\1 { \2', code)					# add space and after {
		code = re.sub(r'((@media|@[\w-]*keyframes)[^\{]+\{)\s*', r'\1\n', code)	# add \n after @media {
		code = re.sub(r'(\S);([^\}])', r'\1; \2', code)					# add space after ;
		code = re.sub(r'\;\s*(\/\*[^\n]*\*\/)\s*', r'; \1\n', code)		# fix comment after ;
		code = re.sub(r'(\/\*[^\n]*\*\/)\s+\}', r'\1}', code)			# remove \n between comment and }
		code = re.sub(r'(\S)\}', r'\1 }', code)							# add space before }
		code = re.sub(r'\}\s*', r'}\n', code)							# add \n after }
		code = re.sub(r';\s*([^\};]+?\{)', r';\n\1', code)				# add \n before included selector
		code = self.indent_rules(code)										# add \t indent
		return code

	def expand_rules(self, code):
		code = re.sub(r'(\S)\{(\S)', r'\1 {\n\2', code)					# add space before { , and add \n after {
		code = re.sub(r'((@media|@[\w-]*keyframes)[^\{]+\{)\s*', r'\1\n', code)	# remove \t after @media {
		code = re.sub(r'(\S);([^\}])', r'\1;\n\2', code)				# add \n after ;
		code = re.sub(r'\;\s*(\/\*[^\n]*\*\/)\s*', r'; \1\n', code)		# fix comment after ;
		code = re.sub(r'([^\}])\s*\}', r'\1\n}', code)					# add \n before }
		code = re.sub(r'\}', r'}\n', code)								# add \n after }
		code = self.indent_rules(code)										# add \t indent
		return code
	
	def compress_rules(self, code):
		code = re.sub(r'\/\*[\s\S]+?\*\/', '', code)		# remove non-empty comments, /**/ maybe a hack
		code = re.sub(r'\s*([\{\}:;,])\s*', r'\1', code)	# remove \s before and after characters {}:;, again
		code = re.sub(r'\s*(!important)', r'\1', code)		# remove space before !important
		return code

	def comma_rules(self, code):
		block = code.split('}')

		for i in range(len(block)):
			b = block[i].split('{')
			for j in range(len(b)):
				if b[j].count('@import'):
					s = b[j].split(';')
					for k in range(len(s)):
						if not s[k].count('@import'):					# ignore @import
							s[k] = re.sub(r',(\S)', r',\n\1', s[k])
					b[j] = ';'.join(s)
				else:
					if j == len(b) - 1 or b[j].count('@media'):
						b[j] = re.sub(r',(\S)', r', \1', b[j])			# add space after properties' or @media's ,
					else:
						b[j] = re.sub(r',(\S)', r',\n\1', b[j])			# add \n after selectors' ,
			block[i] = '{'.join(b)
		code = '}'.join(block)
		return code

	def indent_rules(self, code):
		lines = code.split('\n')
		level = 0

		for i in range(len(lines)):
			increment = lines[i].count('{') - lines[i].count('}')
			level = level + increment
			thisLevel = level - increment if increment > 0 else level
			lines[i] = re.sub(r'\s*(\S+(\s+\S+)*)\s*', r'\1', lines[i])	# trim
			lines[i] = '\t' * thisLevel + lines[i]
		code = '\n'.join(lines)
		return code

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
