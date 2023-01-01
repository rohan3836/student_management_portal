import dbms
import root 

with dbms.dbmanager() as db: 
    while True:
        op = None
        print(str(root.coptions)+'\n')
        while True:
            op = root.intvinput('Select: ')
            if op is not None and not root.chkRange(op, 1, 7): continue
            break
        if op == 1:
            db.insert(2)
        elif op == 2:
            db.update(2)
        elif op == 3:
            db.delete(2) 
        elif op == 6:
            db.clearTable(2)
        elif op == 7:
            print(db.readTable(2))
        else:
            if db.readTable(2).empty:
                print("There are no courses\n")
                continue
            print(db.readTable(2))
            courseID= None
            while True:
                courseID = root.vinput('\nSelect Course ID: ')
                if courseID is None or not db.checkFKey(2, 'course_id', courseID, False): continue
                break
            if op == 4:
                df = db.getCoursePerformance(courseID)
                print("Course Performance of "+courseID+": ")
                print(df.loc[: ,['student_name', 'roll_no', 'marks']])
            elif op == 5:
                db.displayCourseStatistics(courseID)  