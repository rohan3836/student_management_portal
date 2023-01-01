import dbms
import root 

with dbms.dbmanager() as db: 
    while True:
        op = None
        print(str(root.eoptions)+'\n')
        while True:
            op = root.intvinput('Select: ')
            if op is not None and not root.chkRange(op, 1, 7): continue
            break
        if op == 1:
            db.insert(4)
        elif op == 2:
            db.update(4)
        elif op == 3:
            db.delete(4)
        elif op == 5:
            db.displayExamStatistics()
        elif op == 6:
            db.clearTable(4)
        elif op == 7:
            print(db.readTable(4))
        else:
            if db.readTable(4).empty:
                print("There are no student grades\n")
                continue
            print(db.readTable(4))
            while True:
                courseID = root.vinput('\nSelect Course ID: ')
                if courseID is None or not db.checkFKey(4, 'course_id', courseID, False): continue
                break
            if op == 4:
                df = db.getCoursePerformance(courseID)
                print("Course Performance of "+courseID+": ")
                print(df.loc[: ,['student_name', 'roll_no', 'marks']])
