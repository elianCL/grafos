import copy
import time

class Grafo:

    def __init__(self, nome, vertices=0):
        self.nome = nome
        self.vertices = {}
        self.pesos = {}
        for i in range(vertices):
            self.addVertice(i)


    #vertices
    def addVertice(self, vertice, peso=1):
        self.vertices[vertice] = []
        self.pesos[vertice] = peso

    def removeVertice(self, key):
        adjs = self.verticesAdjacentesSEM(key)
        for i in adjs:
            self.removeAresta(key, i)
        self.vertices.pop(key)
        self.pesos.pop(key)

    def verticesAdjacentes(self, key):
        ls = list(map(lambda x: x[0], self.vertices[key]))
        ls.append(key) 
        return ls #adjacente dela mesma     

    def verticesAdjacentesSEM(self, key):
        return list(map(lambda x: x[0], self.vertices[key])) # não adjacente dela mesma
         

    def isVertice(self, key):
        return key in self.vertices

    def quantVertices(self):
        return len(self.vertices)
    

    #arestas 
    def addAresta(self, verA, verB, peso=1):    
        self.vertices[verA].append([verB, peso])
        self.vertices[verB].append([verA, peso])

    def removeAresta(self, verA, verB):
        self.vertices[verA].pop(self.verticesAdjacentes(verA).index(verB))
        self.vertices[verB].pop(self.verticesAdjacentes(verB).index(verA))

    def arestasAdjacentes(self, verA, verB):
        ls = []
        va = self.verticesAdjacentes(verA)
        for i in va:
            ls.append([verA, i])
        vb = self.verticesAdjacentes(verB)
        for i in vb:
            ls.append([verB, i])
            
        return ls #adjacente dela mesma

    def isAresta(self, verA, verB):
        return (lambda i, j: j in self.verticesAdjacentes(i) and j is not i )(verA, verB)

    def quantArestas(self): 
        return int(len(self.arestas()))

    def arestas(self): 
        idx = list(self.vertices.keys())
        res = []
        for i in idx:
            for j in self.verticesAdjacentesSEM(i):
                ls = [j, i]
                if(not((ls in res) or ([ls[-1],ls[0]] in res))):
                    res.append(ls)            
        return res


    #grafo
    def isVazio(self):
        return self.quantVertices() == 0
        
    def isCompleto(self):
        for i in list(self.vertices.keys()):
            if(len(self.verticesAdjacentes(i)) < self.quantVertices()-1):
                return False
        return True

    def listaAdjacencia(self):
        for i in list(self.vertices.keys()):
            print(i, ": ", self.verticesAdjacentesSEM(i))
        
    def matrizAdjacencia(self):
        ls = list(self.vertices.keys())
        print("   ", end="")
        [print(" ", i, end="") for i in ls]
        print()
        for i in ls:
            print(i, ":", end="")
            for j in ls:
                print(" ",int((lambda i, j: j in self.verticesAdjacentesSEM(i))(i, j)) ,end = "")
            print()

    def acharPonteTarjan(self):
        visitados = []
        #discovery, minimum, pai
        DMP = {}
        for i in list(self.vertices.keys()):
            DMP[i] = [-1, -1, -1]
        td = 0
        
        def restantes(ver):
            return list(set(self.verticesAdjacentesSEM(ver))-set(visitados))

        def atualizarPeso(ver):
            aSeremAtualizadas = []
            verticesMenosPai = set(self.verticesAdjacentesSEM(ver))-{DMP[ver][2]}
            for i in verticesMenosPai:
                if(DMP[i][1] != -1 and DMP[i][1] < DMP[ver][1]):
                    DMP[ver][1] = DMP[i][1]
                    for j in verticesMenosPai:
                        atualizarPeso(j)
        
        ver = list(self.vertices.keys())[0]
        visitados.append(ver)
        DMP[ver] = [0, 0, 0]
        while(len(self.vertices.keys()) != len(visitados)):
            td += 1
            if(len(restantes(ver)) == 0):
                ver = list(set(self.vertices.keys())-set(visitados))[0]
                auxP = ver
                if(len(self.verticesAdjacentes(ver)) == 0):
                    auxP = -1
                    #grafo desconexo
                else:
                    auxP = self.verticesAdjacentes(ver)[0]
                #arestas de retorno
            else:
                auxP = ver
                ver = restantes(ver)[0]
            visitados.append(ver)
            DMP[ver] = [td, td, auxP]
            atualizarPeso(ver)

        #print(DMP)
        visitados = []
        pontes = []
        for i in set(DMP.keys())-set(visitados):
            visitados.append(i)
            for j in self.verticesAdjacentesSEM(i):
                if(DMP[i][1] > DMP[j][1]):
                    pontes.append([i, j])
            
        return pontes
    
    def acharPonteNaive(self):
        pontes = []
        for i in range(0, self.quantArestas()):
            clone = copy.deepcopy(self)
            clone.removeAresta(clone.arestas()[i][0], clone.arestas()[i][1])
            if(not clone.isConexo()):
                pontes.append(self.arestas()[i])
        return pontes

    def fleuryNaive(self):
        clone = copy.deepcopy(self)
        caminho = []
        vertices = list(clone.vertices.keys())
        #se V(G) possuir 3 ou mais vértices de grau ímpar então PARE
        impares = []
        for i in vertices:
            if(len(clone.verticesAdjacentesSEM(i))%2 > 0):
                impares.append(i)
        if(len(impares) >= 3):
            return False

        #escolher v cujo grau seja ímpar, se houver
        pontes = [set(x) for x in clone.acharPonteNaive()]
        arestas = [set(i) for i in clone.arestas() if i not in pontes]
        if(len(impares) > 0):
            ver = vertices[impares[0]]
        else:
            ver = vertices[0]
        caminho.append(ver)

        while(len(arestas)>0):
            for i in clone.verticesAdjacentesSEM(ver): 
                if({ver, i} in arestas or (len(clone.verticesAdjacentesSEM(ver)) == 1 and {ver, i} in pontes)):
                    clone.removeAresta(ver, i)
                    caminho.append(i)
                    arestas.remove({ver, i})
                    ver = i
                    break
                
                pontes = [set(x) for x in clone.acharPonteNaive()]
                arestas = [set(j) for j in clone.arestas() if j not in pontes]
    
        return caminho

    def fleuryTarjan(self):
        clone = copy.deepcopy(self)
        caminho = []
        vertices = list(clone.vertices.keys())
        #se V(G) possuir 3 ou mais vértices de grau ímpar então PARE
        impares = []
        for i in vertices:
            if(len(clone.verticesAdjacentesSEM(i))%2 > 0):
                impares.append(i)
        if(len(impares) >= 3):
            return False

        #escolher v cujo grau seja ímpar, se houver
        pontes = [set(x) for x in clone.acharPonteTarjan()]
        arestas = [set(i) for i in clone.arestas() if i not in pontes]
        if(len(impares) > 0):
            ver = vertices[impares[0]]
        else:
            ver = vertices[0]
        caminho.append(ver)

        while(len(arestas)>0):
            for i in clone.verticesAdjacentesSEM(ver): 
                if({ver, i} in arestas or (len(clone.verticesAdjacentesSEM(ver)) == 1 and {ver, i} in pontes)):
                    clone.removeAresta(ver, i)
                    caminho.append(i)
                    arestas.remove({ver, i})
                    ver = i
                    break
                
                pontes = [set(x) for x in clone.acharPonteTarjan()]
                arestas = [set(j) for j in clone.arestas() if j not in pontes]
                
        return caminho

    def isConexo(self):
        #busca em largura
        aVisitar = []
        visitados = []
        aVisitar.append(list(self.vertices.keys())[0])
        while (len(aVisitar) > 0):
            for i in self.verticesAdjacentes(aVisitar[0]):
                if(not(i in visitados or i in aVisitar)):
                    aVisitar.append(i)
                    
            visitados.append(aVisitar.pop(0))
            
        if(len(self.vertices) > len(visitados)):
            return False
        else:
            return True

    def buscaEmProfundidade(self):
        visitados = []
        
        def restantes(ver):
            return list(set(self.verticesAdjacentesSEM(ver))-set(visitados))
        
        ver = list(self.vertices.keys())[0]
        visitados.append(ver)
        while(len(self.vertices.keys()) != len(visitados)):
            if(len(restantes(ver)) == 0):
                ver = list(set(self.vertices.keys())-set(visitados))[0]
                #arestas de retorno
            else:
                ver = restantes(ver)[0]
            visitados.append(ver)
                            
        return visitados



#grafo 100 vertices
ant = 3
gc = Grafo("gc", 100)
for i in gc.vertices:
    gc.addAresta(i, ant)
    ant = i
print("100 vértices")
start_time = time.time()
gc.fleuryNaive()
print("tempo de execução fleury modo naive: %s" % (time.time() - start_time))
start_time = time.time()
gc.fleuryTarjan()
print("tempo de execução fleury modo tarjan: %s" % (time.time() - start_time))


#grafo 1.000 vertices
ant = 3
gm = Grafo("gm", 1000)
for i in gm.vertices:
    gm.addAresta(i, ant)
    ant = i
print("1.000 vértices")
start_time = time.time()
gm.fleuryNaive()
print("tempo de execução fleury modo naive: %s" % (time.time() - start_time))
start_time = time.time()
gm.fleuryTarjan()
print("tempo de execução fleury modo tarjan: %s" % (time.time() - start_time))

#grafo 10.000 vertices
ant = 3
gdm = Grafo("gdm", 10000)
for i in gdm.vertices:
    gdm.addAresta(i, ant)
    ant = i
print("10.000 vértices")
start_time = time.time()
gdm.fleuryNaive()
print("tempo de execução fleury modo naive: %s" % (time.time() - start_time))
start_time = time.time()
gdm.fleuryTarjan()
print("tempo de execução fleury modo tarjan: %s" % (time.time() - start_time))

#grafo 100.000 vertices
ant = 3
gcm = Grafo("gcm", 100000)
for i in gcm.vertices:
    gcm.addAresta(i, ant)
    ant = i
start_time = time.time()
print("100.000 vértices")
start_time = time.time()
gcm.fleuryNaive()
print("tempo de execução fleury modo naive: %s" % (time.time() - start_time))
start_time = time.time()
gcm.fleuryTarjan()
print("tempo de execução fleury modo tarjan: %s" % (time.time() - start_time))
