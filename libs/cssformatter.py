#
# Convert CSS/SASS/SCSS/LESS code to Expanded, Compact or Compressed format.
#   written by Mutian Wang <mutian.wang@gmail.com>
#
# usage:
#   format_code(code, action)
#

"""Convert CSS/SASS/SCSS/LESS code to Expanded, Compact or Compressed format."""

import re


def format_code(code, action='compact', indentation='\t'):
	actFuns = {
		'expand'		: expand_rules,
		'expand-bs'		: expand_rules,			# expand (break selectors)
		'compact'		: compact_rules,
		'compact-bs'	: compact_rules,		# compact (break selectors)
		'compact-ns'	: compact_ns_rules,		# compact (no spaces)
		'compact-bs-ns'	: compact_ns_rules,		# compact (break selectors, no spaces)
		'compress'		: compress_rules
	}

	if action == 'compress':
		code = re.sub(r'\/\*[\s\S]+?\*\/', '', code)	# remove non-empty comments, /**/ maybe a hack

	# Protect Urls
	urls = re.findall(r'url\([^\)]+\)', code)
	code = re.sub(r'url\([^\)]+\)', 'url(~)', code)

	# Pre Process
	code = re.sub(r'\s*([\{\}:;,])\s*', r'\1', code)	# remove \s before and after characters {}:;,
	code = re.sub(r',[\d\s\.\#\+>:]*\{', '{', code)		# remove invalid selectors without \w
	code = re.sub(r';\s*;', ';', code)					# remove superfluous ;

	if action != 'compress':

		# comment
		code = re.sub(r'(\/\*+)\s*([\s\S]+?)\s*(\*+\/)', r'\1 \2 \3', code)	# add space before and after comment content
		code = re.sub(r'\}\s*(\/\*[\s\S]+?\*\/)\s*', r'}\n\1\n', code)	# add \n before and after outside comment

		# selectors group
		if re.search(r'-bs', action):
			code = break_selectors(code)				# break after selectors' ,
		else:
			code = re.sub(r',(\S)', r', \1', code)		# add space after ,

		# add space after :
		if re.search(r'-ns', action):
			code = re.sub(r', +', ',', code)			# remove space after ,
			code = re.sub(r'\s+!important', '!important', code)				# remove space before !important
		else:
			code = re.sub(r'([A-Za-z-]):([^;\{]+[;\}])', r'\1: \2', code)	# add space after properties' :
			code = re.sub(r'(http[s]?:) \/\/', r'\1//', code)				# fix space after http[s]:
			code = re.sub(r'\s*!important', ' !important', code)			# add space before !important

	# Process Action Rules
	code = actFuns[action](code)

	# Trim
	code = re.sub(r'^\s*(\S+(\s+\S+)*)\s*$', r'\1', code)

	if action != 'compress':
		code = indent_code(code, indentation)	# indent
	else:
		code = re.sub(r';\}', r'}', code)		# remove last semicolon

	# Backfill Urls
	while re.search(r'url\(~\)', code):
		code = re.sub(r'url\(~\)', urls[0], code, 1)
		del urls[0]

	return code


# Expand Rules
def expand_rules(code):
	code = re.sub(r'(\S)\{(\S)', r'\1 {\n\2', code)							# add space before { , and add \n after {

	code = re.sub(r'(\S);([^\}])', r'\1;\n\2', code)						# add \n after ;
	# code = re.sub(r'(url\([^\)]*data:[\w\/-:]+)\;\s*', r'\1; ', code)		# fix space after ; in data url
	# code = re.sub(r'(url\([^\)]*charset=[\w-]+)\;\s*', r'\1; ', code)		# fix space after ; in data url
	code = re.sub(r'\;\s*(\/\*[^\n]*\*\/)\s*', r'; \1\n', code)				# fix comment after ;
	code = re.sub(r'((?:@charset|@import)[^;]+;)\s*', r'\1\n', code)		# add \n after @charset & @import

	code = re.sub(r'([^\}])\s*\}', r'\1\n}', code)							# add \n before }
	code = re.sub(r'\}', r'}\n', code)										# add \n after }

	return code


# Compact Rules
def compact_rules(code):
	code = re.sub(r'(\S)\{(\S)', r'\1 { \2', code)							# add space and after {
	code = re.sub(r'((@media|@[\w-]*keyframes)[^\{]+\{)\s*', r'\1\n', code)	# add \n after @media {

	code = re.sub(r'(\S);([^\}])', r'\1; \2', code)							# add space after ;
	code = re.sub(r'\;\s*(\/\*[^\n]*\*\/)\s*', r'; \1\n', code)				# fix comment after ;
	code = re.sub(r'((?:@charset|@import)[^;]+;)\s*', r'\1\n', code)		# add \n after @charset & @import
	code = re.sub(r';\s*([^\};]+?\{)', r';\n\1', code)						# add \n before included selector

	code = re.sub(r'(\/\*[^\n]*\*\/)\s+\}', r'\1}', code)					# remove \n between comment and }
	code = re.sub(r'(\S)\}', r'\1 }', code)									# add space before }
	code = re.sub(r'\}\s*', r'}\n', code)									# add \n after }

	return code


# Compact Rules (no space)
def compact_ns_rules(code):
	code = re.sub(r'((@media|@[\w-]*keyframes)[^\{]+\{)\s*', r'\1\n', code)	# add \n after @media {

	code = re.sub(r'\;\s*(\/\*[^\n]*\*\/)\s*', r'; \1\n', code)				# fix comment after ;
	code = re.sub(r'((?:@charset|@import)[^;]+;)\s*', r'\1\n', code)		# add \n after @charset & @import
	code = re.sub(r';\s*([^\};]+?\{)', r';\n\1', code)						# add \n before included selector

	code = re.sub(r'(\/\*[^\n]*\*\/)\s+\}', r'\1}', code)					# remove \n between comment and }
	code = re.sub(r'\}\s*', r'}\n', code)									# add \n after }

	return code


# Compress Rules
def compress_rules(code):
	code = re.sub(r'\s*([\{\}:;,])\s*', r'\1', code)					# remove \s before and after characters {}:;, again
	code = re.sub(r'\s+!important', '!important', code)					# remove space before !important
	code = re.sub(r'((?:@charset|@import)[^;]+;)\s*', r'\1\n', code)	# add \n after @charset & @import

	return code


# Break after Selector
def break_selectors(code):
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


# Code Indent
def indent_code(code, indentation):
	lines = code.split('\n')
	level = 0

	for i in range(len(lines)):
		increment = lines[i].count('{') - lines[i].count('}')
		level = level + increment
		thisLevel = level - increment if increment > 0 else level
		lines[i] = re.sub(r'\s*(\S+(\s+\S+)*)\s*', r'\1', lines[i])	# trim
		lines[i] = indentation * thisLevel + lines[i]

	code = '\n'.join(lines)

	return code
