import dbms, root
def start():
    with dbms.dbmanager() as db: 
        while True:
            op = None
            print(root.soptions+'\n')
            while True:
                op = root.intvinput('Select: ')
                break
            if op == 1:
                db.insert(0)
            elif op == 2:
                db.update(0)
            elif op == 3:
                db.delete(0)
            elif op == 4:
                if db.readTable(0).empty:
                    print("There are no students\n")
                    continue
                print(db.readTable(0))
                studentdID= None
                while True:
                    studentdID = root.vinput('\nSelect Student ID: ')
                    if studentdID is None or not db.checkFKey(0, 'student_id', studentdID, False): continue
                    break
                db.generateReport(studentdID)
            elif op == 5:
                db.clearTable(0)
            elif op == 6:
                print(db.readTable(0))
if __name__ == '__main__':
    start()