import math



def freq_check(param, basedata, target):
    val_count = {}
    m = 0
    valmax = ""
    index = param.index(target)
    for row in basedata:
        if (val_count.has_key(row[index])):
            val_count[row[index]] += 1 
        else:
            val_count[row[index]] = 1
    for key in val_count.keys():
        if val_count[key]>m:
            m = val_count[key]
            valmax = key
    return valmax


def entropy(param, basedata, targetAttr):
    val_count = {}
    basedataEnt = 0.0
    i = 0
    for entry in param:
        if (targetAttr == entry):
            break
        ++i
    for entry in basedata:
        if (val_count.has_key(entry[i])):
            val_count[entry[i]] += 1.0
        else:
            val_count[entry[i]]  = 1.0
    for val in val_count.values():
        basedataEnt += (-val/len(basedata)) * math.log(val/len(basedata), 2) 
    return basedataEnt

def calc_gain(param, basedata, attr, targetAttr):
    val_count = {}
    sub_entropy = 0.0
    i = param.index(attr)
    for entry in basedata:
        if (val_count.has_key(entry[i])):
            val_count[entry[i]] += 1.0
        else:
            val_count[entry[i]]  = 1.0
    for val in val_count.keys():
        valProb        = val_count[val] / sum(val_count.values())
        basedataSubset     = [entry for entry in basedata if entry[i] == val]
        sub_entropy += valProb * entropy(param, basedataSubset, targetAttr)
    return (entropy(param, basedata, targetAttr) - sub_entropy)

 
def chooseAttr(basedata, param, target):
    cortattr = param[0]
    mGain = 0
    for attr in param:
        if (attr != target):
            #print "chooseattr=" + str(attr)
            revisedGain = calc_gain(param, basedata, attr, target)
            #print "attr=" + str(attr) + "revisedGain" + str(revisedGain) 
            if (revisedGain > mGain):
                mGain = revisedGain
                cortattr = attr
    return cortattr

 
def allData(basedata, param, attr):
    index = param.index(attr)
    values = []
    for entry in basedata:
        if entry[index] not in values:
            if entry[index] != '?':
                values.append(entry[index])
        #print "values=" + str(values)
    return values

def getContinuous(basedata, param, cortattr):
    rows = [[]]
    allEntry = []
    intvList = []
    index = param.index(cortattr)
    #print "cortattr" + cortattr
    for entry in basedata:
        if (entry[index] != '?'):
	    try:
            	allEntry.append(float(entry[index]))
	    except ValueError:
		import pudb
		pudb.set_trace()
        else:
            allEntry.append(0)
    maxL = max(allEntry)
    minL = min(allEntry)
    intl = minL
    intvl = 0.1*(float(maxL)-float(minL))
    intvList.append(minL)
    for i in range(1,10):
        intl=intl+intvl
        intvList.append(intl)
        
    intvList.append(maxL)
    #print "intvList" + str(intvList)
    for entry in basedata:
        newEntry = []
        for i in range(0,len(entry)):
	    #newEntry = []
            if(i != index):
                newEntry.append(entry[i])
            else:
                for l in range(0,11):
                    if (entry[index] != '?'):
                        if (float(entry[i]) <= intvList[l]):
                            if (l != 0):
                                if ((intvList[l]-float(entry[i]))<=(float(entry[i])-intvList[l-1])):
                                    newEntry.append(float("{0:.1f}".format(intvList[l])))
                                else:
                                    newEntry.append(float("{0:.1f}".format(intvList[l-1])))
                                break
                            else:
                                newEntry.append(float("{0:.1f}".format(intvList[l])))
                                break
                    else:
                        #print "question mark training" + str(freq_check(param, basedata, cortattr))
                        newEntry.append(freq_check(param, basedata, cortattr))
        rows.append(newEntry)       
    rows.remove([])
    return rows, intvList

def getContinuousTest(basedata, param, cortattr, Acomp) :
    rows = [[]]
    #newEntry = []
    index = param.index(cortattr)
    #print "index = " + str(index) 
    for entry in basedata:
        newEntry = []
        for i in range(0,len(entry)):
            if(i != index):
                newEntry.append(entry[i])
            else:
                #for l in range(0,11):
		if entry[i] > max(Acomp):
		    newEntry.append(float("{0:.1f}".format(max(Acomp))))
		    continue
	
                if entry[i] < min(Acomp):
                    newEntry.append(float("{0:.1f}".format(min(Acomp))))
                    continue

                if (entry[i] != '?'):
		    for l in range(0,11):
                        #print "index=" + str(index) + "entry = " + str(entry[index])
			try:
			    q = float(entry[i])
			except ValueError:
			    import pudb
			    pudb.set_trace()
                        if (float(entry[i]) <= Acomp[l]):
                    	    if (l != 0):
                                if ((Acomp[l]-float(entry[i]))<=(float(entry[i])-Acomp[l-1])):
                                    newEntry.append(float("{0:.1f}".format(Acomp[l])))
                                else:
                                    newEntry.append(float("{0:.1f}".format(Acomp[l-1])))
                                break
                	    else:
                                newEntry.append(float("{0:.1f}".format(Acomp[l])))
                                break
         
              	else:
                    newEntry.append(float("{0:.1f}".format(Acomp[5])))
        rows.append(newEntry)       
    rows.remove([])
    return rows

    
    
    
def getData(basedata, param, cortattr, val):
    rows = [[]]
    index = param.index(cortattr)
    for entry in basedata:
        if (entry[index] == val):
            newEntry = []
            for i in range(0,len(entry)):
                if(i != index):
                    newEntry.append(entry[i])
            rows.append(newEntry)
    rows.remove([])
    return rows


def ID(basedata, param, target):
    basedata = basedata[:]
    
    currentval = [record[param.index(target)] for record in basedata]
    default = freq_check(param, basedata, target)

    if not basedata or (len(param) - 1) <= 0:
        return default
    elif currentval.count(currentval[0]) == len(currentval):
        return currentval[0]
    else:
        cortattr = chooseAttr(basedata, param, target)
        #print"cortattr====="+str(cortattr)
        tree = {cortattr:{}}
        
    
        for data in allData(basedata, param, cortattr):
            #print "cortattr" + cortattr +"data:" + str(data)
            examples = getData(basedata, param, cortattr, data)
	    newAttr = param[:]
            newAttr.remove(cortattr)
            
            #examples = getData(basedata, param, cortattr, data)
            #print "examples=" + str(examples)
            branch = ID(examples, newAttr, target)
            
            #print "branch=" + str(branch)
            '''
            if (branch != '+' and branch != '-'):
                tD = tree[tree.keys()[0]]
                if (branch in tD.values()):
                    print " branch pruned" + str(branch)
                    continue
    '''
            # Add the new branch to the empty d    ictionary object in our new
            # tree/node we just created.
            tree[cortattr][data] = branch
    
    return tree
    
