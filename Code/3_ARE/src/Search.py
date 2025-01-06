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


from Problem_excuse import Problem_excuse


'''
Method :: Astar Search
'''


#use this first to find explanations if yes then start excuse search
def astarSearch(problem):
    
    startState            = problem.getStartState()
    fringe                = PriorityQueue()
    closed                = set()
    numberOfNodesExpanded = 0

    fringe.put((problem.heuristic(startState), [startState, []]))

    print ("Runnning aStar Search...")

    exc_exp_found_flag = False

    # plan_list = []
    while not fringe.empty() and not exc_exp_found_flag:
        # print("HI")
        node = fringe.get()[1]

        goal_check, old_plan = problem.isGoal(node[0])
        if goal_check:
            # print ("Goal Found! Number of Nodes Expanded =", numberOfNodesExpanded, node[1])
            #problem.add_solution(node[1])
            # print("Len of solution list for explanation: ",len(problem.get_solution()))


            print(" Explanations: ")
            print(problem.previous_difference[-1])

            temp_domain, temp_problem = write_domain_file_from_state(node[0], problem.domainTemplate, problem.problemTemplate)            
            #I may need to change name of the files here
            #basically temp_domain is updated human model

            # print(temp_domain)

            new_file_name = "upd_human_domain.pddl"
            # Extract the directory from the original path
            directory = os.path.dirname(temp_domain)
            # Construct the new path with the same directory but a new file name
            new_human_model_path = os.path.join(directory, new_file_name)
            # Rename the original file to the new path
            os.rename(temp_domain, new_human_model_path)

            #Initial robot problem --static
            #Robot model --static
            #Combined problem file --static
            #human-plan --static
            #robot-plan --static


            model_robot = problem.robot_domain_file
            model_human = new_human_model_path

            # print(new_human_model_path)

            # input()

            problem_robot = problem.robot_problem_file
            hproblem = problem.human_problem_file

            problem_template = problem.problemTemplate
            domain_templete = problem.domainTemplate

            robot_plan_file = problem.robot_plan
            human_plan_file = problem.human_plan

            ground = None
            approx =None
            heuristic = None

            pr_obj_for_exc = Problem_excuse(model_robot, model_human, problem_robot, domain_templete,
            ground, approx, heuristic,
            problem_template, hproblem, robot_plan_file, human_plan_file)

            problem.excuse_list = pr_obj_for_exc.previous_difference

            exc_exp_found_flag = pr_obj_for_exc.MeSearch()


        if frozenset(node[0]) not in closed:

            closed.add(frozenset(node[0]))

            successor_list         = problem.getSuccessors(node, old_plan)
            # print("Len of successor list: ",len(successor_list))

            numberOfNodesExpanded += 1

            if not numberOfNodesExpanded % 1000:
                print ("Number of Nodes Expanded =", numberOfNodesExpanded)
            

            
            while successor_list:
                
                candidate_node     = successor_list.pop()
                new_node           = [candidate_node[0], node[1] + [candidate_node[1]]]
                
                fringe.put((problem.heuristic(candidate_node[0]) + len(new_node[1]), new_node))

    problem.final_node_number = numberOfNodesExpanded
    return numberOfNodesExpanded

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
