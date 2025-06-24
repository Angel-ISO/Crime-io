import pandas as pd
import requests
import json

CLAVE_API = ""
MODELO = "gemini-2.0-flash"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODELO}:generateContent?key={CLAVE_API}"

def generar_analisis_comparativo(df1: pd.DataFrame, df2: pd.DataFrame, zona1: str, zona2: str, pregunta: str) -> str:
    if df1.empty or df2.empty:
        return "No hay suficientes datos para generar un análisis comparativo."

    dias1 = df1["DayOfWeek"].mode().tolist()
    dias2 = df2["DayOfWeek"].mode().tolist()
    
    categorias1 = df1["Category"].value_counts().head(3).index.tolist()
    categorias2 = df2["Category"].value_counts().head(3).index.tolist()

    prompt = f"""
Como analista de seguridad pública, compara las tendencias del crimen entre dos zonas de San Francisco:

Zona A: {zona1}
- Incidentes totales: {len(df1)}
- Días más activos: {', '.join(dias1)}
- Delitos más comunes: {', '.join(categorias1)}

Zona B: {zona2}
- Incidentes totales: {len(df2)}
- Días más activos: {', '.join(dias2)}
- Delitos más comunes: {', '.join(categorias2)}

Pregunta del usuario: {pregunta}

Aquí tienes una muestra de incidentes por zona:

Muestra de la Zona A:
{df1[['Dates', 'PdDistrict', 'DayOfWeek', 'Category', 'Descript', 'Resolution']].head(5).to_csv(index=False)}

Muestra de la Zona B:
{df2[['Dates', 'PdDistrict', 'DayOfWeek', 'Category', 'Descript', 'Resolution']].head(5).to_csv(index=False)}

Proporciona:

1. Comparación breve de los patrones (máx. 3 líneas).
2. Recomendación para las autoridades de la ciudad (máx. 2 líneas).
3. Consejo para los ciudadanos (1 línea).
4. Frase de resumen final.

La respuesta debe estar en español y estrictamente en formato .txt sin markdown ni bloques de código.
    """

    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    try:
        respuesta = requests.post(URL, headers=headers, data=json.dumps(payload))
        respuesta.raise_for_status()
        resultado = respuesta.json()
        texto = resultado["candidates"][0]["content"]["parts"][0]["text"]
        return texto.strip()
    except Exception as e:
        return f"❌ Error al generar análisis con Gemini: {str(e)}"
