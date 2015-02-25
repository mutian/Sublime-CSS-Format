#coding=utf-8
#
# Convert CSS/SASS/SCSS/LESS code to Expanded, Compact or Compressed format.
#
# Usage: format_code(code, action)
# Author: Mutian Wang <mutian@me.com>
#

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

	if action not in actFuns:
		return code

	# Comments
	if action == 'compress':
		# remove comments
		code = re.sub(r'\/\*[\s\S]*?\*\/', '', code)
	else:
		# Protect Comments
		comments = re.findall(r'[ \t]*\/\*[\s\S]*?\*\/', code)
		code = re.sub(r'[ \t]*\/\*[\s\S]*?\*\/', '</**/>', code)

	# Protect Urls
	urls = re.findall(r'url\([^\)]+\)', code)
	code = re.sub(r'url\([^\)]+\)', '<url()>', code)

	# Pre Process
	code = re.sub(r'\s*([\{\}:;,])\s*', r'\1', code)	# remove \s before and after characters {}:;,
	code = re.sub(r',[\d\s\.\#\+>:]*\{', '{', code)		# remove invalid selectors without \w
	code = re.sub(r'([;,])\1+', r'\1', code)			# remove repeated ;,

	if action != 'compress':
		# selectors group
		if re.search(r'-bs', action):
			code = break_selectors(code)				# break after selectors' ,
		else:
			code = re.sub(r',(\S)', r', \1', code)		# add space after ,

		# add space after :
		if re.search(r'-ns', action):
			code = re.sub(r', +', ',', code)								# remove space after ,
			code = re.sub(r'\s+!important', '!important', code)				# remove space before !important
		else:
			code = re.sub(r'([A-Za-z-]):([^;\{]+[;\}])', r'\1: \2', code)	# add space after properties' :
			code = re.sub(r'\s*!important', ' !important', code)			# add space before !important

	# Process Action Rules
	code = actFuns[action](code)


	if action == 'compress':
		# remove last semicolon
		code = re.sub(r';\}', r'}', code)
	else:
		# Fix Comments
		code = re.sub(r'\s*<\/\*\*\/>\s*@', r'\n\n</**/>\n@', code)
		code = re.sub(r'\s*<\/\*\*\/>\s*([^\/\{\};]+?){', r'\n\n</**/>\n\1{', code)
		code = re.sub(r'\s*\n<\/\*\*\/>', r'\n\n</**/>', code)

		# Backfill Comments
		for i in range(len(comments)):
			code = re.sub(r'[ \t]*<\/\*\*\/>', comments[i], code, 1)

		# Indent
		code = indent_code(code, indentation)

	# Backfill Urls
	for i in range(len(urls)):
		code = re.sub(r'<url\(\)>', urls[i], code, 1)

	# Trim
	code = re.sub(r'^\s*(\S+(\s+\S+)*)\s*$', r'\1', code)

	return code


# Expand Rules
def expand_rules(code):
	code = re.sub(r'\{', r' {\n', code)									# add space before { and add \n after {

	code = re.sub(r';', r';\n', code)									# add \n after ;
	code = re.sub(r';\s*([^\{\};]+?){', r';\n\n\1{', code)				# double \n between ; and include selector

	code = re.sub(r'\s*(<\/\*\*\/>)\s*;\s*', r' \1 ;\n', code)			# fix comment before ;
	code = re.sub(r'(:[^:;]+;)\s*(<\/\*\*\/>)\s*', r'\1 \2\n', code)	# fix comment after ;

	code = re.sub(r'\s*\}', r'\n}', code)								# add \n before }
	code = re.sub(r'\}\s*', r'}\n', code)								# add \n after }

	return code


# Compact Rules
def compact_rules(code):
	code = re.sub(r'\{', r' { ', code)										# add space and after {
	code = re.sub(r'(@[\w-]*(document|font-feature-values|keyframes|media|supports)[^;]*?\{)\s*', r'\1\n', code)
																			# add \n after @xxx {

	code = re.sub(r';', r'; ', code)										# add \n after ;
	code = re.sub(r'(@(charset|import|namespace).+?;)\s*', r'\1\n', code)	# add \n after @charset & @import
	code = re.sub(r';\s*([^\};]+?\{)', r';\n\1', code)						# add \n before included selector

	code = re.sub(r'\s*(<\/\*\*\/>)\s*;', r' \1 ;', code)					# fix comment before ;
	code = re.sub(r'(:[^:;]+;)\s*(<\/\*\*\/>)\s*', r'\1 \2 ', code)			# fix comment after ;

	code = re.sub(r'\s*\}', r' }', code)									# add space before }
	code = re.sub(r'\}\s*', r'}\n', code)									# add \n after }

	return code


# Compact Rules (no space)
def compact_ns_rules(code):
	code = re.sub(r'(@[\w-]*(document|font-feature-values|keyframes|media|supports)[^;]*?\{)\s*', r'\1\n', code)
																			# add \n after @xxx {

	code = re.sub(r'(@(charset|import|namespace).+?;)\s*', r'\1\n', code)	# add \n after @charset & @import
	code = re.sub(r';\s*([^\};]+?\{)', r';\n\1', code)						# add \n before included selector

	code = re.sub(r'\s*(<\/\*\*\/>)\s*;', r'\1;', code)						# fix comment before ;
	code = re.sub(r'(:[^:;]+;)\s*(<\/\*\*\/>)\s*', r'\1\2', code)			# fix comment after ;

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
def indent_code(code, indentation='\t'):
	lines = code.split('\n')
	level = 0
	inComment = False
	outPrefix = ''

	for i in range(len(lines)):
		adjustment = lines[i].count('{') - lines[i].count('}')
		nextLevel = level + adjustment
		thisLevel = level if adjustment > 0 else nextLevel
		level = nextLevel

		# Trim
		if not inComment:
			m = re.match(r'^(\s+)\/\*.*', lines[i])
			if m is not None:
				outPrefix = m.group(1)
				lines[i] = re.sub(r'^' + outPrefix + '(.*)\s*$', r'\1', lines[i])
			else:
				lines[i] = re.sub(r'^\s*(.*)\s*$', r'\1', lines[i])
		else:
			lines[i] = re.sub(r'^' + outPrefix + '(.*)\s*$', r'\1', lines[i])

		# Is next line in comment?
		commentQuotes = re.findall(r'\/\*|\*\/', lines[i])
		for quote in commentQuotes:
			if inComment and quote == '*/':
				inComment = False
			elif quote == '/*':
				inComment = True

		# Add Indentation
		lines[i] = indentation * thisLevel + lines[i] if lines[i] != '' else ''

	code = '\n'.join(lines)

	return code
