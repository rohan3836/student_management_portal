import pandas 
import traceback
import sys
import root
import numpy
import matplotlib.pyplot as plt

class dbmanager():
    database = None
    header = None
    
    def __init__(self):
        self.database = ['students', 'batches', 'courses', 'departments', 'marks']
        self.headers = [
            ['student_id', 'student_name', 'roll_no', 'batch_id'],
            ['batch_id', 'batch_name', 'dept_id', 'courses'],
            ['course_id', 'course_name'],
            ['dept_id', 'dept_name'],
            ['student_id', 'course_id', 'marks']]
        for i in range(len(self.database)):
            self.initTable(i) 
            
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)
        sys.exit()
        return True
    
    def initTable(self, table):
        '''initializes a given Table/Add Headers'''
        if self.isjustCreated(self.database[table]+".csv"):
            print("Initiialized "+self.database[table]+".csv")
            
    def clearTable(self, table):
        '''Clears all data from given table'''
        open(self.database[table]+".csv", "w").close()
        
    def clearAll(self):
        '''Clears all data from all tables'''
        for i in range(len(self.database)):
            self.clearTable(i+'.csv')
            
    def readTable(self, table):
        try:
            csvhandler = pandas.read_csv(self.database[table]+'.csv', names=self.headers[table])
            return pandas.DataFrame(csvhandler)
        except:
            print("Error Reading Data\n")
            traceback.print_exc()
            return pandas.DataFrame()
    
    def isjustCreated(self, fname):
        '''initializes a single file/Creates one if not exists'''
        try: 
            with open(fname): return False
        except:
            with open(fname, "w"): return True
            
    def checkFKey(self, table, header, fields, isCol):
        df = self.readTable(table)
        tname = self.database[table].capitalize()
        field = fields if not isCol else fields[header][0]
        if df.empty:
            print("The "+tname+" Table is empty\n")
            return False
        else:
            if not (df[header] == field).any():
                print("No such "+root.singular(tname)+" ID\n")
                print("Select among the "+tname+":")
                print(df)
                print()
                return False
        return True
    
    def getStudentBatch(self, studentID):
        df1 = self.readTable(0)
        if not (df1['student_id'] == studentID).any():
            print("\nNo such Student ID")
            return False
        df1 = df1.loc[df1['student_id'] == studentID]
        return df1.to_numpy()[0][3]
        
    def relationCheck(self, table, fields):
        '''Check Foreign Keys'''
        
        #Database Conditions/Relations
        if table == 0:
            #Student Batch Check
            if not self.checkFKey(1, 'batch_id', fields, True):
                return False
        if table == 1:
            #Batch Dept & Courses
            if not self.checkFKey(3, 'dept_id', fields, True):
                return False
            for course in fields['courses'][0]:
                if not self.checkFKey(2, 'course_id', course, False):
                    return False
        if table == 4:
            #Marks
            if not self.checkFKey(0, 'student_id', fields, True):
                return False
            if not self.checkFKey(2, 'course_id', fields, True):
                return False
            #Chekc if course is in student batch
            b_id = self.getStudentBatch(fields['student_id'][0])
            df2 = self.readTable(1)
            if not (df2['batch_id'] == b_id).any():
                print("No such Batch ID")
                return False
            df2 = df2.loc[df2['batch_id'] == b_id]
            courses = df2.to_numpy()[0][3][2:-2].split("', '")
            if fields['course_id'][0] not in courses:
                print("No such Course in the Student's Batch")
                return False
        return True
            
    def insertdata(self, table, fields):
        '''Insert Data into Table'''
        try:
            df = self.readTable(table)
            if table != 4:
                if (df[self.headers[table][0]] == fields[self.headers[table][0]][0]).any():
                    print("ID already exists\n")
                    return False
                if table == 0:
                    if (df['batch_id'] == fields['batch_id'][0]).any():
                        df = df.loc[df['batch_id'] == fields['batch_id'][0]]
                        if (df['roll_no'] == fields['roll_no'][0]).any():
                            print("The given Roll No. already exists in Batch\n")
                            return False
            else:
                if (df['student_id'] == fields['student_id'][0]).any():
                    df = df.loc[df['student_id'] == fields['student_id'][0]]
                    if (df['course_id'] == fields['course_id'][0]).any():
                        print("Already Marked\n")
                        return False
            if not self.relationCheck(table, fields):
                return False
            df = pandas.DataFrame(fields)
            df.to_csv(self.database[table]+'.csv', header=False, index=False, mode='a')
            return True
        except:
            print("Error Inserting Data\n")
            traceback.print_exc()
            return False
    
    def updatedata(self, table, fields, editingID):
        '''Update Table data'''
        try:
            csvhandler = pandas.read_csv(self.database[table]+'.csv', names=self.headers[table])
            rdf = pandas.DataFrame(csvhandler)
            row_index = rdf.index[rdf[self.headers[table][0]] == editingID][0]
            for key, value in fields.items():
                if len(value[0]) != 0:
                    rdf.at[row_index, key] = value[0]
            if not self.relationCheck(table, fields):
                return False
            rdf.to_csv(self.database[table]+'.csv', header=False, index=False, mode='w')
            return True
        except IndexError:
            print("No such ID\n")
            return False
        except:
            print("Error Updating Data\n")
            traceback.print_exc()
            return False
            
    def deletedata(self, table, deletingID):
        '''Delete Table data'''
        try:
            csvhandler = pandas.read_csv(self.database[table]+'.csv', names=self.headers[table])
            rdf = pandas.DataFrame(csvhandler)
            rdf.drop(rdf.index[rdf[self.headers[table][0]] == deletingID], axis=0, inplace=True)
            rdf.to_csv(self.database[table]+'.csv', header=False, index=False, mode='w')
            return True
        except IndexError:
            print("No such ID\n")
            return False
        except:
            print("Error Deleting Data\n")
            traceback.print_exc()
            return False
        
    def getLOC(self, batchID):
        df2 = self.readTable(1)
        df2 = df2.loc[df2['batch_id'] == batchID]
        bcourses = df2.to_numpy()[0][3][2:-2].split("', '")
        return bcourses
    
    def getLOS(self, batchID):
        df1 = self.readTable(0)
        df1 = df1.loc[df1['batch_id'] == batchID]
        lst = list()
        for ind in df1.index:
            lst.append(df1['student_id'][ind])
        return lst
    
    def getLOB(self, deptID):
        df1 = self.readTable(1)
        df1 = df1.loc[df1['dept_id'] == deptID]
        lst = list()
        for ind in df1.index:
            lst.append(df1['batch_id'][ind])
        return lst
    
    def getStudentMark(self, s_id, c_id):
        df = self.readTable(4)
        if (df['student_id'] == s_id).any():
            df = df.loc[df['student_id'] == s_id]
            if (df['course_id'] == c_id).any():
                df = df.loc[df['course_id'] == c_id]
                return df.to_numpy()[0][2]
        return "0"
    
    def generateReport(self, studentID):
            df1 = self.readTable(0)
            if (df1['student_id'] == studentID).any():
                df1 = df1.loc[df1['student_id'] == studentID]
                df2 = self.readTable(1)
                df1 = df1.merge(df2, how='left', on='batch_id')
                df3 = self.readTable(3)
                df1 = df1.merge(df3, how='left', on='dept_id')
                df4 = self.readTable(2)
                b_id = self.getStudentBatch(studentID)
                df2 = df2.loc[df2['batch_id'] == b_id]
                bcourses = df2.to_numpy()[0][3][2:-2].split("', '")
                dframe = pandas.DataFrame()
                courses, marks, grades = list(), list(), list()
                for c_id in bcourses:
                    cname = df4.loc[df4['course_id'] == c_id].to_numpy()[0][1]
                    courses.append(cname+'['+c_id+']')
                    m = float(self.getStudentMark(studentID, c_id))
                    marks.append(m)
                    grades.append(root.grade(m))
                total = sum(marks)
                avg = round(sum(marks) / len(marks),2)
                fgrade = root.grade(avg)
                dframe = pandas.DataFrame()
                cn = "Pass" if fgrade not in ["F", "N"] else "Fail"
                dframe['Course'] = courses
                dframe['Marks'] = marks
                dframe['Grade'] = grades
                with open('StudentReport'+studentID+'.txt', 'w') as r:
                    r.write("Student ID: {}\nStudent Name: {}\nStudent Roll No: {}\nDepartment Name: {}\nDepartment ID: {}\nBatch Name: {}\nBatch ID: {}\n".format(
                        df1.to_numpy()[0][0],df1.to_numpy()[0][1],df1.to_numpy()[0][2],df1.to_numpy()[0][7],df1.to_numpy()[0][5],df1.to_numpy()[0][4],df1.to_numpy()[0][3])+
                        "\nStudent Grades:\n {}\nTotal Marks: {}\nAverage Marks = {}/{} = {}\nFinal Grade: {}\nConclusion: {}".format(dframe.to_string(index = False),str(total),str(total),str(100*len(marks)),str(avg), str(fgrade), cn))
                print("Generated Report\n")
                
    def getCoursePerformance(self, courseID):
        df1 = self.readTable(4)
        if (df1['course_id'] == courseID).any():
            df1 = df1.loc[df1['course_id'] == courseID]
            df2 = self.readTable(2)
            df1 = df1.merge(df2, how='left', on='course_id')
            df3 = self.readTable(0)
            df1 = df1.merge(df3, how='left', on='student_id')
            return df1.loc[: ,['student_name', 'roll_no', 'marks']]
        
    def displayCourseStatistics(self, courseID):
        df = self.getCoursePerformance(courseID)
        dct, count = dict(), dict()
        for ind in df.index:
            dct[df['student_name'][ind]] = root.grade(float(df['marks'][ind]))
        for (k,v) in dct.items():
            count[v] = count.get(v,0)+1
        #Histogram
        plt.bar(count.keys(), count.values())
        plt.xlabel("Course Marks") 
        plt.ylabel("Number of Students") 
        plt.title("Performance of all Students in the Course")  
        plt.show()
            
    def getBatchPerformance(self, batchID):
        students = self.getLOS(batchID)
        if len(students) < 1:
            return "\nNo Students in Batch\n"
        df1 = self.readTable(0)
        roll_no, name, percentage = list(), list(), list()
        dframe = pandas.DataFrame()
        for student in students:
            df = df1.loc[df1['student_id'] == student]
            name.append(df.to_numpy()[0][1])
            roll_no.append(df.to_numpy()[0][2])
            percentage.append(self.getPencentageMarks(student))
        dframe['Roll No.'] = roll_no
        dframe['Name'] = name
        dframe['Percentage'] = percentage
        return dframe
    
    def getDeptPerformance(self, deptID):
        batches = self.getLOB(deptID)
        if len(batches) < 1:
            return "\nNo Students in Batch\n"
        dframe = pandas.DataFrame()
        bid, name, bperformances = list(), list(), list()
        df1 = self.readTable(1)
        for batch in batches:
            df = df1.loc[df1['batch_id'] == batch]
            bid.append(df.to_numpy()[0][0])
            name.append(df.to_numpy()[0][1])
            students = self.getLOS(batch)
            avgp = 0
            if len(students) >= 1:
                percentage = list()
                for student in students:
                    percentage.append(self.getPencentageMarks(student))
                avgp = round(sum(percentage)/len(percentage), 2)
            bperformances.append(avgp)
        dframe['Batch ID'] = bid
        dframe['Batch Name'] = name
        dframe['Batch Performance'] = bperformances
        return dframe
    
    def getDeptStatistics(self, deptID):
        df = self.getDeptPerformance(deptID)
        name, perf = list(), list()
        for ind in df.index:
            name.append(df['Batch Name'][ind])
            perf.append(df['Batch Performance'][ind])
        plt.plot(perf, name)
        plt.xlabel("Performance(Average Percentage)") 
        plt.ylabel("Batches") 
        plt.title("Performance of all Batches in the Department")  
        plt.show()
    
    def getPencentageMarks(self, studentID):
        df1 = self.readTable(0)
        if (df1['student_id'] == studentID).any():
            b_id = self.getStudentBatch(studentID)
            bcourses = self.getLOC(b_id)
            marks = list()
            for c_id in bcourses:
                marks.append(float(self.getStudentMark(studentID, c_id)))
            return round(sum(marks) / len(marks),2)
            
    def displayPiechartPercentage(self, batchID):
        students = self.getLOS(batchID)
        df1 = self.readTable(0)
        name, percentage = list(), list()
        for student in students:
            df = df1.loc[df1['student_id'] == student]
            name.append(df.to_numpy()[0][0]+'['+df.to_numpy()[0][1]+']')
            percentage.append(self.getPencentageMarks(student))
        plt.figure(figsize =(10, 7))
        myexplode = [0.2, 0, 0, 0]
        plt.legend()
        plt.pie(percentage, labels = name, explode = myexplode, shadow = True)
        plt.show()
        
    def displayExamStatistics(self):
        df1 = self.readTable(2)
        for i in df1.index:
            courseID = df1['course_id'][i]
            df2 = self.readTable(1)
            batch_marks, batch_names = list(), list()
            for j in df2.index:
                batchID = df2['batch_id'][j]
                students, courses = self.getLOS(batchID), self.getLOC(batchID)
                if courseID in courses and len(students) >= 1:
                    student_marks = list()
                    for student in students:
                        student_marks.append(float(self.getStudentMark(student, courseID)))
                    batch_names.append(df2['batch_name'][j])
                    batch_marks.append(round(sum(student_marks)/len(student_marks), 2))
            x = numpy.array(batch_marks)
            y = numpy.array(batch_names)
            plt.scatter(x,y)
        plt.xlabel("Course Marks") 
        plt.ylabel("Batches") 
        plt.title("Batch performance in all courses")  
        plt.show()
          
    
    def insert(self, table):
        #####Insert#####
        dname = str(root.dnames[table+1])
        root.tableops(dname)    
        q = root.intvinput("Enter number of "+dname+" to add: ")
        for n in range(q):
            print('|',root.singular(dname), n+1,'|')
            datafields = dict()
            for i in range(len(root.insoperations[table])):
                #Batch Courses
                if (table, i) == (1, 3):
                    courses = list()
                    for j in range(root.intvinput("Enter the number of courses for the batch: ")):
                        courses.append(root.vinput("Enter Course ID: "))
                    datafields[self.headers[table][i]] = [courses]
                else:
                    datafields[self.headers[table][i]] = [root.vinput(root.insoperations[table][i]+": ")]
            if self.insertdata(table, datafields):
                if table != 4:
                    print(root.singular(dname)+" Data Successfully Inserted\n")
                else:
                    print("Student Graded\n")
                datafields = None
                
    def update(self, table):
        dname = str(root.dnames[table+1])
        print("!Blank Fields Will Not be Updated!\n")
        datafields = dict()
        for i in range(len(root.insoperations[table])):
            datafields[self.headers[table][i]] = [root.vinput(root.insoperations[table][i]+": ")]
        edit_id = root.vinput("Enter "+root.singular(dname)+" ID to be Edited: ")
        if self.updatedata(table, datafields, edit_id):
            print(root.singular(dname)+" Data Successfully Updated\n")
            datafields = None
            
    def delete(self, table):
        dname = str(root.dnames[table+1])
        edit_id = root.vinput("Enter "+root.singular(dname)+" ID for Deletion: ")
        if self.deletedata(table, edit_id):
            print(root.singular(dname)+" Data deleted\n")