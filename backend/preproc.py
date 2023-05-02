from mysql.connector import MySQLConnection,Error
import db_util
import pandas as pd
import os
import json
import BarChartTools as b_t
import ForcePreproc as force_pre

outcome_priorities = (("DE", 'Death'),("DS",'Disabled'),("CA", 'Birth Defects'), ("LT",'Life Threatening'), ("HO", 'Hospitalization'),  ("RI",'Required Intervention'))

def flatten(l):
    return [item for sublist in l for item in sublist]

def drugSubTree(drug_name,eventDict,overwrite = False):

    path = './Data/ReactData_'+drug_name+'.csv'
    if (not overwrite) and os.path.isfile(path):
        return 
    print(drug_name)
    try:
        dbconfig = db_util.read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor(prepared=True)
        queryStr1 = 'SELECT outc_cod FROM OUTC where primaryid = %s'
        queryStr2 = 'SELECT age,age_cod,wt,wt_cod,sex,mfr_sndr,occr_country FROM DEMO where primaryid = %s'

        
        df = pd.DataFrame({'p_id': pd.Series(dtype='int'),
                   'age': pd.Series(dtype='float'),
                   'wt': pd.Series(dtype='float'),
                   'sex': pd.Series(dtype='str'),
                   'manufacturer': pd.Series(dtype='str'),
                   'country': pd.Series(dtype='str'),
                   'Death': pd.Series(dtype='int'),
                   'Disabled': pd.Series(dtype='int'),
                   'Birth Defects': pd.Series(dtype='int'),
                   'Life Threatening': pd.Series(dtype='int'),
                   'Hospitalization': pd.Series(dtype='int'),
                   'Required Intervention': pd.Series(dtype='int'),
                   'Any Outcome': pd.Series(dtype='int'),
                   'Name': pd.Series(dtype='str'),
                   'Description': pd.Series(dtype='str'),
                   'Age_Grp': pd.Series(dtype='str'),
                   'Wt_Grp': pd.Series(dtype='str'),
                   'Adverse Event': pd.Series(dtype='str')
                   })
        for reaction_name, dr_events in eventDict.items():
            print("\t"+reaction_name)
            for event in dr_events:
                
                newIndex = len(df.index)
                cursor.execute(queryStr1,(event,))
                q1_ans = getOutcome(flatten(cursor.fetchall()))
                cursor.execute(queryStr2,(event,))
                q2_ans = flatten(cursor.fetchall())
                rowList = [event,getAgeinYears(q2_ans[0],q2_ans[1]),getWTinKG(q2_ans[2],q2_ans[3]),getSex(q2_ans[4]),q2_ans[5], q2_ans[6].replace('\r',''),*q1_ans,"Case: "+str(event)]
                rowList.append(getDescription(rowList))
                rowList.append(getAgeGrp(rowList[1]))
                #print(rowList)
                rowList.append(getWtGrp(rowList[2]))
                rowList.append(reaction_name)
                df.loc[newIndex] = rowList
            
        with open(path,'w') as data: 
            data.write(df.to_csv(index=True, lineterminator='\n'))   
        
    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()


def drug_reac_Filtering(drug_dict):
    try:
        dbconfig = db_util.read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor(prepared=True)
        queryStr = 'SELECT pt FROM REAC where primaryid = %s'
        newDrugDict = {}
        for drug,p_idList in drug_dict.items():
            print(drug)
            newDict = {}
            for cur_id in p_idList:
                cursor.execute(queryStr,(cur_id,))
                for ae in flatten(cursor.fetchall()):
                    #print(ae)
                    if ae in newDict:
                        newDict[ae].append(cur_id)
                    else:
                        newDict[ae]=[cur_id]
            print(newDict)
            if len(newDict)>0:
                newDrugDict[drug.replace("\\u001a","-").replace("","-")] = newDict
        return newDrugDict
    except Error as e:
        print(e)
    
    finally:
        cursor.close()
        conn.close()

def getAgeGrp(age):
    ages =["under 1 year old","1 to 13 years old","13 to 18 years old","18 to 40 years old","40 to 65 years old"]
    age_ranges = [1,13,18,40,65]
    if age<=0:
        return "Unknown Age"
    for x in range(len(age_ranges)):
        if age<age_ranges[x]:
            return ages[x]
    return "over 65 years old"

def getWtGrp(wt):
    weights =["under 40 kg","40 to 80 kg","80 to 120 kg"]
    wt_ranges = [40,80,120]
    if wt<=0:
        return "Unknown Weight"
    for x in range(len(wt_ranges)):
        if wt<wt_ranges[x]:
            return weights[x]
    return  "120+ kg"

def getOutcome(outcomeList):
    ans = []
    for i in outcome_priorities:
        ans.append(1 if i[0] in outcomeList else 0)
    ans.append(1)
    return ans

def getDescription(rowList):
    ans = "Primary ID: "+str(rowList[0])+"<br>Age: "+str(round(rowList[1],1))+" yrs<br>Weight: "+str(round(rowList[2],1))+" kg<br>Sex: "+rowList[3]+"<br>Manufacturer: "+rowList[4]+"<br>Country: "+rowList[5]+"<br>Serious Outcomes: "+("Death  " if rowList[6]>0 else "")+("Disabled  " if rowList[7]>0 else "")+("Birth Defects  " if rowList[8]>0 else "")+("Life Threatening  " if rowList[9]>0 else "")+("Hospitalization  " if rowList[10]>0 else "")+("Required Intervention  " if rowList[11]>0 else "")
    return ans

def getSex(sex):
    if sex == "M":
        return "Male"
    if sex == "F":
        return "Female"
    return "Unknown Sex"

def getWTinKG(wt,wt_cod=""):
    if wt_cod == "KG":
        return wt
    if wt_cod == "LBS":
        return wt*0.4536
    return 0

def getAgeinYears(age,age_cod=""):
    # adding 0.01 to differentiate true null fields (0) from ones where the age is approximately 0
    if age_cod == "YR":
        return age+0.01
    if age_cod == "DY":
        return age/365+0.01
    if age_cod == "WK":
        return age/52+0.01
    if age_cod == "MON":
        return age/12+0.01
    if age_cod == "HR":
        return age/365/24+0.01
    if age_cod == "DEC": #Decades
        return age*10+5+0.01
    return 0

def build_drugDicts():
    try:
        dbconfig = db_util.read_db_config()
        conn = MySQLConnection(**dbconfig)
        drug_info = {}
        drug_primarysuspect_info = {}
        
        cursor = conn.cursor(prepared=True)
        cursor.execute("SELECT DISTINCT prod_ai FROM DRUG")
        druglist = flatten(cursor.fetchall())
        #druglist = ["INFLIXIMAB","AZATHIOPRINE","PREDNISONE","MESALAMINE","LAMIVUDINE"]
        print('Total Drug Actives found in DB:', cursor.rowcount)
        queryStr = 'SELECT primaryid,role_cod FROM DRUG where prod_ai = %s'
        i=0
        for dr in druglist:
            print(i,dr)
            cursor.execute(queryStr,(dr,))
            drug_info[dr] = []
            drug_primarysuspect_info[dr] = []
            for row in cursor.fetchall():
                #print(row)
                drug_info[dr].append(row[0])
                if row[1]=='PS':
                    drug_primarysuspect_info[dr].append(row[0])
            i+=1
        f1 = open("./Data/active_info_full.json", "w")  
        json.dump(drug_info, f1)
        f1.close()
        f2 = open("./Data/active_info_primary.json", "w")  
        json.dump(drug_primarysuspect_info, f2)
        f2.close()        
         
    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
        
def main_preproc():
    build_drugDicts()
    with open("Data/ae_drug_primary.json", "r") as fp:
        with open("./DrugList.txt",'w') as dr_list:
            mainDict = json.load(fp)
            for dr in mainDict:
                dr_list.write(dr+'\n')
                drugSubTree(dr,mainDict,True)

    b_t.barChartPreproc()
    force_pre.preproc()
    
if __name__ == '__main__':
    main_preproc()