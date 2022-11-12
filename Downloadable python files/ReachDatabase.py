
import sqlite3
import sys

import ErrorCheck
import InitialiseSQL

conn = sqlite3.connect("Busses.db")
c = conn.cursor()
ta = 0
tb = 0
destinations = ["Zurich","Luzern", "Sion" ,"Basel", "Bern", "Lugano", "Davos" ]
 
def Init():
 
    #TableVals
    tblVals = [(1, "Zurich", 50, 45, "11:00", 5, "14:00", 44, "19:00",21 ),(2, "Luzern", 45, 30, "11:30", 15, "13:30", 19, "18:00",3 ),(3, "Sion", 25, 35, "10:00", 35, "15:30", 12, "21:00",33 ),(4, "Basel", 40, 45, "9:00", 11, "14:30", 34, "20:00",45 ),(5, "Bern", 30, 45, "9:30", 34, "13:00", 43, "21:30", 33),(6, "Lugano", 70, 30, "8:30", 12, "12:30", 30, "18:30", 21),(7, "Davos", 60, 30, "8:00", 17, "15:00", 19, "19:30", 14)
    ]
 
    print("Inititalised db")
    #Create table if no SQL table
    InitialiseSQL.init(db ="Busses.db", crtTbl="""CREATE TABLE tblBusses(
                        BusID INT PRIMARY KEY,
                        Destination TEXT,
                        Price INT,
                        Capacity INT,
                        Morning  TIME,
                        Sold1 INT,
                        Afternoon TIME,
                        Sold2 INT,
                        Evening TIME,
                        Sold3 INT
        ); """, initTblVals=tblVals, InsrtCmd = "INSERT INTO tblBusses VALUES (?,?,?,?,?,?,?,?,?,?)")
 
 
def getNewVals(fieldInt, Bus):
    
    field = "ERROR"
    newVal = "ERROR"
    
    if fieldInt == 1:
        print("Cannot change BUS ID")
     
    elif fieldInt == 2:
        field = "Destination"
        newVal = ErrorCheck.CheckInput("What should the new bus destination be?","noList",str)
        print("Destination")
 
    elif fieldInt == 3:
        field = "Price"
        newVal = ErrorCheck.CheckInput("What should the new bus ticket Price be?","noList",int)
        print("Price")
 
    elif fieldInt == 4:
        field = "Capacity"
        newVal = ErrorCheck.CheckInput("What should the new bus Capacity be?","noList",int)
        print("Capacity")
    
    elif fieldInt == 5 or fieldInt == 7 or fieldInt == 9:
        if fieldInt == 5:
            field = "Morning"
            print(field)
        elif fieldInt == 7:
            field = "Afternoon"
        elif fieldInt == 9:
            field = "Evening"
        else:
            print("Field int Error, Field Int: ", fieldInt)
 
        valArr = []
		
        for i in range(5):
            x=9
            
            if i == 0:
                x=2
            elif i == 1 and valArr[0] == 2:
                x=4
            elif (i == 3 or i == 4) and valArr[0] == 2 and valArr[1] == 4:
                x=0
            elif i == 3:
                x=5
            
            if i == 2:
                valArr.append(":")
            else:
                print(valArr)
                valArr.append(ErrorCheck.CheckInput("Enter a digit for the time",list(range(x+1)),int))
 
        newVal = "".join(map(str, valArr))
        print(newVal)
        print("Times")
 
    elif fieldInt == 6 or fieldInt == 8 or fieldInt == 10:
        if fieldInt == 6:
            field = "Sold1"
        if fieldInt == 8:
            field = "Sold2"
        if fieldInt == 10:
            field = "Sold3"
 
        c.execute(f"SELECT Capacity FROM tblBusses WHERE BusID = {Bus}")
        cap = c.fetchone()[0]
        newVal = ErrorCheck.CheckInput("What should the new sold tickets be? (Cannot be higher than capacity)",range(cap+1),int)
        print("sold tickets")
        
    return field, newVal
 
def addRoute():
    a = []

    for i in c.execute("SELECT BusID FROM tblBusses ORDER BY BusID DESC"):
        a.append(i[0])
    
    Bus = a[0]+1
       
    c.execute("INSERT INTO tblBusses VALUES (?,?,?,?,?,?,?,?,?,?)",(Bus, "Default destination", 10, 10, "11:00", 0, "14:00", 0, "19:00",0 ))
 
    for f in range(2,11):
        vals = getNewVals(f, Bus)
        field = vals[0]
        newVal = vals[1]
 
        c.execute(f"UPDATE tblBusses SET {field} = ? WHERE BusID = ?",(newVal,Bus,))
        
    print("Adding Route")
 
def editRoute():
    Bus = getBus("Enter ID of record you would like to change the route of")
    field = ErrorCheck.CheckInput("Which field would you like to change? 1. BusId | 2. Destination | 3. Price | 4. Capacity | 5. Morning | 6. Sold1 | 7. Afternoon | 8. Sold2 | 9. Evening | 10. Sold3 |", list(range(1,11)), int)
 
    vals = getNewVals(field, Bus)
    field = vals[0]
    newVal = vals[1]
 
    c.execute(f"UPDATE tblBusses SET {field} = ? WHERE BusID = ?",(newVal,Bus,))
 
def ChangeRoutes():
    print("\n\n")
    actn = ErrorCheck.CheckInput("Would you like to: \n1. Add Routes\n2.Delete Routes \n3.Edit routes", [1,2,3], int)
    match actn:
        case 1:
            print("Add routes")
            addRoute()
        case 2:
            print("Delete Routes")
            Bus = getBus("Enter ID of Bus route you want to delete: ")
            c.execute("DELETE FROM tblBusses WHERE BusID = ?",(Bus,))
        case 3:
            print("Edit Routes")
            editRoute()
 
 
 
def AdminMenu():
    print("\n\n")
 
    print("Admin Menu:\n")
    inp = ErrorCheck.CheckInput("Would you like to do:\n1. Edit Routes\n2. Print Revenues\n3. Reset Table\n4. Exit Program\n5. Cancel\n", [1,2,3,4,5], int)
   
    match inp:
        case 1:
            print("Editing Route")
            ChangeRoutes()
        case 2:
            print("Printing Revenue")
            printRev()
        case 3:
            print("Reseting Table")
            c.execute("DROP TABLE tblBusses")
            conn.commit()
            Init()
        case 4:
            print("Exiting Program")
            conn.commit()
            conn.close()
            sys.exit()
        case 5:
            print("Canceling...")
            return      
 
 
def printRev():
    print("Printing rev")
    actn = ErrorCheck.CheckInput("Would you like to: \n1. Print Overall revenue\n2.Print specific revenue", [1,2], int)
    match actn:
        case 1:
            printOneRev("ALL")
 
        case 2:
            Bus = getBus("Which bus would you like to print revenue for? [enter ID]")
            printOneRev(Bus)
 
 
def printOneRev(Bus):
 
    if Bus != "ALL":
        print("Printing rev for ", Bus)
        sql = f"SELECT * FROM tblBusses WHERE BusID = \"{Bus}\""
        for row in c.execute(sql):
            BusID, Destination, Price, Capacity, Morning, Sold1, Afternoon, Sold2, Evening, Sold3 = row
            print(f"{Destination}: \nPrice:{Price}$ \n{Morning}: {Sold1} Tickets Sold  {Sold1*Price}$\n{Afternoon}: {Sold2} Tickets Sold  {Sold2*Price}$ \n{Evening}: {Sold3} Tickets Sold  {Sold3*Price}$ \nTotal = {(Sold1*Price)+(Sold2*Price)+(Sold3*Price)}$")
    else:
        print("Printing rev for ", Bus)
        sql = f"SELECT * FROM tblBusses"
        total = 0
        for row in c.execute(sql):
            BusID, Destination, Price, Capacity, Morning, Sold1, Afternoon, Sold2, Evening, Sold3 = row
            lTotal = (Sold1*Price)+(Sold2*Price)+(Sold3*Price)
            print(f"{Destination}:  Total = {lTotal}$")
            total += lTotal
        print(f"\nTotal: {total}$")
 

def getBus(inpStr):
    a = []
    for i in c.execute("SELECT BusID FROM tblBusses ORDER BY BusID DESC"):
        a.append(i[0])
    vals = list(range(1,a[0]+1))
    vals.append(-1)
    return ErrorCheck.CheckInput(inpStr, vals, int)
 
 
 
def PrintOne(bus):
    if bus == "general":
        print("General")
        sql = f"SELECT * FROM tblBusses"
        for row in c.execute(sql):
            BusID, Destination, Price, Capacity, Morning, Sold1, Afternoon, Sold2, Evening, Sold3 = row
            print(BusID, Destination, Price,"$")
    else:
        sql = f"SELECT * FROM tblBusses WHERE BusID = \"{bus}\""
        for row in c.execute(sql):
            BusID, Destination, Price, Capacity, Morning, Sold1, Afternoon, Sold2, Evening, Sold3 = row
            left1 = Capacity-Sold1
            left2 = Capacity-Sold2
            left3 = Capacity-Sold3
            print(f"{Destination}: \nPrice:{Price}$ \n{Morning}: {left1} Tickets Left \n{Afternoon}: {left2} Tickets Left \n{Evening}: {left3} Tickets Left")
 
def PrintBusses():
    PrintOne("general")
    print("\n\n")
    inp = getBus("Enter the BusID of the bus you want to see details for, or -1 to cancel: ")
    if inp == -1:
        print("Canceling...")
        return
    else:
        PrintOne(inp)
        if ErrorCheck.CheckInput("Do you want to buy a ticket for this bus? Y/N",["Y","N"], str) == "Y":
            times = getTimes(inp)
            if len(times) > 0:
                t = ErrorCheck.CheckInput(f"What available time would you like to buy a ticket for (Fully booked times are not shown):\n{times}",list(range(1,len(times)+1)), int)
                if len(times) < 3:
                    if ta != 0:
                        t+=1
                    if tb != 0 and t == 2:
                        t=3
                Buy(inp, t)
            else:
                print("All tickets are fully booked")
        else:
            return
 
def Buy(Bus, time):
    print("\n\n")
    print("Bus",Bus, "Purchased   Time" ,time)
    c.execute(f"UPDATE tblBusses SET Sold{time} = Sold{time} + 1 WHERE BusID = ?",(Bus,))
    print("Thank for buying a ticket")
    print("PointOfSale: \n")
 
def getTimes(bus):
    times = []
    for i in c.execute("SELECT Morning,Afternoon,Evening from tblBusses WHERE BusID = ?", (bus,)):
        times = list(i)
 
    for i in c.execute("SELECT Capacity,Sold1,Sold2,Sold3 from tblBusses WHERE BusID = ?", (bus,)):
        Capacity, Sold1, Sold2, Sold3 = i
        global ta,tb
        if Capacity-Sold1 < 1:
            ta = times.pop(0)
        if Capacity-Sold2 < 1:
            tb = times.pop(1)
        if Capacity-Sold3 < 1:
            times.pop(2)
 
    return times
 

