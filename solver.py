#!/usr/bin/env python3

class Solver:
	'''Class to run the DPLL solver for assignments
	'''
	def __init__(self,clauses,atoms):
		self.clauses = clauses
		self.atoms = atoms
		self.unassigned = set(atoms)
		self.assignments = {}
		self.past_steps = []


	# def is_finished(self):
	# 	if len(self.unassigned) < 1:
	# 		return True
	# 	return False

	def is_finished(self):
		'''Check if there are any clauses left
		'''
		if len(self.clauses) < 1:
			return True
		return False


	def mark_atom_assigned(self, atom):
		self.unassigned.remove(atom)


	def obvious_assign(self, atom):
		'''Assign atom as it appears in the sentence
		'''
		name = atom

		if atom in self.atoms:
			self.assignments[atom] = True

		elif atom.lstrip('!') in self.atoms:
			self.assignments[atom] = False
			name = atom.lstrip('!')

		self.mark_atom_assigned(name)



	def singleton(self):
		'''Returns a singleton (if there is one)
		'''
		for clause in self.clauses:

			sentence = clause.split(' ')
			if len(sentence) == 1:
				singleton = sentence[0]
				print("found a singleton: %s" % singleton)

				return singleton

			if len(sentence) == 0:
				print("err nothing in the sentence")

		# otherwise length of sentence > 1 and this case returns False
		return False



	def _get_pure_literal(self, atom_states):
		'''Iterates through atom appearances
			Returns first available pure literal
			 or returns false if there isnt one.
		'''
		for atom, appearances in atom_states.items():

			if len(appearances) > 1:
				continue

			pure_literal = min(appearances)
			print("actually found a pure literal: %s" % pure_literal)
			#https://stackoverflow.com/questions/1619514/how-to-extract-the-member-from-single-member-set-in-python
			return pure_literal

		return False



	def pure_literal(self):
		'''Returns a pure literal (if there is one)
			Creates a dictionary of sets
			{
				1_RED : {!1_RED, 1_RED},
				1_BLUE : {!1_BLUE},
			}
		'''
		atom_states = {}
		for clause in self.clauses:

			sentence = clause.split(' ')
			for word in sentence:
				base_word = word.lstrip('!')

				if base_word not in atom_states.keys():
					atom_states[base_word] = set()
					atom_states[base_word].add(word)


				# otherwise baseword is already in the dict.
				# if word is not in corresponding set for the atom
				# add it.
				if word not in atom_states[base_word]:
					# print("adding word to the atom's set of appearances")
					atom_states[base_word].add(word)

		a_pure_literal = self._get_pure_literal(atom_states)
		return a_pure_literal



	def has_empty_sentence(self):
		'''Check for the empty sentence
		'''
		for clause in self.clauses:
			if clause is None:
				print("Found the empty sentence, need to backtrack.")
				return True
		return False


	def easy_case(self):
		'''If there is a singleton, return it
			If there is a pure literal, return it
			 Otherwise return false
		''' 
		singleton = self.singleton()
		if singleton:
			return singleton

		pure_literal = self.pure_literal()
		if pure_literal:
			return pure_literal

		return False



	def do_dpll(self):

		print(self.atoms)
		for c in self.clauses:
			print(c)

		# initially, set all atoms to False
		for a in self.atoms:
			self.assignments[a] = False
		print(self.assignments)


		x=0
		while x<3:

			# easy_case = self.easy_case()

			# BASE OF THE RECURSION: SUCCESS OR FAILURE
			#if not self.is_finished():
			if self.is_finished():

				# assign any unbound atoms
				# return the assignments (TRANSFORMED)
				print("success, assign unbound, convert back, return colors")
				for a in self.atoms:
					if self.assignments[a] == False:

						# change it to true to check my work later.
						print("assigning unbound atom: %s" % a)
						self.assignments[a] = True

				# FINISH STEPS
				# transform assignments
				# return transformed assignments

			elif self.has_empty_sentence():
				# some clause is unsatisfiable under current assignments
				print("some sentence is unsatisfiable under current assignments:")
				print(self.assignments)
				print(self.clauses)
				return False
					

			# EASY CASES: PURE LITERAL ELIMINATION AND FORCED ASSIGNMENT
			elif self.easy_case():
				obvious_assign(self.easy_case())
				
			x+=1




































