from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):
        self.DAO = DAO()
        self.G = None
        self.G_max = None
        self.max_vendite = None

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
        return list(self.G.edges(data="weight"))

    def get_nodi(self):
        return self.G.number_of_nodes()

    def get_archi(self):
        return self.G.number_of_edges()

    def max_vendita(self):
        m_vend = []
        for n, a in self.G_max.nodes(data=True):
            m_vend.append((a.get("weight"), a.get("name")))
        return sorted(m_vend, key=lambda x: x[0], reverse=True)




    def cammino_ottimo(self):
        self._cammino_ottimo = []
        self._punteggio_ottimo = 0.0

        for nodo in self._grafo.nodes():
            self._calcola_cammino_ricorsivo([nodo], self._calcola_successivi(nodo))
        return self._cammino_ottimo, self._punteggio_ottimo

    def _calcola_cammino_ricorsivo(self, parziale: list[State], successivi: list[State]):
        if len(successivi) == 0:
            score = self._calcola_score(parziale)
            if score > self._punteggio_ottimo:
                self._punteggio_ottimo = score
                self._cammino_ottimo = copy.deepcopy(parziale)
        else:
            for nodo in successivi:
                # aggiungo il nodo in parziale ed aggiorno le occorrenze del mese corrispondente
                parziale.append(nodo)
                # nuovi successivi
                nuovi_successivi = self._calcola_successivi(nodo)
                # ricorsione
                self._calcola_cammino_ricorsivo(parziale, nuovi_successivi)
                parziale.pop()




if __name__ == '__main__':
    Model = Model()
    print(Model.get_prodotti("Mountain Bikes", "2016-01-01", "2018-12-28"))
    print(Model.get_nodi())
    print(Model.get_archi())
    print(Model.max_vendita())
