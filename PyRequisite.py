#!/usr/bin/python
# -*- coding: UTF-8 -*-

import subprocess
from argparse import ArgumentParser, RawDescriptionHelpFormatter, FileType
import sys
from collections import OrderedDict
import time
import os
import re

module_name = "PyRequisite: Find library prerequisites for Python"
__version__ = "0.2.0"



def pip_search(library):
  output = subprocess.check_output(["pip3", "install", library],
                                    stderr=subprocess.PIPE)
  sys.stdout.write('🔎 Finding prerequisites for : ' + library)
  sys.stdout.write(' ⏱️')  # write the next character 
  sys.stdout.flush()
  time.sleep(1)
  text = str(output)

  # Ignore first item from split as it will contain irrelevant data
  libraries = text.split(r'Installing collected packages: ')[1].split('\\n')[0].split(', ')
  # Iterate over the results and then first word is the library we want
  sys.stdout.flush()
  sys.stdout.write('\b')
  sys.stdout.write('✔️')
  print()
  return libraries
  
def library_search(libraries, index):
  new_libraries = pip_search(libraries[index])
  new_libraries = list(OrderedDict.fromkeys(libraries + new_libraries))
  if (index + 1) != len(new_libraries):
    index +=1
    new_libraries = list(OrderedDict.fromkeys(libraries
                                              + library_search(new_libraries,
                                                                index)))
  
  return new_libraries

# Searches directory for python files ~ Needs optimizing
def file_search(path):
  result = []
  for root, dirs, files in os.walk(path):
    for name in files:
      if ".py" in name and ".pyc" not in name:
        result.append(os.path.join(root, name))
  return result

def scan_for_libraries(file):
  with open(file) as f:
    file_text = f.read()
    from_import_libraries = re.findall("from \w*", file_text)
    import_libraries = re.findall("import \w*", file_text)

    for index in range(len(from_import_libraries)):
      from_import_libraries[index] = (from_import_libraries[index]
                                      .replace("from ", ""))

    for index in range(len(import_libraries)):
      import_libraries[index] = (import_libraries[index]
                                 .replace("import ", ""))
    libraries = list(OrderedDict.fromkeys(from_import_libraries
                                          + import_libraries))
    return libraries

def format_freeze(string):
  replaced = re.sub(r'==.*', '', string)
  return replaced.lower()

def print_prereqs(prereqs, project):
  if project != "":
    print(project + "'s Prerequisites:")
  else:
    print("Prerequisites:")
  if type(prereqs) is str:
    print("  No prerequisites are needed for this input set.")
  for prereq in prereqs:
    print(" > " + prereq)
  
   

def main():
  # Get installed libraries
  installed_libraries = str(subprocess.check_output(["pip3", "freeze"],
                                  stderr=subprocess.PIPE))

  # Turns the text from pip freeze into a list of all libraries
  installed_libraries = list(map(format_freeze, (installed_libraries[2:].split("\\n"))))[:-1]
  parser = ArgumentParser(description=module_name)
  parser.add_argument('-f','--file',
                      action="store_true", dest="file", default=False,
                      help="Specifies whethers libraries is a file.")
  parser.add_argument('-d','--directory',
                      action="store_true", dest="directory", default=False,
                      help="""Specifies whethers libraries is a directory
                              to be searched.""")
  parser.add_argument(type=str, dest='libraries',
                      help="The set of top-level libraries in your project")
  parser.add_argument('-o','--output', dest="output", default=False,
                      help="""Specifies whethers should be redirected to a file.""")
  
  args = parser.parse_args()
  
  project = ""
  # Person puts in a text file
  if args.file:
    with open(args.libraries) as f:
      libraries = f.read().splitlines()
      
  # Person puts in a directory to be searched
  elif args.directory:
    # Finds all .py files in a directory 
    project = os.path.abspath(args.libraries).split('/')[-1]
    files = file_search(args.libraries)
    found_libraries = []
    for file in files:
      found_libraries = list(OrderedDict.fromkeys(found_libraries
                                                  + scan_for_libraries(file)))
    libraries = []
    # Does the intersection of found libraries and installed libraries
    for library in found_libraries:
      if library in installed_libraries:
        libraries.append(library)        
  else:
    libraries = args.libraries.split(",")

  # Make sure all inputted libraries are actually installed
  for library in libraries:
    if library.lower() not in installed_libraries:
      raise Exception("Library: " + library + " is not installed.")
  
  if len(libraries) != 0:

    # Searches for all libraries
    prereqs = library_search(libraries, 0)
    if len(prereqs) == 0:
      print("Prerequisites")
      print("No prerequisites are needed for this input set.")
    elif args.output:
      with open(args.output, 'w') as f:
        for prereq in prereqs:
          f.write(prereq + "\n")
    print_prereqs(prereqs, project)    
if __name__ == "__main__":
  main()
