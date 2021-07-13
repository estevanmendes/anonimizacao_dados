from datetime import datetime
from numpy.core.defchararray import center
import streamlit as st
import pandas as pd
import numpy as np
from anonimizacao import anonymization
import base64


def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="myfilename.csv">Download csv file</a>'
    return href



st.markdown('# Aplicativo de Anonimização de Dados')

st.markdown('## Faça Upoload do Arquivo (.csv,.txt,.xlsx)')
data_file=st.file_uploader('Arquivo',type=['csv','xlsx'])

df=[]

st.markdown('## Determine as características a serem Anonimizadas')


if data_file:
    if data_file.name[-3:]=='csv':
        df=pd.read_csv(data_file)
    elif data_file.name[-4:]=='xlsx':
        df=pd.read_excel(data_file)

    st.markdown('### Selecione as variáveis a serem anonimizadas')
    # left_column,right_column = st.beta_columns(2)
    # pressed = right_column.button('Próxima Etapa')

    st.write(df.head())


    options = df.columns
    checkbox_1=np.zeros(len(options),dtype=bool)
    for i in range(len(options)):
        checkbox_1[i]=st.checkbox(str(options[i]),key='1_'+str(i))
    
    
    # pressed=st.button('selecionado')
    # if pressed or pressed_before:
    N_col=len(np.where(checkbox_1==True)[0])
    cols=options[np.where(checkbox_1==True)]
    if  N_col>0:

        st.markdown('### Variáveis selecionadas:')    
        st.markdown('; '.join(cols))
    

    #selecionar as variáveis diretas e indiretas

        st.markdown("### Selecione as variáveis que identificam de forma direta e indireta")
        left_column,right_column=st.beta_columns(2)

        left_column.write('Direta')
        right_column.write('Indireta')



        checkbox_2_left=np.zeros(N_col,dtype=bool)
        checkbox_2_right=np.zeros(N_col,dtype=bool)
        print(N_col,cols)
        
        for i in range(N_col):
            checkbox_2_left[i]=left_column.checkbox(cols[i],key='2_left_'+str(i))
            checkbox_2_right[i]=right_column.checkbox(cols[i],key='2_right_'+str(i))
        
        personal_info=cols[np.where(checkbox_2_left==True)]
        partial_personal_info=cols[np.where(checkbox_2_right==True)]
        N_PPI=len(partial_personal_info)

        if N_PPI>0:
            st.markdown("### Selecione as variáveis numéricas discretas, ou datas para a adição de ruído")

            checkbox_3=np.zeros(N_PPI,dtype=bool)
            left_column,center_column,right_column=st.beta_columns(3)

            for i in range(N_PPI):
                checkbox_3[i]=left_column.checkbox(partial_personal_info[i],key='3_'+str(i))
            N_noise=len(np.where(checkbox_3==True)[0])

            if N_noise>0:
                datetime=np.zeros(N_noise,dtype=bool)
                amp_noise=np.zeros(N_noise)
                for i in range(N_noise):
                    datetime[i]=center_column.checkbox('Datetime',key='datetime_'+str(i))
                    if i==0:
                        st.write('Amplitude')
                    amp_noise[i]=st.select_slider(partial_personal_info[i],options=np.arange(1,20+1),key=str(i))    

                for i in np.where(datetime==True)[0]:
                    df[partial_personal_info[i]]=pd.to_datetime(df[partial_personal_info[i]])
            ##adicionar butão para fazer isso automáticamente.

            st.markdown("### Selecione as variáveis numéricas contínuas para o arredondamento")


            checkbox_4=np.zeros(N_PPI,dtype=bool)

            for i in range(N_PPI):
                checkbox_4[i]=st.checkbox(partial_personal_info[i],key='4_'+str(i))   


            ## pegar amplitude do ruído de cada 
        else:
            checkbox_3=np.zeros(N_PPI,dtype=bool)
            checkbox_4=np.zeros(N_PPI,dtype=bool)



        pressed=st.button('Anonimizar')
        if pressed:


            cols_noise=partial_personal_info[np.where(checkbox_3==True)]
            cols_round=partial_personal_info[np.where(checkbox_4==True)]

            anony=anonymization(df)
            anony.remove_personal_info(personal_info)
            if len(cols_noise)>0:
                anony.add_noise(cols_noise,amp_noise)
            if len(cols_round)>0:
                anony.round_data(cols_round)

            # st.write(df)

            st.markdown(get_table_download_link(df), unsafe_allow_html=True)
