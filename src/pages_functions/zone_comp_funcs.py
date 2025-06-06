import pandas as pd
from src.config.db import conn

def get_crime_data():
    """
    Fetches crime data from the MongoDB collection and converts it to a DataFrame.
    """
    data = list(conn.find().limit(1000))  
    df = pd.DataFrame(data)
    
    
    df = df.dropna(subset=["PdDistrict", "Category", "Dates"])
    df["Dates"] = pd.to_datetime(df["Dates"], errors='coerce')
    df = df.dropna(subset=["Dates"])
    
    return df