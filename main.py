#!/usr/bin/env python3
import sys, getopt
import argparse

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



def parse_input(lines):
	''' Go through the file initially
			save names and values of things etc.
	'''
	lines = [line.rstrip('\n') for line in lines]

	for line in lines:
		# we know it is a list of child nodes
		data = line.split(':')

		# 1. save the name of the node
		node_name = data[0].strip(' ')
		if node_name not in nodes_list:
			nodes_list.append(node_name)

		# 2. add the children of this to the node_adjacency_mappings
		children = data[1].lstrip()
		children = children.strip('[] ').split(', ')

		node_adjacency_mappings[node_name] = children

		# check to also add leaf nodes
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

	print("adjacency matrix before:")
	for a in adj:
		print("\t", end="")
		print(a)

	for from_node, to_list in node_adjacency_mappings.items():
		index_num_row = index[from_node]
		# print("ROW -- %s: %s" % (from_node, index_num_row))

		if to_list is None:
			continue
		else:
			for to_node in to_list:

				index_num_col = index[to_node]
				adj[index_num_row][index_num_col] +=1


				# DONT KNOW IF I WANT THIS RIGHT NOW.
				# # if you want to make the graph symmetric:
				# print("%s ->> %s" % (from_node,to_node))
				# index_num_row_rev = index[to_node]
				# index_num_column_rev = index[from_node]
				# adj[index_num_row_rev][index_num_column_rev] +=1




	print("adjacency matrix:")
	for a in adj:
		print("\t", end="")
		print(a)

	return adj, index, num, cols


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


	# First, parse the input graph file
	nodes_list, node_adjacency_mappings = parse_input(lines)

	# create the adjacency matrix
	build_adjacency(nodes_list, node_adjacency_mappings)

	# tree_node = setup.build_tree(nodes_list, leaf_values, node_adjacency_mappings)


	# tree = game_setup(lines)
	# # Second, play the game
	# game_play(tree, role)





