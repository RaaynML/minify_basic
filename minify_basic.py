import re
from sys import argv as arglist

global codestream;

def minify_basic(in_data)->str:
	global codestream; codestream = in_data
	
	# Remove comments, except for within "" (single or multi-line)
	# src https://stackoverflow.com/a/58784551
	# un-escaped version is
	# (/\*[^*]*\*+(?:[^/*][^*]*\*+)*/|//(?:[^\\]|\\(?:\r?\n)?)*?(?:\r?\n|$))|("[^"\\]*(?:\\[\S\s][^"\\]*)*"|'[^'\\]*(?:\\[\S\s][^'\\]*)*'|[\S\s][^/"'\\]*)
	
	codestream = re.sub(r"(/\\*[^*]*\\*+(?:[^/*][^*]*\\*+)*/|//(?:[^\\\\]|\\\\(?:\\r?\\n)?)*?(?:\\r?\\n|$))|(\"[^\"\\\\]*(?:\\\\[\\S\\s][^\"\\\\]*)*\"|'[^'\\\\]*(?:\\\\[\\S\\s][^'\\\\]*)*'|[\\S\\s][^/\"'\\\\]*)","",codestream)
	
	# Remove whitespace around non-alphanumerics
	codestream = re.sub(r"(?<=\S)\s*([^\w\s])\s*(?=\S)",r"\1",codestream)
	
	# replace newlines around `else`
	codestream = re.sub(r"else\s*\n","else ",codestream)
	codestream = re.sub(r"\n\s*else"," else",codestream)
	
	# fix `this` following newline
	codestream = re.sub(r"\nthis"," this",codestream)
	
	# remove remaining newlines
	codestream = re.sub(r"\n","",codestream)
	
	return codestream

if len(arglist) != 2:
	print("Usage: script.py <input.js>")
	exit(1)

with open(arglist[1], "r+", encoding="utf-8") as file:
	minified = minify_basic(file.read())
	#rewrite file from start
	file.seek(0)
	file.write(minified)
	#shrinkwrap file to new size
	file.truncate()
