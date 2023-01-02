import dbms, root
def start():
    with dbms.dbmanager() as db: 
        while True:
            op = None
            print(root.boptions+'\n')
            while True:
                op = root.intvinput('Select: ')
                if op is not None and not root.chkRange(op, 1, 9): continue
                break
            if op == 1:
                db.insert(1)
            elif op == 2:
                db.update(1)
            elif op == 3:
                db.delete(1) 
            elif op == 8:
                db.clearTable(1)
            elif op == 9:
                print(db.readTable(1))
            else:
                if db.readTable(1).empty:
                    print("There are no batches\n")
                    continue
                print(db.readTable(1).loc[: ,['batch_id', 'batch_name']])
                batchID= None
                while True:
                    batchID = root.vinput('\nSelect Batch ID: ')
                    if batchID is None or not db.checkFKey(1, 'batch_id', batchID, False): continue 
                    break
                if op == 4:
                    print("\nStudents: "+str(db.getLOS(batchID))+"\n")
                elif op == 5:
                    print("\nCourses: "+str(db.getLOC(batchID))+"\n")
                elif op == 6:
                    print("Overall Student Performance in "+batchID+":\n"+db.getBatchPerformance(batchID).to_string(index = False)+"\n")
                elif op == 7:
                    db.displayPiechartPercentage(batchID)
if __name__ == '__main__':
    start()