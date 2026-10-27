import unittest
import pandas as pd
from src.cleaning import normalize_column_names, clean_fatal, clean_activity, subset_without_invalid
from src.analysis import activity_frequency

class TestPipeline(unittest.TestCase):
    def test_normalizacion(self):
        df = normalize_column_names(pd.DataFrame({'Fatal Y/N':['n',' y ', 'F', None], 'Activity':['swimmingq','spearfishiong',None,'Surfing'], 'Species ':['White shark']*4,'Type':['Invalid','Unprovoked',None,'Invalid']}))
        self.assertIn('fatal_y_n',df)
        df=clean_fatal(clean_activity(df))
        self.assertEqual(df['fatal_clean'].tolist(),['N','Y','UNKNOWN','UNKNOWN'])
        self.assertEqual(df.loc[0,'activity_clean'],'swimming')
        self.assertEqual(df.loc[1,'activity_clean'],'spearfishing')
        self.assertEqual(len(subset_without_invalid(df)),2)
    def test_frequency(self):
        df=pd.DataFrame({'activity_group':['surf y tablas','otras','surf y tablas']})
        self.assertEqual(activity_frequency(df).iloc[0]['recuento'],2)

if __name__=='__main__': unittest.main()
