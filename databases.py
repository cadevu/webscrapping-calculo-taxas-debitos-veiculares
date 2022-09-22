#arquivo python que cria o banco de dados sqlite3
import sqlite3
connector = sqlite3.connect('db_taxas.db')
cursor = connector.cursor()
sql =  """
CREATE TABLE taxas ( site TEXT NOT NULL, 
                     em1x REAL,     
                    em2x REAL,
                    em3X REAL,
                    em4X REAL,
                    em5X REAL,
                    em6X REAL,
                    em7X REAL,
                    em8X REAL,
                    em9X REAL,
                    em10X REAL,
                    em11X REAL,
                    em12X REAL,
                    em16x REAL,
                    em18x REAL,
                    createdDate TEXT) """

cursor.execute(sql)
connector.commit()
cursor.close()