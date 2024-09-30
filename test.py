import pytest
from unittest.mock import patch, mock_open, MagicMock
import pandas as pd
from api import API, DataCleaner, DataSaver


# Test för API-klassen
@patch('builtins.open', new_callable=mock_open, read_data="Datum,Pris\n2024-01-01,5000000\n2024-01-02,6000000")
@patch('os.path.exists', return_value=True)
def test_fetch_data(mock_exists, mock_file):
    """Testar att API fetch_data läser CSV-filen korrekt"""
    api = API('dummy_path.csv')
    data = api.fetch_data()

    # Kontrollera att data laddas korrekt
    assert data is not None
    assert data.shape[0] == 2  # 2 rader
    assert data.columns.tolist() == ['Datum', 'Pris']  


@patch('os.path.exists', return_value=False)
def test_fetch_data_file_not_found(mock_exists):
    """Testar att API hanterar saknad fil korrekt"""
    api = API('dummy_path.csv')
    data = api.fetch_data()

    
    assert data is None


# Test för DataCleaner-klassen
def test_clean_data():
    """Testar att DataCleaner korrekt rensar data"""
    data = pd.DataFrame({
        'Datum': ['2024-01-01', '2024-01-02', None, '2024-01-01'],
        'Pris': [5000000, 6000000, 7000000, 5000000]
    })
    
    cleaner = DataCleaner()
    cleaned_data = cleaner.clean_data(data)

    
    assert len(cleaned_data) == 2  
    assert not cleaned_data.isnull().values.any()  


def test_clean_data_empty():
    """Testar att DataCleaner hanterar tom data"""
    cleaner = DataCleaner()
    cleaned_data = cleaner.clean_data(None)


    assert cleaned_data is None


# Test för DataSaver-klassen
@patch('sqlite3.connect')
def test_save_data(mock_connect):
    """Testar att DataSaver korrekt sparar data i databasen"""
    data = pd.DataFrame({
        'Datum': ['2024-01-01', '2024-01-02'],
        'Pris': [5000000, 6000000]
    })

    mock_conn = mock_connect.return_value  # Mock för databasanslutningen
    mock_cursor = mock_conn.cursor.return_value

    saver = DataSaver('dummy_db_path.db')
    saver.save_data(data)

    # Kolla att to_sql anropades korrekt
    mock_conn.__enter__().cursor().execute.assert_called_with('''
        CREATE TABLE IF NOT EXISTS utgangsprier (
            Datum TEXT,
            Pris INTEGER
        )
    ''')

    
    mock_conn.__enter__().commit.assert_called_once()


def test_save_data_empty():
    """Testar att DataSaver inte sparar om data är tom"""
    data = pd.DataFrame()

    saver = DataSaver('dummy_db_path.db')
    with patch('sqlite3.connect') as mock_connect:
        saver.save_data(data)

    
        mock_connect.assert_not_called()
