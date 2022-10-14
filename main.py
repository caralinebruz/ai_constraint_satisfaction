#!/usr/bin/env python3
import sys, getopt
import argparse


''' This takes an input graph file and a maximum number of colors to use
	and solves the colormap problem such that no adjacent nodes can share
	the same color

	USAGE: ./main.py [-v] $ncolors $input-file
'''

num_colors = ""




if __name__ == '__main__':
	# USAGE: ./main.py -v 2 data/input/tiny.txt

	#
	# PARSE COMMAND LINE 
	#

	infile = "" # graph file
	lines = []

	parser = argparse.ArgumentParser(description='Colormap parser')
	parser.add_argument('-v', action='store_true', help="verbose flag")
	parser.add_argument('num_colors',type=int, nargs=1)
	parser.add_argument('graph_file', type=argparse.FileType('r'))

	args = parser.parse_args()
	print(args)

	if args.v:
		v_verbose = True
	if args.num_colors:
		num_colors = args.num_colors
	if args.graph_file:
		lines = args.graph_file.readlines()
		infile = args.graph_file


	# # First, set up the game
	# tree = game_setup(lines)
	# # Second, play the game
	# game_play(tree, role)





