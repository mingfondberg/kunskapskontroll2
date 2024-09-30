import logging
from api import API, DataCleaner, DataSaver

if __name__ == "__main__":
    # Konfigurera logging för att spara loggar till pipeline.log
    logging.basicConfig(
        filename='pipeline.log',        
        filemode='w',                    # 'w' för att skriva över filen vid varje körning
        level=logging.INFO,              
        format='%(asctime)s - %(levelname)s - %(message)s',  
        datefmt='%Y-%m-%d %H:%M:%S'      
    )

    # Ange filvägar för CSV-fil och SQLite-databas
    csv_file = 'filtered_data.csv'
    db_file = 'utgangspriser.db'

    # Skapa instanser av klasserna
    api = API(csv_file)
    cleaner = DataCleaner()
    saver = DataSaver(db_file)

    # Hämta data från CSV-fil
    data = api.fetch_data()

    # Om data hämtades, rensa den och spara den i SQL
    if data is not None:
        cleaned_data = cleaner.clean_data(data)
        if cleaned_data is not None:
            saver.save_data(cleaned_data)
        else:
            logging.error("Rensad data är tom eller ingen data att spara.")
    else:
        logging.error("Ingen data kunde hämtas från CSV-filen.")



