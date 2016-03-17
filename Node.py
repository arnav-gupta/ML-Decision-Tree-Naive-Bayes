class Node:
    descend = []
    X = ""

    
    def __init__(self, val, dictionary):
        self.fixSet(val)
        self.getChild(dictionary)
        
    def getChild(self, dictionary):
        if(isinstance(dictionary, dict)):
            self.descend = dictionary.keys()
    def fixSet(self, val):
        self.X = val
            
    def __str__(self):
        return str(self.X)
    

