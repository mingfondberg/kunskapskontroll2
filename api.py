import pandas as pd
import sqlite3
import logging

# --------------- API-klassen för att hämta data från CSV ---------------
class API:
    def __init__(self, file_path):
        """Initialiserar API-klassen med sökvägen till CSV-filen."""
        self.logger = logging.getLogger(__name__)
        self.file_path = file_path

    def fetch_data(self):
        """Läser in data från CSV-filen."""
        try:
            self.logger.info(f'Laddar data från {self.file_path}...')
            data = pd.read_csv(self.file_path)
            self.logger.info(f'Data laddad: {data.shape[0]} rader, {data.shape[1]} kolumner.')
            return data
        except Exception as e:
            self.logger.error(f'Kunde inte läsa data från CSV-filen: {e}')
            return None

# --------------- DataCleaner-klassen för att rensa och filtrera data ---------------
class DataCleaner:
    def __init__(self):
        """Initialiserar DataCleaner."""
        self.logger = logging.getLogger(__name__)

    def clean_data(self, data):
        """Rensar datan genom att ta bort tomma värden och dubbletter."""
        if data is None:
            self.logger.error('Ingen data att rensa.')
            return None

        try:
            self.logger.info('Rensar data...')
            cleaned_data = data.dropna().drop_duplicates()
            self.logger.info(f'Data rensad: {len(cleaned_data)} rader kvar efter rensning.')
            return cleaned_data
        except Exception as e:
            self.logger.error(f'Fel vid rensning av data: {e}')
            return None

# --------------- DataSaver-klassen för att spara data i SQL ---------------
class DataSaver:
    def __init__(self, db_path):
        """Initialiserar DataSaver med sökvägen till SQLite-databasen."""
        self.logger = logging.getLogger(__name__)
        self.db_path = db_path

    def save_data(self, data, table_name='utgangsprier'):
        """Sparar data till SQLite-databasen."""
        if data is None or data.empty:
            self.logger.error('Ingen data att spara eller tom data.')
            return

        try:
    
            data['Period'] = pd.to_datetime(data['Period'])

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                
                cursor.execute(f'''
                    CREATE TABLE IF NOT EXISTS {table_name} (
                        Period TEXT,
                        Pris INTEGER
                    )
                ''')

                # Spara datan i tabellen
                data.to_sql(table_name, conn, if_exists='append', index=False)
                self.logger.info(f'Data tillagd till tabell {table_name}.')
        except sqlite3.Error as e:
            self.logger.error(f'Kunde inte spara data till SQLite: {e}')
        except Exception as e:
            self.logger.error(f'Okänt fel vid datalagring: {e}')


