#!/usr/bin/env python3
import sys
from sys import exit

class Solver:
	'''Class to run the DPLL solver for assignments
	'''
	def __init__(self,clauses,atoms,v_verbose=False):
		self.clauses = clauses
		self.atoms = atoms
		self.unassigned = set(atoms)
		self.order_assigned = []
		self.assignments = {}
		self.history = []
		self.verbose = v_verbose


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
		self._snapshot(assignment, type_of_assignment, S, V)

		new_clauses = []
		for clause in S:

			new_clause = []
			sentence = clause.split(' ')

			if assignment in sentence:
				# mark it as resolved, don't add it to new set of clauses
				continue 

			elif assignment.lstrip('!') in sentence:

				if len(sentence) > 1:
					s_sentence = set(sentence)
					s_assignment = set()

					positive_assignment = assignment.lstrip('!')
					s_assignment.add(positive_assignment)

					new_clause = s_sentence - s_assignment
					new_clause = ' '.join(list(new_clause))

				else:
					# print("left with the empty sentence, cannot resolve")
					new_clause = None
				
			# if assignment = T_RED and CNF contains !T_RED
			elif '!' + assignment in sentence:

				if len(sentence) > 1:
					s_sentence = set(sentence)
					s_assignment = set()

					negated_assignment = '!' + assignment
					s_assignment.add(negated_assignment)

					new_clause = s_sentence - s_assignment
					new_clause = ' '.join(list(new_clause))

				else:
					# print("left with the empty sentence, cannot resolve")
					new_clause = None

			else:
				new_clause = clause

			new_clauses.append(new_clause)
		
		S1 = new_clauses
		return S1


	def obvious_assign(self, atom, V):
		'''Assign atom as it appears in the sentence
		'''
		assignment = True
		stripped_atom_name = atom.lstrip('!')
		
		if atom in self.atoms:
			V[atom] = assignment

		elif stripped_atom_name in self.atoms:

			assignment = False
			V[stripped_atom_name] = assignment

		# print("E ASSIGN %s = %s" % (stripped_atom_name, assignment))
		return V


	def assign(self, atom: str, assignment: bool, V):
		'''Assign an atom given a boolean
		'''
		V[atom] = assignment
		return V


	def singleton(self, S):
		'''Returns a singleton (if there is one)
		'''
		for clause in S:

			sentence = clause.split(' ')
			if len(sentence) == 1:
				singleton = sentence[0]
				return singleton

		# otherwise length of sentence > 1 and this case returns False
		return False


	def _get_pure_literal(self, atom_states):
		'''Iterates through atom appearances
		'''
		for atom, appearances in atom_states.items():

			if len(appearances) > 1:
				continue

			pure_literal = min(appearances)
			# https://stackoverflow.com/questions/1619514/how-to-extract-the-member-from-single-member-set-in-python
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
				# print("Found the empty sentence!")
				return True
		return False


	def easy_case(self, S, logging=True):
		'''If there is a singleton, return it
			If there is a pure literal, return it
		''' 
		singleton = self.singleton(S)
		if singleton:
			if (self.verbose and logging):
				print("\tEasy case: singleton %s" % singleton)
			return singleton

		pure_literal = self.pure_literal(S)
		if pure_literal:

			if (self.verbose and logging):
				name = pure_literal.lstrip('!')
				if name == pure_literal:
					assignment = True
				else:
					assignment = False
				print("\tEasy case: pure literal %s=%s" % (name, assignment))

			return pure_literal

		return False


	def pick_hard_case_atom(self, V, index):
		'''Picks the smallest lexicographic atom in unbound
		'''
		unassigned_atoms = []
		for atom, assignment in V.items():

			if assignment is not None:
				continue
			else:
				unassigned_atoms.append(atom)

		unassigned_atoms = sorted(unassigned_atoms)
		guess = unassigned_atoms[index]

		return guess

	def backtrack(self):
		'''Backtracks to most recent hard case

		** Method of retaining "snapshots" of past sates used
			for backtracking is inspired by https://github.com/dizys/nyu-ai-lab-2/blob/main/solver
		'''
		if len(self.history)==0:
			# case when we have no where else to go
			return False

		while True:
			if len(self.history) == 0:
				return False

			past_step = self.history[-1]
			past_step_type = past_step['type_of_assignment']

			if past_step_type == 'easy_case':
				self.history.pop()
			else:
				# pop just once more
				step_just_before = self.history.pop()

				S = step_just_before['S']
				V = step_just_before['V']
				last_atom = step_just_before['propagated_atom']
				last_atom_bool = step_just_before['propagated_assignment']

				return last_atom, last_atom_bool, S,V


	def assign_unbound_atoms(self,V):
		'''Assigns any unbound atoms to False
		'''
		for atom, assignment in V.items():
			if not assignment:
				V[atom] = False
		return V


	def do_dpll(self):
		'''Handler for DPLL Resolution

			RETURNS: Valid atom assignments, or FAIL
		'''
		for a in self.atoms:
			self.assignments[a] = None

		final_assignments = self.dpll(self.clauses, self.assignments)
		return final_assignments


	def dpll(self, S, V):
		'''Main recursion
		'''
		while True:

			# SUCCESS: RETURN FINISH
			if self.is_finished(S):

				V = self.assign_unbound_atoms(V)
				return V

			# EMPTY SENTENCE: RETURN FAIL
			elif self.has_empty_sentence(S):
				
				return None
					
			# EASY CASES: PURE LITERAL ELIMINATION AND FORCED ASSIGNMENT
			elif self.easy_case(S,logging=False):

				atom_to_assign = self.easy_case(S)
				V = self.obvious_assign(atom_to_assign, V)
				S = self.propagate_assignment(atom_to_assign, 'easy_case', S, V)

			else:
				break

		#
		# HARD CASE: PICK ATOM AND TRY
		#
		atom_hard_case = self.pick_hard_case_atom(V,0)

		V = self.assign(atom_hard_case, True, V)
		if (self.verbose):
			print("\tHard case: guess %s=%s" % (atom_hard_case, True))

		S1 = S
		S1 = self.propagate_assignment(atom_hard_case, 'hard_case', S1, V)
		V_guess_true = self.dpll(S1,V)

		#
		# HARD CASE: GUESS FAILED
		#
		if not V_guess_true:

			prev_atom, prev_assignment, S_backtrack_1, V_backtrack_1 = self.backtrack()

			V_guess_false = self.assign(atom_hard_case, False, V)
			if (self.verbose):
				print("\tContradiction: backtrack guess %s=%s" % (atom_hard_case, False))

			S1 = self.propagate_assignment(atom_hard_case, 'retry', S, V_guess_false)
			V_guess_false = self.dpll(S1,V_guess_false)

			#
			# BACKTRACK
			#
			if not V_guess_false:

				prev_atom, prev_assignment, S_backtrack_1, V_backtrack_1 = self.backtrack()

				next_guess = False
				if not prev_assignment:
					next_guess = True

				V_backtracked = self.assign(prev_atom, next_guess, V_backtrack_1)
				if (self.verbose):
					print("\tContradiction: backtrack again guess %s=%s" % (prev_atom, next_guess))

				S1 = self.propagate_assignment(prev_atom, 'backtrack_retry', S_backtrack_1, V_backtracked)
				V_backtracked = self.dpll(S1,V_backtracked)

				if not V_backtracked:
					print("NO VALID ASSIGNMENT")
					exit(1)

			return self.dpll(S1,V_backtracked)

		else:
			# if (self.verbose):
			# 	print("\tSuccess!")
			return V_guess_true




































