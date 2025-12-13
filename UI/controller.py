import flet as ft
from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_grafo(self, e):
        """Callback per il pulsante 'Crea Grafo'."""
        try:
            anno = int(self._view.txt_anno.value)
        except:
            self._view.show_alert("Inserisci un numero valido per l'anno.")
            return
        if anno < 1950 or anno > 2024:
            self._view.show_alert("Anno fuori intervallo (1950-2024).")
            return

        self._model.build_weighted_graph(anno)
        self._view.lista_visualizzazione_1.controls.clear()
        self._view.lista_visualizzazione_1.controls.append(
            ft.Text(f"Grafo calcolato: {self._model.G.number_of_nodes()} nodi, {self._model.G.number_of_edges()} archi")
        )
        min_p, max_p = self._model.get_edges_weight_min_max()
        self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Peso min: {min_p:.2f}, Peso max: {max_p:.2f}"))
        self._view.page.update()

    def handle_conta_archi(self, e):
        """Callback per il pulsante 'Conta Archi'."""
        try:
            soglia = float(self._view.txt_soglia.value)
        except:
            self._view.show_alert("Inserisci un numero valido per la soglia.")
            return

        min_p, max_p = self._model.get_edges_weight_min_max()
        if soglia < min_p or soglia > max_p:
            self._view.show_alert(f"Soglia fuori range ({min_p:.2f}-{max_p:.2f})")
            return

        minori, maggiori = self._model.count_edges_by_threshold(soglia)
        self._view.lista_visualizzazione_2.controls.clear()
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"Archi < {soglia}: {minori}, Archi > {soglia}: {maggiori}"))
        self._view.page.update()

    """Implementare la parte di ricerca del cammino minimo"""
    # TODO
    def handle_cammino_minimo(self, e):

        try:
            soglia = float(self._view.txt_soglia.value)
        except:
            self._view.show_alert("Inserisci un numero valido per la soglia")
            return


        percorso, minimo = self._model.get_cammino_minimo(soglia)

        self._view.lista_visualizzazione_3.controls.clear()

        if isinstance(percorso, str):
            self._view.show_alert(percorso)

        elif isinstance(percorso, list):

            self._view.lista_visualizzazione_3.controls.append(ft.Text("Cammino minimo:"))

            G_filtrato = self._model.crea_grafo_filtrato(soglia)

            for i in range(len(percorso)-1):
                u = percorso[i]
                v = percorso[i+1]

                peso_arco = G_filtrato.get_edge_data(u, v)['weight']

                self._view.lista_visualizzazione_3.controls.append(ft.Text(f"{u} --> {v}  [Peso:{peso_arco}]"))

            self._view.lista_visualizzazione_3.controls.append(ft.Text(f"Peso totale del cammino: {minimo}"))

        else:
            self._view.show_alert("Nessun cammino valido trovato che soddisfi i vincoli (peso > soglia, lunghezza >= 3 nodi).")
            self._view.lista_visualizzazione_3.controls.append(ft.Text("Nessun percorso trovato."))

        self._view.page.update()



