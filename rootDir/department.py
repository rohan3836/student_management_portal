import dbms, root
def start():
    with dbms.dbmanager() as db: 
        while True:
            op = None
            print(root.doptions+'\n')
            while True:
                op = root.intvinput('Select: ')
                if op is not None and not root.chkRange(op, 1, 8): continue
                break
            if op == 1:
                db.insert(3)
            elif op == 2:
                db.update(3)
            elif op == 3:
                db.delete(3)
            elif op == 7:
                db.clearTable(3)
            elif op == 8:
                print(db.readTable(3))
            else:
                if db.readTable(3).empty:
                    print("There are no departments\n")
                    continue
                print(db.readTable(3))
                deptID= None
                while True:
                    deptID = root.vinput('\nSelect Dept ID: ')
                    if deptID is None or not db.checkFKey(3, 'dept_id', deptID, False): continue 
                    break
                if op == 4:
                    print("\nBatches: "+str(db.getLOB(deptID))+"\n")
                elif op == 5:
                    print(db.getDeptPerformance(deptID).to_string(index = False)+"\n")
                elif op == 6:
                    db.getDeptStatistics(deptID)
if __name__ == '__main__':
    start()