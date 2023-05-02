import db_util
import json
from mysql.connector import MySQLConnection,Error
def coDosingGraph():
    try:
        dbconfig = db_util.read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor(buffered=True)
        queryStr = 'SELECT primaryid,prod_ai FROM DRUG'
        queryStr2 = 'SELECT outc_cod FROM OUTC where primaryid = %s'
        caseDict = {}
        deaths = set()
        cursor2 = conn.cursor(prepared=True)
        cursor.execute(queryStr)
        row = cursor.fetchone()
        vertices = set()
        while row is not None:
            #print(row)
            if row[1]!='':
                #print(row)
                v = row[1].replace("\\u001a","-").replace("","-")
                vertices.add(v)
                if row[0] not in caseDict:
                    #print(row[0])
                    caseDict[row[0]] = set()
                    cursor2.execute(queryStr2,(row[0],))
                    #print(row[0])
                    q2_ans = flatten(cursor2.fetchall())
                    #print(q2_ans)
                    if 'DE' in q2_ans:
                        deaths.add(row[0])
                    
                caseDict[row[0]].add(v)
            row = cursor.fetchone()
        #print(row)
        vertexIds = {}
        vertexIdReg = {}
        vertexCaseCt = {}
        vertexDeathCt = {}
        for i,v in enumerate(sorted(vertices)):
            vertexIds[v]=i
            vertexIdReg[i]=v
            vertexCaseCt[i]=0
            vertexDeathCt[i]=0
            #print(v)
        
        edgeDict = {}
        for key, value in caseDict.items():
            death = 1 if key in deaths else 0
            for x in value:
                xId = vertexIds[x]
                vertexDeathCt[xId]+=death
                vertexCaseCt[xId]+=1
                for y in value:
                    yId = vertexIds[y]
                    if xId<yId:
                        edge = str((xId,yId))
                        if edge not in edgeDict:
                            edgeDict[edge] = 1
                        else:
                            edgeDict[edge] += 1
        with open("./Data/Force/ForceEdges.json","w") as e_fp:                  
            json.dump(edgeDict, e_fp)
        with open("./Data/Force/ForceVertices.json","w") as v_fp:                  
            json.dump(vertexIdReg, v_fp)
        adj = edgeListToAdjList(edgeDict)
        with open("./Data/Force/ForceAdjList.json","w") as adj_fp:                  
            json.dump(adj, adj_fp)
        with open("./Data/Force/CaseList.json","w") as c_fp:                  
            json.dump(vertexCaseCt, c_fp)    
        with open("./Data/Force/DeathList.json","w") as d_fp:                  
            json.dump(vertexDeathCt, d_fp)
            
        #for key, value in edgeDict.items():
            #print(key, value)
        
    except Error as e:
        print(e)

    finally:
        cursor.close()
        cursor2.close()
        conn.close()
        
def strVertex(v_id,name,cases, deaths,distance):
    #print(v_id,name,distance)
    return '{"id":'+str(v_id)+',"name":"'+name+'","distance":'+str(distance)+',"cases":'+str(cases)+',"deaths":'+str(deaths)+',"group":1}'
            
def strEdge(edge):
    return '{"source":'+str(edge[0][0])+',"target":'+str(edge[0][1])+',"value":'+str(edge[1][0])+',"BFS EDGE":'+str(edge[1][1])+"}"


def writeFullGraph(fp):
    with open("./Data/Force/ForceEdges.json","r") as e_fp:                  
        edgeTextDict = json.load(e_fp)
    with open("./Data/Force/ForceVertices.json","r") as v_fp:                  
        vertexTextDict = json.load(v_fp)
    with open("./Data/Force/CaseList.json","r") as c_fp:
        vertexCaseCt = json.load(c_fp)
    with open("./Data/Force/DeathList.json","r") as d_fp:                  
        vertexDeathCt = json.load(d_fp)
    vertDict={}
    for key in vertexTextDict:
        vertDict[int(key)] = 0
        
    if fp == None:
        return
    edgeDict={}
    for key in edgeTextDict:
        x=key.split(", ")
        x0 = int(x[0][1:])
        x1 = int(x[1][:-1])
        edgeDict[(x0,x1)]=(edgeTextDict[key],1)
    genGraphtoFile(fp,vertDict,vertexTextDict,edgeDict,vertexCaseCt,vertexDeathCt)

def genGraphtoFile(fp,vertices,vertexIds,edges,cases,deaths):

    fp.write('{"nodes":[\n')
    v_iter = iter(sorted(vertices.items()))
    v_cur = next(v_iter)
    print(cases[str(v_cur[0])])
    fp.write(strVertex(v_cur[0],vertexIds[str(v_cur[0])],cases[str(v_cur[0])],deaths[str(v_cur[0])],v_cur[1]))
    for k,v in v_iter:
        #print(k,v)
        fp.write(','+strVertex(k,vertexIds[str(k)],cases[str(k)],deaths[str(k)],v))
    fp.write('],\n"links": [\n')
    if len(edges)>0:
        e_iter = iter(sorted(edges.items()))
    
        fp.write(strEdge(next(e_iter)))
        for val in e_iter:
            if val[1][0]>=1:
                fp.write(',\n'+strEdge(val))
    fp.write(']}')


def edgeListToAdjList(edges):
    ans = {}
    for e in edges:
        x=e.split(", ")
        print(x)
        x0 = int(x[0][1:])
        x1 = int(x[1][:-1])
        print(x0,x1)
        ans.setdefault(x0,[])
        ans.setdefault(x1,[]) 
        ans[x0].append(x1)
        ans[x1].append(x0)
    return ans

def flatten(l):
    return [item for sublist in l for item in sublist]

def preproc():
    coDosingGraph()
    with open("./Data/Force/3dGraph_full_attr.json", "w") as fp:
        writeFullGraph(fp)
