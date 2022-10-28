#!/usr/bin/env python3
import os
import sys, getopt
import argparse
from enum import Enum

import pprint
from pprint import pprint


nodes_list = []
node_adjacency_mappings = {}

def parse_input(lines):
	''' Go through the file initially
			save names and values of things etc.
	'''
	lines = [line.rstrip('\n') for line in lines]

	for line in lines:
		if ":" in line:
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

			# https://pythonexamples.org/check-if-all-strings-in-python-list-are-not-empty
			# true if all the strings are non-empty
			if all(children):
				node_adjacency_mappings[node_name] = children

				for i in children:
					if i not in nodes_list:
						nodes_list.append(i)


	# print("names of all nodes in the graph:")
	# print(nodes_list)
	# print("node-adjacency-mappings:")
	# pprint(node_adjacency_mappings)

	return nodes_list, node_adjacency_mappings


def build_adjacency(nodes_list, node_adjacency_mappings):
	''' Create the adjacency matrix
	'''
	# print("creating adj matrix ...")
	cols = nodes_list
	cols.sort()
	num = len(cols)
	index = {}

	i = 0
	for node_name in cols:
		index[node_name] = i
		i = i + 1

	adj = [[0 for col in range(num)] for row in range(num)]


	for from_node, to_list in node_adjacency_mappings.items():
		index_num_row = index[from_node]

		if to_list is None:
			continue
		else:
			for to_node in to_list:

				index_num_col = index[to_node]
				adj[index_num_row][index_num_col] +=1

				# make the adj matrix symmetric:
				# print("%s ->> %s" % (from_node,to_node))

				index_num_row_rev = index[to_node]
				index_num_column_rev = index[from_node]
				adj[index_num_row_rev][index_num_column_rev] +=1

	# print("adjacency matrix:")
	# for a in adj:
	# 	print("\t", end="")
	# 	print(a)

	return adj, index, num, cols
