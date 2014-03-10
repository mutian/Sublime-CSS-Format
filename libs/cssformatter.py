#
# Convert CSS/SASS/SCSS/LESS code to Expanded, Compact or Compressed format.
#   written by Mutian Wang <mutian.wang@gmail.com>
#
# usage:
#   format_code(code, action)
#

"""Convert CSS/SASS/SCSS/LESS code to Expanded, Compact or Compressed format."""

import re

def format_code(code, action='compact'):
	actFuns = {
		'expand'	: expand_rules,
		'compact'	: compact_rules,
		'compress'	: compress_rules
	}
	code = re.sub(r'\s*([\{\}:;,])\s*', r'\1', code)		# remove \s before and after characters {}:;,
	code = re.sub(r',[\d\s\.\#\+>:]*\{', '{', code)			# remove invalid selector
	code = re.sub(r';\s*;', ';', code)						# remove superfluous ;

	if action != 'compress':
		code = re.sub(r'\/\*\s*([\s\S]+?)\s*\*\/', r'/* \1 */', code)	# add space before and after comment content
		code = re.sub(r'\}\s*(\/\*[\s\S]+?\*\/)\s*', r'}\n\1\n', code)	# add \n before and after outside comment
		code = comma_rules(code)										# add space or \n after ,
		code = re.sub(r'([A-Za-z-]):([^;\{]+[;\}])', r'\1: \2', code)	# add space after properties' :
		code = re.sub(r'(http[s]?:) \/\/', r'\1//', code)				# fix space after http[s]:
		code = re.sub(r'\s*!important', ' !important', code)			# add space before !important

	code = actFuns[action](code)
	code = re.sub(r'^\s*(\S+(\s+\S+)*)\s*$', r'\1', code)				# trim
	return code

def expand_rules(code):
	code = re.sub(r'(\S)\{(\S)', r'\1 {\n\2', code)						# add space before { , and add \n after {

	code = re.sub(r'(\S);([^\}])', r'\1;\n\2', code)					# add \n after ;
	code = re.sub(r'(url\([^\)]*data:[\w\/-:]+)\;\s*', r'\1; ', code)	# fix space after ; in data url
	code = re.sub(r'(url\([^\)]*charset=[\w-]+)\;\s*', r'\1; ', code)	# fix space after ; in data url
	code = re.sub(r'\;\s*(\/\*[^\n]*\*\/)\s*', r'; \1\n', code)			# fix comment after ;
	code = re.sub(r'((?:@charset|@import)[^;]+;)\s*', r'\1\n', code)	# add \n after @charset & @import

	code = re.sub(r'([^\}])\s*\}', r'\1\n}', code)						# add \n before }
	code = re.sub(r'\}', r'}\n', code)									# add \n after }

	code = indent_rules(code)											# add \t indent
	return code

def compact_rules(code):
	code = re.sub(r'(\S)\{(\S)', r'\1 { \2', code)						# add space and after {
	code = re.sub(r'((@media|@[\w-]*keyframes)[^\{]+\{)\s*', r'\1\n', code)	# add \n after @media {

	code = re.sub(r'(\S);([^\}])', r'\1; \2', code)						# add space after ;
	code = re.sub(r'\;\s*(\/\*[^\n]*\*\/)\s*', r'; \1\n', code)			# fix comment after ;
	code = re.sub(r'((?:@charset|@import)[^;]+;)\s*', r'\1\n', code)	# add \n after @charset & @import
	code = re.sub(r';\s*([^\};]+?\{)', r';\n\1', code)					# add \n before included selector

	code = re.sub(r'(\/\*[^\n]*\*\/)\s+\}', r'\1}', code)				# remove \n between comment and }
	code = re.sub(r'(\S)\}', r'\1 }', code)								# add space before }
	code = re.sub(r'\}\s*', r'}\n', code)								# add \n after }

	code = indent_rules(code)											# add \t indent
	return code

def compress_rules(code):
	code = re.sub(r'\/\*[\s\S]+?\*\/', '', code)		# remove non-empty comments, /**/ maybe a hack
	code = re.sub(r'\s*([\{\}:;,])\s*', r'\1', code)	# remove \s before and after characters {}:;, again
	code = re.sub(r'\s*(!important)', r'\1', code)		# remove space before !important
	code = re.sub(r'((?:@charset|@import)[^;]+;)\s*', r'\1\n', code)	# add \n after @charset & @import
	return code

def comma_rules(code):
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

def indent_rules(code):
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
