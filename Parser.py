class InvalidArgumentError(ValueError):
    pass

def periodOpt(p):
    valid_options = ['M1', 'M5', 'M15', 'M30', 'H1', 'H4', 'D1']
    if p not in valid_options:
        raise InvalidArgumentError("Invalid period options")
def formatOpt(p):
    valid_options = ['CSV','JSON']
    if p not in valid_options:
        raise InvalidArgumentError("Invalid format options")  
def parOpt(p):
    valid_options = ['BRENTCMDUSD','BTCUSD','EURUSD','GBPUSD','USA30IDXUSD','USA500IDXUSD','USATECHIDXUSD','XAGUSD','XAUUSD']
    if p not in valid_options:
        raise InvalidArgumentError("Invalid PAR options") 
def is_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def reqStructure(list):
    starting_index=0
    if len(list)!=5 and len(list)!=7:
        raise InvalidArgumentError("Lack arguments") 
    if list[1]=="-p":
        periodOpt(list[2])
        starting_index=2
    elif list[starting_index+1]!="-f":
        raise InvalidArgumentError("-f flag is missing") 
    elif list[starting_index+3]!="-m":
        raise InvalidArgumentError("-m flag is missing")
    
    formatOpt(list[starting_index+2])
    parOpt(list[starting_index+4])
def buyStructure(list):
    if list[1]!="-m":
        raise InvalidArgumentError("-m flag is missing")
    
    else:
      parOpt(list[2])
    if not is_number(list[3]):
        raise InvalidArgumentError("number of actions to buy must be an integer")