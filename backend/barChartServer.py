def getAEJson(drugname,ae):
    with open("./BarChart/AE_BAR_"+drugname+".txt",'r') as f:
        for x in f:
            
            loc = x.find('$')
            #print(x[:loc])
            if x[:loc] == ae:
                return x[loc+1:].strip()

def getDrugJson(drugname):
    with open("./BarChart/BAR_"+drugname+"_main.json",'r') as f:
        return '['+f.readline().strip()+']'
