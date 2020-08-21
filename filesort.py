import os, argparse, sys, fnmatch, re

if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-s', '--string', help="String which to group the files according to", type=str)
    PARSER.add_argument('-f', '--folder', help="Folder path", type=str)
    PARSER.add_argument('-v', '--verbose', help="Additional verbose", action='store_true', default=False)
    PARSER.add_argument('-e', '--extension', help="File extension which to filter the files in the folder, leaving it empty ignores extensions", default="", type=str)
    PARSER.add_argument('-o', '--output', help="Output folder which to create and move the files to, by default creates a folder named <string>", type=str)
    ARGS = PARSER.parse_args()

    verbose = ARGS.verbose
    extension = ARGS.extension
    wd = os.getcwd()
    wildcards = False

    if not ARGS.string:
        print("String is required, use -s or --string")
        sys.exit()
    string = str(ARGS.string)

    if ARGS.folder:
        if os.path.exists(ARGS.folder):
            folder = ARGS.folder.replace(".", wd)
        else:
            print("Folder you're searching through doesn't exist!")
            sys.exit()
    else:
        folder = wd

    if ARGS.output:
        output = ARGS.output.replace(".", wd)
    else:
        output = os.path.join(folder, "{}_{}".format("filesort", re.sub('[\W_]+', "", string)))

    destination, found, origin = ([] for i in range(3))
    
    for file in os.listdir(folder):
        if file.endswith(extension) and fnmatch.fnmatch(file, string):
            print("adding: " + file)
            found.append(file)
            destination.append(os.path.join(output,file))

    if len(found) == 0:
        print("No files found for the fnmatch {}".format(string))
        sys.exit()

    for file in found:
        origin.append(os.path.join(folder, file))

    if verbose:
        print("Extension set to: {}\nFile path set to: {}\nSearch string set to: {}\nOutput folder set to: {}\nList of found files: {}\nOrigin locations: {}\nDestination locations: {}" \
            .format(extension, folder, string, output, str(found), str(origin), str(destination)))

    dialogue = input("We're moving {} files into {}\nAre you sure? (y/n/review)   ".format(str(len(found)), output))
    if dialogue == "review" or dialogue == "y":
        if dialogue == "review":
            print("\n" + "-" * len(origin[0] + " -> " + destination[0]))
            for i in range(0, len(origin)):
                print(origin[i] + " -> " + destination[i])
            print("-" * len(origin[0] + " -> " + destination[0]) + "\n")
            cont = input("Finish moving? (y/n)   ")
            if cont != "y":
                print("Exiting...")
                sys.exit()

        if not os.path.exists(str(output)): 
            try:
                os.makedirs(output)
            except:
                print("Errors with creating folder. Please use -o or --output to set output directory.")
                sys.exit(1)
            if verbose: print("Creating a folder '{}' as one does not exist.".format(output))
        if len(origin) == len(destination):
            for i in range(0, len(origin)):
                os.rename(origin[i], destination[i])
                if verbose: print("Moving {} from {} to {}".format(str(found[i]),origin[i],destination[i]))
                print("Move completed.")
        else:
            print("Error, origin and destination count don't match!")
            sys.exit()
    else:
        print("Exiting...")