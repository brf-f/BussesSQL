import sqlite3
 
def init(db, crtTbl, initTblVals, InsrtCmd):
    #connect to database
    conn = sqlite3.connect(db)
    c = conn.cursor()
 
    try:
        c.execute(crtTbl)
 
        newTblVals = initTblVals
        c.executemany(InsrtCmd,newTblVals)
        conn.commit()
        print("Table created")
       
    except sqlite3.OperationalError:
        print("Table Exists")
        pass
 
    c.close()
