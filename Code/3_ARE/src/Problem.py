#!/usr/bin/env python

'''
Topic   :: Environment definition
Project :: Explanations for Multi-Model Planning
Author  :: XXXX
Date    :: 09/29/2016
'''

from PDDLhelp import *
from Search   import *
import copy

'''
Class :: Environment Definition
'''

def is_superset_of_any_solution(new_state, solution_list):
    # print(new_state)
    for sol in solution_list:
        if new_state >= sol:
            return True
    return False

def get_cost_from_plan(file_path):
    with open(file_path, 'r') as f:
        plan_len = 0
        for line in f:
            # Check if the line starts with ';'
            if line.strip().startswith(';'):
                break
            plan_len += 1
    return plan_len

class Problem:

    def __init__(self, robotModelFile, humanModelFile, robotProblemFile, domainTemplate,
                 ground_flag, approx_flag, heuristic_flag,
                 problemTemplate, humanProblemFile, robot_plan_file, human_plan_file):

        print ("Setting up MMP...")

        if humanProblemFile == None:
            humanProblemFile = robotProblemFile

        self.human_problem_file = humanProblemFile
        self.robot_problem_file = robotProblemFile

        self.robot_domain_file = robotModelFile

        #new list
        self.solutions = []
        self.previous_difference = []
        

        self.domainTemplate = domainTemplate
        self.problemTemplate = problemTemplate
        self.approx_flag = approx_flag
        self.heuristic_flag = heuristic_flag
        self.ground_flag = ground_flag

        self.k_plan_list = []
        
        self.final_node_number = 0

        self.robot_plan = robot_plan_file
        self.robot_plan_cost = get_cost_from_plan(robot_plan_file)


        self.human_plan = human_plan_file
        self.human_plan_cost = get_cost_from_plan(human_plan_file)


        #else:
        self.robot_state = read_state_from_domain_file(robotModelFile, robotProblemFile)
        self.human_state = read_state_from_domain_file(humanModelFile, humanProblemFile)
        #temp_plan, temp_cost = get_plan(humanModelFile, humanProblemFile)

 
        create_temp_files(humanModelFile, humanProblemFile)
        self.groundedHumanPlanFile = '../../domain/cache_human_grounded_plan.dat'
        grounded_human_plan, self.human_grounded_plan_cost = get_plan('tr-domain.pddl', 'tr-problem.pddl')
        self.grounded_human_plan =  set([i for i in grounded_human_plan])

        self.excuse_list = []
    
    def add_solution(self, new_solution):
        self.solutions.append(new_solution)
    
    def get_solution(self):
        return self.solutions
    
    
    def MeSearch(self):
        self.initialState = copy.copy(self.human_state)
        self.goalState = copy.copy(self.robot_state)
        plan = astarSearch(self)
        #print(self.initialState)
        return plan

    def MCESearch(self):

        self.initialState = copy.copy(self.robot_state)
        self.goalState = copy.copy(self.human_state)
        k_plan = BFSearch(self)
        #(set(k_plan))
        return list(((set(self.initialState) - set(self.human_state))| (set(self.human_state) - set(self.initialState)))
                    - set(k_plan))

    def getStartState(self):
        return self.initialState

    def isGoal(self, state):
        if self.approx_flag:
            return self.approx_isGoal(state)
        return self.orig_isGoal(state)


    def orig_isGoal(self, state):
        # if is_superset_of_any_solution(set(state)-set(self.human_state), self.previous_difference):
        #     return (False, [])
        temp_domain, temp_problem = write_domain_file_from_state(state, self.domainTemplate, self.problemTemplate)
        

        #first check if robot plan file is valid in updated HUman model
         #I am not using temp_problem because it is excuse, after this step we'll use it
        #first check if explanation makes sense
        feasibility_flag_for_explanation = validate_plan(temp_domain, self.human_problem_file, self.robot_plan)
        
        optimality_flag = False
        optimality_flag_for_exp = False
        plan = []
        optimality_flag_for_exc_and_exp_to_human = False
        if feasibility_flag_for_explanation:
            # print("feasibility_flag: ", feasibility_flag)

            #get new plan for updated huuman model to see if it is optimal
            #I am not using temp_problem because it is excuse, after this step we'll use it
            plan, cost       = get_plan(temp_domain, self.human_problem_file)
            # print("feasibility_flag_for_explanation costs: " )
            # print(self.robot_plan_cost, cost)

            optimality_flag_for_exp  = cost == self.robot_plan_cost

            #Explanations are good, now checck excuses 
            if optimality_flag_for_exp == True and feasibility_flag_for_explanation == True:
                self.add_solution(set(state))
                self.previous_difference.append(set(state)-set(self.human_state) )




        return (optimality_flag_for_exp, plan)

    def approx_isGoal(self, state):
        temp_domain, temp_problem = write_domain_file_from_state(state,  self.domainTemplate, self.problemTemplate)

        if not validate_plan(temp_domain, temp_problem, self.groundedRobotPlanFile):
            #fail_pos = find_fail_point(temp_domain, temp_problem, self.groundedRobotPlanFile)
            return (False, list(self.plan)) #[ : min(fail_pos + 1 ,len(self.grounded_robot_plan) ) ])

        if self.human_grounded_plan_cost > 0 and self.human_grounded_plan_cost <= self.cost and \
                validate_plan(temp_domain, temp_problem, self.groundedHumanPlanFile):
            return (False, self.plan)

        graph_test_result = plan_graph_test(temp_domain, temp_problem, self.groundedRobotPlanFile)
        return (graph_test_result, self.plan)
    
    def heuristic(self, state):
        return 0.0

    
    def getSuccessors(self, node, old_plan = None):
        if self.heuristic_flag:
            return self.heuristic_successors(node, old_plan)
        return self.ordinary_successors(node)
    
    

    def ordinary_successors(self, node):


        #helper function


        listOfSuccessors = []

        state            = set(node[0])
        ground_state     = set(copy.copy(self.goalState))

        add_set          = ground_state.difference(state)
        del_set          = state.difference(ground_state)

        #we need only the model/domain changes here so ignore xcuses/initial changes for now
        
        add_set = {item for item in add_set if not item.startswith('has-initial-state')}

        # print("add and del sets: ")
        # print(add_set)
        # print(del_set)

        # input()

    #690 -38 
        for item in add_set:
            new_state    = copy.deepcopy(state)
            new_state.add(item)

            # if not is_superset_of_any_solution(new_state, self.solutions):
            listOfSuccessors.append([list(new_state), item])

            # print("New State:", new_state)
            # listOfSuccessors.append([list(new_state), item])
            # if not any(set(new_state).issuperset(s) for s in solution_list):
            #     listOfSuccessors.append([list(new_state), item])
            #     # print("NNoooooooooooooooot SUPERSET")

        for item in del_set:
            new_state    = copy.deepcopy(state)
            new_state.remove(item)

            # if not is_superset_of_any_solution(new_state, self.solutions):
            listOfSuccessors.append([list(new_state), item])
            # # listOfSuccessors.append([list(new_state), item])
            # if not any(set(new_state).issuperset(s) for s in solution_list):
            #     listOfSuccessors.append([list(new_state), item])
            
        return listOfSuccessors


    def heuristic_successors(self, node, old_plan):
        listOfSuccessors = []

        state = set(node[0])
        ground_state = set(self.robot_state)

        all_relevent_actions = set([i.lower().split()[0] for i in old_plan]) | set(
        [j.lower().split()[0] for j in self.plan])

        add_set = ground_state.difference(state)
        del_set = state.difference(ground_state)

        for item in add_set:
            if item.split('-has-')[0].lower() in all_relevent_actions:
                new_state = copy.deepcopy(state)
                new_state.add(item)
                listOfSuccessors.append([list(new_state), item])

        for item in del_set:
            if item.split('-has-')[0] in all_relevent_actions:
                new_state = copy.deepcopy(state)
                new_state.remove(item)
                listOfSuccessors.append([list(new_state), item])

        return listOfSuccessors
    
    def heuristic_calculation(self, temp_domain, temp_problem, plan_list):

        original_directory = os.getcwd()
        temp_domain = original_directory+"/"+temp_domain
        temp_problem = original_directory+"/"+temp_problem

        # print(temp_domain)
        # print(temp_problem)
        # print(plan_list)

        init_plan_list = plan_list
        h = len(plan_list)

        for a_plan in init_plan_list:
            feasibility_flag = validate_plan(temp_domain, temp_problem, a_plan)
            if not feasibility_flag:
                # print("Feas flag: ", feasibility_flag)
                h -= 1
        heuristic_value = h/len(plan_list)

        

        return heuristic_value


    def get_k_plan_list(self, domain_path, problem_path, top_k):
        # Save the current working directory
        original_directory = os.getcwd()

        # print("domain_path", domain_path)

        domain_full_path = original_directory + "/" + domain_path
        problem_full_path = original_directory + "/" + problem_path

        # Define the script name and working directory
        script_name = "plan_topk.sh"
        working_directory = "/Users/xxxx/Documents/forbiditerative/forbiditerative-main"
        plans_directory = os.path.join(working_directory, "found_plans", "done")

        # print("domain_full_path",domain_full_path)
        # Combine the command and arguments into a single string
        command = f"./{script_name} {domain_full_path} {problem_full_path} {top_k}"

        # Change the current working directory to where the script is located
        os.chdir(working_directory)

        # Run the command
        status = os.system(command)

        # Check if the command was executed successfully
        if status == 0:
            # print("Script executed successfully!")
            a=1
        else:
            # print("Error in script execution")
            # Return to the original working directory before exiting
            os.chdir(original_directory)
            return []

        # List all files starting with "sas_" in the specified directory and create full paths
        plan_files = [os.path.join(plans_directory, file) for file in os.listdir(plans_directory) if file.startswith("sas_")]



        # Return to the original working directory
        os.chdir(original_directory)

        # Return the sorted list of full paths to the plan files
        return plan_files


