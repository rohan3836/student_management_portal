import sys
options = {'Manage Tables' : 1, 'Get Student Report' : 2, 'View Course Student Performances/Histogram' : 3, 'View Batch Performance/L.O.C/L.O.S/Statistics' : 4, 'Department Performance/Statistics' : 5, 'Show Examination Statistics' : 6,'Back' : 'back', 'Exit' : 'exit'}
soptions = {'Create Student' : 1, 'Update Student' : 2, 'Delete Student' : 3, 'Generate Student Report' : 4, 'Clear Student Table' : 5, 'View Student Table' : 6}
coptions = {'Create Course' : 1, 'Update Course' : 2, 'Delete Course' : 3, 'View Performance of all Students in the Course' : 4, 'Show Course Statistics/Histogram' : 5, 'Clear Course Table' : 6, 'View Course Table' : 7}
boptions = {'Create Batch' : 1, 'Update Batch' : 2, 'Delete Batch' : 3, 'View list of all Students in a Batch' : 4, 'View list of all Courses taught in the Batch' : 5, 'View complete Performance of all Students in a Batch' : 6, 'View Pie Chart of Percentage of all Students' : 7, 'Clear Batch Table' : 8, 'View Batch Table' : 9}
doptions = {'Create Department' : 1, 'Update Department' : 2, 'Delete Department' : 3, 'View all Batches in a Department' : 4, 'View average Performance of all Batches in the Department' : 5, 'Show Department Statistics' : 6, 'Clear Department Table' : 7, 'View Department Table' : 8}
eoptions = {'Enter Marks' : 1,'Delete Marks' : 2, 'Update Marks' : 3, 'View Performance of all Students in the Examination' : 4, 'Show Examination Statistics' : 5, 'Clear Marks Table' : 6, 'View Marks Table' : 7}
cdatabase = {'Students' : 1, 'Batches' : 2, 'Courses' : 3, 'Departments' : 4, 'Marks' : 5, 'Clear all tables' : 6, 'Back' : 'back'}
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
    elif v1 == "back":
        global back
        back = True
        return ""
    else:
        print()
        return v1
    
def intvinput(line):
    v1 = input(line)
    if v1 == "exit":
        sys.exit()
    elif v1 == "back":
        global back
        back = True
        return 1
    else:
        try:
            v2 = int(v1)
        except:
            print("Enter a valid Integer")
            return intvinput(line)
        else:
            print()
            return v2
    
def tableops(tname):
    sname = singular(tname)
    options = {'Create ' + sname : 1, 'Update '+sname : 2, 'Delete '+sname : 3, 'Clear Table' : 4, 'View Table' : 5}
    if(tname == 'Marks'):
        options = {sname+' Student' : 1, 'Update '+tname : 2, 'Delete '+tname : 3, 'Clear Table' : 4, 'View Table' : 5}
    print(str(options)+"\n")
    
def chkRange(x,a,b):
    if not a <= x <= b:
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
