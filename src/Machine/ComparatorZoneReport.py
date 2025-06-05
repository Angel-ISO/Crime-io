import pandas as pd
import requests
import json

API_KEY = ""
MODEL = "gemini-2.0-flash"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

def generar_analisis_comparativo(df1: pd.DataFrame, df2: pd.DataFrame, zona1: str, zona2: str, pregunta: str) -> str:
    if df1.empty or df2.empty:
        return "No hay suficientes datos para generar un análisis comparativo."

    
    dias1 = df1["DayOfWeek"].mode().tolist()
    dias2 = df2["DayOfWeek"].mode().tolist()
    
    categorias1 = df1["Category"].value_counts().head(3).index.tolist()
    categorias2 = df2["Category"].value_counts().head(3).index.tolist()

    prompt = f"""
As a public safety analyst, compare crime trends between two areas in San Francisco:

Zone A: {zona1}
- Total incidents: {len(df1)}
- Most active days: {', '.join(dias1)}
- Top crimes: {', '.join(categorias1)}

Zone B: {zona2}
- Total incidents: {len(df2)}
- Most active days: {', '.join(dias2)}
- Top crimes: {', '.join(categorias2)}

User question: {pregunta}

Here is a sample of incidents for each zone:

Zone A sample:
{df1[['Dates', 'PdDistrict', 'DayOfWeek', 'Category', 'Descript', 'Resolution']].head(5).to_csv(index=False)}

Zone B sample:
{df2[['Dates', 'PdDistrict', 'DayOfWeek', 'Category', 'Descript', 'Resolution']].head(5).to_csv(index=False)}

Provide:

1. Brief comparison of patterns (max 3 lines).
2. Recommendation for city officials (max 2 lines).
3. Citizen advice (1 line).
4. Final summary sentence.

Answer must be in English and strictly in raw .txt format (no markdown, no code blocks).
    """

    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    try:
        response = requests.post(URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        result = response.json()
        text = result["candidates"][0]["content"]["parts"][0]["text"]
        return text.strip()
    except Exception as e:
        return f"❌ Error al generar análisis con Gemini: {str(e)}"
