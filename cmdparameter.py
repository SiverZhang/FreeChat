import sys


if sys.argv[1]:
    option = sys.argv[1][2:]
    if option == 'version':
        print('version 1.2 ')
    elif option == 'help':
        print('''This program prints files to the standard output.
             Any number of files can be specified.
             Options include:
             --version : Prints the version number
             --help     : Display this help''' )
    else:
        print( 'Unknow option.')