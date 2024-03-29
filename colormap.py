#!/usr/bin/env python3
import os
import sys, getopt
import argparse
from enum import Enum

import pprint
from pprint import pprint

import parse
from parse import parse_input, build_adjacency

import constraints
from constraints import Constraints

import solver
from solver import Solver


''' This takes an input graph file and a maximum number of colors to use
	and solves the colormap problem such that no adjacent nodes can share
	the same color

	USAGE: ./colormap.py [-v] $ncolors $input-file
'''

v_verbose = False
num_colors = ""

ColorMap = {
	1 : 'RED',
	2 : 'GREEN',
	3 : 'BLUE',
	4 : 'YELLOW',
}


def get_colors(num_colors):
	'''Returns a list of colors to be used
	'''
	use_colors = []
	for x in range(num_colors):

		x = x+1
		use_colors.append(ColorMap[x])

	return use_colors


def convert_back(atoms,assignments):
	'''Converts the assignments back to a readable solution
	'''
	solution = {}

	for atom, assignment in assignments.items():
		if not assignment:
			continue

		true_thing = atom.split('_')
		name = true_thing[0]
		color = true_thing[1]

		if name not in solution.keys():
			solution[name] = color

	return solution


def map_coloring_via_dpll(infile, lines):
	'''Main program execution
	'''

	# Get the names of the colors to be used
	use_colors = get_colors(num_colors)

	#
	# FIRST, parse the input graph file
	#
	nodes_list, node_adjacency_mappings = parse.parse_input(lines)
	adj, index, num, cols = parse.build_adjacency(nodes_list, node_adjacency_mappings)

	#
	# SECOND, generate CNF clauses
	#
	C = Constraints(adj,index,cols,use_colors)
	clauses, atoms = C.graph_constraints()
	C.write_constraints(infile)

	# convert to list rather than set for now
	atoms = list(atoms)
	atoms.sort()

	#
	# THIRD, do DPLL solver
	#
	S = Solver(clauses, atoms, v_verbose)
	assignments = S.do_dpll()

	if not assignments:
		print("NO VALID ASSIGNMENT")
		exit(1)

	#
	# FOURTH, convert assignments back to something meaningful
	#
	solution = convert_back(atoms, assignments)

	#
	# PRINT SOLUTION
	#
	for vertex, color in solution.items():
		print("%s = %s" % (vertex,color))


if __name__ == '__main__':
	# USAGE: ./colormap.py -v 2 data/input/tiny.txt

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
	# print(args)

	if args.v:
		v_verbose = True
	if args.num_colors:
		num_colors = int(args.num_colors[0])
	if args.graph_file:
		lines = args.graph_file.readlines()
		infile = args.graph_file


	map_coloring_via_dpll(infile, lines)







