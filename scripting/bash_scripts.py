

# settingset up a folder structure
mkdir -p ~/programming/github/solo/{data-structures,algorithms,oop,design-patterns,cli-tools,scripting,apis,etl-pipelines,databases,testing,projects,my-website}
# git init in repo route dir
cd ~/code/solo
git init
touch README.md

# add README to each empty dir + .gitkeep file to any empty folders so git tracks them
touch ~/code/solo/algorithms/.gitkeep

# add a file to all folders in local dir
for dir in */; do touch "$dir.gitkeep"; done
    
# or more explicit — find instead of glob, skips the current dir, and works with folder names which have spaces.
find . -maxdepth 1 -type d ! -name '.' -exec touch {}/.gitkeep \;
