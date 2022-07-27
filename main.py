import json #import packages
import os
from tabulate import tabulate

DBFolder = "catalogues" #location of catalogues


def getDBList(): #gets list of catalogues
    dblist = []
    for i in os.listdir(DBFolder): #itterate through the directory and add the names to s list
        dblist.append(i[:i.rfind(".")])#the index removes the .json file extention
    return dblist


def tableify(list, index = False): #turn list into table, index will number the rows
    print()#padding
    
    print(tabulate(list["data"], headers = list["headers"], showindex = index))

    print()#padding
    

def readDB(name): #read a file 
    with open(f"{DBFolder}/{name}.json") as file: #open file
        data = json.load(file)
        tableify(data) #print the table


def editDB(name): #edit a file
    with open(f"{DBFolder}/{name}.json") as file: #open file
        data = json.load(file)
    while True:
        tableify(data, index = True) #print data
        print("Type each column of data separated by '|' to add it.\nData is added left to right, so not adding enough will leave areas blank.\nTo add a row in a certain spot, type 'n>' and replace 'n' with the row index.\nPress 'B' to go back.\nPress 'S' to save and go back.")
        action = input("> ").lower() #get the action and convert it to lowercase
        
        if action == "b": #if action is back, exit function
            return
            
        elif action == "s": #if action is save
            with open(f"{DBFolder}/{name}.json", "w") as file: #open file
                json.dump(data, file, indent = 4) #write changes
            return #exit
            
        if len(action) == 0: #if action is blank, loop back
            continue

        index = -1 #set index to -1
        if len(action) > 1: #if action is longer than 1
            if action[1] == ">": #if action index 1 is >
                try:
                    index = int(action[0]) #make index the first character and delete n>
                    action = action[2:]
                        
                except ValueError: #if index is not a number, print error and loop
                    print("Index must be a number!")
                    continue

        action = action.split("|") #split action at the character |, turn into list
        
        if len(action) > len(data["headers"]): #if there are more inputs than columns
            print("Too many data instances!") #print error
            continue #loop back
        
        if index == -1: #if no inde was given, set index to one more then the number of rows
            index = len(data["data"]) + 1
        
        data["data"].insert(index, action) #insert data at index

        continue #loop
        
    
def openDB(): #open a file
    list = getDBList() #get list of files
    for n, i in enumerate(list):
        print(f"{n}: {i}") #print the list
    print("What set would you like to open? (type the name or number)")

    while True:
        selection = input("> ") #get input
        
        try:
            selection = int(selection)
            if selection < 0:  # if not a positive int print message and ask for input again
                print("Sorry, input must be positive!") #print error
                continue
                
            if selection in range(len(list)): #if selection if valid, break loop
                break
            else:
                print("That number is out of range!") #otherwise, print error
        except ValueError: #if there is an error due to not a number, print error
            print("Sorry, input must be an integer!")  
            continue

    while True:
        print()
        print("Press 'E' to edit the file")
        print("Press 'R' to read from the file")
        print("Press 'B' to go back")
        print()
    
        option = input("> ").lower() #get input and convert to lowercase
        if option == "e": #if editing, call editDB
            editDB(list[selection])
            
        elif option == "r": #if reading, call readDB
            readDB(list[selection])

        elif option == "b": #if going back, exit function
            return
        else: #if invalid, print error
            print("INVALID OPTION!")
            continue


def newDB(): #make a new file
    while True:
        print("What do you want to name the file?")
        print()
        name = input("> ") #get file name
        try:
            open(f"{DBFolder}/{name}.json", "x") #make file

        except FileExistsError: #if file exists, print error
            print(f"There is already a file with the name '{name}'!")

        print("What do you want the columns to be?\nType each column name separated by '|' to add it.")
        print()
        cols = input("> ") #get cols
        cols = cols.split("|") #split cols at character '|'

        with open(f"{DBFolder}/{name}.json", "w") as file: #open file
            json.dump({"headers":cols, "data":[]}, file, indent = 4) #dump cols and blank data
        return

        
def main(): #MAIN PROGRAM
    print("\
  ______      _          _____       _        _                             \n\
  |  _  \    | |        /  __ \     | |      | |                            \n\
  | | | |__ _| |_ __ _  | /  \/ __ _| |_ __ _| | ___   __ _ _   _  ___ _ __ \n\
  | | | / _` | __/ _` | | |    / _` | __/ _` | |/ _ \ / _` | | | |/ _ \ '__|\n\
  | |/ / (_| | || (_| | | \__/\ (_| | || (_| | | (_) | (_| | |_| |  __/ |   \n\
  |___/ \__,_|\__\__,_|  \____/\__,_|\__\__,_|_|\___/ \__, |\__,_|\___|_|   \n\
                                                       __/ |                \n\
                                                      |___/                 \n\
        ")

    while True: #main loop
        list = getDBList() #get the file list
    
        if len(list) <= 0: #if the file list has 0 items
            print("You have no data sets!") #print error
        else:
            print("Press 'O' to open an existing file (or one you just made)") #prompt
        print("Press 'N' to create a new file")
        
        print()
    
        action = input("> ").lower() #get input and convert to lowercase
        
        print()
    
        if action == "o": #if opening files
            if len(list) <= 0: #check if there are no files
                print("You have no files! Press 'N' to create one!")#print error
                return
            else: #if there are files
                openDB() #call openDB function
                
        elif action == "n": #if new file
            newDB() #call newDB function
            

if __name__ == "__main__": #boilerplate stuff, makes sure the file is being run directly
    main()
    