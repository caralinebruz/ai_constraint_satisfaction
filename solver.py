#!/usr/bin/env python3
import sys
from sys import exit

class Solver:
	'''Class to run the DPLL solver for assignments
	'''
	def __init__(self,clauses,atoms):
		self.clauses = clauses
		self.atoms = atoms
		self.unassigned = set(atoms)
		self.order_assigned = []
		self.assignments = {}
		self.history = []  # will contain V, S


	def is_finished(self, S):
		'''Check if there are any clauses left
		'''
		if len(S) < 1:
			return True
		return False


	# def mark_atom_assigned(self, atom):
	# 	print("current unassigned: ")
	# 	print(self.unassigned)

	# 	self.unassigned.remove(atom)
	# 	self.order_assigned.append(atom)

	# 	print("current unassigned: ")
	# 	print(self.unassigned)



	def _snapshot(self, assignment, type_of_assignment, S, V):
		'''Saves the current assignment AND resolved propagated sentences
		'''
		atom = assignment.lstrip('!')
		this_iteration = {
							'S': S, 
							'V': V,
							'propagated_atom': atom,
							'propagated_assignment': V[atom],
							'type_of_assignment': type_of_assignment
							}
		self.history.append(this_iteration)


	def propagate_assignment(self, assignment, type_of_assignment, S, V):
		'''Propagates the assignment to the clauses

		Assignment is in:
			!T_RED 
			T_RED
		'''
		print("snapshotting before propagating assignment ....")
		self._snapshot(assignment, type_of_assignment, S, V)



		print("\nPROPAGATING ASSIGNMENT: ")
		new_clauses = []
		# for clause in self.clauses:
		for clause in S:

			print("old clause: %s" % clause)

			# prepare to write new sentences
			new_clause = []

			# if the clause contains the assignment, 
			sentence = clause.split(' ')

			# if assignment = !T_RED and CNF contains !T_RED
			#		or if assignment = T_RED and CNF contains T_RED
			if assignment in sentence:
				print("1: Resolving entire line, satisfied: %s" % clause)
				# mark it as resolved, don't add it to new set of clauses
				continue 

			# if assignment = !T_RED and CNF contains T_RED
			elif assignment.lstrip('!') in sentence:
				# shorten the sentence if len > 1
				print("2")
				if len(sentence) > 1:
					# shorten it
					s_sentence = set(sentence)

					s_assignment = set()
					positive_assignment = assignment.lstrip('!')
					s_assignment.add(positive_assignment)

					new_clause = s_sentence - s_assignment
					print("sentence:%s, assignment:%s new_clause:%s" % (s_sentence, s_assignment, new_clause))

					new_clause = ' '.join(list(new_clause))

				else:
					# sentence cannot be resolved, the empty sentence
					print("left with the empty sentence, cannot resolve")
					new_clause = None
				

			# if assignment = T_RED and CNF contains !T_RED
			elif '!' + assignment in sentence:
				# shorten the sentence if len > 1
				print("3")
				if len(sentence) > 1:
					# shorten it
					s_sentence = set(sentence)

					s_assignment = set()
					negated_assignment = '!' + assignment
					s_assignment.add(negated_assignment)

					new_clause = s_sentence - s_assignment

					print("sentence:%s, assignment:%s new_clause:%s" % (s_sentence, s_assignment, new_clause))

					new_clause = ' '.join(list(new_clause))

				else:
					# sentence cannot be resolved, the empty sentence
					print("left with the empty sentence, cannot resolve")
					new_clause = None

			else:
				new_clause = clause

			# add it to the new set of clauses
			new_clauses.append(new_clause)


		print("new set of clauses:")
		print(new_clauses)

		
		S1 = new_clauses
		print("\nDONE PROPAGATING ASSIGNMENT\n\n")


		
		return S1



	def obvious_assign(self, atom, V):
		'''Assign atom as it appears in the sentence
		'''
		name = atom

		if atom in self.atoms:
			V[atom] = True

		elif atom.lstrip('!') in self.atoms:
			V[atom] = False
			name = atom.lstrip('!')

		return V


	def assign(self, atom: str, assignment: bool, V):
		'''Assign an atom given a boolean
		'''
		V[atom] = assignment
		# self.mark_atom_assigned(atom)
		return V


	def singleton(self, S):
		'''Returns a singleton (if there is one)
		'''
		for clause in S:

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


	def pure_literal(self, S):
		'''Returns a pure literal (if there is one)
			Creates a dictionary of sets
			{
				1_RED : {!1_RED, 1_RED},
				1_BLUE : {!1_BLUE},
			}
		'''
		atom_states = {}
		for clause in S:

			sentence = clause.split(' ')
			for word in sentence:
				base_word = word.lstrip('!')

				if base_word not in atom_states.keys():
					atom_states[base_word] = set()
					atom_states[base_word].add(word)

				if word not in atom_states[base_word]:
					atom_states[base_word].add(word)

		a_pure_literal = self._get_pure_literal(atom_states)
		return a_pure_literal


	def has_empty_sentence(self, S):
		'''Check for the empty sentence
		'''
		for clause in S:
			if clause is None:
				print("Found the empty sentence!")
				return True
		return False


	def easy_case(self, S):
		'''If there is a singleton, return it
			If there is a pure literal, return it
			 Otherwise return false
		''' 
		singleton = self.singleton(S)
		if singleton:
			return singleton

		pure_literal = self.pure_literal(S)
		if pure_literal:
			return pure_literal

		return False


	def pick_hard_case_atom(self, V, index):
		'''Picks the smallest lexicographic atom in unbound
		'''
		print("picking a hard case")

		unassigned_atoms = []
		for atom, assignment in V.items():
			print("%s:%s" % (atom, assignment))
			if assignment is not None:
				continue
			else:
				unassigned_atoms.append(atom)


		print(unassigned_atoms)
		unassigned_atoms = sorted(unassigned_atoms)

		guess = unassigned_atoms[index]
		print("guess %s = True" % guess)

		return guess

	def backtrack(self):
		'''Backtracks to most recent hard case

		** Method of retaining "snapshots" of past sates used
			for backtracking is inspired by https://github.com/dizys/nyu-ai-lab-2/blob/main/solver
		'''
		if len(self.history)==0:
			print("weird case, handle later")

		while True:
			if len(self.history) == 0:
				print("reached the end of the line, handle this case.")
				return False

			past_step = self.history[-1]
			past_step_type = past_step['type_of_assignment']

			if past_step_type == 'easy_case':
				print("popping easy case..")
				print("\t backtrack assignment of %s = %s" % (past_step['propagated_atom'],past_step['propagated_assignment']))
				self.history.pop()
			else:
				print("returning last hard case guess S and V (and the atom that was tried)...")
				S = past_step['S']
				V = past_step['V']
				last_guessed_atom = past_step['propagated_atom']
				last_guessed_atom_bool = past_step['propagated_assignment']


				return last_guessed_atom, last_guessed_atom_bool, S,V

			print("while True still going...")
			# return False


	def do_dpll(self):

		# initially, set all atoms to False
		for a in self.atoms:
			self.assignments[a] = None
		print(self.assignments)

		# unassigned = self.atoms
		self.dpll(self.clauses, self.assignments)



	def dpll(self, S, V):

		x=0
		# Loop as long as there are easy cases to cherry pick
		while True:

			# easy_case = self.easy_case()
			print("x=%s" % x)

			# BASE OF THE RECURSION: SUCCESS OR FAILURE
			if self.is_finished(S):

				# assign any unbound atoms
				# return the assignments (TRANSFORMED)
				print("success, assign unbound, convert back, return colors")
				# for a in self.atoms:
				# 	if self.assignments[a] == None:

				# 		# change it to true to check my work later.
				# 		# in the lab doc he says "For default assignments, use False"
				# 		# default assignments are set to False
				# 		print("assigning unbound atom: %s" % a)
				# 		self.assignments[a] = False

				return V
				# FINISH STEPS
				# transform assignments
				# return transformed assignments

			elif self.has_empty_sentence(S):
				# some clause is unsatisfiable under current assignments
				print("some sentence is unsatisfiable under current assignments.. returning FAIL")

				prev_snapshot = self.history[-1]
				print("failed on assignment:")
				print(prev_snapshot['propagated_atom'])
				print(prev_snapshot['propagated_assignment'])

				# take a look at the failed assignment, and try the other way



				
				return False
					

			# EASY CASES: PURE LITERAL ELIMINATION AND FORCED ASSIGNMENT
			elif self.easy_case(S):
				atom_to_assign = self.easy_case(S)
				# obvious assign
				V = self.obvious_assign(atom_to_assign, V)
				# propagate
				print("\nEASY CASE: assign %s" % atom_to_assign)
				print("propagating assignment: %s" % atom_to_assign)
				S = self.propagate_assignment(atom_to_assign, 'easy_case', S, V)
				

			else:
				# no easy cases, break out of this.
				break
	
			if x==20:
				return
				exit()

			x+=1


		# otherwise go to hard case
		# HARD CASE: PICK SOME ATOM AND TRY EACH ASSIGNMENT IN TURN

		# pick the smallest lexicographic atom in unbound
		atom_hard_case = self.pick_hard_case_atom(V,0)

		print("\nHARD CASE: assign %s = %s" % (atom_hard_case, True))
		V = self.assign(atom_hard_case, True, V)

		S1 = S
		S1 = self.propagate_assignment(atom_hard_case, 'hard_case', S1, V)

		# call DPLL again
		V_NEW = self.dpll(S1,V)

		

		# if it returned with the empty sentence, try hard case = False
		if not V_NEW:

			print("you failed with hard case=True guess, try assign False instead...")

			print("\nHARD CASE: assign %s = %s" % (atom_hard_case, False))
			V = self.assign(atom_hard_case, False, V)
			S1 = self.propagate_assignment(atom_hard_case, 'hard_case', S, V)


			V_NEW_2 = self.dpll(S1,V)
			if not V_NEW_2:

				print("now you actually need to backtrack.")



				# prev_snapshot = self.history[-1]
				# print(prev_snapshot['propagated_assignment'])


				# prev_prev_snapshot = self.history[-2]
				# print(prev_prev_snapshot['propagated_assignment'])


				# prev_prev_prev_snapshot = self.history[-3]
				# print(prev_prev_prev_snapshot['propagated_assignment'])


				guessed_atom, guessed_assignment, S_backtrack, V_backtrack = self.backtrack()
				print("backtracked to state when guessed %s = %s" % (guessed_atom, guessed_assignment))



			# # if that still doesnt work, need to backtrack previous atom
			# return dpll(S1,V)
				exit(1)


		else:
			print("found a satisfying condition, now what?")
			return V_NEW




































