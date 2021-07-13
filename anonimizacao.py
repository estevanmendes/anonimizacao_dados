import pandas as pd
import numpy as np
from cape_privacy.pandas.transformations import NumericPerturbation
from cape_privacy.pandas.transformations import Tokenizer
from cape_privacy.pandas import dtypes


class anonymization:

    def __init__(self,df):
        self.df=df
    
    def remove_personal_info(self,cols):
        for column in cols:
            self.df[column]=self.df[column].astype(str)
            random=np.random.randint(0,9,size=20)
            lengths = self.df[column].astype(str).map(len)
            tokenize = Tokenizer(max_token_len=max(lengths), key=str(random))
            self.df[column]=tokenize(self.df[column])

        return self.df

    def add_noise(self,cols,amplitudes,):
        #fazer essa função funcionar com datetime tambem    
        for column,amp in zip(cols,amplitudes):
            perturb_numeric = NumericPerturbation(dtype=dtypes.Integer, min=-amp, max=amp)          
            if np.issubdtype(self.df[column].dtype, np.datetime64):
                zeros=np.zeros(len(self.df))                
                self.df[column]=self.df[column]+pd.to_timedelta(perturb_numeric(zeros),unit='day')

            else:    
                perturb_numeric = NumericPerturbation(dtype=dtypes.Integer, min=-amp, max=amp)
                self.df[column]=perturb_numeric(self.df[column])
    
        return self.df


    def round_data(self,cols):
        
        for column in cols:
            self.df[column]=self.df[column].apply(round,0)
        
        return self.df
