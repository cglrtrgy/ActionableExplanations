# Define the path of your PDDL file
file_path = '../domain/Network/FinalNetworkProblem.pddl'

# Initialize a flag to determine whether the current line is in the objects section
in_objects_section = False

# Initialize a counter for the number of objects
object_count = 0

# Open the file and read it line by line
try:
    with open(file_path, 'r') as file:
        for line in file:
            # If the line contains (:objects, set the flag to True
            if '(:objects' in line:
                in_objects_section = True
                
            # If the flag is True and the line contains ')', set the flag to False
            elif ')' in line and in_objects_section:
                in_objects_section = False
                
            # If the flag is True, count the objects in the current line
            if in_objects_section:
                # Split the line by spaces and count the number of words (objects)
                # Exclude words that are PDDL types (start with '-')
                objects = [word for word in line.split() if not word.startswith('-')]
                object_count += len(objects)

    print("Number of objects:", object_count)

except FileNotFoundError:
    print(f"The file at path {file_path} does not exist.")
except Exception as e:
    print(f"An error occurred: {e}")
