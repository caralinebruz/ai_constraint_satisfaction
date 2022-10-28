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


		print("\nPROPAGATING ASSIGNMENT: %s ; %s" % (assignment, type_of_assignment))
		new_clauses = []
		# for clause in self.clauses:
		for clause in S:

			# print("old clause: %s" % clause)

			# prepare to write new sentences
			new_clause = []

			# if the clause contains the assignment, 
			sentence = clause.split(' ')

			# if assignment = !T_RED and CNF contains !T_RED
			#		or if assignment = T_RED and CNF contains T_RED
			if assignment in sentence:
				# print("1: Resolving entire line, satisfied: %s" % clause)
				# mark it as resolved, don't add it to new set of clauses
				continue 

			# if assignment = !T_RED and CNF contains T_RED
			elif assignment.lstrip('!') in sentence:
				# shorten the sentence if len > 1
				# print("2")
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
				# print("3")
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
		assignment = True

		# for k,v in V.items():
		# 	print("%s:%s" % (k,v))

		stripped_atom_name = atom.lstrip('!')

		if atom in self.atoms:
			V[atom] = assignment

		elif stripped_atom_name in self.atoms:

			assignment = False
			V[stripped_atom_name] = assignment


		print("E ASSIGN %s = %s" % (stripped_atom_name, assignment))

		return V


	def assign(self, atom: str, assignment: bool, V):
		'''Assign an atom given a boolean
		'''
		print("H ASSIGN %s = %s" % (atom, assignment))
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


	def backtrack_once(self):
		'''Only back up one more atom assignment (since full backtrack)
		'''
		if len(self.history)==0:
			print("weird case, handle later")

		# past_step = self.history[-1]
		past_step = self.history.pop()

		S = past_step['S']
		V = past_step['V']
		last_atom = past_step['propagated_atom']
		last_atom_bool = past_step['propagated_assignment']


		# for atom, assignment in V.items():
		# 	print("%s:%s" % (atom, assignment))

		return last_atom, last_atom_bool, S,V



	def do_dpll(self):

		# initially, set all atoms to False
		for a in self.atoms:
			self.assignments[a] = None
		print(self.assignments)

		# unassigned = self.atoms
		final_assignments = self.dpll(self.clauses, self.assignments)

		return final_assignments



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

				print(V)
				return V
				# FINISH STEPS
				# transform assignments
				# return transformed assignments

			elif self.has_empty_sentence(S):
				# some clause is unsatisfiable under current assignments
				print("some sentence is unsatisfiable under current assignments.. returning FAIL")

				return None
					

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

		print("\n1.HARD CASE: assign %s = %s" % (atom_hard_case, True))
		V = self.assign(atom_hard_case, True, V)

		S1 = S
		S1 = self.propagate_assignment(atom_hard_case, 'hard_case', S1, V)

		# this may return None or False
		V_guess_true = self.dpll(S1,V)

		# if it returned with the empty sentence, try hard case = False
		if not V_guess_true:

			print("2.you failed with last picking %s = %s, try assign False instead..." % (atom_hard_case, True))

			guessed_atom, guessed_assignment, S_backtrack, V_backtrack = self.backtrack()
			print("2. backtracked to state when guessed %s = %s" % (guessed_atom, guessed_assignment))
			prev_atom, prev_assignment, S_backtrack_1, V_backtrack_1 = self.backtrack_once()

			print("\n2. HARD CASE: assign %s = %s" % (atom_hard_case, False))
			V_guess_false = self.assign(atom_hard_case, False, V)
			S1 = self.propagate_assignment(atom_hard_case, 'retry', S, V_guess_false)


			# this may return None or False
			V_guess_false = self.dpll(S1,V_guess_false)

			if not V_guess_false:
				print("now you actually need to backtrack.")


				guessed_atom, guessed_assignment, S_backtrack, V_backtrack = self.backtrack()
				print("backtracked to state when guessed %s = %s" % (guessed_atom, guessed_assignment))

				# actually need to backtrack one more, and then try the opposite assignment
				prev_atom, prev_assignment, S_backtrack_1, V_backtrack_1 = self.backtrack_once()

				print("now try the other assignemnt")
				next_guess = False
				if not guessed_assignment:
					next_guess = True

				print("\nBACKTRACKED CASE: assign %s = %s" % (prev_atom, next_guess))

				V_backtracked = self.assign(prev_atom, next_guess, V_backtrack_1)
				S1 = self.propagate_assignment(prev_atom, 'backtrack_retry', S_backtrack_1, V_backtracked)

				# this may return none or false
				V_backtracked = self.dpll(S1,V_backtracked)

				if not V_backtracked:
					print("backtrack didnt work, do i do it again?")


				y=0
				while not V_backtracked:
					print("backtrack didnt work loop: %s, do i do it again?" % y)
					if y==20:
						exit(1)

					# # actually need to backtrack one more, and then try the opposite assignment
					# prev_atom, prev_assignment, S_backtrack_2, V_backtrack_2 = self.backtrack_twice()

					guessed_atom, guessed_assignment, S_backtrack, V_backtrack = self.backtrack()
					print("2::backtracked to state when guessed %s = %s" % (guessed_atom, guessed_assignment))
					# actually need to backtrack one more, and then try the opposite assignment
					prev_atom, prev_assignment, S_backtrack_1, V_backtrack_1 = self.backtrack_once()

					print("now try the other assignemnt")
					next_guess = False
					if not guessed_assignment:
						next_guess = True

					print("\nBACKTRACKED TWICE CASE: assign %s = %s" % (prev_atom, next_guess))
					V_backtracked = self.assign(prev_atom, next_guess, V_backtrack_1)
					S1 = self.propagate_assignment(prev_atom, 'backtrack_retry', S_backtrack_1, V_backtracked)

					# this may return none or false
					V_backtracked = self.dpll(S1,V_backtracked)
					y+=1


					print("assigned order:")
					for i in self.history:
						print("%s = %s (%s)" % (i['propagated_atom'], i['propagated_assignment'], i['type_of_assignment']))



			# # if that still doesnt work, need to backtrack previous atom
			return self.dpll(S1,V_backtracked)
				# exit(1)


		else:
			print("found a satisfying condition, now what?")
			return V_guess_true




































