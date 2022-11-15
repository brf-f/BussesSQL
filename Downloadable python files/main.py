import ErrorCheck
import ReachDatabase
from rich.console import Console
from rich.text import Text

#Init console
console = Console()

def welcome():
    txt = """\n\n
   ___              ____ _       _        _   _                 __           _                 
  / __\_   _ ___   /__   (_) ___| | _____| |_(_)_ __   __ _    / _\_   _ ___| |_ ___ _ __ ___  
 /__\// | | / __|    / /\/ |/ __| |/ / _ \ __| | '_ \ / _` |   \ \| | | / __| __/ _ \ '_ ` _ \ 
/ \/  \ |_| \__ \   / /  | | (__|   <  __/ |_| | | | | (_| |   _\ \ |_| \__ \ ||  __/ | | | | |
\_____/\__,_|___/   \/   |_|\___|_|\_\___|\__|_|_| |_|\__, |   \__/\__, |___/\__\___|_| |_| |_|
                                                      |___/        |___/                       
    
    
    Code can be found at: https://github.com/bruno-ff/BussesSQL   
    
    Made by:  Bruno F.  and  Jack T.
         
    Using:
    
        •Python
        •SQL
    \n\n"""
    text = Text(txt)
    #Title style
    text.stylize("bold blink #99ECD9", 0, 590)
    #code found style
    text.stylize("bold #FFE2BA", 590, 615)
    #Link style
    text.stylize("underline magenta", 615, 652)
    #Made by style
    text.stylize("#E67E22", 660, 700)
    #Bold names style
    text.stylize("bold", 669, 684)
    text.stylize("bold", 688, 702)
    #Using langs style
    text.stylize("green", 700, 760)
    text.stylize("bold", 730, 760)
    console.print(text)
    
    input("\nPress [Enter] to start the program\n: ")
    print("\n\n\n")

#init db at launch
ReachDatabase.Init()
 
#main
def main():
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

welcome()
main()