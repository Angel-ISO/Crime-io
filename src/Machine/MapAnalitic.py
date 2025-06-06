import pandas as pd
import requests
import json

API_KEY = "AIzaSyAVd8tt_8ah9RORbzbc0HUM7GpOgb53j-w"
MODEL = "gemini-2.0-flash"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

def generar_analisis_criminalidad(df: pd.DataFrame, distritos, dias, categorias) -> str:
    if df.empty:
        return "No hay suficientes datos para generar un análisis."

    prompt = f"""
As an expert in urban safety, analyze these crime incident records in San Francisco:

- Districts: {', '.join(distritos)}
- Most active days: {', '.join(dias)}
- Crime types: {', '.join(categorias)}
- Total incidents analyzed: {len(df)}

Here are the first few records as a sample:

{df[['Dates', 'PdDistrict', 'DayOfWeek', 'Category', 'Descript', 'Resolution']].head(10).to_csv(index=False)}

Please provide:

1. **Main pattern** (e.g., peak times/critical areas).
2. **Recommendation for authorities** (max 2 lines).
3. **Advice for citizens** (max 1 line).

Answer must be in English and strictly in txt format (not inside a code block or markdown).
    """

    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    try:
        response = requests.post(URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()

        result = response.json()
        
        text = result["candidates"][0]["content"]["parts"][0]["text"]
        return text.strip()

    except Exception as e:
        return f"❌ Error al generar el análisis con Gemini: {str(e)}"
