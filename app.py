# Importar Bibliotecas

import streamlit as st
import pandas as pd


riscoURL = r"https://github.com/bruninhanic/riscoVisaMG/blob/main/riscoVisa.csv?raw=true"

perguntaURL = "https://github.com/bruninhanic/riscoVisaMG/blob/main/perguntas.csv"

respostaURL = "https://github.com/bruninhanic/riscoVisaMG/blob/main/respostaRisco.csv"

atividadeURL = "https://github.com/bruninhanic/riscoVisaMG/blob/main/cnaesVisa.csv?raw=True"

@st.cache

def load_atividade():
    # carrega os dados das atividades
    atividade = pd.read_csv(atividadeURL,
                        dtype={'codigoCnae': 'object', 'descricaoCnae': 'object'},
                        sep=';', encoding='utf8', on_bad_lines='skip', engine='c', header=0)
    dAtividade = dict([(i, j) for i, j in zip(atividade.codigoCnae, atividade.descricaoCnae)])
    return dAtividade

dAtividade = load_atividade()

def load_data():
    # carrega os dados de risco

    data = pd.read_csv(riscoURL,
                       dtype={'codigoCnae':'object', 'classificacaoRisco':'object', 'idPergunta':'object'},
                       sep=';', encoding='latin1', header=0, on_bad_lines='skip', engine='c')

    data['descricaoCnae'] = data['codigoCnae'].map(dAtividade)
    data['codDesc'] = (data.codigoCnae + " - " + data.descricaoCnae)

    data.set_index('codigoCnae', inplace=True)
    return data

df = load_data()


labels = sorted(df.codDesc.tolist())


def load_perguntas():
    # carrega os dados das perguntas
    col_names_perguntas = ['idPergunta', 'descricaoPergunta']
    perguntas_df = pd.read_csv(perguntaURL, encoding='utf8', sep=';', names=col_names_perguntas,
                               dtype={'idPergunta': 'object','descricaoPergunta': 'object'},
                               index_col='idPergunta' )
    return perguntas_df

perguntas_df = load_perguntas()

def load_respostas():
    # carrega os dados das respostas
    col_names_respostas = ['idPergunta', 'resposta', 'risco']
    respostas_df = pd.read_csv(respostaURL, encoding='utf8', sep=';', names=col_names_respostas,
                               dtype={'idPergunta': 'object','resposta': 'object', 'risco': 'object'}
                               )
    respostas_df['idResposta']=(respostas_df['idPergunta']+respostas_df['resposta'])
    return respostas_df

respostas_df = load_respostas()


st.header('Consulta a classificação do risco sanitário de estabelecimentos segundo a legislação de Minas Gerais')
st.text('Código de Saúde do Estado de Minas Gerais')
st.text('Resolução SES/MG n. 7426/2021')

st.markdown('Aviso 1:')
st.caption('As classificações de risco da aplicação se referem ao disposto na Resolução SES/MG 7426/2021, aplicável aos estabelecimentos mineiros.')
st.markdown('Aviso 2:')
st.caption('Caso exista norma específica em algum Município mineiro, pode haver diferença entre os resultados apresentados e a orientação fornecida pela Vigilância Sanitária Municipal concernente.')
st.markdown('Aviso 3:')
st.caption('Este projeto encontra-se em fase de teste e validação.')
st.markdown('Aviso 4:')
st.caption('A utilização desta ferramenta não substitui a consulta aos Órgãos de Vigilância Sanitária.')
st.text('')

# ESCOLHER ATIVIDADES

st.subheader('Vamos começar!')
# Checbox do cnae

label_to_filter = st.multiselect(
    'Escolha as atividades:',
    labels
    )
# Informação
st.caption(' ')
st.caption(
    '** Para a correta classificação de risco, você deve informar todas as atividades sujeitas a controle sanitário. **')
st.caption(' ')

#Exibição das perguntas
filtered_df = df[df.codDesc.isin(label_to_filter)]

idPerguntas = list()
for i,j in zip(filtered_df.index, filtered_df.idPergunta):
    item = (i+' - '+j)
    if item not in idPerguntas:
        idPerguntas.append(item)

perguntas = dict([(i, j) for i, j in zip(perguntas_df.idPergunta, perguntas_df.descricaoPergunta)])        

perguntas

descPerguntas = list()
for i in idPerguntas:
    n = i.split(' - ')[1]
    a = i.split(' - ')[0]
    if n != '0':
        p = (a+" - "+n+" - "+perguntas[n])
        descPerguntas.append(p)

#Definição do risco após a resposta
drespostas = {'10NÃO': 'Nível de Risco I',
 '10SIM': 'Nível de Risco III',
 '11NÃO': 'Nível de Risco I',
 '11SIM': 'Nível de Risco III',
 '12NÃO': 'Nível de Risco II',
 '12SIM': 'Nível de Risco III',
 '13NÃO': 'Nível de Risco II',
 '13SIM': 'Nível de Risco III',
 '14NÃO': 'Nível de Risco I',
 '14SIM': 'Nível de Risco III',
 '15NÃO': 'Nível de Risco I',
 '15SIM': 'Nível de Risco III',
 '16NÃO': 'Nível de Risco I',
 '16SIM': 'Nível de Risco III',
 '17NÃO': 'Nível de Risco I',
 '17SIM': 'Nível de Risco III',
 '18NÃO': 'Nível de Risco I',
 '18SIM': 'Nível de Risco III',
 '19NÃO': 'Nível de Risco I',
 '19SIM': 'Nível de Risco III',
 '1NÃO': 'Nível de Risco III',
 '1SIM': 'Nível de Risco II',
 '20NÃO': 'Nível de Risco I',
 '20SIM': 'Nível de Risco III',
 '21NÃO': 'Nível de Risco II',
 '21SIM': 'Nível de Risco III',
 '22NÃO': 'Nível de Risco I',
 '22SIM': 'Nível de Risco III',
 '23NÃO': 'Nível de Risco II',
 '23SIM': 'Nível de Risco III',
 '24NÃO': 'Nível de Risco II',
 '24SIM': 'Nível de Risco III',
 '25NÃO': 'Nível de Risco II',
 '25SIM': 'Nível de Risco III',
 '26NÃO': 'Nível de Risco II',
 '26SIM': 'Nível de Risco III',
 '27NÃO': 'Nível de Risco I',
 '27SIM': 'Nível de Risco II',
 '28NÃO': 'Nível de Risco I',
 '28SIM': 'Nível de Risco II',
 '29NÃO': 'Nível de Risco I',
 '29SIM': 'Nível de Risco III',
 '2NÃO': 'Nível de Risco III',
 '2SIM': 'Nível de Risco II',
 '30NÃO': 'Nível de Risco I',
 '30SIM': 'Nível de Risco III',
 '31NÃO': 'Nível de Risco I',
 '31SIM': 'Nível de Risco III',
 '32NÃO': 'Nível de Risco I',
 '32SIM': 'Nível de Risco III',
 '33NÃO': 'Nível de Risco II',
 '33SIM': 'Nível de Risco III',
 '34NÃO': 'Nível de Risco I',
 '34SIM': 'Nível de Risco III',
 '35NÃO': 'Nível de Risco I',
 '35SIM': 'Nível de Risco III',
 '36NÃO': 'Nível de Risco II',
 '36SIM': 'Nível de Risco III',
 '37NÃO': 'Nível de Risco II',
 '37SIM': 'Nível de Risco III',
 '38NÃO': 'Nível de Risco II',
 '38SIM': 'Nível de Risco III',
 '39NÃO': 'Nível de Risco II',
 '39SIM': 'Nível de Risco III',
 '3NÃO': 'Nível de Risco I',
 '3SIM': 'Nível de Risco III',
 '40NÃO': 'Nível de Risco II',
 '40SIM': 'Nível de Risco III',
 '41NÃO': 'Nível de Risco I',
 '41SIM': 'Nível de Risco II',
 '42NÃO': 'Nível de Risco II',
 '42SIM': 'Nível de Risco III',
 '43NÃO': 'Nível de Risco II',
 '43SIM': 'Nível de Risco III',
 '44NÃO': 'Nível de Risco I',
 '44SIM': 'Nível de Risco II',
 '45NÃO': 'Nível de Risco II',
 '45SIM': 'Nível de Risco III',
 '4NÃO': 'Nível de Risco III',
 '4SIM': 'Nível de Risco I',
 '5NÃO': 'Nível de Risco III',
 '5SIM': 'Nível de Risco II',
 '6NÃO': 'Nível de Risco III',
 '6SIM': 'Nível de Risco II',
 '7NÃO': 'Nível de Risco III',
 '7SIM': 'Nível de Risco I',
 '8NÃO': 'Nível de Risco I',
 '8SIM': 'Nível de Risco III',
 '9NÃO': 'Nível de Risco I',
 '9SIM': 'Nível de Risco III'}


# PRINCIPAL

respostas = list()
riscosinfo = list()

st.text(' ')
if descPerguntas:
    st.text("Responda à(s) pergunta(s) para concluir a classificação do risco:")


    for i in descPerguntas:
        if i != None:
            option = st.radio(f"Para a atividade {i.split(' - ')[0]}: {i.split(' - ')[2]} (pergunta {i.split(' - ')[1]})", options=['SIM', 'NÃO'])
            st.text(' ')
            p=str(i).split(sep=' - ')[1]
            resposta=(p+option)
            respostas.append(resposta)

    for i in respostas:
        risco=drespostas[i]
        riscosinfo.append(risco)

# Aplicação do filtro no dataframe e classificação do risco

riscos = filtered_df.classificacaoRisco.to_list() + riscosinfo

try:
    while True:
        riscos.remove('Atividade econômica dependente de informação e condicionante')
except ValueError:
    pass

def risco_estabelecimento():
    if not riscos:
        classificacaoRisco = ''
        return classificacaoRisco
    if 'Nível de Risco III' in riscos:
        classificacaoRisco = 'Nível de Risco III'
        return classificacaoRisco
    elif 'Nível de Risco III' not in riscos and 'Para a determinação do grau de risco das atividades econômicas constituídas é necessário a avaliação do órgão de Vigilância Sanitária Municipal' in riscos:
        classificacaoRisco = 'Para a determinação do grau de risco das atividades econômicas constituídas é necessário a avaliação do órgão de Vigilância Sanitária Municipal'
        return classificacaoRisco
    elif 'Nível de Risco II' in riscos and 'Para a determinação do grau de risco das atividades econômicas constituídas é necessário a avaliação do órgão de Vigilância Sanitária Municipal' not in riscos and 'Nível de Risco III' not in riscos:
        classificacaoRisco = 'Nível de Risco II'
        return classificacaoRisco
    else:
        classificacaoRisco = 'Nível de Risco I'
        return classificacaoRisco


classificacaoRisco = risco_estabelecimento()
st.text(' ')
st.markdown(f"""
                Para o estabelecimento que realiza as atividades classificadas como **{", ".join(label_to_filter)}**, o risco sanitário do estabelecimento é:""")
st.text_area('Risco do estabelecimento:', value=classificacaoRisco)
st.text(' ')

filtered_df = filtered_df[['descricaoCnae', 'classificacaoRisco']]
filtered_df.columns = ['Atividade (subclasse CNAE)', 'Risco da Atividade']


st.text('')
st.text('Risco(s) da(s) atividade(s):')
st.table(filtered_df)

st.text('')

c = st.container()
c.subheader('Deseja solicitar alguma alteração?')
c.write('Se a circunstância que enseja a alteração não se refere a nenhum dos casos enumerados nos Avisos 1 e 2, você pode submeter um pedido de alteração, preenchendo a solicitação pelo formulário:')
c.caption('https://forms.office.com/r/ezyqvjzJJH')
