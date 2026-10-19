
"""Conexión con Groq para StatMentor AI (versión revisada)."""
import os
import re
import traceback

import groq
from dotenv import load_dotenv
from groq import Groq

load_dotenv()  # Local: lee el archivo .env (nunca se sube a GitHub)

MODELO = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
MAX_CARACTERES = 3000

PROMPT_SISTEMA = """Eres StatMentor AI, tutor de Estadística Aplicada para estudiantes \
universitarios de ingeniería. Responde siempre en español, de forma clara, paciente y didáctica.

ALCANCE:
- Solo resuelves temas de estadística descriptiva, datos experimentales y unidades, tablas \
y gráficas, probabilidad, distribución normal, correlación y regresión lineal simple.
- Si la pregunta es de otro tema, indica amablemente que solo ayudas con estadística.


FORMATO MATEMÁTICO:
- Escribe las fórmulas y operaciones en texto plano, nunca en LaTeX.
- No utilices barras invertidas ni comandos como frac, sum, boxed,
  sqrt, displaystyle, begin o end.
- Para la media, escribe: Media = suma de los datos / número de observaciones.
- Para la mediana, explica cuáles son las posiciones centrales y
  escribe la operación completa.
- Para la desviación estándar, escribe:
  Desviación estándar = raíz cuadrada de la varianza.
- Muestra las operaciones con números reales del ejercicio.
- Utiliza Markdown para destacar los resultados importantes.
- Antes de responder, verifica que las fórmulas, operaciones y
  resultados sean coherentes entre sí.


ESTRUCTURA OBLIGATORIA (usa exactamente estos encabezados de Markdown):
## Datos
Resume los datos recibidos, con sus unidades, y qué se pide calcular.
## Procedimiento
Fórmula con sus elementos definidos, sustitución paso a paso y operaciones intermedias. \
Separa la fórmula, la sustitución y el resultado de cada paso.
## Resultado final
Solo las respuestas finales, con unidades y 4 decimales cuando corresponda.
## Interpretación
Explica el resultado en el contexto del ejercicio.

REGLAS:
- Si faltan datos, hay datos inconsistentes (por ejemplo x e y con distinta cantidad) o no es \
posible resolver el caso, dilo claramente y pide lo que falta. No inventes datos ni cálculos.
- Indica siempre si usas desviación estándar muestral (n - 1) o poblacional (n) y por qué. \
Si no se aclara, asume muestral para mediciones y avísalo.
- En la mediana, ordena los datos y muestra las posiciones centrales. En la moda, indica qué \
valores se repiten; si ninguno, dilo.
- Resuelve todos los apartados solicitados y evita repetir información.

- No afirmes que una distribución es simétrica solo porque la media
  y la mediana coinciden.
- No afirmes que la mayoría de los datos está dentro de una desviación
  estándar de la media sin comprobarlo.
- Interpreta la desviación estándar como una medida de dispersión
  respecto a la media.
- No confundas correlación con causalidad.
- Si el usuario pide varios cálculos, resuelve todos los apartados.
- Si el resultado depende de un supuesto, explica cuál estás usando."""


def _obtener_clave():
    """Busca la clave en .env/variables de entorno y, si no, en st.secrets (Streamlit Cloud)."""
    clave = os.getenv("GROQ_API_KEY")
    if clave:
        return clave
    try:
        import streamlit as st
        return st.secrets.get("GROQ_API_KEY")
    except Exception:
        return None


def consultar_groq(pregunta):
    """Envía una pregunta de estadística a Groq y devuelve el texto de respuesta."""
    if not pregunta or not pregunta.strip():
        return "Escribe una pregunta para poder ayudarte."
    if len(pregunta) > MAX_CARACTERES:
        return f"La pregunta es muy larga (máximo {MAX_CARACTERES} caracteres). Resúmela un poco."

    clave = _obtener_clave()
    if not clave:
        return ("No se encontró GROQ_API_KEY. En local revisa tu archivo .env; "
                "en Streamlit Cloud agrégala en Settings → Secrets.")

    try:
        cliente = Groq(api_key=clave, timeout=45.0, max_retries=2)
        parametros = dict(
            model=MODELO,
            messages=[
                {"role": "system", "content": PROMPT_SISTEMA},
                {"role": "user", "content": pregunta.strip()},
            ],
            temperature=0.2,
            max_completion_tokens=8000,  # los modelos de razonamiento gastan tokens "pensando"
        )
        if "gpt-oss" in MODELO:
            parametros["reasoning_effort"] = "medium"

        respuesta = cliente.chat.completions.create(**parametros)
        eleccion = respuesta.choices[0]
        texto = eleccion.message.content
        motivo = eleccion.finish_reason

        if not texto or not texto.strip():
            if motivo == "length":
                return ("La IA agotó su límite de longitud antes de responder. "
                        "Intenta con una pregunta más corta o por partes.")
            return "La IA no devolvió una respuesta. Inténtalo nuevamente."

        if motivo == "length":
            texto += ("\n\n**Nota:** la respuesta alcanzó el límite de longitud. "
                      "Puedes pedir que continúe desde el último apartado.")
        return texto

    except groq.AuthenticationError:
        return "La clave de Groq no es válida o fue revocada. Genera una nueva en console.groq.com."
    except groq.RateLimitError:
        return "Se alcanzó el límite de uso gratuito de Groq. Espera un minuto e inténtalo de nuevo."
    except groq.APIConnectionError:
        return "No se pudo conectar con Groq. Revisa tu conexión a internet."
    except groq.APIStatusError as e:
        print(traceback.format_exc())
        return f"Groq respondió con el error {e.status_code}. Verifica que el modelo '{MODELO}' siga disponible."
    except Exception as e:
        print(traceback.format_exc())  # el detalle queda en la consola, no en pantalla
        return f"Ocurrió un error inesperado ({type(e).__name__}). Inténtalo nuevamente."


def dividir_secciones(texto):
    """Separa la respuesta en datos / procedimiento / resultado / interpretacion."""
    out = {"datos": "", "procedimiento": "", "resultado": "", "interpretacion": ""}
    actual, previo = None, []
    for linea in texto.splitlines():
        m = re.match(r"^\s*#{1,4}\s*(datos|procedimiento|resultado|interpretaci[oó]n)", linea, re.I)
        if m:
            actual = m.group(1).lower().replace("ó", "o")
            continue
        if actual:
            out[actual] += linea + "\n"
        else:
            previo.append(linea)
    if not any(v.strip() for v in out.values()):
        out["procedimiento"] = texto  # el modelo no usó encabezados: se muestra todo junto
    elif "\n".join(previo).strip() and not out["datos"].strip():
        out["datos"] = "\n".join(previo)
    return {k: v.strip() for k, v in out.items()}   


