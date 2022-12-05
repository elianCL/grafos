import copy

class Grafo:

    def __init__(self, nome, vertices=0): #rotulação das vértices só pode ser feita com o número do index
        self.nome = nome
        self.matrizAdj = []
        self.pesoVer = []
        self.pesoAre = []
        for i in range(0, vertices):
            self.matrizAdj.append([0 for i in range(0,vertices)])
            self.pesoVer.append([i, 1])
            self.pesoAre.append([0 for i in range(0,vertices)])

    #vertices
    def addVertice(self, peso=1):
        self.matrizAdj.append([0 for i in range(0,len(self.matrizAdj))])
        self.pesoAre.append([0 for i in range(0,len(self.pesoAre))])
        self.pesoVer.append([len(self.pesoVer)+1, peso])
        for i in self.matrizAdj:
            i.append(0)
        for i in self.pesoAre:
            i.append(0)

    #def removeVertice(self):

    def verticesAdjacentes(self, key):
        res = []
        for i in range(0, len(self.matrizAdj[key])):
            if (self.matrizAdj[key][i] == 1):
                res.append(i)
        return res

    def vertices(self):
        return list(range(0, len(self.matrizAdj)))

    def isVertice(self, key):
        return len(self.matrizAdj)>key
    
    def quantVertices(self):
        return len(self.matrizAdj)


    #arestas
    def addAresta(self, verA, verB, peso=1):
        self.matrizAdj[verA][verB] = 1
        self.matrizAdj[verB][verA] = 1
        self.pesoAre[verA][verB] = 1
        self.pesoAre[verB][verA] = 1

    def removeAresta(self, verA, verB):
        self.matrizAdj[verA][verB] = 0
        self.matrizAdj[verB][verA] = 0
        self.pesoAre[verA][verB] = 0
        self.pesoAre[verB][verA] = 0

    def arestasAdjacentes(self, verA, verB):
        ls = []
        va = self.verticesAdjacentes(verA)
        for i in va:
            if {verA, i} not in ls: ls.append({verA, i})
        vb = self.verticesAdjacentes(verB)
        for i in vb:
            if {verB, i} not in ls: ls.append({verB, i})
        return ls

    def isAresta(self, verA, verB):
        return {verA, verB} in self.arestas()
    
    def quantArestas(self):
        return len(self.arestas())

    def arestas(self):
        res = []
        for i in range(0, len(self.matrizAdj)):
            for j in self.verticesAdjacentes(i):
                if {i,j} not in res: res.append({i, j})
        return res


    #grafo
    def matrizAdjacencia(self):
        print("   ", end="")
        for i in range(0, len(self.matrizAdj)):
            print(i," ", end="")
        print()
        for j in range(0, len(self.matrizAdj)):
            print (j, self.matrizAdj[j])

    def isVazio(self):
        return self.quantVertices() == 0

    def isCompleto(self):
        for i in self.vertices():
            if(len(self.verticesAdjacentes(i)) < self.quantVertices()-1):
                return False
        return True

    def isConexo(self):
        aVisitar = []
        visitados = []
        aVisitar.append(self.vertices()[0])
        while (len(aVisitar) > 0):
            for i in self.verticesAdjacentes(aVisitar[0]):
                if(not(i in visitados or i in aVisitar)):
                    aVisitar.append(i)
                    
            visitados.append(aVisitar.pop(0))
            
        if(len(self.matrizAdj) > len(visitados)):
            return False
        else:
            return True

    def acharPonteNaive(self):
        pontes = []
        for i in range(0, self.quantArestas()):
            clone = copy.deepcopy(self)
            are = list(clone.arestas()[i])
            clone.removeAresta(are[0], are[1])
            if(not clone.isConexo()):
                pontes.append(self.arestas()[i])
        return pontes

    def acharPonteTarjan(self):
        visitados = []
        #discovery, minimum, pai
        DMP = {}
        for i in list(self.vertices()):
            DMP[i] = [-1, -1, -1]
        td = 0
        
        def restantes(ver):
            return list(set(self.verticesAdjacentes(ver))-set(visitados))

        def atualizarPeso(ver):
            aSeremAtualizadas = []
            verticesMenosPai = set(self.verticesAdjacentes(ver))-{DMP[ver][2]}
            for i in verticesMenosPai:
                if(DMP[i][1] != -1 and DMP[i][1] < DMP[ver][1]):
                    DMP[ver][1] = DMP[i][1]
                    for j in verticesMenosPai:
                        atualizarPeso(j)
        
        ver = list(self.vertices())[0]
        visitados.append(ver)
        DMP[ver] = [0, 0, 0]
        while(len(self.vertices()) != len(visitados)):
            td += 1
            if(len(restantes(ver)) == 0):
                ver = list(set(self.vertices())-set(visitados))[0]
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
            for j in self.verticesAdjacentes(i):
                if(DMP[i][1] > DMP[j][1]):
                    pontes.append({i, j})
            
        return pontes

    def fleuryNaive(self):
        clone = copy.deepcopy(self)
        caminho = []
        vertices = list(clone.vertices())
        #se V(G) possuir 3 ou mais vértices de grau ímpar então PARE
        impares = []
        for i in vertices:
            if(len(clone.verticesAdjacentes(i))%2 > 0):
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
            for i in clone.verticesAdjacentes(ver): 
                if({ver, i} in arestas or (len(clone.verticesAdjacentes(ver)) == 1 and {ver, i} in pontes)):
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
        vertices = list(clone.vertices())
        #se V(G) possuir 3 ou mais vértices de grau ímpar então PARE
        impares = []
        for i in vertices:
            if(len(clone.verticesAdjacentes(i))%2 > 0):
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
            for i in clone.verticesAdjacentes(ver): 
                if({ver, i} in arestas or (len(clone.verticesAdjacentes(ver)) == 1 and {ver, i} in pontes)):
                    clone.removeAresta(ver, i)
                    caminho.append(i)
                    arestas.remove({ver, i})
                    ver = i
                    break
                
                pontes = [set(x) for x in clone.acharPonteTarjan()]
                arestas = [set(j) for j in clone.arestas() if j not in pontes]
                
        return caminho

    

a = Grafo("a", 7)
a.addAresta(1,0)
a.addAresta(1,2)
a.addAresta(2,6)
a.addAresta(2,3)
a.addAresta(2,4)
a.addAresta(3,4)
a.addAresta(3,5)
a.addAresta(4,5)

b = Grafo("b", 5)
b.addAresta(0,3)
b.addAresta(0,2)
b.addAresta(1,4)
b.addAresta(1,3)
b.addAresta(1,2)
b.addAresta(2,3)
b.addAresta(2,4)
