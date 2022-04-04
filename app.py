# Importar Bibliotecas

import streamlit as st
import pandas as pd
from annotated_text import annotated_text
from urllib import request
import requests
import wget
from pathlib import Path
import sys
import os

riscoURL = r"https://github.com/bruninhanic/riscoVisaMG/blob/main/riscoVisa.csv?raw=true"

perguntaURL = "https://github.com/bruninhanic/riscoVisaMG/blob/main/perguntas.csv"

respostaURL = "https://github.com/bruninhanic/riscoVisaMG/blob/main/respostaRisco.csv"

atividadeURL = "https://github.com/bruninhanic/riscoVisaMG/blob/main/cnaesVisa.csv?raw=True"


st.set_page_config(
    page_title='Risco VISA/MG', 
    page_icon='https://github.com/bruninhanic/riscoVisaMG/blob/main/favicon.ico', 
    layout='centered', 
    initial_sidebar_state='collapsed', 
    menu_items={'Get help': 'https://github.com/bruninhanic/riscoVisaMG/blob/main/AtividadesVisaAbril2022.txt',
                'Report a Bug':'https://forms.office.com/r/ezyqvjzJJH',
                'About': 'Esta aplicação permite a identificação do grau de risco do estabelecimento de acordo com a legislação mineira. Deve-se, para tanto, informar/escolher as atividades (subclasse CNAE) realizadas no estabelecimento.'
    }
)

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


labels = df.codDesc.tolist()


def load_perguntas():
    # carrega os dados das perguntas
    col_names_perguntas = ['idPergunta', 'descricaoPergunta']
    perguntas_df = pd.read_csv(perguntaURL, encoding='latin1', sep=';', names=col_names_perguntas,
                               dtype={'idPergunta': 'object','descricaoPergunta': 'object'},
                               index_col='idPergunta', on_bad_lines='skip', engine='c' )
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
annotated_text(('Código de Saúde', 'de Minas Gerais', '#8ef'),)
annotated_text(('Resolução SES/MG', 'n. 7426/2021', '#faa'),)
st.text('')

st.warning('Por meio da aplicação é possível consultar, a partir da inserção de todas as atividades sujeitas a controle sanitário, em qual grau de risco sanitário o estabelecimento se enquadra, de acordo com o Código de Saúde do Estado de Minas Gerais e a a Resolução SES/MG n. 7426/2021.')
st.text('')
             
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
    labels,
    help='Clique na seta a direita, comece a escrever um código ou uma palavra e então escolha as atividades realizadas pelo estabelecimento.'    
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

perguntas = {'1': 'A produção é artesanal?',
 '2': 'A produção é artesanal e diferente de conservas?',
 '3': 'Há produção de bebidas à base de soja?',
 '4': 'Há exclusivamente a produção de não comestíveis?',
 '5': 'A produção é artesanal?',
 '6': 'A produção é artesanal e de alimentos com dispensa de registro sanitário?',
 '7': 'Há exclusivamente a produção de alimentos com Padrão de Identidade e Qualidade do Ministério da Agricultura, Pecuária e Abastecimento?',
 '8': 'Há produção de embalagem para alimentos?',
 '9': 'Há fabricação de gases medicinais ou gases substâncias ativas?',
 '10': 'Há fabricação de  produtos químicos orgânicos empregados como aditivos para alimento, saneantes ou insumos para fabricação de saneantes?',
 '11': 'Há fabricação de saneantes?',
 '12': 'O resultado do exercício da atividade for utilizado para o revestimento interno de embalagens que entram em contato com alimentos? E  sejam tintas, vernizes, esmaltes, lacas, pigmentos e/ou corantes que utilizam precursores no processo de síntese química nestes compostos?',
 '13': 'O resultado do exercício da atividade for utilizado para o revestimento interno de embalagens que entram em contato com alimentos? E  sejam, adesivos, colas, decalques e selantes para uso industrial e doméstico de origem animal, vegetal e sintética que utilizam precursores no processo de síntese química destes compostos?',
 '14': 'Há fabricação de aditivo alimentar, insumos farmacêuticos, insumos para cosméticos, perfumes, produtos de higiene ou saneantes?',
 '15': 'Há produção de insumo farmacêutico ou insumos para cosméticos, perfumes e produto de higiene ou saneantes?',
 '16': 'Há fabricação de chupetas, bico de mamadeiras, produtos para saúde ou produtos de higiene?',
 '17': 'Há produção de mamadeiras?',
 '18': 'Há fabricação de  produtos para saúde, produtos de higiene ou destinados a entrar em contato com alimentos?',
 '19': 'Há fabricação de produtos para saúde?',
 '20': 'Há fabricação de produtos de higiene?',
 '21': 'Há comercialização de produtos para saúde de uso profissional?',
 '22': 'Há comércio atacadista de água mineral com atividade de engarrafamento?',
 '23': 'Há comercialização de medicamentos, gases medicinais, produtos de higiene, perfumes, cosméticos, saneantes e insumos para fabricação dos mesmos ou produtos para saúde?',
 '24': 'Há distribuição de gases medicinais?',
 '25': 'Há atividade de transformação artesanal e/ou autosserviço?',
 '26': 'Há comercialização de medicamentos (drugstore)?',
 '27': 'Há comercialização de cosméticos, saneantes, produtos para saúde ou alimentos?',
 '28': 'Há transporte de alimentos?',
 '29': 'Há armazenamento de produtos sujeitos ao controle sanitário?',
 '30': 'Há desenvolvimento de produtos para saúde (softwares que realizam ou influenciam diretamente no diagnóstico, monitoramento, terapia (tratamento) para a saúde)?',
 '31': 'Há realização de uma das seguintes análises: física, química, biotecnológica, bromatológica, cromatográfica, biológica, microbiológica, toxicológica e outros testes analíticos em produtos sujeitos à Vigilância Sanitária (água para consumo humano e outros fins, alimentos, medicamentos, insumos farmacêuticos, produtos para saúde, cosméticos, produtos de higiene, perfumes, saneantes domissanitários)?',
 '32': 'Há realização de pesquisas de bioequivalência, biodisponibilidade, ensaios clínicos ou análise de controle de qualidade de produtos sujeitos ao controle sanitário?',
 '33': 'Há aluguel de produtos para saúde de uso profissional?',
 '34': 'Há processamento de produtos para saúde (materiais médico hospitalares)?',
 '35': 'Ocorre o envase ou empacotamento de medicamentos, gases medicinais, gases substâncias ativas, produtos de higiene, perfumes, cosméticos, saneantes, insumos para fabricação dos mesmos, produtos para saúde ou alimentos (exceto de origem animal)?',
 '36': 'Há realização de procedimentos invasivos e/ou procedimento com utilização de anestesia e sedação?',
 '39': 'Há realização de procedimentos invasivos e/ou procedimento com utilização anestesia e sedação ou uso de radiação ionizante?',
 '40': 'O estabelecimento possui leitos de internação?',
 '41': 'O estabelecimento possui piscina?',
 '42': 'Há processamento de roupas hospitalares?',
 '43': 'O serviço realiza atividade de necrópsia?',
 '44': 'A produção é para consumo humano ou  é destinada a entrar em contato com alimentos e/ou bebidas?',
 '45': 'Atende exclusivamente crianças até 3 anos de idade?',
 '46': 'A produção é exclusivamente de polpa de fruta para bebida?',
 '47': 'Há transporte de medicamentos, gases medicinais, gases substâncias ativas, produtos de higiene, perfumes, cosméticos, saneantes, insumos para fabricação dos mesmos,  produtos para saúde ou material biológico humano?',
 '48': 'Há transporte de medicamentos, gases medicinais, produtos de higiene, perfumes, cosméticos, saneantes, insumos para fabricação dos mesmos ou produtos para saúde?',
 '49': 'Há transporte de medicamentos, gases medicinais, produtos de higiene, perfumes, cosméticos, saneantes, insumos para fabricação dos mesmos,  produtos para saúde ou material biológico humano?',
 '50': 'O resultado do exercício da atividade inclui a utilização produtos sujeitos ao controle sanitário do SNVS e/ou realizam serviços de radiologia diagnóstica?'}


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
 '12NÃO': 'Nível de Risco I',
 '12SIM': 'Nível de Risco III',
 '13NÃO': 'Nível de Risco I',
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
 '1SIM': 'P46',
 '20NÃO': 'Nível de Risco I',
 '20SIM': 'Nível de Risco III',
 '21NÃO': 'Nível de Risco II',
 '21SIM': 'Nível de Risco III',
 '22NÃO': 'Nível de Risco I',
 '22SIM': 'Nível de Risco III',
 '23NÃO': 'Nível de Risco II',
 '23SIM': 'Nível de Risco III',
 '24NÃO': 'Nível de Risco I',
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
 '38NÃO': 'Nível de Risco I',
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
 '46NÃO': 'Nível de Risco II',
 '46SIM': 'Nível de Risco I',
 '47NÃO': 'P28',
 '47SIM': 'Nível de Risco III',
 '48NÃO': 'P28',
 '48SIM': 'Nível de Risco III',
 '49NÃO': 'P28',
 '49SIM': 'Nível de Risco III',
 '4NÃO': 'Nível de Risco III',
 '4SIM': 'Nível de Risco I',
 '50SIM': 'Nível de Risco III',
 '50NÃO': 'Nível de Risco II',             
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
            if resposta not in respostas:
                respostas.append(resposta)
            
         
    #atividades com dois condicionantes
    for i in respostas:
        if '1SIM' in respostas:
            option = st.radio(f"Para a atividade 1031-7/00, realizada de forma artesanal: {perguntas['46']} (pergunta 46)", options=['SIM', 'NÃO'])
            resposta=('46'+option)
            respostas.append(resposta)
            respostas.remove('1SIM')
        if '47NÃO' in respostas:
            option = st.radio(f"Para a atividade 5021-1/01 e/ou 5021-1/02 e/ou 5120-0/00, responda também: {perguntas['28']} (pergunta 28)", options=['SIM', 'NÃO'])
            resposta=('28'+option)
            respostas.append(resposta)
            respostas.remove('47NÃO')
        if '48NÃO' in respostas:
            option = st.radio(f"Para a atividade 4930-2/03, responda também: {perguntas['28']} (pergunta 28)", options=['SIM', 'NÃO'])
            resposta=('28'+option)
            respostas.append(resposta)
            respostas.remove('48NÃO') 
        if '49NÃO' in respostas:
            option = st.radio(f"Para a(s) atividade(s) 4911-6/00 e/ou 4930-2/01 e/ou 4930-2/02, responda também: {perguntas['28']} (pergunta 28)", options=['SIM', 'NÃO'])
            resposta=('28'+option)
            respostas.append(resposta)
            respostas.remove('49NÃO')  

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

submit = st.button('Atividades')

remote_url = 'https://github.com/bruninhanic/riscoVisaMG/blob/main/AtividadesVisaAbril2022.txt'
local_file = 'AtividadesVISAMG.txt'

if submit:
    request.urlretrieve(remote_url, local_file)

c = st.container()
c.subheader('Deseja solicitar alguma alteração?')
c.write('Se a circunstância que enseja a alteração não se refere a nenhum dos casos enumerados nos Avisos 1 e 2, você pode submeter um pedido de alteração, preenchendo a solicitação pelo formulário:')
c.caption('https://forms.office.com/r/ezyqvjzJJH')
