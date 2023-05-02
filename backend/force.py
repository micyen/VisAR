import json
from collections import deque

def fullGraph(minWt):
    with open("./Data/Force/3dGraph_full_attr.json","r") as fp:
        val = json.load(fp)
        if minWt > 1:
            e=val['links']
            newE = []
            for x in e:
                if x['value']>=minWt:
                    newE.append(x)
            val['links'] = newE
        return json.dumps(val)

def coDosingGraphFromFile(start,distance,minWt=1):
    path = "."
    edgeTextDict = {}
    vertexIds = {}
    adjList = {}
    vertexCaseCt = {}
    vertexDeathCt = {}
    with open(path+"/Data/Force/ForceEdges.json","r") as e_fp:                  
        edgeTextDict = json.load(e_fp)
    with open(path+"/Data/Force/ForceVertices.json","r") as v_fp:                  
        vertexIds = json.load(v_fp)
    with open(path+"/Data/Force/ForceAdjList.json","r") as adj_fp:
        adjList = json.load(adj_fp)
    with open(path+"/Data/Force/CaseList.json","r") as c_fp:
        vertexCaseCt = json.load(c_fp)
    with open(path+"/Data/Force/DeathList.json","r") as d_fp:                  
        vertexDeathCt = json.load(d_fp)
    startId = -1
    for key, value in vertexIds.items():
        if value[:100] == start[:100]:
            startId = int(key)
            break
    print(start,startId)
    vertices,edgeDict = dijkstraFilter(adjList,edgeTextDict, distance, startId,minWt)
    print("Vertices:",len(vertices))
    #print(edgeTextDict.values())
    
    for key in edgeTextDict:
        x=key.split(", ")
        x0 = int(x[0][1:])
        x1 = int(x[1][:-1])
        if (x0 in vertices and x1 in vertices) and edgeTextDict[key]>=minWt and not (x0,x1) in edgeDict:
            edgeDict[(x0,x1)]=(edgeTextDict[key],0)
    print("Edges:",len(edgeDict))
    return genGraph(vertices,vertexIds,edgeDict,vertexCaseCt,vertexDeathCt)

def genGraph(vertices,vertexIds,edges,cases,deaths):
    ans = []
    ans.append('{"nodes":[\n')
    v_iter = iter(sorted(vertices.items()))
    v_cur = next(v_iter)
    print(cases[str(v_cur[0])])
    ans.append(strVertex(v_cur[0],vertexIds[str(v_cur[0])],cases[str(v_cur[0])],deaths[str(v_cur[0])],v_cur[1]))
    for k,v in v_iter:
        #print(k,v)
        ans.append(','+strVertex(k,vertexIds[str(k)],cases[str(k)],deaths[str(k)],v))
    ans.append('],\n"links": [\n')
    if len(edges)>0:
        e_iter = iter(sorted(edges.items()))
    
        ans.append(strEdge(next(e_iter)))
        for val in e_iter:
            if val[1][0]>=1:
                ans.append(',\n'+strEdge(val))
    ans.append(']}')
    #print(ans)
    return ''.join(ans)

def dijkstraFilter(adjacencyList,edgeDict, distance, start,minWt = 1):
    initDist = distance
    bfsQ = deque()
    bfsQ.append((start,-1))
    subGraphEdges = {}
    vertexDistances = {}
    while distance >=0 and len(bfsQ)>0:
        print(distance, len(bfsQ))
        loop_i = len(bfsQ)-1
        while loop_i>=0:
            #print(loop_i)
            loop_i-=1 
            cur,par = bfsQ.popleft()
            if not cur in vertexDistances:
                #print(cur,type(cur))
                vertexDistances[cur]=initDist-distance
                if par != -1:
                    parEdge = (cur,par) if cur<par else (par,cur)
                    subGraphEdges[parEdge] = (edgeDict[str(parEdge)],1)
                
                #print("A")
                if distance>0 and str(cur) in adjacencyList:
                    for x in adjacencyList[str(cur)]:
                        #print(x)
                        k = (cur,x) if cur<x else (x,cur)
                        #print(str(k))
                        if not x in vertexDistances and edgeDict[str(k)]>=minWt:
                            bfsQ.append((x,cur))
                            #print("AAA")
                            
        distance -= 1
    return vertexDistances,subGraphEdges

def strVertex(v_id,name,cases, deaths,distance):
    #print(v_id,name,distance)
    return '{"id":'+str(v_id)+',"name":"'+name+'","distance":'+str(distance)+',"cases":'+str(cases)+',"deaths":'+str(deaths)+',"group":1}'
            
def strEdge(edge):
    return '{"source":'+str(edge[0][0])+',"target":'+str(edge[0][1])+',"value":'+str(edge[1][0])+',"BFS EDGE":'+str(edge[1][1])+"}"

#x= coDosingGraphFromFile("ACETAMINOPHEN",1,200)
#with open("ForceTestFilter.json","w") as fp:  
#   fp.write(x)