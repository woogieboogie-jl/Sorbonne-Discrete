# -*- coding: utf-8 -*-
from transition import *
from state import *
import os
import copy
from itertools import product
from automateBase import AutomateBase



class Automate(AutomateBase):
        
    def succElem(self, state, lettre):
        """State x str -> list[State]
        rend la liste des états accessibles à partir d'un état
        state par l'étiquette lettre
        """
        successeurs = []
        # t: Transitions
        for t in self.getListTransitionsFrom(state):
            if t.etiquette == lettre and t.stateDest not in successeurs:
                successeurs.append(t.stateDest)
        return successeurs


    def succ (self, listStates, lettre):
        """list[State] x str -> list[State]
        rend la liste des états accessibles à partir de la liste d'états
        listStates par l'étiquette lettre
        """        
        successeurs = []
        for state in listStates:
            for t in self.getListTransitionsFrom(state):
                if t.etiquette == lettre and t.stateDest not in successeurs:
                    successeurs.append(t.stateDest)

        return successeurs

    """ Définition d'une fonction déterminant si un mot est accepté par un automate.
    Exemple :
            a=Automate.creationAutomate("monAutomate.txt")
            if Automate.accepte(a,"abc"):
                print "L'automate accepte le mot abc"
            else:
                print "L'automate n'accepte pas le mot abc"
    """

    @staticmethod
    def accepte(auto,mot) :
        """ Automate x str -> bool
        rend True si auto accepte mot, False sinon
        """
        # get the initial states
        state_list = auto.getListInitialStates()

        # initiate succession out of initial states
        for lettre in mot:
            state_list = auto.succ(state_list, lettre)

        # check if final any final state is in the state_list
        state_list_final = auto.getListFinalStates()        

        # check if any final state is in state list and return True if exists
        for state in state_list_final:
            if state in state_list:
                return True

        # else return False
        return False
        


    @staticmethod
    def estComplet(auto, alphabet) :
        """ Automate x str -> bool
         rend True si auto est complet pour alphabet, False sinon
        """
        # for every state, check if all alphabet transitions exist
        listStates = auto.listStates
        for state in listStates:

            # etiquette list of a state
            list_etiquette = [t.etiquette for t in auto.getListTransitionsFrom(state)]

            # check in set if list_etiquette has all the elements of alphabet
            if set(alphabet) != set(list_etiquette):
                return False
                
        # if all states passes the test, return True
        return True



        
    @staticmethod
    def estDeterministe(auto) :
        """ Automate  -> bool
        rend True si auto est déterministe, False sinon
        """
        
        # if there are more than two initial states, return False
        if len(auto.getListInitialStates()) != 1:
            return False

        # for every state, check if there is an overlap of alphabets
        for state in auto.listStates:

            # etiquette list of a state
            list_etiquette = [t.etiquette for t in auto.getListTransitionsFrom(state)]
            
            # check in set if list_etiquette and it's set has the same number of elements
            if len(list_etiquette) != len(set(list_etiquette)):
                return False
                
        # if all states passes the test, return True
        return True
        

       
    @staticmethod
    def completeAutomate(auto,alphabet) :
        """ Automate x str -> Automate
        rend l'automate complété d'auto, par rapport à alphabet
        """

        # deep copy automata
        copied_auto = copy.deepcopy(auto)

        # create a null state then add to the copied automata
        s_n = State(-1, False, False, "null")
        copied_auto.addState(s_n)

        # check each state if each alphabet exists in the etiquette list of the state. 
        # if not, add a new transition to null state
        for state in copied_auto.listStates:
            list_etiquette = [t.etiquette for t in copied_auto.getListTransitionsFrom(state)]
            for letter in alphabet:
                if letter not in list_etiquette:
                    copied_auto.addTransition(Transition(state, letter, s_n))
        return copied_auto

       
    @staticmethod
    def determinisation(auto) :
        """ Automate  -> Automate
        rend l'automate déterminisé d'auto
        """
            # check if automata is already deterministic or not
        if Automate.estDeterministe(auto) is True:
            return auto
        else:
            # initial state into state_index
            state_index = []
            state_index.append(set(auto.getListInitialStates()))

            # initial State / Transition declaration
            state_cnt = 0
            state_list = []
            trans_list = []
            alphabet_list = auto.getAlphabetFromTransitions()
            state_list.append(State(state_cnt,True,State.isFinalIn(state_index[0]),state_index[0]))

            # loop from each added state from state_index
            for idx, state_in in enumerate(state_index):
                for alphabet in alphabet_list:
                    state_out = set(auto.succ(state_in,alphabet))
                    if len(state_out) != 0:
                        if state_out in state_index:
                            idx_state = state_index.index(state_out)
                            new_trans = Transition(state_list[idx], alphabet, state_list[idx_state])
                            trans_list.append(new_trans)
                        else:
                            state_index.append(state_out)
                            state_cnt += 1
                            state_list.append(State(state_cnt,False,State.isFinalIn(state_out),state_index[state_cnt]))
                            trans_list.append(Transition(state_list[idx],alphabet,state_list[state_cnt]))

            return Automate(trans_list)
                       
        
        
    @staticmethod
    def complementaire(auto):
        """ Automate -> Automate
        rend  l'automate acceptant pour langage le complémentaire du langage de a
        """
        alphabet = auto.getAlphabetFromTransitions()
        new_auto = copy.deepcopy(auto)
        new_auto_c = Automate.completeAutomate(new_auto ,alphabet)
        new_auto_cd= Automate.determinisation(new_auto_c)
        
        for s in new_auto_cd.listStates:
                s.fin = False if s.fin is True else True
        return new_auto_cd                
   

    @staticmethod
    def intersection (auto0, auto1):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage l'intersection des langages des deux automates
        """
        state_cnt = 0
        state_init = (set(auto0.getListInitialStates()), set(auto1.getListInitialStates()))
        state_index = [state_init]
        
        state_list = [State(0, True, State.isFinalIn(state_init[0]) and State.isFinalIn(state_init[1], state_index[0]))]
        alphabet_list = set.intersection(set(list(auto0.getAlphabetFromTransitions())), set(list(auto1.getAlphabetFromTransitions())))
        trans_list = []

        for idx, state in enumerate(state_index):
                for alphabet in alphabet_list:
                        state_out = (set(auto0.succ(state[0],alphabet)) , set(auto1.succ(state[1],alphabet)))
                        if state_out in state_index:
                                idx_state = state_index.index(state_out)
                                new_trans = Transition(state_list[idx], alphabet, state_list[idx_state])
                                trans_list.append(new_trans)
                        else:
                                state_index.append(state_out)
                                state_cnt += 1
                                state_list.append(State(state_out,False,State.isFinalIn(state_out[0]) and State.isFinalIn(state_out[1]),state_index[state_cnt]))
                                new_trans = Transition(state_list[idx], alphabet, state_list[state_cnt])
                                trans_list.append(new_trans)

        return Automate(trans_list)
                

    @staticmethod
    def union (auto0, auto1):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage l'union des langages des deux automates
        """
        state_cnt = 0
        state_init = (set(auto0.getListInitialStates()), set(auto1.getListInitialStates()))
        state_index = [state_init]
        
        state_list = [State(0, True, State.isFinalIn(state_init[0]) or State.isFinalIn(state_init[1], state_index[0]))]
        alphabet_list = set.union(set(list(auto0.getAlphabetFromTransitions())), set(list(auto1.getAlphabetFromTransitions())))
        trans_list = []

        for idx, state in enumerate(state_index):
                for alphabet in alphabet_list:
                        state_out = (set(auto0.succ(state[0],alphabet)) , set(auto1.succ(state[1],alphabet)))
                        if state_out in state_index:
                                idx_state = state_index.index(state_out)
                                new_trans = Transition(state_list[idx], alphabet, state_list[idx_state])
                                trans_list.append(new_trans)
                        else:
                                state_index.append(state_out)
                                state_cnt += 1
                                state_list.append(State(state_out,False,State.isFinalIn(state_out[0]) or State.isFinalIn(state_out[1]),state_index[state_cnt]))
                                new_trans = Transition(state_list[idx], alphabet, state_list[state_cnt])
                                trans_list.append(new_trans)
                                
        return Automate(trans_list)
        

    @staticmethod
    def concatenation (auto1, auto2):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage la concaténation des langages des deux automates
        """
        return
        
       
    @staticmethod
    def etoile (auto):
        """ Automate  -> Automate
        rend l'automate acceptant pour langage l'étoile du langage de a
        """
        newAuto = copy.deepcopy(auto)
        
        currentList = []
        initialStates = auto.getListInitialStates()
        for l in auto.getAlphabetFromTransitions():
                for e in auto.listStates:
                        currentList = auto.succ(auto.listStates,l)
                        for s in currentList:
                                if e.fin == True:
                                        for si in initialStates:
                                                newAuto.addState(State(e,l,si))
        return newAuto  
                                                         




