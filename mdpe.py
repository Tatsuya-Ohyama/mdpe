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
SKIP_LINE_START = ["####"]
RE_LINE_START_WITH = re.compile(r"^[\s\t]*\*")



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
	with open(input_file, "r") as obj_input:
		for line_val in obj_input:
			if RE_LINE_START_WITH.search(line_val) and "<!--" in line_val:
				indent, line_val = line_val.split(LINE_START_WITH, maxsplit=1)
				line_val = line_val.replace(COMMENT_END, "", 1)
				line_val = line_val.strip()
				elems = [v.strip() for v in line_val.split(COMMENT_START, 1)]
				output_line_vals.append("{0}* {1} <!-- {2} -->\n".format(indent, elems[1], elems[0]))

			else:
				output_line_vals.append(line_val)

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
	with open(input_file, "r") as obj_input:
		for line_val in obj_input:
			if any([line_val.startswith(v) for v in SKIP_LINE_START]):
				continue

			if RE_LINE_START_WITH.search(line_val) and COMMENT_START in line_val:
				line_val = line_val.split(LINE_START_WITH, maxsplit=1)[1]
				line_val = line_val.replace(COMMENT_END, "", 1)
				line_val = line_val.strip()
				elems = [v.strip() for v in line_val.split(COMMENT_START, 1)]
				elem = None
				if enable_region == "main":
					elem = elems[0]
				else:
					elem = elems[1]

				if is_continued_list_bullet:
					output_line_vals[-1] += " {0}".format(elem)
				else:
					output_line_vals.append(elem)
				is_continued_list_bullet = True

			else:
				output_line_vals.append(line_val)
				is_continued_list_bullet = False

	return [v if v.endswith("\n") else v + "\n" for v in output_line_vals]



# =============== main =============== #
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Program to convert papers in markdown format to each other", formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("TYPE", metavar="OPERATION", choices=["swap", "main", "comment"], help="operation type (`swap`, `main`, or `comment`)")
	parser.add_argument("INPUT_FILE", metavar="INPUT.md", help="source markdown paper file")
	parser.add_argument("OUTPUT_FILE", metavar="OUTPUT.md", nargs="?", help="output markdown paper file (Default: `-i`)")
	parser.add_argument("-O", dest="FLAG_OVERWRITE", action="store_true", default=False, help="overwrite forcibly")
	args = parser.parse_args()

	check_exist(args.INPUT_FILE, 2)

	output_file = args.INPUT_FILE
	if args.OUTPUT_FILE is not None:
		output_file = args.OUTPUT_FILE

	output_line_vals = []
	if args.TYPE == "swap":
		output_line_vals = swap_main_and_comment(args.INPUT_FILE)
	else:
		output_line_vals = formatting(args.INPUT_FILE, args.TYPE)


	if args.FLAG_OVERWRITE == False:
		check_overwrite(output_file)

	with open(output_file, "w") as obj_output:
		for line_val in output_line_vals:
			obj_output.write(line_val)
