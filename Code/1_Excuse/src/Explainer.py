#!/usr/bin/env python

'''
Topic   :: The driver Script for the Explanation generation
Project :: Explanations for Multi-Model Planning
Date    :: 
'''

SEARCH_OPTIONS = ["me", "mce"]

import argparse, sys
import re
import os
import subprocess
from PDDLhelp import *
from Problem import Problem
from PDDLhelp import *
from Search   import *
import copy
import time

def main():
    start_time = time.time()
    
    parser = argparse.ArgumentParser(description='''The driver Script for the Explanation generation''',
                                     epilog="Usage >> ./Explainer.py -m ../domain/fetchworld-tuck-m.pddl -n" +
                                            " ../domain/fetchworld-base-m.pddl -f ../domain/problem1.pddl ")

    # Flags for the search
    parser.add_argument('--approx',   action='store_true',
                        help="Enable use of approximation (currently only supported for ME).")
    parser.add_argument('--heuristic', action='store_true',
                        help="Enable use of heuristic (currently only supported for ME)")
    parser.add_argument('--ground', action='store_true',
                        help="Consider model difference in grounded domain model")

    # Search option
    parser.add_argument('-s', '--search', type=str, help="Search to be use (ME or MCE)")

    # Arguments for the explanation
    parser.add_argument('-m', '--model',   type=str, help="Domain file with real PDDL model of robot.", required=True)
    parser.add_argument('-n', '--nmodel',  type=str, help="Domain file with human model of the robot.", required=True)
    parser.add_argument('-t', '--tmodel', type=str, help="Domain file template for the problem.", required=True)
    parser.add_argument('-p', '--problem', type=str, help="Problem file for robot.", required=True)
    parser.add_argument('-q', '--hproblem', type=str, help="Problem file for human.")
    parser.add_argument('-r', '--tproblem', type=str, help="Problem file template.", required=True)
    parser.add_argument('-f', '--plan_file',    type=str, help="Plan file.")
    parser.add_argument('-l', '--label', type=str, help="Label for output files")
 

    if not sys.argv[1:] or '-h' in sys.argv[1:]:
        print (parser.print_help())
        sys.exit(1)
    args = parser.parse_args()


    if args.search.lower() not in SEARCH_OPTIONS:
        print("Unknown: Search option, please select either ME or MCE")
        sys.exit(1)


    # define problem object and run the required search
    pr_obj = Problem(args.model, args.nmodel, args.problem, args.tmodel,
     False, args.approx, args.heuristic,
     args.tproblem, args.hproblem, args.plan_file)

    if args.search.lower() == "me":
        plan = pr_obj.MeSearch()
    else:
        if args.approx and args.heuristic:
            print("MCE doesn't support heuristic or approx")
            exit(1)
        plan = pr_obj.MCESearch()
    solutions = pr_obj.solutions

    explanation= ''
    # for item in solutions:
    #     explanation += "Explanation >> {}\n".format(item)

    # #print(explanation.strip())
    # with open('exp.dat', 'w') as explanation_file:
    #     explanation_file.write(explanation.strip())

    solutions = pr_obj.solutions

    # Convert all items to string
    str_solutions = [str(item) for item in solutions]

    # Remove duplicates by converting to a set and back to a list
    unique_str_solutions = list(set(str_solutions))

    # Sort the list
    sorted_unique_str_solutions = sorted(unique_str_solutions)

    explanation= ''
    for item in sorted_unique_str_solutions:
        explanation += "Explanation >> {}\n".format(item)
    
    with open('explanations.dat', 'w') as explanation_file:
        explanation_file.write(explanation.strip())

    changes = pr_obj.previous_difference
    all_Original_Chnages= ''
    for item in changes:
        all_Original_Chnages += "Orig_changes >> {}\n".format(item)
    with open('Orig_changes.dat', 'w') as explanation_file:
        explanation_file.write(all_Original_Chnages.strip())
    # Convert all items to string
    str_changes = [str(item) for item in changes]
    # Remove duplicates by converting to a set and back to a list
    unique_str_changes = list(set(str_changes))

    label = args.label
    #changes_file_name = f"{label}_changes.dat"
    # Sort the list
    sorted_unique_str_changes = sorted(unique_str_changes)
    all_Chnages= ''
    for item in sorted_unique_str_changes:
        all_Chnages += "changes >> {}\n".format(item)
    with open(f"modified_changes_{label}.dat", 'w') as explanation_file: ##Change "modified" to "original" when running for modified.
        explanation_file.write(all_Chnages.strip())

    # for i, explanation in enumerate(solutions):
    #     new_domain_file_name = f"modified_domain_{i + 1}.pddl"
    #     new_problem_file_name = f"modified_problem_{i + 1}.pddl"
    #     new_domain_file, new_problem_file = write_domain_file_from_state(explanation, '../domain/Network/domain_template.pddl', '../domain/Network/prob_template.pddl')
    #     os.rename(new_domain_file, new_domain_file_name)
    #     os.rename(new_problem_file, new_problem_file_name)

    directory_name = "Solutions"

    # Check if the directory already exists, if not, create it
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

    for i, explanation in enumerate(solutions):
        new_domain_file_name = os.path.join(directory_name, f"modified_domain_{i + 1}.pddl")
        new_problem_file_name = os.path.join(directory_name, f"modified_problem_{i + 1}.pddl")

        # For Original File 
        new_domain_file, new_problem_file = write_domain_file_from_state(explanation, '../domain/All_Network/Original_Network/AdminServer/domain_template.pddl', '../domain/All_Network/Original_Network/AdminServer/prob_template.pddl')
        
        # For Modified File 
        # new_domain_file, new_problem_file = write_domain_file_from_state(explanation, '../domain/All_Network/Modified_Network/AdminServer/domain_template.pddl', '../domain/All_Network/Modified_Network/AdminServer/prob_template.pddl')
        
        os.rename(new_domain_file, new_domain_file_name)
        os.rename(new_problem_file, new_problem_file_name)

  
    
   # plan = 'plan.dat'
   # flag = validate_plan('FinalNetworkDomain.pddl', 'FinalNetworkProblem.pddl', plan)
   # print("So plan is : ", flag)ß
   

# Your script here

    end_time = time.time()
    execution_time = end_time - start_time

    print(f"Execution time: {execution_time} seconds")




if __name__ == '__main__':
    main()
