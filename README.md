# Compare_Hashes_py

In this script, I'm searching for hash values of files from a given csv file(Blacklist)
and compers it to all files(recursively) from a given path
If there is a match - the program askes the user wheather to delete the file/s or not
There is a text file wit the output when the program terminated. 

In src.py file: run cmd with the following flags
-p : path of search
-n : path of the Blacklist.csv file(can be located anywhere in os file system)

To run in cmd :
python src.py "Path to search" "Path to Blacklist.csv file"
for example:
python src.py -p "C:\Users\Lior Mahfoda\Downloads\test" -n "C:\Users\Lior Mahfoda\Downloads\test\Blacklist.csv"
