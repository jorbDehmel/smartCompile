import os
import sys

# os.path.getmtime('/tmp')

COMPILER_STEM = 'clang++ -pedantic -Wall '

def make_dirs():
    if not os.path.exists('objs'):
        os.makedirs('objs')
    if not os.path.exists('bin'):
        os.makedirs('bin')
    if not os.path.exists('headers'):
        os.makedirs('headers')
        os.system('sudo mv *.h headers')
    if not os.path.exists('source'):
        os.makedirs('source')
        os.system('sudo mv *.cpp source')
    if not os.path.exists('logs'):
        os.makedirs('logs')
        os.system('sudo mv *.log logs')
    if not os.path.exists('.gitignore'):
        with open('.gitignore', 'w') as file:
            file.write('objs/\nbin/\n*.o\nlogs/\n*.log')

def to_objects(extra=None):
    l = os.listdir('source')
    if extra != None:
        l.append(extra)
    for cpp in l:
        o = os.path.join('objs', cpp.replace('.cpp', '.o'))
        header = os.path.join('headers', cpp.replace('.cpp', '.h'))
        cpp = os.path.join('source', cpp)

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

        command = COMPILER_STEM + cpp + ' -c -o ' + o
        print(command)
        os.system(command)
    return


def to_executable(out='bin/main.out'):
    if os.path.exists(out):
        o_age = max([os.path.getmtime(os.path.join('objs', obj)) for obj in os.listdir('objs')])
        if os.path.getmtime(out) > o_age:
            print(out, 'up to date.')
            return

    objs_str = ' '.join([os.path.join('objs', obj) for obj in os.listdir('objs')])
    command = COMPILER_STEM + objs_str + ' -o bin/main.out'
    print(command)
    os.system(command)
    return

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '-pclean':
            os.system('sudo rm -f bin/*.out objs/*.o')
        elif sys.argv[1] == '-dclean':
            os.system('sudo mv headers/*.h .')
            os.system('mv logs/*.log .')
            os.system('mv source/*.cpp .')
            os.system('rm -f -r objs bin headers source logs')
        elif os.path.exists(sys.argv[1]):
            make_dirs()

            os.system('cp ' + sys.argv[1] + ' source')
            extra = sys.argv[1].split('/')[-1]
            to_objects(extra)
            os.system('rm source/' + extra)

            to_executable()
    else:
        make_dirs()
        to_objects()
        to_executable()
