from ast import literal_eval
 
# Returns type of input and Capitalises strings
def getType(input):
    try:
        input = literal_eval(input)
        return type(input), input
    except (ValueError, SyntaxError):
        # A string, so return str
        return str, input.capitalize()
 
#checks if user input is valid and expected
def CheckInput(InpStr, expected, type):    
    inp = input(InpStr)
    while True:
        # Get user input type and check if it is the correct type
        getT = getType(inp)
        if getT[0] == type:
            # Check if the user input is in one of the expected defined inputs or if any input is allowed
            if expected == "positive":
                if getT[1] > 0:
                    return getT[1]
            elif expected == "noList" or getT[1] in expected:
                return getT[1]
 
        # Input was invalid run through again
        print("Please enter a valid value")
        inp = input(InpStr)
