# Importar Bibliotecas

import streamlit as st
import pandas as pd

cnaeURL = "https://github.com/bruninhanic/riscoVisaMG/blob/main/cnaesVisa.csv?raw=true"
#riscoURL =

@st.cache
def load_data():
    # carrega os dados das atividades

    data = pd.read_csv(cnaeURL, dtype='object', encoding='utf8', sep=';', index_col='codigoCnae')

    return data

df = load_data()
labels = df.index.tolist()

#SIDEBAR

st.sidebar.header('Informe as atividades do estabelecimento')
info_sidebar = st.sidebar.empty()

#Checbox do cnae
st.sidebar.header('Atividades Econômicas')
label_to_filter = st.sidebar.multiselect(
    'Escolha as atividades:',
    labels
)
#Informação no rodapé do sidebar
st.sidebar.markdown('Para a correta classificação de risco, você deve informar todas as atividades sujeitas a controle sanitário.')

#Aplicação do filtro no dataframe e classificação do risco
filtered_df = df[df.index.isin(label_to_filter)]

riscos = filtered_df.classificacaoRisco.to_list()

def risco_estabelecimento():
    
    if not riscos:
        classificacaoRisco = None
        return classificacaoRisco        
    if 'Nível de Risco III' in riscos:
        classificacaoRisco = 'Nível de Risco III'
        return classificacaoRisco
    elif 'Nível de Risco III' not in riscos and 'Atividade econômica dependente de informação e condicionante' in riscos:
        classificacaoRisco = 'Atividade econômica dependente de informação e condicionante'
        return classificacaoRisco
    elif 'Nível de Risco II' in riscos and 'Atividade econômica dependente de informação e condicionante' not in riscos and 'Nível de Risco III' not in riscos:
        classificacaoRisco = 'Nível de Risco II'
        return classificacaoRisco
    else:
        classificacaoRisco = 'Nível de Risco I'
        return classificacaoRisco

classificacaoRisco = risco_estabelecimento()


#PRINCIPAL
st.title('Consulta a classificação de risco sanitário do estabelecimento - Resolução SES/MG n. 7426/2021')
st.markdown(f"""
            Para o estabelecimento que realiza as atividades classificadas como **{", ".join(label_to_filter)}**, o risco sanitário do estabelecimento é:""")
st.text_area('Risco do estabelecimento:', value=classificacaoRisco)
st.write('Riscos das atividades:', filtered_df)
