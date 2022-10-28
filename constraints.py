#!/usr/bin/env python3
import os

class Constraints:
	''' Class to generate all rules to be used for this graph

		** rule 1: each node gets at least one color
		** rule 2: no adjacent nodes may share a color
	'''
	def __init__(self,adj,index,cols,use_colors):
		self.adj = adj
		self.index = index
		self.cols = cols
		self.use_colors = use_colors
		self.all_rules = []
		self.atoms = set()

	def get_alphaname(self,x):
		# given an index of the adj matrix, return the alphaname
		# ex. 3rd row of adj means return "NSW"
		for k,v in self.index.items():
			if v==x:
				return str(k)

	def rule_1_at_least_one_color(self, x):
		''' Generates a single rule based on
				assigning the node at least one color

			** a node gets at least one color

			RETURNS:
				A SINGLE RULE
		'''
		rules = []
		alphaname = self.get_alphaname(x)
		# print("creating rule 1 for %s..." % alphaname)

		for color in self.use_colors:
			atom = alphaname + '_' + str(color)
			rules.append(atom)

			# also add it to the set of atoms
			if atom not in self.atoms:
				self.atoms.add(atom)

		rule_1 = ' '.join(rules)
		return rule_1


	def rule_2_adjacencies_no_share(self, x):
		''' Generates a list of rules based on
				the adjacent nodes

			** no two adjacent nodes share a color

			RETURNS:
				A LIST OF RULES
		'''
		rules = []

		primary_alphaname = self.get_alphaname(x)
		row = self.adj[x]

		for color in self.use_colors:
			# 1. FIRST HALF of the rule
			left_atom = primary_alphaname + '_' + str(color)

			if left_atom not in self.atoms:
				self.atoms.add(left_atom)

			left_rule = '!' + left_atom

			# 2. SECOND HALF of the rule
			# for any adjacency
			for adjacent_index in range(len(row)):

				adjacency = self.adj[x][adjacent_index]
				if adjacency > 0:

					# look up the alphaname of the adjacent node
					adjacent_alphaname = self.get_alphaname(adjacent_index)
					right_atom = adjacent_alphaname + '_' + str(color)

					if right_atom not in self.atoms:
						self.atoms.add(right_atom)

					right_rule = '!' + right_atom

					# 3. PUT BOTH HALVES TOGETHER
					rule = left_rule + ' ' + right_rule
					rules.append(rule)

		return rules


	def graph_constraints(self):
		'''		
		RETURNS: 
			A LIST OF ALL RULES 
		'''
		# print("starting constraints logic...")
		for x in range(len(self.cols)):

			# method to create rule #1
			rule_1 = self.rule_1_at_least_one_color(x)
			self.all_rules.append(rule_1)

			# method to create rule #2
			rules_2 = self.rule_2_adjacencies_no_share(x)
			for rule in rules_2:
				self.all_rules.append(rule)

		return self.all_rules, self.atoms


	def write_constraints(self, infilename):
		''' Writes CNF clauses to data/out directory
		'''
		infile = os.path.basename(str(infilename.name))
		curr_dir = os.getcwd()
		out_file = curr_dir + '/data/out/cnf_' + infile + '_out'

		# print("writing to file %s" % out_file)

		with open(out_file, "w") as f:
			for rule in self.all_rules:
				f.write(rule)
				f.write("\n")

		return out_file


