import sys

options = 'Manage Students : 1, Manage Courses : 2, Manage Batches : 3, Manage Departments : 4, Manage Examinations : 5, Exit : exit'

soptions = 'Create Student : 1, Update Student : 2, Delete Student : 3\nGenerate Student Report : 4, Clear Student Table : 5, View Student Table : 6, Exit : exit'

coptions = 'Create Course : 1, Update Course : 2, Delete Course : 3\nView Performance of all Students in the Course : 4, Show Course Statistics/Histogram : 5\nClear Course Table : 6, View Course Table : 7, Exit : exit'

boptions = 'Create Batch : 1, Update Batch : 2, Delete Batch : 3\nView list of all Students in a Batch : 4, View list of all Courses taught in the Batch : 5\nView complete Performance of all Students in a Batch : 6, View Pie Chart of Percentage of all Students : 7\nClear Batch Table : 8, View Batch Table : 9, Exit : exit'

doptions = 'Create Department : 1, Update Department : 2, Delete Department : 3\nView List of all Batches in a Department : 4, View average Performance of all Batches in the Department : 5\nShow Department Statistics : 6, Clear Department Table : 7, View Department Table : 8, Exit : exit'

eoptions = 'Enter Marks : 1, Delete Marks : 2, Update Marks : 3\nView Performance of all Students in the Examination : 4, Show Examination Statistics : 5\nClear Marks Table : 6, View Marks Table : 7, Exit : exit'

cdatabase = {'Students' : 1, 'Batches' : 2, 'Courses' : 3, 'Departments' : 4, 'Marks' : 5}

dnames = {v:k for (k,v) in cdatabase.items()}
 
insoperations = {
    0 : {0 : 'Enter Student ID',1 : 'Enter Student name', 2 : 'Enter Student roll no', 3 : 'Enter Student batch'},
    1 : {0 : 'Enter Batch ID',1 : 'Enter Batch name', 2 : 'Enter Department ID', 3 : 'Enter Courses'},
    2 : {0 : 'Enter Course id',1 : 'Enter Course name'},
    3 : {0 : 'Enter Department id',1 : 'Enter Department name'},
    4 : {0 : 'Enter Student id',1 : 'Enter Course id',2 : 'Enter Marks'}
   }   
def vinput(line):
    v1 = input(line)
    if v1 == 'exit':
        sys.exit()
    else:
        print()
        return v1
    
def intvinput(line):
    v1 = input(line)
    if v1 == "exit":
        sys.exit()
    else:
        try:
            v2 = int(v1)
        except:
            print("Enter a valid Integer")
            return intvinput(line)
        else:
            print()
            return v2
    
def chkRange(x,a,b):
    if not x == 'back' and not a <= x <= b:
        print("Please pick a choice")
        print()
        return False
    return True
    
def singular(t):
    return t[0:-1] if t != 'Batches' else t[0:-2]

def grade(m):
    if 100>=m>=90:
        return "A"
    if m>=80:
        return "B"
    if m>=70:
        return "C"
    if m>=60:
        return "D"
    if m>=50:
        return "E"
    if 0<=m<50:
        return "F"
    else:
        return "N"
