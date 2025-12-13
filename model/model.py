import math

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
            elif peso > soglia:
                lista_sopra.append(peso)

        return len(lista_sotto), len(lista_sopra)



    """Implementare la parte di ricerca del cammino minimo"""
    # TODO

    def get_cammino_minimo(self, soglia):
    
    #---Metodo con NETWORKX---

        #Creazione grafo filtrato
        G_filtrato = self.crea_grafo_filtrato(soglia)

        if G_filtrato.number_of_edges() == 0:     #Verifico che il grafo contenga almeno un collegamento
            return [], 0.0

        #Calcolo TUTTI i percorsi minimi (sequenze di nodi) per OGNI coppia
        percorsi_minimi_per_coppia = dict(nx.all_pairs_dijkstra_path(G_filtrato, weight = 'weight'))
        #Restituisce un DIZIONARIO DI DIZIONARI che mappa ogni nodo di partenza con i percorsi minimi verso tutti gli altri nodi
        #-> Percorsi minimi per coppia = {u1 : {v1 : percorso(u1,v1), v2 : percorso(u1,v2), ...}, u2 : {v1 : percorso(u2,v1), ...}, ...}

        minimo_assoluto = float('inf')   #Infinito positivo
        miglior_percorso = []


        for u in G_filtrato.nodes():                                   #Ciclo su tutti i nodi del grafo
            #v -> Nodo di arrivo ; percorso -> La sequenza del cammino minimo da u a v
            for v, percorso in percorsi_minimi_per_coppia[u].items():     #Per ogni nodo ciclo sui percorsi che lo collegano agli altri nodi

                if len(percorso) >= 3:       #Condizione sulla lunghezza minima del percorso -> Deve contenere almeno 3 nodi (2 archi)

                    peso_corrente = self.calcola_peso_percorso(G_filtrato, percorso)

                    if peso_corrente < minimo_assoluto:     #Condizione sul peso minimo assoluto tra i percorsi
                        minimo_assoluto = peso_corrente
                        miglior_percorso = percorso

        if not miglior_percorso:
            return "Nessun sentiero trovato...", 0.0

        return miglior_percorso, minimo_assoluto




    def calcola_peso_percorso(self, G, percorso_nodi):
        peso = 0

        for i in range(len(percorso_nodi) - 1):     #Iteriamo sugli indici per condiserare le coppie di nodi consecutive
            u = percorso_nodi[i]          #Nodo di partenza della coppia
            v = percorso_nodi[i + 1]      #Nodo di arrivo della coppia

            peso += G.get_edge_data(u, v)['weight']    #G.get_edge_data(u, v) restituisce un dizionario con gli attributi dell'arco da cui noi estraiamo il peso

        return peso


    """
    def get_cammino_minimo_ricorsivo(self, soglia):

    #---Metodo con RICORSIONE---   ---> NON funzionante

        G_filtrato = self.crea_grafo_filtrato(soglia)

        if G_filtrato.number_of_edges() == 0:
            return "Nessun sentiero trovato...", 0.0

        tutti_i_cammini = []

        for start_node in G_filtrato.nodes():


            self.ricerca_cammino_ricorsiva(G_filtrato,
                                           start_node,
                                           set(),
                                           0.0,
                                           [],
                                           tutti_i_cammini)

        if not tutti_i_cammini:
            return "Nessun cammino valido trovato che soddisfi la lunghezza minima...", 0.0


        miglior_cammino = min(tutti_i_cammini, key=lambda x: x['peso'])

        miglior_percorso = miglior_cammino['percorso']
        minimo_assoluto = miglior_cammino['peso']

        return miglior_percorso, minimo_assoluto



    def ricerca_cammino_ricorsiva(self, G, nodo_corrente, visitati, peso_attuale, percorso_attuale, tutti_i_cammini):

        percorso_attuale.append(nodo_corrente)
        visitati.add(nodo_corrente)


        if len(percorso_attuale) >= 3:
            tutti_i_cammini.append({"percorso":percorso_attuale.copy(), "peso":peso_attuale})


        for u, v, data in G.edges(nodo_corrente, data=True):     #La funzione G.edges(nodo, data=True) restituisce la tupla (u, v, data_arco)

            if u == nodo_corrente:
                vicino = v
            elif v == nodo_corrente:
                vicino = u
            else:
                continue

            if vicino not in visitati:

                peso_arco = data['weight']


                self.ricerca_cammino_ricorsiva(G,
                                               vicino,
                                               visitati,
                                               peso_attuale + peso_arco,
                                               percorso_attuale,
                                               tutti_i_cammini)

                                            #Usiamo le funzioni .copy per creare una copia e non creare un alias rischiando di compromettere gli oggetti originali
        percorso_attuale.pop()
        visitati.remove(nodo_corrente)
        
    """


    def crea_grafo_filtrato(self, soglia):
        G_filtrato = nx.Graph()
        lista_edges_sopra_soglia = []

        for u, v, d in self.G.edges(data=True):
            if d['weight'] > soglia:
                lista_edges_sopra_soglia.append((u, v, d))

        G_filtrato.add_edges_from(lista_edges_sopra_soglia)

        return G_filtrato

