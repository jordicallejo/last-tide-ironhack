"""Ejecutar: python run_analysis.py ruta/al/GSAF5.xlsx"""
import sys
import json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'src'))
from cleaning import run_pipeline, subset_without_invalid, subset_with_outcome
from analysis import activity_frequency, activity_by_outcome, outcome_by_era, geography_concentration, species_share, species_coverage_by_outcome, cramers_v
import pandas as pd

def main(path):
    df=run_pipeline(path)
    out=Path(__file__).parent/'outputs'
    out.mkdir(exist_ok=True)
    activity_frequency(df,top=15).to_csv(out/'h1_actividades.csv',index=False)
    pd.DataFrame([geography_concentration(df)]).to_csv(out/'h2_geografia.csv',index=False)
    h3=activity_by_outcome(df)
    h3.to_csv(out/'h3_des_enlace.csv')
    outcome_by_era(df).to_csv(out/'h3_epocas.csv',index=False)
    species_share(df).to_csv(out/'h4_especies.csv',index=False)
    species_coverage_by_outcome(subset_without_invalid(df)).to_csv(out/'h4_cobertura_por_des_enlace.csv')
    df[['activity','activity_clean','activity_group','fatal_y_n','fatal_clean','species','species_clean','species_group','species_identificada','country_clean','state_clean','location_clean']].to_csv(out/'auditoria_limpieza.csv',index=False)
    summary={'n_original':len(df),'invalid':int(len(df)-len(subset_without_invalid(df))), 'outcome_known':len(subset_with_outcome(df)),'fatal':df['fatal_clean'].value_counts().to_dict(),'cramers_v_actividad_des_enlace':round(cramers_v(pd.crosstab(subset_with_outcome(df)['activity_group'],subset_with_outcome(df)['fatal_clean'])),4),'identified_species_filtered':int(subset_without_invalid(df)['species_identificada'].sum()),'ruleset':'Reglas reproducibles en src/cleaning.py; NO idénticas necesariamente a las categorías de diapositivas'}
    (out/'resumen.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__':
    if len(sys.argv)<2: raise SystemExit('Uso: python run_analysis.py ruta/GSAF5.xlsx')
    main(sys.argv[1])
