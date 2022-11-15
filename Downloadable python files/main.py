import ErrorCheck
import ReachDatabase
from rich.console import Console
from rich.text import Text

#Init console
console = Console()

#init db at launch
ReachDatabase.Init()
 
#main
while True:
    text = Text("\nMain Menu:")
    text.stylize("bold magenta")
    console.print(text)
    #Get input of user action
    inp = ErrorCheck.CheckInput("What would you like to access? \n1. Admin Menu \n2. Show bussess\n: ", [1,2], int)
    match inp:
        # run admin menu if user chooses
        case 1:
            ReachDatabase.AdminMenu()
        # show busses if user chooses
        case 2:
            ReachDatabase.PrintBusses()
