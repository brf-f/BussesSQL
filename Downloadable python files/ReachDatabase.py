from rich.console import Console
from rich.table import Table
import sqlite3
import sys
import ErrorCheck
import InitialiseSQL
from rich.text import Text
from rich.prompt import Prompt, Confirm

# connect to database and get cursor
conn = sqlite3.connect("Busses.db")
c = conn.cursor()

#Init console
console = Console()
confirmAsk = Text("Would you like to proceed with what you entered?")
confirmAsk.stylize("red")

#Init ta and tb variables with 0
ta = 0
tb = 0
 
# Init function runs InitialiseSQL with proper variables to create the table with proper values if needed.
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
    
    print("\n\n")
 
 
# getNewVals gets new proper values for any field to be used for editing or adding records.
def getNewVals(fieldInt, Bus):
    
    # Initialise variable with Error value
    field = "ERROR"
    newVal = "ERROR"
    
    # Change field and newVal to their correct values according to user input
    
    #Bus ID field
    if fieldInt == 1:
        text = Text("Cannot change BUS ID")
        text.stylize("bold red on white")
        console.print(text)
        return
     
    #Destination field
    elif fieldInt == 2:
        field = "Destination"
        is_correct = False
        while not is_correct:
            newVal = ErrorCheck.CheckInput("\n\nWhat should the new bus destination be?\n: ","noList",str)
            is_correct = Confirm.ask(confirmAsk)
     
    #Price field
    elif fieldInt == 3:
        field = "Price"
        is_correct = False
        while not is_correct:
            newVal = ErrorCheck.CheckInput("\n\nWhat should the new bus ticket Price be?\n: ","positive",int)
            is_correct = Confirm.ask(confirmAsk)
     
    #Capacity field
    elif fieldInt == 4:
        field = "Capacity"
        is_correct = False
        while not is_correct:
            newVal = ErrorCheck.CheckInput("\n\nWhat should the new bus Capacity be?\n: ","positive",int)
            is_correct = Confirm.ask(confirmAsk)
        # Set all sold values back to 0 to prevent more seats sold than capacity
        c.execute("UPDATE tblBusses SET Sold1 = 0, Sold2 = 0, Sold3 = 0 WHERE BusID = ?",(Bus,))
        print("New capacity set and all sold tickets reset")
     
    #Time fields
    elif fieldInt == 5 or fieldInt == 7 or fieldInt == 9:
        is_correct = False
        while not is_correct:
        
            if fieldInt == 5:
                field = "Morning"
                print("\n\nChanging ",field," time.\n")
            elif fieldInt == 7:
                field = "Afternoon"
                print("\n\nChanging ",field," time.\n")
            elif fieldInt == 9:
                field = "Evening"
                print("\n\nChanging ",field," time.\n")
            else:
                print("Field int Error, Field Int: ", fieldInt)
    
            valArr = []
            
            # Change time one digit at a time to check for a valid time value
            for i in range(5):
                
                # Print as neat table
                table = Table(title="Time",box=None)
                table.add_column("", style="#A3E4D7")
                table.add_column("", style="#A3E4D7")
                table.add_column("  ", style="#A3E4D7")
                table.add_column("", style="#A3E4D7")
                table.add_column("", style="#A3E4D7")	
                
                x=9
                
                if i == 0:
                    x=2
                elif i == 1 and valArr[0] == 2:
                    x=4
                elif (i == 3 or i == 4) and valArr[0] == 2 and valArr[1] == 4:
                    x=0
                elif i == 3:
                    x=5
                
                match len(valArr):
                        case 0:
                            table.add_row("_","_",":","_","_")
                        case 1:
                            table.add_row(str(valArr[0]),"_",":","_","_")
                        case 2:
                            table.add_row(str(valArr[0]),str(valArr[1]),":","_","_")
                        case 4:
                            table.add_row(str(valArr[0]),str(valArr[1]),":",str(valArr[3]),"_")
                
                if len(valArr) != 3: 
                    console.print(table)
                    print("\n")
                
                if i == 2:
                    valArr.append(":")
                else:
                    
                    valArr.append(ErrorCheck.CheckInput("Enter a digit for the time\n:",list(range(x+1)),int))
                    print("\n")
            
            # Print as neat table
            table = Table(title="Time",box=None)
            table.add_column("", style="#A3E4D7")
            table.add_column("", style="#A3E4D7")
            table.add_column("  ", style="#A3E4D7")
            table.add_column("", style="#A3E4D7")
            table.add_column("", style="#A3E4D7")	
                    
            table.add_row(str(valArr[0]),str(valArr[1]),":",str(valArr[3]),str(valArr[4]))
            console.print(table)
    
            #Join all time digits together for final time
            newVal = "".join(map(str, valArr))
            is_correct = Confirm.ask(confirmAsk)
        print("\n",newVal, " set as new time\n\n")
     
    #Sold fields
    elif fieldInt == 6 or fieldInt == 8 or fieldInt == 10:
        if fieldInt == 6:
            field = "Sold1"
        if fieldInt == 8:
            field = "Sold2"
        if fieldInt == 10:
            field = "Sold3"
 
        c.execute(f"SELECT Capacity FROM tblBusses WHERE BusID = {Bus}")
        cap = c.fetchone()[0]
        is_correct = False
        while not is_correct:
            newVal = ErrorCheck.CheckInput("What should the new sold tickets be? (Cannot be higher than capacity)\n:",range(cap+1),int)
            is_correct = Confirm.ask(confirmAsk)
        print("sold tickets")
        
    # return the field and new value
    return field, newVal
 
# addRoute() creates a new record
def addRoute():
    
    # Set Bus variable = to the largest ID +1
    a = []

    for i in c.execute("SELECT BusID FROM tblBusses ORDER BY BusID DESC"):
        a.append(i[0])
    
    Bus = a[0]+1
       
    # Create the record with the new ID and default values
    c.execute("INSERT INTO tblBusses VALUES (?,?,?,?,?,?,?,?,?,?)",(Bus, "Default destination", 10, 10, "11:00", 0, "14:00", 0, "19:00",0 ))
 
    # Edit each other value of the new record
    for f in range(2,11):
        vals = getNewVals(f, Bus)
        field = vals[0]
        newVal = vals[1]
 
        c.execute(f"UPDATE tblBusses SET {field} = ? WHERE BusID = ?",(newVal,Bus,))
        
    print("Adding Route")
 
# editRoute() edits a field within a record
def editRoute():
    # Get bus and field that need to be changed
    Bus = getBus("\n\nEnter ID of Bus you would like to change the route of\n: ")
    field = ErrorCheck.CheckInput("\nWhich field would you like to change? 1. BusId | 2. Destination | 3. Price | 4. Capacity | 5. Morning Time | 6. Sold1 | 7. Afternoon Time | 8. Sold2 | 9. Evening Time | 10. Sold3 |\n:", list(range(1,11)), int)
 
    # get the new values
    vals = getNewVals(field, Bus)
    field = vals[0]
    newVal = vals[1]
 
    # Update db
    c.execute(f"UPDATE tblBusses SET {field} = ? WHERE BusID = ?",(newVal,Bus,))
    print("\nRecord Updated\n\n")
 
# ChangeRoutes() redirects the user to the correct function add/delete/or edit route
def ChangeRoutes():
    print("\n\n")
    
    text = Text("\nAdmin Edit Menu:")
    text.stylize("bold red")
    console.print(text)
    # Get action user wants to do
    actn = ErrorCheck.CheckInput("Would you like to: \n1. Add Routes\n2. Delete Routes \n3. Edit routes\n4. Cancel\n: ", [1,2,3], int)
    #Run the appropriate function
    match actn:
        case 1:
            addRoute()
        case 2:
            print("\n\n")
            is_correct = False
            while not is_correct:
                Bus = getBus("Enter ID of Bus route you want to delete: ")
                is_correct = Confirm.ask(confirmAsk)
            c.execute("DELETE FROM tblBusses WHERE BusID = ?",(Bus,))
            text = Text(f"\n\nDELETED RECORD {Bus}\n\n")
            text.stylize("bold red on white")
            console.print(text)
        case 3:
            editRoute()
        case 4:
            text = Text("Canceling...\n")
            text.stylize("red")
            console.print(text)
            return
 
 
# AdminMenu() redirects user to correct function for action
def AdminMenu():
    print("\n\n")
 
    text = Text("\nAdmin Menu:")
    text.stylize("bold #DC7633")
    console.print(text)
    # Get user action input
    inp = ErrorCheck.CheckInput("Would you like to do:\n1. Add/Delete/Edit Routes\n2. Print Revenues\n3. Reset Table\n4. Exit Program\n5. Cancel\n: ", [1,2,3,4,5], int)
   
    #Do the appropriate action or run appropriate function
    match inp:
        case 1:
            ChangeRoutes()
        case 2:
            print("\n\n")
            printRev()
        case 3:
            c.execute("DROP TABLE tblBusses")
            conn.commit()
            Init()
            text = Text("\n\nRESET TABLE\n\n")
            text.stylize("bold red on white")
            console.print(text)
        case 4:
            text = Text("\n\nExiting Program")
            text.stylize("bold red on white")
            console.print(text)
            #Commit changes to db and close connection
            conn.commit()
            conn.close()
            #exit program
            sys.exit()
        case 5:
            text = Text("Canceling...\n")
            text.stylize("red")
            console.print(text)
            return      
 
# printRev() redirects user to print overall or specific revenue
def printRev():
    text = Text("\nAdmin Revenue Menu:")
    text.stylize("bold #87FC79")
    console.print(text)
    #get user action
    actn = ErrorCheck.CheckInput("Would you like to: \n1. Print Overall revenue\n2. Print specific revenue\n3. Cancel\n: ", [1,2], int)
    #run the printOneRev() function with the correct parametres
    match actn:
        case 1:
            printOneRev("ALL")
 
        case 2:
            Bus = getBus("\n\nWhich bus would you like to print revenue for? [enter ID]")
            printOneRev(Bus)
        case 3:
            text = Text("Canceling...\n")
            text.stylize("red")
            console.print(text)
            return
 
# printOneRev() prints revenues
def printOneRev(Bus):
    #Printing revenue for specific bus
    if Bus != "ALL":
                        #Print as neat table
        table = Table(title="Bus information")

        table.add_column("Destination", style="magenta")
        table.add_column("Price", style="green")
        table.add_column("Morning", style="#3437EE")
        table.add_column("Sold", style="#EEA119")
        table.add_column("Revenue", style="green")
        table.add_column("Afternoon", style="#3437EE")
        table.add_column("Sold", style="#EEA119")
        table.add_column("Revenue", style="green")
        table.add_column("Evening", style="#3437EE")
        table.add_column("Sold", style="#EEA119")
        table.add_column("Revenue", style="green")
        table.add_column("Total", style="green")
        
        print("\n\nPrinting revenue for ", Bus,"\n")
        #Select all variables from correct bus
        sql = f"SELECT * FROM tblBusses WHERE BusID = \"{Bus}\""
        for row in c.execute(sql):
            #Print all needed variables
            BusID, Destination, Price, Capacity, Morning, Sold1, Afternoon, Sold2, Evening, Sold3 = row
            table.add_row(str(Destination), str(Price)+" $", str(Morning), str(Sold1), str(Sold1*Price)+" $", str(Afternoon), str(Sold2), str(Sold2*Price)+" $", str(Evening), str(Sold3), str(Sold3*Price)+" $", str((Sold1*Price)+(Sold2*Price)+(Sold3*Price))+" $")
        
        console.print(table)
        print("\n\n")
    
    #Print a more generic revenue for all busses
    else:
        #Print as neat table
        table = Table(title="Bus Revenue")

        table.add_column("Destination", style="magenta")
        table.add_column("Total", style="green")
        
        print("\n\nPrinting revenue for ", Bus,"\n")
        sql = f"SELECT * FROM tblBusses"
        total = 0
        #Print generic revenue of each bus
        for row in c.execute(sql):
            BusID, Destination, Price, Capacity, Morning, Sold1, Afternoon, Sold2, Evening, Sold3 = row
            lTotal = (Sold1*Price)+(Sold2*Price)+(Sold3*Price)
            table.add_row(str(Destination), str(lTotal)+" $")
            total += lTotal
        #Print total of all combined
        table.add_row("", "")
        table.add_row("Combined Total", str(total)+" $")
        console.print(table)
        print("\n\n")
 
# getBus() Checks if user bus ID input is valid
def getBus(inpStr):
    #Init empty vals list
    vals = []
    for i in c.execute("SELECT BusID FROM tblBusses"):
        vals.append(i[0])
    # Add -1 to Vals array for canceling the action
    vals.append(-1)
    # return an errorchecked input
    return ErrorCheck.CheckInput(inpStr, vals, int)
 
 
# PrintOne() prints busses info
def PrintOne(bus):
    #General busses info
    if bus == "general":
        
        print("\n\n")
        #Print as neat table
        table = Table(title="General Busses information")

        table.add_column("Bus ID", style="cyan", no_wrap=True)
        table.add_column("Destination", style="magenta")
        table.add_column("Price", style="green")
        
        #Select all busses and print needed values
        sql = f"SELECT * FROM tblBusses"
        for row in c.execute(sql):
            BusID, Destination, Price, Capacity, Morning, Sold1, Afternoon, Sold2, Evening, Sold3 = row
            table.add_row(str(BusID), str(Destination), str(Price)+" $")

        console.print(table)
    #A specific bus's info
    else:
        print("\n\n")
                #Print as neat table
        table = Table(title="Bus information")

        table.add_column("Destination", style="magenta")
        table.add_column("Price", style="green")
        table.add_column("Morning", style="#3437EE")
        table.add_column("Tickets", style="#EEA119")
        table.add_column("Afternoon", style="#3437EE")
        table.add_column("Tickets", style="#EEA119")
        table.add_column("Evening", style="#3437EE")
        table.add_column("Tickets", style="#EEA119")
        
        #Select specific bus and print all needed values
        sql = f"SELECT * FROM tblBusses WHERE BusID = \"{bus}\""
        for row in c.execute(sql):
            BusID, Destination, Price, Capacity, Morning, Sold1, Afternoon, Sold2, Evening, Sold3 = row
            #Get tickets left for each time
            left1 = Capacity-Sold1
            left2 = Capacity-Sold2
            left3 = Capacity-Sold3
            table.add_row(str(Destination), str(Price)+" $", str(Morning), str(left1), str(Afternoon), str(left2), str(Evening), str(left3))

        console.print(table)
 
# PrintBusses() runs PrintOne() and redirects user to Buying tickets with correct time if necessary
def PrintBusses():
    PrintOne("general")
    print("\n\n")
    #Get user input
    inp = getBus("Enter the BusID of the bus you want to see details for, or -1 to cancel: ")
    if inp == -1:
        text = Text("Canceling...\n")
        text.stylize("red")
        console.print(text)
        return
    else:
        #Print info on bus
        PrintOne(inp)
        #Asks if user wants to buy ticket
        if ErrorCheck.CheckInput("Do you want to buy a ticket for this bus? Y/N",["Y","N"], str) == "Y":
            #set times = to all valid times (have tickets left)
            times = getTimes(inp)
            #If any time still has tickets left ask what VALID time they want a ticket for.
            if len(times) > 0:
                avTimes = times
                match len(times):
                    case 1:
                        avTimes = f"1. {times[0]} "
                    case 2:
                        avTimes = f"1. {times[0]} \n2. {times[1]} "
                    case 3:
                        avTimes = f"1. {times[0]} \n2. {times[1]} \n3. {times[2]}"
                t = ErrorCheck.CheckInput(f"\n\nWhat available time would you like to buy a ticket for (Fully booked times are not shown):\n{avTimes}",list(range(1,len(times)+1)), int)
                #Change the user input to the correct variable based on which times where hidden due to being fully booked.
                if len(times) < 3:
                    if ta != 0:
                        t+=1
                    if tb != 0 and t == 2:
                        t=3
                Buy(inp, t)
                
            #No time has tickets left
            else:
                print("All tickets are fully booked")
        #User does not want to buy tickets
        else:
            return
 
# Buy() buys a ticket for the specified parametres Bus and Time
def Buy(Bus, time):
    print("\n")
    print("Bus",Bus, "Purchased   Time" ,time)
    #Update db with Sold tickets
    c.execute(f"UPDATE tblBusses SET Sold{time} = Sold{time} + 1 WHERE BusID = ?",(Bus,))
    print("Thank you for buying a ticket\n\n")
 
# getTime() gets valid times where tickets are not sold out
def getTimes(bus):
    #Initialise empty times list
    times = []
    
    #Add all times for that bus in the list
    for i in c.execute("SELECT Morning,Afternoon,Evening from tblBusses WHERE BusID = ?", (bus,)):
        times = list(i)
    
    #get the capacity and sold tickets
    for i in c.execute("SELECT Capacity,Sold1,Sold2,Sold3 from tblBusses WHERE BusID = ?", (bus,)):
        Capacity, Sold1, Sold2, Sold3 = i
        global ta,tb
        #For each time check if it is fully booked, if so remove that time from the list - Checking the second time first as it can move when checking other times
        if Capacity-Sold2 < 1:
            #Remove fully booked time from list
            tb = times.pop(1)
        if Capacity-Sold3 < 1:
            #(Getting the list id as last in the list in case other times where also fully booked and changed position of this time)
            times.pop(-1)
        if Capacity-Sold1 < 1:
            ta = times.pop(0)
    # Return all valid times as a list
    return times
 

