# anonimizacao_dados

Contexto

O código desenvolvido tem por objetivo a anonimização de dados sensíveis. As variáveis que podem identificar um indivíduo de forma direta, por exemplo, o nome, endereço, CPF são criptografadas de forma irreversível. As variáveis que podem identificar os indivíduos de forma indireta podem ser perturbadas adicionando um ruído, ou serem arredondadas.


O código apresenta 3 métodos, além do construtor. São eles ``remove_personal_info()``, ``add_noise()``, ``round_data()``.

Foi utilizada a biblioteca [CapePrivacy](https://github.com/capeprivacy/cape-python) para realizar a criptografia e adicionar o ruído.

além disso, as bibliotecas pandas e numpy foram utilizadas.


## Guia rápido:
 
 ´´´
from anonimizacao.py import * 

dados_anonimizados=anonymization(df=dataframe)

supoonhamos que hajam 5 colunas, ['nome','altura','data_nascimento','data_obito','idade']

dados_anonimizados.remove_personal_info(cols=['nome'])

dados_anonimizados.add_noise(cols=['data_nascimento','data_obtido','idade'],amplitudes=[5,5,2])

dados_anonimizados.round_data(cols=['altura'])


novo_dataframe=dados_anonimizados.df

´´´

