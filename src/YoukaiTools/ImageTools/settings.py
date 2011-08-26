verbosity = 0

def vmessage(message, v):
    if verbosity >= v:
        print(message)
