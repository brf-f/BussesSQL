import ErrorCheck
import ReachDatabase
 
#init db at launch
ReachDatabase.Init()
 
#main
while True:
    print("\n\n Main Menu:\n")
    #Get input of user action
    inp = ErrorCheck.CheckInput("What would you like to access? \n1. Admin Menu \n2. Show bussess\n ", [1,2], int)
    match inp:
        # run admin menu if user chooses
        case 1:
            print("Admin Menu accessed")
            ReachDatabase.AdminMenu()
        # show busses if user chooses
        case 2:
            print("\n\nShowing Busses")
            ReachDatabase.PrintBusses()
