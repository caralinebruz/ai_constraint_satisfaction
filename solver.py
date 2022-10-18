#!/usr/bin/env python3

class Solver:
	''' Class to run the DPLL solver for assignments
	'''
	def __init__(self,clauses,atoms):
		self.clauses = clauses
		self.assignments = []
		self.atoms = atoms


	def do_dpll(self):

		print(self.atoms)
