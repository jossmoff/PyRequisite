#!/usr/bin/python
# -*- coding: UTF-8 -*-

import subprocess
from argparse import ArgumentParser, RawDescriptionHelpFormatter, FileType
import sys
from collections import OrderedDict
import time
import os
import re

module_name = "pyRequisite: Find library prerequisites for Python"
__version__ = "0.1.0"



def pip_search(library):
  output = subprocess.check_output(["pip ", "install", library],
                                    stderr=subprocess.PIPE)
  sys.stdout.write("Finding prerequisites for : " + library)
  sys.stdout.write(' [SEARCHING]')  # write the next character 
  text = str(output)
  libraries = []
  # Ignore first item from split as it will contain irrelevant data
  results = text.split(r"Requirement already satisfied: ")[1:]

  # Iterate over the results and then first word is the library we want
  for result in results:
    library = result.split(">=")[0]
    library = library.split(" in")[0]
    libraries.append(library)
  time.sleep(1)
  for i in range(11):
    sys.stdout.flush()
    sys.stdout.write('\b')
  sys.stdout.write(' [FINISHED]')
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

   

def main():

    # Get installed libraries
    installed_libraries = str(subprocess.check_output(["pip", "freeze"],
                                    stderr=subprocess.PIPE))
    
    # Turns the text from pip freeze into a list of all libraries
    installed_libraries = list(map(format_freeze, (installed_libraries[2:]
                                                   .split("\\r\\n"))))[:-1]
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
    args = parser.parse_args()
    
    # Person puts in a text file
    if args.file:
      with open(args.libraries) as f:
        libraries = f.read().splitlines()
        
    # Person puts in a directory to be searched
    elif args.directory:
      
      # Finds all .py files in a directory 
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
    if len(libraries) == 0:
      prereqs = "No prerequisites are needed for this input."
    else:
      prereqs = library_search(libraries, 0)
if __name__ == "__main__":
  main()
