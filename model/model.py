import networkx as nx
from database.dao import DAO


class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        # TODO
        self.G = nx.Graph()
        self._lista_rifugi = DAO.get_rifugio()
        self._dizionario_rifugi = {}
        self._lista_connessioni = []

        self._lista_pesi = []


    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """
        # TODO
        self.G.clear()       #Puliamo il grafo per non sovrascrivere
        self._lista_connessioni.clear()
        self._lista_connessioni = DAO.get_connessioni_per_anno(year)

        for rifugio in self._lista_rifugi:
            self._dizionario_rifugi[rifugio.id] = rifugio

        for connessione in self._lista_connessioni:
            peso = (float(connessione.distanza) * float(connessione.converti_difficolta(connessione.difficolta)))
            self.G.add_edge(self._dizionario_rifugi[connessione.id_1], self._dizionario_rifugi[connessione.id_2],  weight = peso )
            self._lista_pesi.append(peso)

        return self.G

    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """
        # TODO
        minimo = min(self._lista_pesi)
        massimo = max(self._lista_pesi)
        return minimo, massimo

    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: archi con peso < soglia
        :return maggiori: archi con peso > soglia
        """
        # TODO
        lista_sopra = []
        lista_sotto = []

        for peso in self._lista_pesi:
            if peso < soglia:
                lista_sotto.append(peso)
            elif peso >= soglia:
                lista_sopra.append(peso)

        return len(lista_sotto), len(lista_sopra)



    """Implementare la parte di ricerca del cammino minimo"""
    # TODO
