from dataclasses import dataclass

@dataclass
class Connessione:
    id : int
    id_1 : int
    id_2 : int
    anno : int
    distanza : int
    difficolta : str


    @staticmethod
    def converti_difficolta(difficolta):

        if difficolta == "facile":
            return 1
        elif difficolta == "medio":
            return 1.5
        elif difficolta == "difficile":
            return 2
        else:
            print("Dato mancante all'interno del database")
            return None



