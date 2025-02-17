##Exploração dos dados:

#Importação dos dados e definição do data.frame:

import pandas as pd

tabela_dados = 'C:\\Users\\eves\\Desktop\\DIT\\dados_ficha_a_desafio.csv'

df = pd.read_csv(tabela_dados)

##Tamanho do banco de dados: 
print(df.shape)    

##Exibir as 15 primeiras linhas do data.frame, a intenção é visualizar como está a tabulação dos dados. 
pd.set_option('display.max_columns', None)
print(df.head(15))

#Análise exploratória básica: 

print(df.describe(include='all'))

###Verificação da existência de lacuna / dado não preenchido:

print("Colunas vazias:", df.columns[df.isna().all()].tolist())
print("Valores ausentes?", df.isna().any().any())
print("Colunas com valores ausentes:", df.columns[df.isna().any()].tolist())

#Aqui é possível analisar quais colunas apresentam valores ausentes / falta de preenchimento. 
#Dada a natureza do dado e da forma de coleta, naturalmente algumas informações serão ausentes, porém 
#a ausência de informação pode estar sendo tratada com não preenchimento do campo 
#ou representada de outra forma. 

#Análise dos tipos de dados: 
#print(df.dtypes)

for c1 in df.columns:
    tipos_dados = df[c1].apply(type).unique() 
    print(f"{c1}: {tipos_dados}")

##Dados de peso e altura = float 
##Dados de contagem de atendimentos = int 

##Análise de diferenças no preenchimento dos dados.

#Nomes das colunas para mais fácil acesso às consultas.
#print(df.columns)

#Encontrar valores únicos para as colunas de interesse: (variáveis booleanas e categóricas com duas opções)

variavel_binaria = {
    'sexo': df['sexo'].unique(),
    'obito': df['obito'].unique(),
    'luz_eletrica': df['luz_eletrica'].unique(),
    'em_situacao_de_rua': df['em_situacao_de_rua'].unique(),
    'frequenta_escola': df['frequenta_escola'].unique(),
    'possui_plano_saude': df['possui_plano_saude'].unique(),
    'vulnerabilidade_social': df['vulnerabilidade_social'].unique(),
    'familia_beneficiaria_auxilio_brasil': df['familia_beneficiaria_auxilio_brasil'].unique(),
    'crianca_matriculada_creche_pre_escola': df['crianca_matriculada_creche_pre_escola'].unique(),
    'tipo': df['tipo'].unique()
}

##print(variavel_binaria)

##A partir daqui é possível identificar quais valores aparecem no banco de dados e determinar um padrão de preenchimento 
#posteriormente no dbt:

for vb, valores1 in variavel_binaria.items():   ##vb = variável binária e valores1= valores inseridos
    print(f"Variável: {vb}")
    print(f"Valores: {valores1}\n")

#print(df.columns)

import re 

# Colunas em preenchimento de texto longo. (Aqui busca-se encontrar quais palavras estão sendo utilizadas 
# para preencher os campos, quais possuem acentuação gráfica ou apresentam algum problema de formatação.)

colunas_texto = [
    "religiao", "escolaridade", "nacionalidade", "raca_cor",
    "renda_familiar", "meios_transporte", "doencas_condicoes", "identidade_genero",
    "meios_comunicacao", "orientacao_sexual", "em_caso_doenca_procura", "situacao_profissional"
]
palavras_coluna = {}

for coluna in colunas_texto:
    df[coluna] = df[coluna].astype(str)  
    palavras_unicas = set()  # Armazenar palavras únicas da coluna
    
    for texto in df[coluna]:  
        palavras = texto.split()  # Separar palavras
        palavras_unicas.update(palavras)  #atualizando o conjunto
    
    palavras_coluna[coluna] = sorted(palavras_unicas)

#Palavras encontradas por coluna:

for coluna, palavras in palavras_coluna.items():
    print(f"Coluna: {coluna}")
    print(palavras)
    print("-" * 150)


# Formato de datas:
import re

def formatos_data(coluna):
    """
    Verifica quais formatos de data estão presentes na coluna.

    Parameters
    ----------
    coluna : str
        Nome da coluna a ser analisada.

    Returns
    -------
    set
        Conjunto de formatos de data encontrados na coluna.
    """

    formatos_encontrados = set()  #Adiciona os formatos encontrados aqui. 
    tipos_data = {
        r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}$': 'YYYY-MM-DD HH:MM:SS.SSS',
        r'^\d{4}-\d{2}-\d{2}$': 'YYYY-MM-DD',                             
        r'^\d{2}/\d{2}/\d{4}$': 'DD/MM/YYYY',                             
        r'^\d{2}-\d{2}-\d{4}$': 'DD-MM-YYYY',                             
        r'^\d{4}/\d{2}/\d{2}$': 'YYYY/MM/DD'                              
    }
    """
    Função para encontrar formatos de data em uma coluna.

    A função utiliza expressões regulares para encontrar padrões de data em uma coluna.
    Os padrões de data são armazenados em um dicionário, onde a chave é a expressão regular
    e o valor é uma string descrevendo o formato de data.

    Parameters
    ----------
    coluna : str
        Nome da coluna a ser analisada.

    Returns
    -------
    set
        Conjunto de formatos de data encontrados na coluna.
    """
    for valor in df[coluna]:
        for formato, descricao in tipos_data.items():
            if re.match(formato, str(valor)):
                formatos_encontrados.add(descricao)
                break

    return formatos_encontrados
for col in ["data_nascimento", "data_cadastro", "data_atualizacao_cadastro", "updated_at"]:
    formatos = formatos_data(col)
    if formatos:
        print(f"Coluna '{col}' possui os formatos de data:")
        for formato in formatos:
            print(f"- {formato}")
    else:
        print(f"Coluna '{col}' possui outro formato de data.")

##Datas estão padronizadas. 

##Dados de contagem e mensuração: 

#Para verificar a conformidade com a unidade de medida, a visualização por meio de plotagem de gráfico de dispersão
#indicaria outliers e valores discrepantes entre si, sugerindo uma diferença na escala / unidade de medida. 

import matplotlib.pyplot as plt
import seaborn as sns

##Configuração dos gráficos:

var_numeros = ["n_atendimentos_atencao_primaria", "n_atendimentos_hospital", "altura", "peso", "pressao_sistolica", "pressao_diastolica"]

#for var in var_numeros:
 #   plt.figure(figsize=(8, 5))
  #  sns.histplot(df[var], bins=30, stat="density", kde=True) 
   # plt.title(f'Histograma de Densidade - {var}')
   # plt.xlabel(var)
    #plt.ylabel('Densidade')
    #plt.grid(True)
    #plt.show()

###Os dados não apresentam discrepâncias, sugerindo uma mesma unidade de medida. 

#Análise exploratória básica: 

print(df.describe(include='all'))



###ANALISAR COLUNAS DE BAIRRO E OCUPAÇÃO 
