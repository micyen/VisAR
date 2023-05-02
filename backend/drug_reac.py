import pandas as pd
import plotly.express as px
import plotly.io as p_i

# takes a string (drug_name)
# and list of ints (dr_events)
# queries all events in the list and 
outcomes = ('Death','Disabled','Birth Defects','Life Threatening','Hospitalization','Required Intervention','Any Outcome')
attrs = ('ageMin','ageMax','wtMin','wtMax','sex','outcome')

notEntered = -999999

def getTreeMapFiltered(jsonDict):
    #print(jsonDict)
    #request = json.loads(jsonDict)
    #print("getMap")
    #print(jsonDict)
    print(jsonDict['drug'])
    df_raw =readReacFile("./Data/ReactData_"+jsonDict['drug']+".csv")
    #print("open")
    for key in attrs:
        if key not in jsonDict:
            jsonDict[key] = notEntered
    
    df = dataSearch(df_raw,jsonDict['ageMin'],jsonDict['ageMax'],jsonDict['wtMin'],jsonDict['wtMax'],jsonDict['sex'],jsonDict['outcome'])
    #print(df)
    return treemapPlot(df,title = jsonDict['drug'])



def dataSearch(df,ageMin = notEntered,ageMax = notEntered, wtMin = notEntered, wtMax = notEntered,sex = "ANY", outcome= 'Any Outcome'):
    #print("AAA")
    if ageMin != notEntered:
        df = df.loc[(df['age'] >= ageMin) & (df['age'] > 0)]
    if ageMax != notEntered:
        df = df.loc[(df['age'] <= ageMax) & (df['age'] > 0)]
    if wtMin != notEntered:
        df = df.loc[(df['wt'] >= wtMin) & (df['wt'] > 0)]  
    if wtMax != notEntered:
        df = df.loc[(df['wt'] <= wtMax) & (df['wt'] > 0)]
    if sex != 'ANY' and sex != notEntered:
        df = df.loc[(df['sex'] == sex)]
    if outcome != 'Any Outcome' and outcome in outcomes:
        df = df.loc[df[outcome]==1]
    return df

def treemapPlot(df,title = "all",react = True):
    fig = 0
    df2 = df[['Wt_Grp','Adverse Event', 'Age_Grp', 'sex','Name','Any Outcome','Description']].copy()
    if react:
        fig = px.treemap(df2, path=[px.Constant(title),'Adverse Event', 'Wt_Grp', 'Age_Grp', 'sex','Name'], values='Any Outcome',
                  hover_data=['Description'])
    else:
        fig = px.treemap(df2, path=[px.Constant(title), 'Wt_Grp', 'Age_Grp', 'sex','Name'], values='Any Outcome',
                  hover_data=['Description'])
    fig.update_traces(root_color="lightgrey")
    #fig.show()
    return p_i.to_json(fig)

def readReacFile(fileName):
    print(fileName)
    return pd.read_csv(fileName,sep = ',', dtype = {'p_id': 'int','age': 'float','wt': 'float','sex': 'str','manufacturer': 'str','country': 'str','Death': 'int','Disabled': 'int','Birth Defects': 'int','Life Threatening': 'int','Hospitalization': 'int','Required Intervention': 'int','Any Outcome': 'int','Name': 'str','Description': 'str','Age_Grp': 'str','Wt_Grp': 'str','Adverse Event': 'str'})
