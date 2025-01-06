#!/bin/bash

# Default directory
DIRECTORY="../domain/Network"

# Parse command-line options
while getopts "d:" opt; do
  case $opt in
    d) DIRECTORY=$OPTARG;;
    \?) echo "Invalid option -$OPTARG" >&2; exit 1;;
  esac
done

# Extract the last directory name as a label
LABEL=$(basename "$DIRECTORY")

# Running the Python Explainer script with the specified directory and label
python Explainer.py \
  -s ME \
  -m "$DIRECTORY/UnSolvableDomain.pddl" \
  -n "$DIRECTORY/FinalNetworkDomain.pddl" \
  -t "$DIRECTORY/domain_template.pddl" \
  -p "$DIRECTORY/UnSolvableProblem.pddl" \
  -q "$DIRECTORY/FinalNetworkProblem.pddl" \
  -r "$DIRECTORY/prob_template.pddl" \
  -l "$LABEL"
