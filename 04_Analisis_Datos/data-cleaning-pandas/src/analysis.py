"""
analysis.py — análisis exploratorio del GSAF limpio.

Proyecto LAST TIDE · Data Analytics · Ironhack.

QUÉ ESTÁ IMPLEMENTADO Y QUÉ NO
------------------------------
Implementadas (utilidades, no análisis propio):
    cramers_v()                     fórmula estadística estándar
    species_coverage_by_outcome()   comprobación para cerrar una duda abierta

Implementados los cinco análisis. Las cifras del documento original eran referencias
de Claude y no deben confundirse con resultados recalculados.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency


# --------------------------------------------------------------------------- #
# UTILIDADES — implementadas
# --------------------------------------------------------------------------- #
def cramers_v(confusion: pd.DataFrame) -> float:
    """V de Cramér a partir de una tabla de contingencia.

    Mide el TAMAÑO del efecto, entre 0 y 1. Con miles de filas el p-valor del
    χ² sale significativo casi siempre, así que es la V la que hay que
    presentar, no el p-valor.

    Referencia del proyecto: actividad × desenlace -> V ≈ 0,385.
    """
    chi2 = chi2_contingency(confusion)[0]
    n = confusion.to_numpy().sum()
    r, k = confusion.shape
    return float(np.sqrt((chi2 / n) / (min(r, k) - 1)))


def species_coverage_by_outcome(df: pd.DataFrame) -> pd.DataFrame:
    """% de registros CON especie identificada, dentro de cada desenlace.

    IMPLEMENTADA A PROPÓSITO: resuelve una contradicción abierta en el equipo.
    Circulan dos versiones incompatibles (18,6 % y 31,7 % para los mortales) y
    ninguna de las dos cuadra con las 2.058 identificaciones totales. Ejecuta
    esto sobre tu DataFrame limpio y la cifra que salga es la buena.

    Espera las columnas `fatal_clean` y `species_identificada`.

    Devuelve, por desenlace: n de registros, n identificados y % identificado.
    """
    base = df[df["fatal_clean"].isin(["Y", "N"])]
    out = (
        base.groupby("fatal_clean")["species_identificada"]
        .agg(n="size", identificadas="sum")
        .assign(pct_identificada=lambda t: (100 * t["identificadas"] / t["n"]).round(1))
    )
    out.index = out.index.map({"N": "No mortales", "Y": "Mortales"})
    return out


# --------------------------------------------------------------------------- #
# ANÁLISIS — el cuerpo lo escribes tú
# --------------------------------------------------------------------------- #
def activity_frequency(df: pd.DataFrame, top: int = 10) -> pd.DataFrame:
    """H1 — frecuencia de cada actividad sobre la base completa de 7.125.

    Devuelve `activity_group`, recuento y porcentaje sobre 7.125, ordenado.

    Control: surf y tablas 1.162 (16,31 %) · natación y baño 1.076 (15,10 %)
             pesca 7,2 % · pesca submarina 5,7 %
             Las cuatro primeras suman el 44,3 %.

    Recuerda al presentarlo: esto es frecuencia registrada, no probabilidad de
    ataque. Falta el denominador de exposición.
    """
    counts = df['activity_group'].value_counts(dropna=False).head(top)
    return pd.DataFrame({'activity_group':counts.index, 'recuento':counts.values, 'porcentaje':(counts.values/len(df)*100).round(2)})


def activity_by_outcome(df: pd.DataFrame) -> pd.DataFrame:
    """H3 — reparto de actividades DENTRO de cada desenlace.

    Es el núcleo de la hipótesis 3. La clave es normalizar por COLUMNA, no por
    el total: cada columna (N e Y) debe sumar 100 %. Así se compara la
    composición de cada grupo, no la probabilidad de morir.

    Pasos:
        1. Partir de subset_with_outcome(df) -> 6.482 filas.
        2. pd.crosstab(activity_group, fatal_clean, normalize='columns') * 100.
        3. Redondear a un decimal y ordenar por la diferencia entre columnas.

    Control (columnas al 100 % dentro de cada desenlace, N=4.986, Y=1.496):
             surf y tablas       28,8 % (N)  frente a   7,6 % (Y)
             natación y baño     23,3 % (N)  frente a  37,0 % (Y)
             naufragio / caída    1,8 % (N)  frente a  16,2 % (Y)
    """
    base = df.loc[df['fatal_clean'].isin(['N','Y'])]
    return (pd.crosstab(base['activity_group'],base['fatal_clean'],normalize='columns')*100).round(2).sort_values('Y',ascending=False)


def outcome_by_era(df: pd.DataFrame, corte: int = 2000) -> pd.DataFrame:
    """H3 — la misma tabla, partida por época, para ver qué es histórico.

    Separar por épocas NO controla el sesgo: solo enseña cuánto depende de la
    época. Dilo así en la defensa.

    Control: desde el año 2000 la diferencia de natación y baño entre
             desenlaces cae de +13,6 a +5,6 puntos; la del surf se mantiene.
    """
    base = df[df['fatal_clean'].isin(['Y','N'])].copy()
    years = pd.to_numeric(base['year'],errors='coerce')
    base['epoca'] = np.where(years>=corte, f'Desde {corte}', f'Antes de {corte}')
    base = base.loc[years.notna()]
    if base.empty: return pd.DataFrame(columns=['epoca','activity_group','fatal_clean','porcentaje'])
    tab = pd.crosstab([base['epoca'],base['activity_group']], base['fatal_clean'],normalize='columns')
    # Porcentajes por desenlace DENTRO de cada época; no sobre todos los años.
    out = []
    for era, g in base.groupby('epoca'):
        t = pd.crosstab(g['activity_group'],g['fatal_clean'],normalize='columns')*100
        for activity,row in t.iterrows():
            for outcome,val in row.items(): out.append({'epoca':era,'activity_group':activity,'fatal_clean':outcome,'porcentaje':round(float(val),2)})
    return pd.DataFrame(out)


def geography_concentration(df: pd.DataFrame) -> dict:
    """H2 — concentración por país y dispersión por lugar.

    Devuelve un dict con: pct_top3_paises, pct_top10_paises, pct_florida,
    pct_top10_lugares y n_lugares_distintos.

    Control: 66,9 % en EE. UU. + Australia + Sudáfrica (sobre registros con
             país conocido) · 78,3 % los diez primeros · Florida 18,1 % sobre
             registros con estado conocido · 6,1 % los diez lugares más
             frecuentes · 4.569 lugares distintos.
    """
    country = df['country_clean'].replace('DESCONOCIDO',pd.NA).dropna()
    state = df['state_clean'].replace('DESCONOCIDO',pd.NA).dropna()
    place = df['location_clean'].replace('DESCONOCIDO',pd.NA).dropna()
    cv = country.value_counts(); sv=state.value_counts(); pv=place.value_counts()
    top3_names = ['USA','AUSTRALIA','SOUTH AFRICA']
    return {'pct_top3_paises':round(100*sum(cv.get(x,0) for x in top3_names)/len(country),2) if len(country) else None,'pct_top10_paises':round(100*cv.head(10).sum()/len(country),2) if len(country) else None, 'pct_florida':round(100*sv.get('Florida',0)/len(state),2) if len(state) else None,'pct_top10_lugares':round(100*pv.head(10).sum()/len(place),2) if len(place) else None,'n_lugares_distintos':int(place.nunique()),'n_pais_conocido':len(country),'n_estado_conocido':len(state),'n_lugar_conocido':len(place)}


def species_share(df: pd.DataFrame) -> pd.DataFrame:
    """H4 — reparto de especies, solo sobre las identificadas.

    Pasos:
        1. Partir de subset_without_invalid(df) -> 6.573 filas.
        2. Filtrar species_identificada == True -> 2.058 filas.
        3. Porcentaje de cada species_group sobre esas 2.058.

    Control: blanco 34 % · tigre 15 % · toro 13 %
             Cobertura: 2.058 / 6.573 = 31,3 % identificada; ~69 % sin especie.

    Al presentarlo: esto mide cobertura documental, no peligrosidad. Antes de
    afirmar nada sobre el sesgo, ejecuta species_coverage_by_outcome().
    """
    base = df.loc[~df['type'].astype('string').str.strip().str.lower().eq('invalid').fillna(False)]
    valid = base.loc[base['species_identificada']]
    counts=valid['species_group'].value_counts()
    return pd.DataFrame({'especie':counts.index,'recuento':counts.values,'porcentaje':(100*counts.values/max(1,len(valid))).round(2)})
