#!/bin/bash
PROJECT_DIR=~/reorganized_project

echo "Running pylint on the project..."
find $PROJECT_DIR -name "*.py" | xargs pylint

echo "Running black to check formatting..."
black $PROJECT_DIR --check

echo "Applying formatting fixes with black..."
black $PROJECT_DIR
