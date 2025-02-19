##Exploração dos dados:

#Importação dos dados e definição do data.frame:

import pandas as pd

tabela_dados = 'C:\\Users\\eves\\Desktop\\DIT\\dados_ficha_a_desafio.csv'

df = pd.read_csv(tabela_dados)

#Tamanho do banco de dados: 
#print(df.shape)    

#Exibir as 15 primeiras linhas do data.frame, a intenção é visualizar como está a tabulação dos dados. 

pd.set_option('display.max_columns', None)
print(df.head(15))

#Análise exploratória básica: 

print(df.describe(include='all'))

#Aqui é possível identificar algumas informações essenciais sobre os dados, por meio de estatísticas como quartis
#moda, média, e o valor max e min. Dessa forma é possível já identificar se existem valores máximos que se afastam
#muito do valor médio, indicando inconformidade nas unidades de medida adotadas, e também outras informações como repetição
#do mesmo ID para pacientes diferentes (posteriormente é analisado se se referem ao mesmo paciente ou se são diferentes pacientes).

###Verificação da existência de lacuna / dado não preenchido:

print("Colunas vazias:", df.columns[df.isna().all()].tolist())
print("Valores ausentes?", df.isna().any().any())
print("Colunas com valores ausentes:", df.columns[df.isna().any()].tolist())

#Aqui é possível analisar quais colunas apresentam valores ausentes / falta de preenchimento. 
#Dada a natureza do dado e da forma de coleta, naturalmente algumas informações serão ausentes, porém 
#a ausência de informação pode estar sendo tratada com não preenchimento do campo 
#ou representada de outra forma. 

#Análise dos tipos de dados: 
print(df.dtypes)

#for c1 in df.columns:
    #tipos_dados = df[c1].apply(type).unique() 
    #print(f"{c1}: {tipos_dados}")

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

print(variavel_binaria)

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
    print("-" * 150)   ### separação para melhor visualização

#Foram encontrados diversos erros de formatação, que serão corrigidos via modelo dbt. 

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

##Datas estão padronizadas, porém de acordo com o describe, existem datas de atualização de cadastro com ano de 1900
#e updated_at também com o ano de 1900, indicando preenchimento errado. 

##Dados de contagem e mensuração: 

#Para verificar a conformidade com a unidade de medida, a visualização por meio de plotagem gráfica
#indicaria outliers e valores discrepantes entre si, sugerindo uma diferença na escala / unidade de medida. 

import matplotlib.pyplot as plt
import seaborn as sns

##Configuração dos gráficos:

var_numeros = ["n_atendimentos_atencao_primaria", "n_atendimentos_hospital", "altura", "peso", "pressao_sistolica", "pressao_diastolica"]

for var in var_numeros:
    plt.figure(figsize=(8, 5))
    sns.histplot(df[var], bins=30, stat="density", kde=True) 
    plt.title(f'Histograma de Densidade - {var}')
    plt.xlabel(var)
    plt.ylabel('Densidade')
    plt.grid(True)
    plt.show()

for var in var_numeros:
    plt.figure(figsize=(8, 5))
    sns.boxplot(x=df[var]) 
    plt.title(f'Boxplot - {var}')
    plt.xlabel(var)
    plt.grid(True)  
    plt.show()

##Por meio da função describe e dos gráficos, foi identificado que as colunas peso e altura apresentam valores discrepantes.
#Para identificar melhor quais valores apresentam problemas, vamos filtrar os dados com altura acima de 2 metros
#e peso acima de 200kg. 

#print(df.loc[df['altura'] > 200, 'altura'].reset_index())
#print(df.loc[df['peso'] > 200, 'peso'].reset_index())

#A partir do describe:

##Pressão sistolica valor max 900, Q1 e Q3 = 120 e 140, indicando que esse valor de 900 pode ser dividido por 10, por exemplo.
#Pressão diastolica max 921, Q1 e Q3 = 70 e 87, indicando que esse valor também pode ser dividido por 10. Pois houve erro de tabulação. 

#Altura: Foram encontradas 11 linhas com valores acima de 200cm. Enquanto o describe: Q1 = 145cm e Q3= 165cm
#entretanto, o valor max é de 810, o que em centímetros indicaria 8m, provavelmente foi cadastrado em mm.

#Peso: Q1 = 50kg e Q3 = 82kg, enquanto o max é 998. Qual unidade de medida poderia ser usada? Penso em hectogramas
#pois evitaria casas decimais em alguns sistemas.
#Foram encontrados 114 valores acima de 200kg. 

#Colunas de bairro e ocupação:

#Foram encontrados 748 valores para as colunas de bairro e 1355 para tipos de ocupação. 

#Bairros: 
#Identificação de valores únicos pros bairros apenas para visualização inicial: 

print(df['bairro'].unique()[:10]) ##Aqui dá pra alterar e ver os 748 valores :)

#Visualmente os bairros não aparentam erro de formatação, para garantir: 

# Função para identificar valores problemáticos
def verificar_bairro(bairro):
    """
    Verifica se um bairro tem caracteres problemáticos.

    Verifica se o bairro tem caracteres numéricos ou caracteres especiais
    fora do padrão de acentos e espaços.

    Parameters
    ----------
    bairro : str
        Bairro a ser verificado.

    Returns
    -------
    bool
        True se o bairro tem caracteres problemáticos, False caso contrário.
    """
    if pd.isna(bairro): 
        return False
    return bool(re.search(r'\d|[^a-zA-ZÀ-ÿ\s\-()]|[äöüÿèìòùîûýşţřňů]', bairro))

# Filtro

bairros = df.loc[df['bairro'].apply(verificar_bairro), 'bairro'].unique()

if bairros.size > 0:
    print(bairros)
else:
    print("Nenhum bairro encontrado")

#Não apresentou nenhum tipo de caractere problemático, apenas uso de () e []. Permitindo a presença de () uma vez que
#estes especificam algumas funções. 

#Ocupação 

print(df['ocupacao'].unique()[:10]) 

#Visualmente os bairros não aparentam erro de formatação, para garantir: 

# Função para identificar valores problemáticos
def verificar_bairro(ocupacao):
   
    if pd.isna(ocupacao): 
        return False
    return bool(re.search(r'\d|[^a-zA-ZÀ-ÿ\s\-()]|[äöüÿèìòùîûýşţřňů]', ocupacao))

# Filtro

ocupacao1 = df.loc[df['ocupacao'].apply(verificar_bairro), 'ocupacao'].unique()

if ocupacao1.size > 0:
    print(ocupacao1)
else:
    print("Nenhuma ocupação encontrada")

###Não foram encontrados dados com problemas na tabulação, entretanto, o preenchimento dos dados possui diversas informações
#as quais eu não sei se são necessárias para o analista. Portanto, serão mantidas. 


##IDS repetidos:

id_repetidos = df[df['id_paciente'].duplicated(keep=False)]

#print(id_repetidos['id_paciente'].value_counts().head(10))

#Verificando se os ids pertencem aos mesmos pacientes ou se é duplicidade de ids para pacientes diferentes:

diferencas = id_repetidos.groupby('id_paciente')[['peso']].nunique()
diferencas = diferencas[(diferencas > 1).any(axis=1)]

#Aqui escolhi utilizar a coluna de peso como coluna de comparação. Se os ids são iguais e os pesos tbm, dessa forma
#foi possível identificar que se trata de duplicidade de identificador, sendo para pacientes diferentes. 

print(diferencas.head(10))

#Aqui peguei um id repetido e visualizei, se trata de um homem e uma mulher com o mesmo id. 

print(df[df['id_paciente'] == "001070a8-f405-43da-bc59-8239bfc53d14"])

