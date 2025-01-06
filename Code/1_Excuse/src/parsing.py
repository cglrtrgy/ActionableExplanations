import re
import ast
import os
import pddl
from pddl import parse_domain, parse_problem
from pddl import formatter
from collections import defaultdict
import random



def read_state_from_domain_file(domainFileName, problemFileName):
    problem = parse_problem(problemFileName)
    domain = parse_domain(domainFileName)
    state = []
    #Process domain name
    domain_name = domain.name
    state.append(f"domain-has-name-{''.join([str(l) for l in domain_name])}")
    # Process Problem Name
    problem_name = problem.name
    state.append(f"problem-has-name-{problem_name}")

    # Process objects
    for o in problem.objects:
        state.append(f"object-{o.name}-has-type-{o.type_tags}")

    # Process initial state to debug
    init = problem.init
    for pred in init:
        initpredname = pred.name
        for char in pred.terms:
            initpredconst = char
            state.append(f"init-{initpredname}-has-constants-{initpredconst}")
    
    # Process goal state to debug
    goal = str(problem.goal).strip("()").split(" ")
    goal[-1] += ")"
    goalpred = " ".join(goal)
    state.append(f"goal-has-{goalpred}")
    return state


def write_domain_file_from_state(state, domain_output_file, problem_output_file):
    init_state = []
    goal_state = []
    types =[]
    actnames = []
    actparams = []
    actprec = []
    acteff = []
    domain_name = ""
    problem_name = ""
    objects = []
    predicates = []
    requirements = []
    objects = []
    action_dict = {}
    nodes = int(input("Please enter a number of Nodes: "))
    each_node = nodes/5
    for item in state:
        key,value = item.split("has-",1)
        if "domain-" in key:
            domain_name = value.strip("name").strip("-")
        elif "problem-" in key:
            problem_name = value[5:]
        elif "types-" in key:
            for values in value:
                types.append(values)
            types = "".join(types)
        elif "object-" in key:
            octname = key.strip("object")
            octname = octname.strip("- -")
            octtype = value.strip("type")
            octtype = octtype.strip("-")
            if octtype == "set()":
                octtype = ""
            octtype = octtype.replace("'","").replace("{","").replace("}","")
            probobj = octname + " - " + octtype
            if probobj[-1] == "-":
                probobj = probobj.rstrip("-")
            objects.append(probobj)
       # elif "init-" in key:
        #    initpredname = key.strip("init")
       #     initpredname = initpredname.strip("- -")
        # #   initval = value.strip("constants")
       #     initval = initval.strip("- -")
        #    initpred = "(" + initpredname + " " + initval + ")"
       #     init_state.append(initpred)
        elif "init-" in key:
            initpredname = key[5:]  # removes 'init-' from the beginning
            if initpredname.endswith("-"):
                initpredname = initpredname.rstrip("-")  # removes trailing '-'
            initval = value.replace("constants-", "")  # removes 'constants-' from the beginning
            initpred = f"({initpredname} {initval})"
            init_state.append(initpred)


        elif "goal-" in key:
            goal_state = "(" + value + ")"

    #print(action_dict)
    problem_str = f"(define (problem {problem_name})\n"
    problem_str += f"(:domain {domain_name})\n"
    problem_str += f"(:objects \n"  
   # for object in objects:
    #   problem_str += f"{object}\n"
    # add more objects here
    #temp_object = ""
    #for i in range(1, 11):  # create 10 objects
    #    temp_object += f"ms-web-server{i} "

    #problem_str += f"{temp_object} - webserver\n"
    #problem_str += f")\n"
    # List to store all created web server names
    web_server_names = []
    objects_dict = defaultdict(list)
    for object in objects:
        object_name, object_type = object.split(" - ")
        objects_dict[object_type].append(object_name)
        
    for object_type, object_names in objects_dict.items():
        problem_str += " ".join(object_names) + " - " + object_type + "\n"

    # add more objects here
    for i in range(1, int(each_node) + 1):  # create 10 objects
        temp_object = f"Web-Server-{i}"
        objects_dict["webserver"].append(temp_object)
        web_server_names.append(temp_object)
    
    for object_type, object_names in objects_dict.items():
        if object_type == "webserver":
            problem_str += " ".join(object_names) + " - " + object_type + "\n"
    # Choose a random web server and add it to the init state
    random_web_server = random.choice(web_server_names)
    #init_state.append(f"(web-server {random_web_server})")


    # List to store all created SQL server names
    sql_server_names = []

    # Create your 10 SQL servers
    for i in range(1, int(each_node) + 1):  
        temp_object = f"Database-Server-{i}"
        objects_dict["sqlserver"].append(temp_object)
        sql_server_names.append(temp_object)
        init_state.append(f"(sql-server {temp_object})")

    for object_type, object_names in objects_dict.items():
        if object_type == "sqlserver":
            problem_str += " ".join(object_names) + " - " + object_type + "\n"

    # Choose a random SQL server and add it to the init state
    #random_sql_server = random.choice(sql_server_names)
    #init_state.append(f"(sql-server {random_sql_server})") 

    # List to store all created FTP server names
    # ftp_server_names = []

    # # Create your 10 FTP servers
    # for i in range(1, int(each_node) + 1):  
    #     temp_object = f"FTP-Server-{i}"
    #     objects_dict["ftpserver"].append(temp_object)
    #     ftp_server_names.append(temp_object)

    # for object_type, object_names in objects_dict.items():
    #     if object_type == "ftpserver":
    #         problem_str += " ".join(object_names) + " - " + object_type + "\n"

    # # Choose a random FTP server and add it to the init state
    # random_ftp_server = random.choice(ftp_server_names)
    # init_state.append(f"(ftp-server {random_ftp_server})") 
     # List to store all created Admin server names
    # admin_server_names = []

    # # Create your 10 Admin servers
    # for i in range(1, int(each_node) + 1):  
    #     temp_object = f"Admin-Server-{i}"
    #     objects_dict["adminserver"].append(temp_object)
    #     admin_server_names.append(temp_object)

    # for object_type, object_names in objects_dict.items():
    #     if object_type == "adminserver":
    #         problem_str += " ".join(object_names) + " - " + object_type + "\n"

    # # Choose a random Admin server and add it to the init state
    # random_admin_server = random.choice(admin_server_names)
    # init_state.append(f"(admin-server {random_admin_server})") 
    
     # List to store all created DNS server names

    # dns_server_names = []

    # # Create your 10 DNS servers
    # for i in range(1, int(each_node) + 1):  
    #     temp_object = f"DNS-Server-{i}"
    #     objects_dict["dnsserver"].append(temp_object)
    #     dns_server_names.append(temp_object)

    # for object_type, object_names in objects_dict.items():
    #     if object_type == "dnsserver":
    #         problem_str += " ".join(object_names) + " - " + object_type + "\n"

    # # Choose a random DNS server and add it to the init state
    # random_dns_server = random.choice(dns_server_names)
    # init_state.append(f"(dns-server {random_dns_server})") 

    for i in range(1, int(each_node) + 1):
         init_state.append(f"(has-connection-web-to-sql Web-Server-{i} Database-Server-{i})")
         init_state.append(f"(has-connection-sql-to-web Database-Server-{i} Web-Server-{i+1})") 

    #init_state.append(f"(has-connected {random_web_server} {random_sql_server} {random_admin_server} {random_ftp_server} {random_dns_server})") 

    problem_str += f")\n"

    count_ob = 0
    for object_type, object_names in objects_dict.items():
        count_ob += len(object_names)
    print("No.of Objects: ", count_ob)

    problem_str += f"(:init\n"
    for pred in init_state:
        problem_str += f"{pred}\n"
    problem_str += f")\n"

    problem_str += f"(:goal {goal_state})\n"
    #problem_str += ")\n"
    #problem_str += ")"

    with open(problem_output_file, "w") as problem_file:
        problem_file.write(problem_str)

state = read_state_from_domain_file("FinalNetworkDomain.pddl", "FinalNetworkProblem.pddl")
#print(state)
write_domain_file_from_state(state, "output_domain.pddl", "output_problem.pddl")

