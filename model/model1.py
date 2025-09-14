from database.DAO import DAO
import networkx as nx
import copy


class Model:
    def __init__(self):
        self.DAO = DAO()
        self.G = None
        self.G_max = None
        self.max_vendite = None
        self.sol_best = []
        self.peso_best = 0

    def getDateRange(self):
        return DAO.getDateRange()

    def get_product(self):
        return DAO.get_product()

    def get_prodotti(self, categoria, data1, data2):
        self.max_vendite = []
        self.G = nx.DiGraph()
        self.G_max = nx.Graph()
        prodot = DAO.get_prodotti(categoria, data1, data2)
        for i in prodot:
            self.G.add_node(i.product_id)
            self.G_max.add_node(i.product_id, name=i.product_name, weight=0)
        for i in prodot:
            c=0
            if i.num_vendite == 0:
                continue
            for j in prodot:
                if j.num_vendite == 0 or i.product_id == j.product_id:
                    continue
                if i.num_vendite > j.num_vendite:
                    self.G.add_edge(i.product_id, j.product_id, weight=i.num_vendite + j.num_vendite)
                    c = c + i.num_vendite + j.num_vendite
                elif j.num_vendite > i.num_vendite:
                    self.G.add_edge(j.product_id, i.product_id, weight=i.num_vendite + j.num_vendite)
                    c = c - (i.num_vendite + j.num_vendite)
                else:
                    self.G.add_edge(i.product_id, j.product_id, weight=i.num_vendite + j.num_vendite)
                    self.G.add_edge(j.product_id, i.product_id, weight=i.num_vendite + j.num_vendite)
                    c = c
            self.G_max.nodes[i.product_id]['weight'] = c
        print(sorted(list(self.G.edges(data="weight")), key=lambda x: x[2], reverse=True))
        return list(self.G.edges(data="weight"))

    #sorted(list(self.G.edges(data="weight")), key=lambda x: x[2], reverse=True)

    def get_nodi(self):
        return self.G.number_of_nodes()

    def get_archi(self):
        return self.G.number_of_edges()

    def max_vendita(self):
        m_vend = []
        for n, a in self.G_max.nodes(data=True):
            m_vend.append((a.get("weight"), a.get("name")))
        print(list(self.G.successors(2)))
        return sorted(m_vend, key=lambda x: x[0], reverse=True)


    def cammino(self, lun, start, end):
        percorso = [start]
        for n in self.G.successors(start):
            p = self.G[start][n]["weight"]
            percorso.append(n)
            self.ricorsione(lun, end, percorso, p)
            percorso.pop()
        return self.sol_best, self.peso_best

    def ricorsione(self, lun, end, percorso, p):
        if len(percorso) - 1 == lun:
            if percorso[-1] == end and p > self.peso_best:
                    self.sol_best = copy.deepcopy(percorso)
                    self.peso_best = p
            return
        else:
            for n in self.G.successors(percorso[-1]):
                if n in percorso:
                    continue
                peso = self.G[percorso[-1]][n]["weight"]
                percorso.append(n)
                self.ricorsione(lun, end, percorso, peso+p)
                percorso.pop()
        return









if __name__ == '__main__':
    Model = Model()
    print(Model.get_prodotti("Mountain Bikes", "2016-01-01", "2018-12-28"))
    print(Model.get_nodi())
    print(Model.get_archi())
    print(Model.max_vendita())
    print(Model.cammino(2, 2, 114))
