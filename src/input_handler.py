
import glob
import os
import time
import shutil as su
import sys

# Get list of files matching search 
def find_matching_files(search_dict):
    file_list=[]
    for search in search_dict:
        file_list += glob.glob(gs.base_dir + gs.sl + search)
    return file_list   

# Delete matching files
def clean_matching_files(file_list):
    tally=0
    for f in file_list:
        try:
            os.remove(f)
            tally +=1
        except:
            print("Error cleaning the file", f)
    return tally

# Clean up temp files such as logs
def clean_temp_files():
    print("Cleaning up temp files...")
    search_dict = ['*.out*',
                   '*.err*',
                   '*.log',
                   'tmp.*'
                  ]

    file_list = find_matching_files(search_dict)

    if file_list:
        print("Found the following files to delete:")
        for f in file_list:
            print(f)

        print("Proceeding in", gs.timeout, "seconds...")
        time.sleep(gs.timeout)
        print("No going back now...")
        deleted = clean_matching_files(file_list)
        print("Done, ", str(deleted), " files successfuly cleaned.")

    else:
        print("No temp files found.")

# Detele application and module matching path provided
def remove_app(code_str):
    if code_str.count('/') < 4:
        print("Your application selection '"+code_str+"' could be ambiguous.")
        print("Please provide the application path in the form: [system]/[compiler]/[mpi]/[code]/[arch]")
        print("HINT: rerun with '--installed' to get valid build paths for all installed applications.")
        sys.exit(1)

    code_dict = code_str.split('/')

    top_dir = gs.base_dir
    if not code_dict[0] == "build":
       top_dir += gs.sl + "build"

    # Get module dir from app dir, by adding 'modulefiles' prefix and stripping [version] suffix
    mod_dir = top_dir + gs.sl + "modulefiles" + gs.sl + gs.sl.join(code_dict[:-1])
    app_dir = top_dir + gs.sl + code_str

    print("Removing application installed in "+app_dir)
    print("Proceeding in", gs.timeout, "seconds...")
    time.sleep(gs.timeout)
    print("No going back now...")

    # Delete application dir
    try:
        su.rmtree(app_dir)
        print("")
        print("Application removed.")
    except:
        print("Warning: Failed to remove application directory "+app_dir)
        print("Skipping")

    print()
    # Detele module dir
    try:
        su.rmtree(mod_dir)
        print("Module removed.")
    except:
        print("Warning: no associated module located in "+mod_dir)
        print("Skipping")

# Get all sub directories 
def get_subdirs(base):
    return [name for name in os.listdir(base)
        if os.path.isdir(os.path.join(base, name))]

# Recurse down tree 5 levels to get full applciation installation path
def recurse_down(app_dir, start_depth, current_depth, max_depth):
    for d in get_subdirs(app_dir):
        if d != 'modulefiles':
            new_dir = app_dir + gs.sl + d
            if current_depth == max_depth:
                print("    "+gs.sl.join(new_dir.split(gs.sl)[start_depth+1:]))
            else:
                recurse_down(new_dir, start_depth, current_depth+1, max_depth)

# Print currently installed apps, used together with 'remove' 
def show_installed():
    print("Currently installed applications:")
    print("---------------------------------")
    app_dir = gs.base_dir + gs.sl + "build" 
    start = app_dir.count(gs.sl)
    recurse_down(app_dir, start, start, start+5)

# Print applications that can be installed from available cfg files 
def show_available():
    print("Available application profiles:")
    print("---------------------------------")
    app_dir = gs.base_dir + gs.sl + "config" + gs.sl + "build" + gs.sl
    temp_files = glob.glob(app_dir+"*.cfg")    
    for f in temp_files:
        code = f.split('/')[-1]
        if "_build" in code:
            print("    "+code[:-10])
        else:
            print("    "+code[:-4])


class init(object):
   def __init__(self, gs):
      self.gs = gs

