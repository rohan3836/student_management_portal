import dbms, root, student, batch, course, department, examination
with dbms.dbmanager() as db: 
    while True:
        print(db.readTable(3))
        print(root.options+'\n')
        while True:
            op = root.intvinput('Select: ')
            if not root.chkRange(op, 1, 6): continue
            break
        ###Database Operations###
        if op == 1:
            student.start()
        elif op == 2:
            course.start()
        elif op == 3:
            batch.start()
        elif op == 4:
            department.start()
        elif op == 5:
            examination.start()