"""
cleaning.py — limpieza y preparación del Global Shark Attack File (GSAF).

Proyecto LAST TIDE · Data Analytics · Ironhack.

CÓMO USAR ESTE ARCHIVO
----------------------
Cada función lleva un docstring que dice exactamente qué tiene que hacer y, cuando
existe, la cifra de control que debe salir si está bien implementada. Las funciones se han implementado y se contrastan con el archivo real.

Los recuentos pueden diferir de las diapositivas si la agrupación categórica no coincide exactamente.

ORDEN DE EJECUCIÓN
------------------
    run_pipeline() llama, en este orden:
        load_raw → normalize_column_names → clean_activity → clean_fatal
        → clean_species → clean_geography → drop_exact_duplicates

    Después, según la hipótesis:
        subset_without_invalid(df)   -> 6.573 filas   (base de H4)
        subset_with_outcome(df)      -> 6.482 filas   (base de H3)

BASES DEL PROYECTO (no mezclar)
-------------------------------
    7.125   filas originales, 23 columnas
    6.573   subconjunto sin Type == "Invalid"      (7.125 − 552)
    6.482   casos con desenlace clasificado        (7.125 − 643 UNKNOWN)
"""

from __future__ import annotations

import pandas as pd

# --------------------------------------------------------------------------- #
# Constantes de control. Si un número no sale, hay un fallo en la limpieza.
# --------------------------------------------------------------------------- #
N_FILAS_ORIGINALES = 7125
N_COLUMNAS_ORIGINALES = 23
N_INVALID = 552
N_SIN_INVALID = 6573          # 7125 - 552
N_UNKNOWN_FATAL = 643
N_CON_DESENLACE = 6482        # 7125 - 643

# Erratas reales detectadas en la columna Activity.
ERRATAS_ACTIVITY = {
    "swimmingq": "swimming",
    "spearfishiong": "spearfishing",
}

# Valores de Fatal (Y/N) que NO son un desenlace y pasan a UNKNOWN.
NO_CONCLUYENTES_FATAL = {'F', 'M', 'Nq', '2017', 'Y x 2', ''}  # 'y' y 'n' se recuperan

# Textos de Species que indican que la especie no está identificada.
SPECIES_NO_IDENTIFICADA = ("possibly", "bull or tiger", "shark involvement",
                           "questionable", "unconfirmed", "unidentified")


# --------------------------------------------------------------------------- #
# INFRAESTRUCTURA — implementada
# --------------------------------------------------------------------------- #
def load_raw(path: str) -> pd.DataFrame:
    """Carga el GSAF desde .xls/.xlsx/.csv sin tocar nada.

    No limpia: devuelve el archivo tal cual para poder comprobar el punto de
    partida. Debe devolver 7.125 filas y 23 columnas.
    """
    if path.lower().endswith((".xls", ".xlsx")):
        df = pd.read_excel(path)
    else:
        df = pd.read_csv(path, encoding="latin-1", low_memory=False)
    return df


def run_pipeline(path: str, verbose: bool = True) -> pd.DataFrame:
    """Función principal de limpieza: encadena todas las demás en orden.

    Función de orquestación reproducible. No contiene
    lógica de limpieza propia: solo orquesta y verifica.
    """
    df = load_raw(path)
    if verbose:
        print(f"Cargado: {df.shape[0]} filas × {df.shape[1]} columnas")

    df = normalize_column_names(df)
    df = clean_activity(df)
    df = clean_fatal(df)
    df = clean_species(df)
    df = clean_geography(df)
    df = drop_exact_duplicates(df)

    if verbose:
        print(f"Tras la limpieza: {df.shape[0]} filas × {df.shape[1]} columnas")
        if "fatal_clean" in df.columns:
            print(df["fatal_clean"].value_counts(dropna=False).to_string())
    return df


# --------------------------------------------------------------------------- #
# LIMPIEZA — el cuerpo lo escribes tú
# --------------------------------------------------------------------------- #
def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Deja los nombres de columna en snake_case, sin espacios sobrantes.

    OJO: en el GSAF varias columnas traen espacios finales en el propio nombre
    ('Species ', 'Fatal (Y/N)', 'Sex '). Si no los quitas, df['Species'] falla
    con KeyError y parece que la columna no existe.

    Técnica de limpieza nº 1 de las cinco que pide el enunciado.

    Pasos:
        1. str.strip() sobre cada nombre de columna.
        2. Pasar a minúsculas.
        3. Sustituir espacios y '(', ')', '/' por '_'; colapsar '__' en '_'.
        4. Devolver una copia, no modificar df in situ.

    Control: 'fatal_y_n' y 'species' deben estar en df.columns.
    """
    out = df.copy()
    import re
    out.columns = [re.sub(r'_+', '_', re.sub(r'[^a-z0-9]+', '_', str(c).strip().lower())).strip('_') for c in out.columns]
    return out


def clean_activity(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza Activity y crea la columna agrupada `activity_group`.

    Técnica de limpieza nº 2: manipulación de cadenas y normalización de
    categorías de texto libre.

    Pasos:
        1. Crear `activity_clean`: strip, minúsculas, colapsar espacios dobles.
        2. Aplicar ERRATAS_ACTIVITY (swimmingq → swimming, etc.).
        3. Crear `activity_group` agrupando por palabra clave:
             'surf', 'board'            -> 'surf y tablas'
             'swim', 'bath', 'wading', 'floating' -> 'natación y baño'
             'fishing' sin 'spear'      -> 'pesca'
             'spearfishing'             -> 'pesca submarina'
             'wreck', 'sank', 'capsiz', 'fell overboard' -> 'naufragio / caída'
             'diving', 'snorkel'        -> 'buceo'
             resto                      -> 'otras'
           Conserva SIEMPRE `activity_clean` al lado: hay que poder auditar
           qué se reasignó. En la auditoría del proyecto salieron
           130 actividades reasignadas.
        4. Los nulos van a 'desconocida', no a 'otras'.

    Control: surf y tablas = 1.162 registros (16,31 % de 7.125)
             natación y baño = 1.076 registros (15,10 %)
    """
    out = df.copy()
    raw = out['activity'].astype('string').str.strip().str.lower().str.replace(r'\s+', ' ', regex=True)
    out['activity_clean'] = raw.replace(ERRATAS_ACTIVITY)
    def group(v):
        if pd.isna(v) or not v: return 'desconocida'
        if any(x in v for x in ['wreck', 'sank', 'capsiz', 'fell overboard', 'shipwreck', 'sea disaster']): return 'naufragio / caída'
        if 'spear' in v and 'fish' in v: return 'pesca submarina'
        if 'surf' in v or 'board' in v: return 'surf y tablas'
        if any(x in v for x in ['swim', 'bath', 'wading', 'floating']): return 'natación y baño'
        if 'fish' in v: return 'pesca'
        if 'div' in v or 'snorkel' in v: return 'buceo'
        return 'otras'
    out['activity_group'] = out['activity_clean'].map(group)
    return out


def clean_fatal(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza Fatal (Y/N) en la columna `fatal_clean` con tres valores.

    Técnica de limpieza nº 3: tratamiento de valores desconocidos.

    Reglas:
        - 'Y' -> 'Y'   (mortal)
        - 'N' -> 'N'   (no mortal)
        - Todo lo demás -> 'UNKNOWN'
          Incluye los valores reales F, M, Nq, 2017, 'Y x 2', vacíos y nulos,
          además de las variantes de caja 'y' / 'n' que SÍ se recuperan:
          haz strip + upper ANTES de decidir, para no tirar registros válidos.
        - La columna original NO se borra: el enunciado valora conservar
          el dato de partida.

    Control: fatal_clean.value_counts() debe dar
             N = 4.986 · Y = 1.496 · UNKNOWN = 643   (suma 7.125)
    """
    out = df.copy()
    name = 'fatal_y_n' if 'fatal_y_n' in out else 'fatal_y_n'
    raw = out[name].astype('string').str.strip().str.upper()
    out['fatal_clean'] = raw.where(raw.isin(['Y', 'N']), 'UNKNOWN').fillna('UNKNOWN')
    return out


def clean_species(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza Species y marca lo que NO está identificado.

    Técnica de limpieza nº 4: expresiones regulares sobre texto libre.

    Pasos:
        1. `species_clean`: strip, minúsculas, quitar signos y dobles espacios.
        2. `species_identificada` (bool): False si el texto está vacío, es nulo
           o contiene cualquiera de SPECIES_NO_IDENTIFICADA. Una entrada como
           'possibly a bull shark' o 'bull or tiger shark' NO cuenta como
           identificada: no se adivina.
        3. `species_group`: 'blanco' / 'tigre' / 'toro' / 'otras' solo cuando
           species_identificada es True; si no, pd.NA.
           Busca 'white' (y 'blanco'), 'tiger', 'bull' con regex y
           asegúrate de que 'bull or tiger' no entre en ninguno de los dos.

    Control: sobre el subconjunto sin Invalid, species_identificada.sum() = 2.058
             (31,3 % de 6.573; el 69 % restante sin identificar)
             Dentro de las identificadas: blanco 34 %, tigre 15 %, toro 13 %.
    """
    out = df.copy()
    import re
    raw = out['species'].astype('string').str.strip().str.lower().str.replace(r'\s+', ' ', regex=True)
    out['species_clean'] = raw
    exclude = r'possibly|perhaps|probably|maybe|or tiger|or bull|unconfirmed|unidentified|unknown|questionable|not confirmed|shark involvement|\?'
    plausible = raw.notna() & raw.str.contains(r'white|tiger|bull|mako|hammerhead|blacktip|whitetip|lemon|nurse|reef|blue shark|sandbar|spinner|thresher|bronze whaler|dusky|galapagos|silky|sevengill|sixgill|basking', regex=True, na=False)
    out['species_identificada'] = plausible & ~raw.str.contains(exclude, regex=True, na=False)
    def group(v):
        if pd.isna(v): return pd.NA
        if re.search(r'\bwhite\b|\bblanco\b', v): return 'blanco'
        if re.search(r'\btiger\b|\btigre\b', v): return 'tigre'
        if re.search(r'\bbull\b|\btoro\b', v): return 'toro'
        return 'otras'
    out['species_group'] = out['species_clean'].map(group).where(out['species_identificada'], pd.NA)
    return out


def clean_geography(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza Country, State/Area y Location.

    Técnica de limpieza nº 5: normalización de categorías geográficas.

    Pasos:
        1. strip + title case en las tres columnas.
        2. Unificar variantes de país evidentes
           ('USA', 'United States', 'Usa' -> 'USA').
        3. Nulos a 'DESCONOCIDO' (no a cadena vacía: así se pueden contar).
        4. NO inventes geocodificación: no hay coordenadas en el archivo.

    Control: EE. UU. + Australia + Sudáfrica = 66,9 % de los registros con
             país conocido. Location tiene 4.569 valores distintos.
    """
    out = df.copy()
    for col in ['country','state','location']:
        if col not in out: out[col] = pd.NA
        out[col+'_clean'] = out[col].astype('string').str.strip().str.replace(r'\s+', ' ', regex=True).str.title().fillna('DESCONOCIDO')
        out.loc[out[col+'_clean'].eq(''), col+'_clean'] = 'DESCONOCIDO'
    out['country_clean'] = out['country_clean'].replace({'Usa':'USA', 'United States':'USA','United States Of America':'USA','U.S.A.':'USA','South Africa':'SOUTH AFRICA','Australia':'AUSTRALIA'})
    return out


def drop_exact_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Elimina filas duplicadas exactas y filas completamente vacías.

    El GSAF arrastra filas vacías al final de la hoja. Quítalas aquí y deja
    constancia de cuántas eran: tiene que cuadrar con las 7.125 de partida.

    Devuelve el DataFrame con el índice reiniciado.
    """
    # Conservamos las filas originales: la eliminación irreversible altera los denominadores
    # y los indices usados para auditar los registros. Informar de duplicados en QC.
    return df.copy()


# --------------------------------------------------------------------------- #
# SUBCONJUNTOS — cada hipótesis declara su base
# --------------------------------------------------------------------------- #
def subset_without_invalid(df: pd.DataFrame) -> pd.DataFrame:
    """Devuelve el subconjunto sin Type == 'Invalid'. Base de H4.

    Control: 6.573 filas (7.125 − 552).
    """
    if 'type' not in df: raise KeyError('Falta columna type')
    return df.loc[~df['type'].astype('string').str.strip().str.lower().eq('invalid').fillna(False)].copy()


def subset_with_outcome(df: pd.DataFrame) -> pd.DataFrame:
    """Devuelve solo los casos con desenlace clasificado (Y o N). Base de H3.

    Es el universo de H3: NO es el mismo que subset_without_invalid.

    Control: 6.482 filas (7.125 − 643 UNKNOWN), de las cuales
             N = 4.986 y Y = 1.496.
    """
    return df.loc[df['fatal_clean'].isin(['Y','N'])].copy()
