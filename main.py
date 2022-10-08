"""
A simple make-esque smart compiler and directory organizer for cpp projects.
(See readme.txt)
"""

import os
import sys

# The compiler, plus arguments. Used in all compiling/linking calls.
COMPILER_STEM = 'clang++ -pedantic -Wall '

# Establish the needed directory structure if it is not present
def make_dirs():
    # Make objs/ for *.o
    if not os.path.exists('objs'):
        os.makedirs('objs')

    # Make bin/ for *.out
    if not os.path.exists('bin'):
        os.makedirs('bin')
    
    # Make headers/ for *.h
    if not os.path.exists('headers'):
        os.makedirs('headers')
        os.system('sudo mv *.h headers')
    
    # Make source/ for *.cpp
    if not os.path.exists('source'):
        os.makedirs('source')
        os.system('sudo mv *.cpp source')
    
    # Make logs/ for *.log
    if not os.path.exists('logs'):
        os.makedirs('logs')
        os.system('sudo mv *.log logs')
    
    # Make .gitignore if not present
    if not os.path.exists('.gitignore'):
        with open('.gitignore', 'w') as file:
            file.write('objs/\nbin/\n*.o\nlogs/\n*.log')

# Compile all objects in source/
def to_objects(extra=None):
    # Handle extra file if given
    l = os.listdir('source')
    if extra != None:
        l.append(extra)

    # Iterate over cpp files in source/
    for cpp in l:
        # Get filenames for the *.o , *.h , and *.h
        o = os.path.join('objs', cpp.replace('.cpp', '.o'))
        header = os.path.join('headers', cpp.replace('.cpp', '.h'))
        cpp = os.path.join('source', cpp)

        # If the *.o file exists, check its age against its sources.
        # If up to date, skip
        if os.path.exists(o):
            o_age = os.path.getmtime(o)
            if os.path.exists(header):
                if o_age > os.path.getmtime(cpp) and o_age > os.path.getmtime(header):
                    print(o, ' up to date.')
                    continue
            else:
                if o_age > os.path.getmtime(cpp):
                    print(o, ' up to date.')
                    continue

        # If compilation is needed, call the compiler (using the compiler stem)
        command = COMPILER_STEM + cpp + ' -c -o ' + o
        print(command)
        os.system(command)
    return

# Link the compiled *.o files in objs/
def to_executable(out='bin/main.out'):
    # If the *.out file already exists, check its age against its sources
    if os.path.exists(out):
        o_age = max([os.path.getmtime(os.path.join('objs', obj)) for obj in os.listdir('objs')])
        if os.path.getmtime(out) > o_age:
            print(out, 'up to date.')
            return

    # Link if needed (using compiler stem)
    objs_str = ' '.join([os.path.join('objs', obj) for obj in os.listdir('objs')])
    command = COMPILER_STEM + objs_str + ' -o bin/main.out'
    print(command)
    os.system(command)
    return

# Main function
if __name__ == '__main__':
    # Check command line arguments
    if len(sys.argv) > 1:
        # Iterage over given arguments
        for i in range(1, len(sys.argv)):
            # Erase all .o and .out
            if sys.argv[i] == 'pclean':
                os.system('sudo rm -f bin/*.out objs/*.o')
            
            # Destroy directory structure (keep files)
            elif sys.argv[i] == 'dclean':
                os.system('sudo mv headers/*.h .')
                os.system('mv logs/*.log .')
                os.system('mv source/*.cpp .')
                os.system('rm -f -r objs bin headers source logs')

            # Output to (`sc -o <outpath>``)
            elif sys.argv[i] == '-o':
                make_dirs()
                to_objects()
                to_executable(sys.argv[i + 1])
            
            # Equivolent to `sc dclean`, `sc`
            elif sys.argv[i] == 'remake':
                os.system('sudo mv headers/*.h .')
                os.system('mv logs/*.log .')
                os.system('mv source/*.cpp .')
                os.system('rm -f -r objs bin headers source logs')

                make_dirs()
                to_objects()
                to_executable()
            
            # If argument is a valid file, include it as a .cpp for compilation
            elif os.path.exists(sys.argv[i]):
                make_dirs()

                os.system('cp ' + sys.argv[i] + ' source')
                extra = sys.argv[i].split('/')[-1]
                to_objects(extra)
                os.system('rm source/' + extra)

                to_executable()
            
            # Otherwise, pass arg to compiler
            else:
                COMPILER_STEM += sys.argv[i] + ' '
    
    # If no command line args, create using default settings
    else:
        make_dirs()
        to_objects()
        to_executable()
