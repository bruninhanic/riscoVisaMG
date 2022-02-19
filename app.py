# Importar Bibliotecas
from io import StringIO

import streamlit as st
import pandas as pd

riscoURL = r"https://github.com/bruninhanic/riscoVisaMG/blob/main/riscoVisa.csv?raw=true"

perguntaURL = "https://github.com/bruninhanic/riscoVisaMG/blob/main/perguntas.csv"

respostaURL = "https://github.com/bruninhanic/riscoVisaMG/blob/main/respostaRisco.csv"

@st.cache
def load_data():
    # carrega os dados das atividades

    col_names = ['codigoCnae', 'classificacaoRisco', 'idPergunta']
    data = pd.read_csv(riscoURL, names=col_names,
                       dtype={'codigoCnae':'object', 'classificacaoRisco':'object', 'idPergunta':'object'},
                       index_col='codigoCnae', sep=';', encoding='utf8')

    return data

df = load_data()
labels = sorted(df.index.tolist())


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

# SIDEBAR

st.sidebar.header('Informe as atividades do estabelecimento')
info_sidebar = st.sidebar.empty()

# Checbox do cnae
st.sidebar.header('Atividades Econômicas')
label_to_filter = st.sidebar.multiselect(
    'Escolha as atividades:',
    labels
)
# Informação no rodapé do sidebar
st.sidebar.markdown(
    'Para a correta classificação de risco, você deve informar todas as atividades sujeitas a controle sanitário.')

#Exibição das perguntas
filtered_df = df[df.index.isin(label_to_filter)]

idPerguntas = list()
for item in filtered_df.idPergunta:
    if item not in idPerguntas:
        idPerguntas.append(item)

perguntas = {'1': 'A produção é artesanal?',
 '2': 'A produção é artesanal e diferente de conservas?',
 '3': 'Há produção de bebidas à base de soja?',
 '4': 'Há exclusivamente a produção de não comestíveis?',
 '5': 'A produção é artesanal?',
 '6': 'A produção é artesanal e de alimentos com dispensa de registro sanitário?',
 '7': 'Há exclusivamente a produção de alimentos com Padrão de Identidade e Qualidade do Ministério da Agricultura, Pecuária e Abastecimeto?',
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
 '36': 'Há realização de procedimentos invasivos? ',
 '37': 'Há realização de procedimentos invasivos e/ou procedimento com utilização de anestesia e sedação?',
 '38': 'Há realização de procedimentos invasivos?',
 '39': 'Há realização de procedimentos invasivos e/ou procedimento com utilização anestesia e sedação ou uso de radiação ionizante?',
 '40': 'O estabelecimento possui leitos de internação?',
 '41': 'O estabelecimento possui piscina?',
 '42': 'Há processamento de roupas hospitalares?',
 '43': 'O serviço realiza atividade de necrópsia?'}


descPerguntas = list()
for i in idPerguntas:
    if i != '0':
        p = i+"-"+perguntas[i]
        descPerguntas.append(p)

#Definição do risco após a resposta
drespostas = {'10NÃO': 'Nível de Risco II',
 '10SIM': 'Nível de Risco III',
 '11NÃO': 'Nível de Risco II',
 '11SIM': 'Nível de Risco III',
 '12NÃO': 'Nível de Risco II',
 '12SIM': 'Nível de Risco III',
 '13NÃO': 'Nível de Risco II',
 '13SIM': 'Nível de Risco III',
 '14NÃO': 'Nível de Risco II',
 '14SIM': 'Nível de Risco III',
 '15NÃO': 'Nível de Risco II',
 '15SIM': 'Nível de Risco III',
 '16NÃO': 'Nível de Risco II',
 '16SIM': 'Nível de Risco III',
 '17NÃO': 'Nível de Risco II',
 '17SIM': 'Nível de Risco III',
 '18NÃO': 'Nível de Risco II',
 '18SIM': 'Nível de Risco III',
 '19NÃO': 'Nível de Risco II',
 '19SIM': 'Nível de Risco III',
 '1NÃO': 'Nível de Risco III',
 '1SIM': 'Para a determinação do grau de risco das atividades econômicas constituídas é necessário a avaliação do órgão de Vigilância Sanitária Municipal',
 '20NÃO': 'Nível de Risco II',
 '20SIM': 'Nível de Risco III',
 '21NÃO': 'Nível de Risco I',
 '21SIM': 'Nível de Risco III',
 '22NÃO': 'Nível de Risco II',
 '22SIM': 'Nível de Risco III',
 '23NÃO': 'Nível de Risco I',
 '23SIM': 'Nível de Risco III',
 '24NÃO': 'Nível de Risco II',
 '24SIM': 'Nível de Risco III',
 '25NÃO': 'Nível de Risco I',
 '25SIM': 'Nível de Risco III',
 '26NÃO': 'Nível de Risco I',
 '26SIM': 'Nível de Risco III',
 '27NÃO': 'Nível de Risco II',
 '27SIM': 'Nível de Risco I',
 '28NÃO': 'Nível de Risco II',
 '28SIM': 'Para a determinação do grau de risco das atividades econômicas constituídas é necessário a avaliação do órgão de Vigilância Sanitária Municipal',
 '29NÃO': 'Nível de Risco II',
 '29SIM': 'Nível de Risco III',
 '2NÃO': 'Nível de Risco III',
 '2SIM': 'Nível de Risco I',
 '30NÃO': 'Nível de Risco II',
 '30SIM': 'Nível de Risco III',
 '31NÃO': 'Nível de Risco II',
 '31SIM': 'Nível de Risco III',
 '32NÃO': 'Nível de Risco II',
 '32SIM': 'Nível de Risco III',
 '33NÃO': 'Nível de Risco I',
 '33SIM': 'Nível de Risco III',
 '34NÃO': 'Nível de Risco II',
 '34SIM': 'Nível de Risco III',
 '35NÃO': 'Nível de Risco II',
 '35SIM': 'Nível de Risco III',
 '36NÃO': 'Nível de Risco I',
 '36SIM': 'Nível de Risco III',
 '37NÃO': 'Nível de Risco I',
 '37SIM': 'Nível de Risco III',
 '38NÃO': 'Nível de Risco II',
 '38SIM': 'Nível de Risco III',
 '39NÃO': 'Nível de Risco I',
 '39SIM': 'Nível de Risco III',
 '3NÃO': 'Nível de Risco II',
 '3SIM': 'Nível de Risco III',
 '40NÃO': 'Nível de Risco I',
 '40SIM': 'Nível de Risco III',
 '41NÃO': 'Nível de Risco II',
 '41SIM': 'Nível de Risco I',
 '42NÃO': 'Nível de Risco I',
 '42SIM': 'Nível de Risco III',
 '43NÃO': 'Nível de Risco I',
 '43SIM': 'Nível de Risco III',
 '4NÃO': 'Nível de Risco III',
 '4SIM': 'Nível de Risco II',
 '5NÃO': 'Nível de Risco III',
 '5SIM': 'Nível de Risco I',
 '6NÃO': 'Nível de Risco III',
 '6SIM': 'Nível de Risco I',
 '7NÃO': 'Nível de Risco III',
 '7SIM': 'Nível de Risco II',
 '8NÃO': 'Nível de Risco II',
 '8SIM': 'Nível de Risco III',
 '9NÃO': 'Nível de Risco II',
 '9SIM': 'Nível de Risco III'}


# PRINCIPAL
st.title('Consulta a classificação de risco sanitário do estabelecimento - Resolução SES/MG n. 7426/2021')

respostas = list()
riscosinfo = list()

if descPerguntas:
    st.markdown("Responda à(s) pergunta(s) para concluir a classificação do risco:{}".format(len(descPerguntas)))


    for i in descPerguntas:
        if i != None:
            option = st.radio(f"{i}", options=['SIM', 'NÃO'])
            p=str(i).split(sep='-')[0]
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

st.markdown(f"""
            Para o estabelecimento que realiza as atividades classificadas como **{", ".join(label_to_filter)}**, o risco sanitário do estabelecimento é:""")
st.text_area('Risco do estabelecimento:', value=classificacaoRisco)

filtered_df = filtered_df[['classificacaoRisco']]
st.write('Riscos das atividades:', filtered_df)
