from dataclasses import dataclass

@dataclass
class Rifugio:
    id : int
    nome : str
    localita : str

    def __hash__(self):
        return hash(self.id)






