from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.rifugio import Rifugio


class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """
    # TODO
    @staticmethod
    def get_rifugio():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor()
        result = []

        if cnx is None:
            print("Errore di connessione al database")

        query = """select r.id, r.nome, r.localita
                    from rifugio r  """

        try:
            cursor.execute(query)

            for row in cursor:
                rifugio = Rifugio(id=row[0],
                                  nome=row[1],
                                  localita=row[2])
                result.append(rifugio)

        except Exception as e:
            print(f"errore durante l'esecuzione della query: {e}")
            result = None

        finally:
            cursor.close()
            cnx.close()

        return result


    @staticmethod
    def get_connessioni_per_anno(anno):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor()
        result = []

        if cnx is None:
            print("Errore di connessionile al database")

        query = """select c.id, c.id_rifugio1, c.id_rifugio2, c.anno, c.distanza, c.difficolta 
                    from connessione c
                    where anno <= %s"""

        try:
            cursor.execute(query, (anno,))

            for row in cursor:
                connessione = Connessione(id=row[0],
                                          id_1=row[1],
                                          id_2=row[2],
                                          anno=row[3],
                                          distanza=row[4],
                                          difficolta=row[5])
                result.append(connessione)

        except Exception as e:
            print(f"errore durante la query: {e}")

        finally:
            cursor.close()
            cnx.close()

        return result
