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
           list_transition = []
           done = []
           set_done = set()
           list_init = auto.getListInitialStates()
           set_init = set(list_init)
           list_fin = auto.getListFinalStates()
           set_fin = set(list_fin)
           to_do = [set_init]
           alphabet = auto.getAlphabetFromTransitions()
           compteur = 0
           while(len(to_do)>0):     # Cover the listInitialStates
                states = to_do.pop()
                set_states = set(states)
                for a in alphabet:
                        next = auto.succ(states,a) # getting states by label
                        if(next == []):
                                break
                        else:
                                set_next=set(next)
                                if(set_states == set_init):
                                        init = True
                                else:
                                        init = False
                                if(set_states.isdisjoint(set_fin)):
                                        fin = False
                                else:
                                        fin = True
                                if(set_next == set_init):
                                        init_n = True
                                else:
                                        init_n = False
                                if (set_next.isdisjoint(set_fin)):
                                        fin_n=False
                                else:
                                        fin_n = True
                                s_states = State(compteur,init,fin,set_states)
                                compteur+=1
                                s_next = State(compteur,init_n,fin_n,set_next)
                                compteur+=1
                                for t in list_transition:
                                        if (t.stateSrc.label == set_states):  # from a label we get initial states
                                                s_states = t.statesSrc
                                        if (t.stateDest.label == set.states):
                                                s_states = t.stateDest        # from a label we get initial states
                                        if (t.stateSrc.label == set_next()):
                                                s_next = t.stateSrc
                                                
                                        if (t.stateDest.label == set_next()):
                                                s_next = t.stateDest
                                transitions = Transition(s_state,a,s_next)  
                                list_transition.append(transitions)
                                if(set_next not in to_do) and (set_next not in done):
                                        to_do.append(set_next)
                         
                                                
           return auto                   
                        
                       
        
        
        
        
    @staticmethod
    def complementaire(auto,alphabet):
        """ Automate -> Automate
        rend  l'automate acceptant pour langage le complémentaire du langage de a
        """
        newAuto = copy.deepcopy(auto)
        newAuto = newAuto.completeAutomate(newAuto)
        newAuto = newAuto.determinisation(newAuto)
        
        for a in newAuto.listStates:
                if s.fin == True:
                        s.fin = False
                else:
                        s.fin = True
        return newAuto                
   
    @staticmethod
    def intersection (auto0, auto1):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage l'intersection des langages des deux automates
        """
        return

    @staticmethod
    def union (auto0, auto1):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage l'union des langages des deux automates
        """
        return
        

   
       

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
        return




