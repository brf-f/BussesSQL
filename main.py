import InitialiseSQL
import sqlite3
import ErrorCheck
import ReachDatabase
 
#init db
ReachDatabase.Init()
 
#main
while True:
    print("\n\n Main Menu:\n")
    inp = ErrorCheck.CheckInput("What would you like to access? \n1. Admin Menu \n2. Show bussess\n ", [1,2], int)
    match inp:
        case 1:
            print("Admin Menu accessed")
            ReachDatabase.AdminMenu()
        case 2:
            print("\n\nShowing Busses")
            ReachDatabase.PrintBusses()
