import pandas as pd

def convertDataToBarChart(drugname,grouping="manufacturer",counter = "Any Outcome"):
    main_df = pd.read_csv("./Data/ReactData_"+drugname+".csv",sep = ',', dtype = {'p_id': 'int','age': 'float','wt': 'float','sex': 'str','manufacturer': 'str','country': 'str','Death': 'int','Disabled': 'int','Birth Defects': 'int','Life Threatening': 'int','Hospitalization': 'int','Required Intervention': 'int','Any Outcome': 'int','Name': 'str','Description': 'str','Age_Grp': 'str','Wt_Grp': 'str','Adverse Event': 'str'})
    df2 = pd.DataFrame({'Adverse Event': pd.Series(dtype='str'),
                    "manufacturer": pd.Series(dtype='str'),
                   'Count': pd.Series(dtype='int'),
                   'Death': pd.Series(dtype='int'),
                   'Adjusted Count': pd.Series(dtype='float')
                   })
    #print(main_df)
    all_groups = main_df[grouping].unique()
    groupCts={}
    for group in all_groups:
        groupCts[group]=main_df.loc[main_df[grouping] == group, counter].sum()
    #print(groupCts)
    
    manufList = main_df['manufacturer'].unique()
    aeList = main_df['Adverse Event'].unique()
    #print(df2)
    for ae in aeList:
        dfAE = main_df.loc[main_df['Adverse Event'] == ae]
        for manuf in manufList:
            dfManuf = dfAE.loc[dfAE['manufacturer'] == manuf]
            #print(dfManuf)
            ct = dfManuf['Any Outcome'].sum()
            row = [ae,manuf,ct,dfManuf['Death'].sum(),ct/groupCts[group]]
            #print (row)
            df2.loc[len(df2.index)] = row
            #print(df2)
            
    #print(df2)
    with open("./BarChart/BAR_"+drugname+"_main.json",'w') as data:
        with open("./BarChart/AE_BAR_"+drugname+".txt",'w') as subdata:
            aeIter = iter(aeList)
            ae = next(aeIter)
            #print(ae)
            df = df2.loc[df2['Adverse Event'] == ae]
            writeAE(data,ae,df['Count'].sum(),df['Death'].sum())
            subdata.write(ae+'$[')
            manufIter = iter(manufList)
            manuf=next(manufIter)
            
            writeAESubGroup(subdata,manuf,df.loc[df['manufacturer'] == manuf].iloc[0]['Count'],df.loc[df['manufacturer'] == manuf].iloc[0]['Death'],groupCts[manuf])
            for manuf in manufIter:
                subdata.write(',')
                writeAESubGroup(subdata,manuf,df.loc[df['manufacturer'] == manuf].iloc[0]['Count'],df.loc[df['manufacturer'] == manuf].iloc[0]['Death'],groupCts[manuf])
            subdata.write(']\n')
            
            
            for ae in aeIter:
                #print(ae)
                data.write(',')
                df = df2.loc[df2['Adverse Event'] == ae]
                writeAE(data,ae,df['Count'].sum(),df['Death'].sum())
                subdata.write(ae+'$[')
                manufIter = iter(manufList)
                manuf=next(manufIter)
                writeAESubGroup(subdata,manuf,df.loc[df['manufacturer'] == manuf].iloc[0]['Count'],df.loc[df['manufacturer'] == manuf].iloc[0]['Death'],groupCts[manuf])
                for manuf in manufIter:
                    subdata.write(',')
                    writeAESubGroup(subdata,manuf,df.loc[df['manufacturer'] == manuf].iloc[0]['Count'],df.loc[df['manufacturer'] == manuf].iloc[0]['Death'],groupCts[manuf])
                subdata.write(']\n')
    #return df2
    #print(df2)


def readReacFile(fileName):
    print(fileName)
    return 

def handleSub(outfile,ae,df,total):
    for index, row in df.iterrows():
        outfile.write(ae)


def getAEJson(drugname,ae):
    #with open("./BarData/"+drugname+".txt",'r') as f:
    with open("./BarChart/AE_BAR_"+drugname+".txt",'r') as f:
        for x in f:
            
            loc = x.find('$')
            print(x[:loc])
            if x[:loc] == ae:
                return x[loc+1:]
def writeAE(file,ae,ct,death):
    file.write('{"AE":"')
    file.write(str(ae))
    file.write('","Count":')
    file.write(str(ct))
    if ct ==0:
        ct = 1
    file.write(',"% Death":')
    file.write(str(death/ct))
    file.write('}')

def writeAESubGroup(file,manuf,ct,death,total):
    file.write('{"manufacturer":"')
    file.write(str(manuf))
    file.write('","Count":')
    file.write(str(ct))
    if ct ==0:
        ct = 1
    file.write(',"% Death":')
    file.write(str(death/ct))
    file.write(',"Adj Count":')
    file.write(str(ct/total))
    file.write('}')
#convertDataToBarChart("ALCOHOL")

def barChartPreproc():
    i=0
    with open("./DrugList.txt",'r') as f:
        for line in f:
            dr = line.strip() 
            print(i, dr)
            convertDataToBarChart(dr)
            i+=1
