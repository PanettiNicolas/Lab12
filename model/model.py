import networkx as nx

from database.dao import DAO


class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        # TODO
        self.G = nx.Graph()
        self.lista_rifugi = DAO.get_rifugio()
        self.dizionario_rifugi = {rifugio["id"] : {"nome": rifugio["nome"], "localita": rifugio["localita"]} for rifugio in self.lista_rifugi}
        self.lista_connessioni = []
        self.lista_minore_soglia = []
        self.lista_maggiore_soglia = []


    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """
        # TODO
        self.G.clear()       #Puliamo il grafo per non sovrascrivere
        self.lista_connessioni = DAO.get_connessioni_per_anno(year)

        for connessione in self.lista_connessioni:
            self.G.add_edge(self.dizionario_rifugi[connessione.id_1], self.dizionario_rifugi[connessione.id_2],  weight = (connessione.distanza * connessione.converti_difficolta(connessione.difficolta)))

        return self.G

    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """
        # TODO

    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: archi con peso < soglia
        :return maggiori: archi con peso > soglia
        """
        # TODO

    """Implementare la parte di ricerca del cammino minimo"""
    # TODO
