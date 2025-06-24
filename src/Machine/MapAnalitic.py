import pandas as pd
import requests
import json

CLAVE_API = ""
MODELO = "gemini-2.0-flash"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODELO}:generateContent?key={CLAVE_API}"

def generar_analisis_criminalidad(df: pd.DataFrame, distritos, dias, categorias) -> str:
    if df.empty:
        return "No hay suficientes datos para generar un análisis."

    prompt = f"""
Como experto en seguridad urbana, analiza estos registros de incidentes delictivos en San Francisco:

- Distritos: {', '.join(distritos)}
- Días más activos: {', '.join(dias)}
- Tipos de delito: {', '.join(categorias)}
- Total de incidentes analizados: {len(df)}

Aquí están los primeros registros como muestra:

{df[['Dates', 'PdDistrict', 'DayOfWeek', 'Category', 'Descript', 'Resolution']].head(10).to_csv(index=False)}

Por favor proporciona:

1. **Patrón principal** (por ejemplo, horas pico / áreas críticas).
2. **Recomendación para las autoridades** (máx. 2 líneas).
3. **Consejo para los ciudadanos** (máx. 1 línea).

La respuesta debe estar en español y estrictamente en formato .txt (sin bloques de código ni markdown).
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
        respuesta = requests.post(URL, headers=headers, data=json.dumps(payload))
        respuesta.raise_for_status()

        resultado = respuesta.json()
        texto = resultado["candidates"][0]["content"]["parts"][0]["text"]
        return texto.strip()

    except Exception as e:
        return f"❌ Error al generar el análisis con Gemini: {str(e)}"
