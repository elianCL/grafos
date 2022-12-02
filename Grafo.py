import copy

class Grafo:

    def __init__(self, nome, vertices=0):
        self.nome = nome
        self.vertices = {}
        self.pesos = {}
        for i in range(vertices):
            self.addVertice(i)


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
        #DMP = dict(zip(self.vertices.keys(), [-1, -1, -1]))
        DMP = dict(zip(self.vertices.keys(), [-1, -1, -1]))
        td = 0
        
        def restantes(ver):
            return list(set(self.verticesAdjacentesSEM(ver))-set(visitados))
        
        ver = list(self.vertices.keys())[0]
        visitados.append(ver)
        DMP[ver] = [0, 0, 0]
        while(len(self.vertices.keys()) != len(visitados)):
            td += 1
            if(len(restantes(ver)) == 0):
                ver = list(set(self.vertices.keys())-set(visitados))[0]
                auxP = td
                #arestas de retorno
            else:
                auxP = ver
                ver = restantes(ver)[0]
            visitados.append(ver)
            DMP[ver] = [td, td, auxP]
            print(DMP)
            for i in list(set(self.verticesAdjacentesSEM(ver))-{auxP}):
                if(DMP[i][1] != -1 and DMP[i][1] < DMP[ver][1]):
                    DMP[ver][1] = DMP[i][1]
            #como as vertices são atualizadas?
        print(DMP)
        return visitados
    
    def acharPonteNaive(self):
        pontes = []
        for i in range(0, self.quantArestas()):
            clone = copy.deepcopy(self)
            clone.removeAresta(clone.arestas()[i][0], clone.arestas()[i][1])
            if(not clone.isConexo()):
                pontes.append(self.arestas()[i])
        return pontes

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

    
        
    

    

a = Grafo("a", 7)
a.addAresta(1,0)
a.addAresta(1,2)
a.addAresta(2,6)
a.addAresta(2,3)
a.addAresta(2,4)
a.addAresta(3,4)
a.addAresta(3,5)
a.addAresta(4,5)
