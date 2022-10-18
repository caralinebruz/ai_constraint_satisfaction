#!/usr/bin/env python3
import os
import sys, getopt
import argparse
from enum import Enum

import pprint
from pprint import pprint

''' This takes an input graph file and a maximum number of colors to use
	and solves the colormap problem such that no adjacent nodes can share
	the same color

	USAGE: ./main.py [-v] $ncolors $input-file
'''

num_colors = ""
nodes_list = []
node_adjacency_mappings = {}

ColorMap = {
	1 : 'RED',
	2 : 'GREEN',
	3 : 'BLUE',
	4 : 'YELLOW',
}



def get_colors(num_colors):

	use_colors = []
	for x in range(num_colors):

		x = x+1
		use_colors.append(ColorMap[x])

	return use_colors



def parse_input(lines):
	''' Go through the file initially
			save names and values of things etc.
	'''
	lines = [line.rstrip('\n') for line in lines]

	for line in lines:
		if ":" in line:

			print(line)
			# we know it is a list of child nodes
			data = line.split(':')

			# 1. save the name of the node
			node_name = data[0].strip(' ')
			if node_name not in nodes_list:
				nodes_list.append(node_name)

			# 2. add the children of this to the node_adjacency_mappings
			children = data[1].lstrip()
			children = children.replace(' ','')
			children = children.strip('[] ').split(',')
			print(children)

			# https://pythonexamples.org/check-if-all-strings-in-python-list-are-not-empty
			# true if all the strings are non-empty
			if all(children):
				node_adjacency_mappings[node_name] = children

				for i in children:
					if i not in nodes_list:
						nodes_list.append(i)


	print("names of all nodes in the graph:")
	print(nodes_list)
	print("node-adjacency-mappings:")
	pprint(node_adjacency_mappings)

	return nodes_list, node_adjacency_mappings


def build_adjacency(nodes_list, node_adjacency_mappings):
	''' Create the adjacency matrix
	'''
	print("creating adj matrix ...")
	cols = nodes_list
	cols.sort()
	print(cols)
		# now they are in ascending order

	num = len(cols)
	index = {}

	i = 0
	for node_name in cols:
		index[node_name] = i
		i = i + 1

	adj = [[0 for col in range(num)] for row in range(num)]

	# print("adjacency matrix before:")
	# for a in adj:
	# 	print("\t", end="")
	# 	print(a)

	for from_node, to_list in node_adjacency_mappings.items():
		index_num_row = index[from_node]
		# print("ROW -- %s: %s" % (from_node, index_num_row))

		if to_list is None:
			continue
		else:
			for to_node in to_list:

				index_num_col = index[to_node]
				adj[index_num_row][index_num_col] +=1

				# make the adj matrix symmetric:
				print("%s ->> %s" % (from_node,to_node))
				index_num_row_rev = index[to_node]
				index_num_column_rev = index[from_node]
				adj[index_num_row_rev][index_num_column_rev] +=1

	print("index:")
	for k,v in index.items():
		print("\t%s:%s" % (k,v))

	print("adjacency matrix:")
	for a in adj:
		print("\t", end="")
		print(a)

	return adj, index, num, cols


def get_alphaname(x,index):
	# given an index of the adj matrix, return the alphaname
	# ex. 3rd row of adj means return "NSW"
	for k,v in index.items():
		if v==x:
			return str(k)


def rule_1_at_least_one_color(x, index, use_colors):
	''' Generates a single rule based on
			assigning the node at least one color

		** a node gets at least one color

		RETURNS:
			A SINGLE RULE
	'''
	rules = []
	alphaname = get_alphaname(x, index)
	print("creating rule 1 for %s..." % alphaname)

	for color in use_colors:
		atom = alphaname + '_' + str(color)
		rules.append(atom)

	rule_1 = ' '.join(rules)
	return rule_1


def rule_2_adjacencies_no_share(x, adj, index, use_colors):
	''' Generates a list of rules based on
			the adjacent nodes

		** no two adjacent nodes share a color

		RETURNS:
			A LIST OF RULES
	'''
	print("creating rule 2...")
	rules = []

	primary_alphaname = get_alphaname(x, index)
	row = adj[x]

	for color in use_colors:
		# 1. FIRST HALF of the rule
		left_rule = '!' + primary_alphaname + '_' + str(color)

		# 2. SECOND HALF of the rule
		# for any adjacency
		for adjacent_index in range(len(row)):

			adjacency = adj[x][adjacent_index]
			if adjacency > 0:

				# look up the alphaname of the adjacent node
				adjacent_alphaname = get_alphaname(adjacent_index, index)
				right_rule = '!' + adjacent_alphaname + '_' + str(color)

				# 3. PUT BOTH HALVES TOGETHER
				rule = left_rule + ' ' + right_rule
				rules.append(rule)

	return rules


def write_constraints(rules, infilename):
	''' Writes CNF clauses to data/out directory
	'''
	infile = os.path.basename(str(infilename.name))
	curr_dir = os.getcwd()
	out_file = curr_dir + '/data/out/cnf_' + infile + '_out'

	print("writing to file %s" % out_file)

	with open(out_file, "w") as f:
		for rule in rules:
			f.write(rule)
			f.write("\n")

	return out_file

def graph_constraints(adj,index,cols,use_colors):
	''' Generates all rules to be used for this graph

		** rule 1: each node gets at least one color
		** rule 2: no adjacent nodes may share a color

		RETURNS: 
			A LIST OF ALL RULES 
	'''
	print("starting constraints logic...")
	all_rules = []

	for x in range(len(cols)):

		# method to create rule #1
		rule_1 = rule_1_at_least_one_color(x, index, use_colors)
		all_rules.append(rule_1)

		# method to create rule #2
		rules_2 = rule_2_adjacencies_no_share(x, adj, index, use_colors)
		for rule in rules_2:
			all_rules.append(rule)

	return all_rules



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
		num_colors = int(args.num_colors[0])
	if args.graph_file:
		lines = args.graph_file.readlines()
		infile = args.graph_file

	# 0, get the colors to be used in this graph
	use_colors = get_colors(num_colors)
	print("using colors for map:")
	print(use_colors)


	# First, parse the input graph file
	# graph = parseInput(filename)
	nodes_list, node_adjacency_mappings = parse_input(lines)

	# create the adjacency matrix
	adj, index, num, cols = build_adjacency(nodes_list, node_adjacency_mappings)

	# Second, generate CNF clauses
	clauses = graph_constraints(adj,index,cols,use_colors)
	out_filename = write_constraints(clauses, infile)

	# for clause in clauses:
	# 	print(clause)






