import os, argparse, sys, tempfile, subprocess

if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-s', '--string', help="String which to group the files according to")
    PARSER.add_argument('-f', '--folder', help="Folder path")
    PARSER.add_argument('-v', '--verbose', help="Additional verbose", action='store_true', default=False)
    PARSER.add_argument('-e', '--extension', help="File extension which to filter the files in the folder, leaving it empty ignores extensions", default="")
    PARSER.add_argument('-o', '--output', help="Output folder which to create and move the files to, by default creates a folder named <string>")
    ARGS = PARSER.parse_args()

    verbose = ARGS.verbose
    extension = ARGS.extension

    if not ARGS.string:
        print("String is required, use -s or --string")
        sys.exit(1)
    string = ARGS.string

    if ARGS.folder:
        if os.path.exists(ARGS.folder):
            folder = ARGS.folder
        else:
            print("Folder you're searching through doesn't exist!")
            sys.exit(1)
    else:
        folder = os.getcwd()

    if ARGS.output:
        output = ARGS.output
    else:
        output = os.path.join(folder, string)

    destination, found, origin = ([] for i in range(3))
    for file in os.listdir(folder):
        if (extension == ""  or file.endswith(extension)) and string in file:
            found.append(file)
            destination.append(os.path.join(output,file))

    for file in found:
        origin.append(os.path.join(folder, file))

    if verbose:
        print("Extension set to: " + extension)
        print("File path set to: " + folder)
        print("Search string set to: " + string)
        print("Output folder set to: " + output)
        print("List of found files: " + str(found))
        print("Origin locations: " + str(origin))
        print("Destination locations: " + str(destination))

    dialogue = input("We're moving {} files into {}\nAre you sure? (y/n/review)   ".format(str(len(found)), output))
    if dialogue == "review" or dialogue == "y":
        if dialogue == "review":
            temp = tempfile.NamedTemporaryFile('w+t')
            if verbose: print("Temporary file created: {}".format(temp.name))

            try:
                for i in range(0, len(origin)):
                    temp.writelines(origin[i] + "   " + destination[i] + "\n")
                temp.seek(0)

                opener = "open" if sys.platform == "darwin" else "xdg-open"
                #subprocess.call([opener, temp.name])
                subprocess.Popen([opener,temp.name])

                cont = input("Finish moving? (y/n)   ")
                if cont != "y":
                    print("Exiting...")
                    sys.exit(1)
            finally:
                if verbose: print("Closing temporary file...")
                temp.close()

        if not os.path.exists(output): 
            os.makedirs(output)
            if verbose: print("Creating a folder '{}' as one does not exist.".format(output))
        if len(origin) == len(destination):
            for i in range(0, len(origin)):
                os.rename(origin[i], destination[i])
                print("Moving {} from {} to {}".format(str(found[i]),origin[i],destination[i]))
        else:
            print("Error, origin and destination count don't match!")
            sys.exit(1)
    else:
        print("Exiting...")