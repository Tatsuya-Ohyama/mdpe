#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Program to convert papers in markdown format to each other
"""

import sys, signal
sys.dont_write_bytecode = True
signal.signal(signal.SIGINT, signal.SIG_DFL)

import argparse
import re

from mods.func_prompt_io import check_exist, check_overwrite



# =============== constant =============== #
LINE_START_WITH = "*"
COMMENT_START = "<!--"
COMMENT_END = "-->"
RE_LINE_START_WITH = re.compile(r"^[\s\t]*\*")
RE_YAML = re.compile(r"^-{3}[\s\t]*\n")
RE_PERIOD = re.compile(r"(。)|(\.)|(\n)")
RE_START_DIGIT = re.compile(r"^\d+\.$")
IGNORE_PERIOD = {
	"Fig.": "Fig\0",
	"Figs.": "Figs\0",
	" i.e.": " i\0e\0",
	" e.g.": " e\0g\0",
	" et al.": " et al\0",
	" etc.": " etc\0",
	" cf.": " cf\0",
	" ca.": " ca\0"
}
RE_IGNORE_FLOAT = re.compile(r"(-?\d+)\.(\d+)")



# =============== class =============== #
class FileMD:
	def __init__(self, input_file):
		self._yaml = []
		self._list_lines = []

		self._read_file(input_file)

	@property
	def yaml(self):
		return self._yaml

	@property
	def lines(self):
		return self._list_lines

	@property
	def has_yaml(self):
		if len(self._yaml) == 0:
			return True
		else:
			return False


	def _read_file(self, input_file):
		"""
		Method to read file

		Args:
			input_file (str): file path
			exist_yaml (bool): YAML state (Default: False)

		Returns:
			list: [[indent(str), main(str), comment(str)], ...]
		"""
		in_yaml = False
		line_type = 0
		with open(input_file, "r") as obj_input:
			for line_val in obj_input:
				if "<!--" not in line_val and "@import" in line_val:
					# @import line
					include_path = line_val.strip().replace("@import", "").strip()[1:-1]
					obj_file_MD = FileMD(include_path)
					if not self.has_yaml and obj_file_MD.has_yaml:
						self._yaml = obj_file_MD.yaml
					self._list_lines.extend(obj_file_MD.lines)

				elif RE_LINE_START_WITH.search(line_val):
					# regular line
					line_type = 1
					indent, line_val = line_val.split(LINE_START_WITH, maxsplit=1)
					line_val = line_val.replace(COMMENT_END, "", 1)
					line_val = line_val.strip()
					elems = [v.strip() for v in line_val.split(COMMENT_START, 1)]
					if len(elems) != 2:
						elems.append("")
					self._list_lines.append([indent, elems[0], elems[1]])

				elif RE_YAML.search(line_val):
					# start and end of YAML
					line_type = 2
					if in_yaml:
						# end of YAML
						in_yaml = False
						self._yaml.append("---\n\n")

					else:
						# start of YAML
						in_yaml = True
						self._yaml.append("\n---\n")

				elif in_yaml:
					line_type = 2
					self._yaml.append(line_val)

				else:
					if line_type == 2 and len(line_val.strip()) == 0:
						continue
					self._list_lines.append([line_val])

		return self



# =============== function =============== #
def swap_main_and_comment(input_file):
	"""
	Function to swap main text and comment

	Args:
		input_file (str): input file path

	Returns:
		list: [line_val(str), ...]
	"""
	output_line_vals = []
	obj_file_MD = FileMD(input_file)
	for elems in obj_file_MD.lines:
		if len(elems) == 3:
			indent, main, comment = elems
			output_line_vals.append("{0}* {1} <!-- {2} -->\n".format(indent, comment, main))

		else:
			output_line_vals.append(elems[0])

	output_line_vals = output_line_vals[:1] + obj_file_MD.yaml + output_line_vals[1:]
	return output_line_vals



def formatting(input_file, enable_region):
	"""
	Function to format to paper (remove main text or comment)

	Args:
		input_file (str): input file path
		enable_region (str): remain region: `main` or `comment`

	Returns:
		list: [line_val(str), ...]
	"""
	output_line_vals = []
	is_continued_list_bullet = False
	indent_status = [0, 0]

	obj_file_MD = FileMD(input_file)
	for elems in obj_file_MD.lines:
		if len(elems) == 3:
			indent, main, comment = elems
			indent_sp = indent.count(" ")
			indent_tb = indent.count("\t")

			if indent_sp < indent_status[0] or indent_tb < indent_status[1]:
				is_continued_list_bullet = False
			indent_status = [indent_sp, indent_tb]

			if enable_region == "comment" and len(comment) != 0:
				main = comment

			if is_continued_list_bullet:
				output_line_vals[-1] += " {0}".format(main)
			else:
				output_line_vals.append("\n")
				output_line_vals.append(main)
			is_continued_list_bullet = True

		else:
			output_line_vals.append(elems[0])
			is_continued_list_bullet = False

	output_line_vals = output_line_vals[:1] + obj_file_MD.yaml + output_line_vals[1:]
	return [v if v.endswith("\n") else v+"\n" for v in output_line_vals]


def import_txt(input_file):
	"""
	Function to import text

	Args:
		input_file (str): input file path

	Returns:
		list: [line_val(str), ...]
	"""
	with open(input_file, "r") as obj_input:
		for line_val in obj_input:
			pos = [0, 0]
			indent = None
			if len(line_val.strip()) == 0:
				# empty line
				output_line_vals.append(line_val)
				continue

			for ignore_key in IGNORE_PERIOD.keys():
				# ignore special period
				if ignore_key in line_val:
					line_val = line_val.replace(ignore_key, IGNORE_PERIOD[ignore_key])
			line_val = RE_IGNORE_FLOAT.sub(r"\1\0\2", line_val)

			for obj_match in RE_PERIOD.finditer(line_val):
				# line contain period
				_, pos[1] = obj_match.span()
				text = line_val[pos[0]:pos[1]].strip()

				if pos[0] == 0 and RE_START_DIGIT.search(text):
					# skip start with digit and period (ordered list)
					continue

				if len(text.strip()) == 0:
					# empty text (space only)
					continue

				pos[0] = pos[1]

				if indent is None:
					indent = ""
				elif indent == "":
					indent = "\t"

				text = text.replace("\0", ".")
				output_line_vals.append("{0}* {1} <!--  -->\n".format(indent, text))

	return [v if v.endswith("\n") else v+"\n" for v in output_line_vals]



# =============== main =============== #
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Program to convert papers in markdown format to each other", formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("TYPE", metavar="OPERATION", choices=["swap", "main", "comment", "import"], help="operation type (`swap`, `main`, or `comment`)")
	parser.add_argument("INPUT_FILE", metavar="INPUT.md", help="source markdown paper file")
	parser.add_argument("OUTPUT_FILE", metavar="OUTPUT.md", nargs="?", help="output markdown paper file (Default: `-i`)")
	parser.add_argument("-a", "--append", dest="FLAG_APPEND", action="store_true", default=False, help="append markdown for `import` mode")
	parser.add_argument("-O", dest="FLAG_OVERWRITE", action="store_true", default=False, help="overwrite forcibly")
	args = parser.parse_args()

	check_exist(args.INPUT_FILE, 2)

	output_file = args.INPUT_FILE
	if args.OUTPUT_FILE is not None:
		output_file = args.OUTPUT_FILE

	output_line_vals = []
	if args.TYPE == "swap":
		output_line_vals = swap_main_and_comment(args.INPUT_FILE)
	elif args.TYPE == "import":
		output_line_vals = import_txt(args.INPUT_FILE)
	else:
		output_line_vals = formatting(args.INPUT_FILE, args.TYPE)


	if args.FLAG_OVERWRITE == False:
		check_overwrite(output_file)

	write_option = "w"
	if args.TYPE == "import" and args.FLAG_APPEND:
		write_option = "a"

	with open(output_file, write_option) as obj_output:
		for line_val in output_line_vals:
			obj_output.write(line_val)
