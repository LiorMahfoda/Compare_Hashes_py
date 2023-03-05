import hashlib  #for SHA1 AND MD5
import os # recursive path search
import csv # csv module
import keyboard # read keys
import sys # gets arguments from cmd
import pandas as pd # data
import time # for sleep
import argparse # add flags to main

BLOCK_SIZE = 65536


def file_hash_hex(file_path, hash_func):
    with open(file_path, 'rb') as f:
        return hash_func(f.read()).hexdigest()


def recursive_file_listing(base_dir):
    for directory, subDirs, files in os.walk(base_dir):
        for filename in files:
            yield directory, filename, os.path.join(directory, filename)


def recursive_search(filename):
    global base_path
    lst = []
    for dirPath, dirs, files in os.walk(base_path, topdown=False):
        for name in files:
            if name != filename:
                continue
            else:
                path_name = os.path.join(dirPath, name)
                lst.append(path_name)
    # list of paths
    return lst


def get_hash_md5(file):
    m = hashlib.md5()
    m.update(file.encode())
    return m.digest()


def get_hash_sha1(file):
    m = hashlib.sha1()
    m.update(file.encode())
    return m.digest()


def file_exists(path):
    return os.path.exists(path)


def file_length(filename):
    with open(filename) as f:
        return sum(1 for line in f)


def make_list(file_name, args):
    with open(file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        # write headers
        writer.writerow(("Name", "MD5", "SHA1"))
        # scan from args[0] - user input
        for directory, filename, path in recursive_file_listing(args):
            writer.writerow((filename, file_hash_hex(path, hashlib.md5), file_hash_hex(path, hashlib.sha1)))
    print("File List.csv created! in " + file_name)
    f.close()


def make_csv(file_name):
    df = pd.read_csv(file_name)
    df.drop_duplicates(subset=None, inplace=True)   
    df.to_csv(file_name_modified, index=False)
    print("The \"ModifiedList.csv\"file created or modified in " + file_name_modified + "\n")


def make_csv_file(name):
    #global count
    lines = list()
    with open(file_name_modified, 'r') as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            lines.append(row)
            if row[0] == name or row[0].endswith('.csv'):
                lines.remove(row)                           
    with open(file_name_modified, 'w', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(lines)
    file = open(file_name_modified)
    reader = csv.reader(file)
    curr_lines = len(list(reader)) - 1
    file_bl = open(file_name_blacklist)
    reader_bl = csv.reader(file_bl)
    curr_bl_lines = len(list(reader_bl)) - 1
    # equal to count_deleted: # not equal to zero(0)
    if curr_lines - curr_bl_lines == curr_bl_lines:
        return None 
    # if count == len(file_name_modified):
    #     return None 
    return "Ok"    


def row_exists(line):
    with open(file_name_blacklist) as f:
        lines = csv.reader(f)
        for row in lines:
            if row == line:
                f.close()
                return True
    f.close()          
    return False    


#delete temporaraly files: List.csv & modifiedList.csv
def remove_files():
    global base_path
    file = base_path + "\\List.csv"
    try:
        if file_exists(file):
            with open(file) as f:
                pass
            os.rename(file, file)   
            os.remove(file)
            print("Temp file " + file + " was removed from os")
        with open(outLogFile, 'a+') as log:
            log.write('Total files which have been deleted is: ' + str(removedFilesCount))
            print('Total files which have been deleted is: ' + str(removedFilesCount))
            os.startfile(outLogFile)
        exit()
    except PermissionError as e:
        print(e) 
        exit()


# unified_list-Blacklist.csv values
def compare_values(unified_list):
    global count, removedFilesCount
    removedFilesCount = 0
    with open(file_name_modified, 'r') as inp: 
        # if count == file_length(file_name_blacklist) - 1:
        #     print("\nScanned all files - program terminated ")
        #     remove_files()
        #     log_flag = False
        #     exit()
        reader = csv.DictReader(inp)
        rows = []
        for row in reader:
            rows.append(row)
        while len(unified_list) > 0:    
            value = unified_list.pop(0)  
            for row in rows:
                line = [row['Name'], row['MD5'], row['SHA1']]
                if not row_exists(line):
                    continue
                # The name of the file
                name = row["Name"]
                if row["MD5"] in (value[0], value[1]) or row["SHA1"] in (value[0], value[1]):
                    print("Would you like to delete the file \"" + name
                          + "\"? \npress y/Y to agree, else press n/N")
                    #count += 1
                    key = keyboard.read_key()
                    # Wait 2 seconds after key pressed
                    time.sleep(2)
                    if key.lower() == "y":
                        location = recursive_search(name)
                        print("Deleting file from location/s {}".format(location))
                        for p in location:
                            os.remove(p)
                            with open(outLogFile, "a+") as log:
                                print("The file \"" + name + "\" was removed from os in location " + p)
                                removedFilesCount += 1
                                log.write("The file \"" + name + "\" was removed from os in location " + p + "\n")
                                log.close()
                        status = make_csv_file(name)
                        if status is None:
                            print("\nScanned all files - program terminated ")
                            remove_files()
                        break
                    elif key.lower() == "n":
                        status = make_csv_file(name)
                        if status is None:
                            print("\nScanned all files - program terminated ")
                            remove_files()
                            exit()
                        print("\nMoving to the next file")
                        break
                    else:
                        print("\nWrong input, exiting program")
                        remove_files()
                        if inp.closed is False:
                            inp.close()
                        exit()
        inp.close()               


def main(args):
    global file_name_modified, file_name_blacklist, outLogFile
    # arg 1 from cmd
    file_name = args[1]
    # give the file a name
    file_name += "\\List.csv"
    file_name_modified = args[1] + "\\modifiedList.csv"
    # arg 3 from cmd
    file_name_blacklist = args[3]
    print("The path to search is in " + args[1])
    print("The file to search values is in " + file_name_blacklist)        
    outLogFile = args[1] + "\\log.txt"
    with open(outLogFile, 'w') as file:
        file.truncate(0)
        pass
    make_list(file_name, args[1])
    make_csv(file_name)
    # Create the hash object
    file_hash_md5 = hashlib.md5()
    file_hash_sha1 = hashlib.sha1()  
    unified_list = list()

    # fml is file_modified_list
    with open(file_name, 'r', encoding='utf-8') as fml:
        # Read from the file. Take in the amount declared above
        fb = fml.read(BLOCK_SIZE)
        # While there is still data being read from the file
        while len(fb) > 0:
            # Update the hash
            file_hash_md5.update(get_hash_md5(fb))
            file_hash_sha1.update(get_hash_sha1(fb))
            # Read the next block from the file
            fb = fml.read(BLOCK_SIZE)
            # fbl is file_black_list
            with open(file_name_blacklist, 'r') as fbl:
                reader_obj = csv.reader(fbl)
                for row in reader_obj:
                    md5, sha1 = row[1], row[2]
                    # passes
                    if md5 == "MD5" or sha1 == "SHA1":
                        continue
                    # adds tuple
                    unified_list.append((md5, sha1))
            fbl.close()
    fml.close() 
    compare_values(unified_list)
    remove_files()


if __name__ == "__main__":
    # Create the parser
    parser = argparse.ArgumentParser()
    # Add an argument
    parser.add_argument('--path', '-p', type=str, required=True, help="The path to search for files, add flag --path or -p")
    # Add an argument
    parser.add_argument('--name', '-n', type=str, required=True, help="The path of Blacklist file, add flag --name or -n")
    # Parse the argument
    args = parser.parse_args()
    try:
        base_path = sys.argv[2]
        file_name_blacklist = sys.argv[4]
        file_name_modified = base_path + "\\modifiedList.csv"
        #count = 0
        while True:
            main(sys.argv[1:])
    except (RuntimeError, FileNotFoundError) as error: 
        #if log_flag is False:
        print("Error: Missing path to search / Missing file in path / No files from Blacklist.csv")
        print("\nPlease try again")
    finally:
        exit()
