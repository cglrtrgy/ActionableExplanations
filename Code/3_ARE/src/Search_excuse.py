#!/usr/bin/env python

'''
Topic   :: Search methods
Project :: Explanations for Multi-Model Planning
Author  :: XXXX
Date    :: 09/29/2016
'''

from queue import PriorityQueue, Queue
from PDDLhelp import *
import copy

'''
Method :: Astar Search
'''


#use this first to find explanations if yes then start excuse search
def astarSearch_excuse(problem):
    
    startState            = problem.getStartState()
    fringe                = PriorityQueue()
    closed                = set()
    numberOfNodesExpanded = 0

    fringe.put((problem.heuristic(startState), [startState, []]))

    print ("Runnning aStar Search...")


    exc_exp_found_flag = False

    # plan_list = []
    while not fringe.empty():
        
        node = fringe.get()[1]

        goal_check, old_plan, get_successor_flag = problem.isGoal(node[0])
        if goal_check:
            # print ("Goal Found! Number of Nodes Expanded =", numberOfNodesExpanded, node[1])
            #problem.add_solution(node[1])
            print("We have Exc+Exp ",len(problem.get_solution()))
            print(problem.previous_difference)

            exc_exp_found_flag = True

            ###Start excuse problem then search

            #dont return anything
            # return node[1]

            return numberOfNodesExpanded, exc_exp_found_flag

            #save the list
            # plan_list.append(node[1])
        #else:
        #    print "Goal not found for", node[1]

        if frozenset(node[0]) not in closed:

            closed.add(frozenset(node[0]))

            if get_successor_flag:

                successor_list         = problem.getSuccessors(node, old_plan)
                # print("Len of successor list: ",len(successor_list))

                numberOfNodesExpanded += 1

                if not numberOfNodesExpanded % 1000:
                    print ("Number of Nodes Expanded =", numberOfNodesExpanded)

            

            
            while successor_list:
                
                candidate_node     = successor_list.pop()
                new_node           = [candidate_node[0], node[1] + [candidate_node[1]]]
                
                fringe.put((problem.heuristic(candidate_node[0]) + len(new_node[1]), new_node))
        # if numberOfNodesExpanded == 10000:
        #     break
    #return the plan list
    # return plan_list
    problem.final_node_number = numberOfNodesExpanded
    return numberOfNodesExpanded, exc_exp_found_flag

def BFSearch(problem):

    startState            = problem.getStartState()
    fringe                = Queue()
    closed                = set()
    numberOfNodesExpanded = 0
    conflict_list = []
    current_sol = []

    fringe.put((problem.heuristic(startState), [startState, []]))

    print ("Runnning BFS...")
    while not fringe.empty():
        node = fringe.get()[1]
        goal_check, old_plan = problem.isGoal(node[0])
        if not goal_check:
            #print "Goal not Found! Number of Nodes Expanded =", numberOfNodesExpanded
            #print "Failed for path",node[1]
            conflict_list.append(set(node[1]))
        else:
            #print "It was fine"
            if frozenset(node[0]) not in closed:
                conflict_flag = False
                for item in conflict_list:
                    if item <= set(node[1]) and len(item) > 0:
                        conflict_flag = True
                if not conflict_flag:
                    current_sol = node[1]
                    closed.add(frozenset(node[0]))

                    successor_list         = problem.getSuccessors(node, old_plan)
                    numberOfNodesExpanded += 1
                    #print successor_list, node[1]
                    if not numberOfNodesExpanded % 100:
                        print ("Number of Nodes Expanded =", numberOfNodesExpanded)

                    while successor_list:

                        candidate_node     = successor_list.pop()
                        new_node           = [candidate_node[0], node[1] + [candidate_node[1]]]

                        fringe.put((problem.heuristic(candidate_node[0]) + len(new_node[1]), new_node))
    #print "curr", current_sol
                        
    
    return current_sol
