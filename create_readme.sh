#!/bin/bash

# Function to create README.md in each directory
create_readme() {
  for dir in "$1"/*; do
    if [ -d "$dir" ]; then
      readme_path="$dir/README.md"
      if [ ! -f "$readme_path" ]; then
        echo "Creating $readme_path"
        echo "# $(basename "$dir")" > "$readme_path"
      fi
      create_readme "$dir"
    fi
  done
}

# Start from the current directory
create_readme .