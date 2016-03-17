import DecisionTree
import Node
import time
def main():
    row1 = 0
    count = 0
    accuracy = 0
    orig_op = []
    print "Training Naive-Bayes ..."
    tic = time.clock()

    file1 = open('CreditTraining.csv')
    finattr = "class"
    base1 = [[]]
    baseT1 = [[]]
    basedata = [[]]
    basedata1 = [[]]
    basedata2 = [[]]
    for line in file1:
        line = line.strip("\r\n")
        basedata.append(line.split(','))
        
    basedata.remove([])
    #print " base main "+str(basedata)
    parameters = basedata[0]
    basedata.remove(parameters)
   
    #import pudb
    #pudb.set_trace() 
    #base1, A2 = DecisionTree.getContinuous(basedata, parameters, parameters[1])
    #base1, A3 = DecisionTree.getContinuous(base1, parameters, parameters[2])
    #base1, A8 = DecisionTree.getContinuous(base1, parameters, parameters[7])
    #base1, A11 = DecisionTree.getContinuous(base1, parameters, parameters[10])
    #base1, A14 = DecisionTree.getContinuous(base1, parameters, parameters[13])
    #base1, A15 = DecisionTree.getContinuous(base1, parameters, parameters[14])
    
    #print " base final " + str(base1)
    #print " A2 " + str(A2)
    #print " A3" + str(A3)
    #print " A8 " + str(A8)
    #print " A11 " + str(A11)
    #print " A14 " + str(A14)
    #Run ID3'''
    
    tree = DecisionTree.ID(basedata, parameters, finattr)
    #print "generated decision tree"+ str(tree)
    f = open('Credit.csv')
    for line in f:
        line = line.strip("\r\n")
        basedata1.append(line.split(','))
    basedata1.remove([])
    #import pudb
    #pudb.set_trace()
    '''baseT1= DecisionTree.getContinuousTest(basedata1, parameters, parameters[1],A2)
    #print "based="+str(basedata1)
    #print "baset="+str(baseT1)
    baseT1= DecisionTree.getContinuousTest(baseT1, parameters, parameters[2],A3)
    baseT1= DecisionTree.getContinuousTest(baseT1, parameters, parameters[7],A8)
    #import pudb
    #pudb.set_trace()
    baseT1= DecisionTree.getContinuousTest(baseT1, parameters, parameters[10],A11)
    baseT1= DecisionTree.getContinuousTest(baseT1, parameters, parameters[13],A14)
    baseT1= DecisionTree.getContinuousTest(baseT1, parameters, parameters[14],A15)'''
    #print " baseT1 " + str(baseT1)
    #import pudb
    #pudb.set_trace()
    for entry in basedata1:
        row1 += 1
        train_data = tree.copy()
        output = ""
        #import pudb
	#pudb.set_trace() 
        while(isinstance(train_data, dict)):
            root = Node.Node(train_data.keys()[0], train_data[train_data.keys()[0]])
            
            train_data = train_data[train_data.keys()[0]]
            index = parameters.index(root.X)
            value = entry[index]
            if(value in train_data.keys()):
                Node.Node(value, train_data[value])
                output = train_data[value]
                train_data = train_data[value]
            else:
                #print " value break at " + str(value)
                
                #print "can't process input %s" % count
                output = DecisionTree.freq_check(parameters, basedata, parameters[15])
                break
                
        orig_op.append(output)
        #print ("row%s = %s" % (row1, output))

    #print "written program"
    
    f1 = open('classcredit.csv')
    for line in f1:
        line = line.strip("\r\n")
        basedata2.append(line)
    basedata2.remove([])
    i = 0
    for ent in basedata2:
        #print "orig_op[i] " + str(orig_op[i]) + "ent = " + ent
        if (ent == orig_op[i]):
            count += 1
        i += 1
    accuracy = (int)(count/100)
    
    print "Calculated accuracy for the testing data = "+ str(count)
        
    
    
    

    
if __name__ == '__main__':
    main()
