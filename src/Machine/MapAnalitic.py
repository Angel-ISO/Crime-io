from openai import OpenAI
import pandas as pd

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="",
)

def generar_analisis_criminalidad(df: pd.DataFrame, distritos, dias, categorias) -> str:
    if df.empty:
        return "No hay suficientes datos para generar un análisis."

    prompt = f"""
Como experto en seguridad urbana, analiza estos datos de incidentes criminales en San Francisco:

- Distritos: {', '.join(distritos)}
- Días más activos: {', '.join(dias)}
- Tipos de crimen: {', '.join(categorias)}
- Total de incidentes analizados: {len(df)}

Se presentan los primeros registros como muestra:

{df[['Dates', 'PdDistrict', 'DayOfWeek', 'Category', 'Descript', 'Resolution']].head(10).to_csv(index=False)}

Solicito:

1. **Patrón principal** (ej: horarios/lugares críticos).
2. **Recomendación para autoridades** (máx 2 líneas).
3. **Consejo ciudadano** (máx 1 línea).

Respuesta en español y formato markdown.
    """

    try:
        completion = client.chat.completions.create(
            model="deepseek/deepseek-r1:free",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            extra_headers={
                "HTTP-Referer": "https://tusitio.com",  
                "X-Title": "AnalisisCriminalSF",        
            },
            extra_body={}
        )
        return completion.choices[0].message.content

    except Exception as e:
        return f"❌ Error al generar el análisis con IA: {str(e)}"
