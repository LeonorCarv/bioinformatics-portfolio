import json
import pandas as pd
import numpy as np
from numpy import asarray
from PIL import Image # python package Pillow
import networkx as nx


#####################################################################################
# T1
#####################################################################################

with open('dados_2/prize.json','r') as f:
    prizes = json.load(f)["prizes"]

with open('dados_2/laureate.json','r') as f:
    laureates = json.load(f)["laureates"]


##### T1.F1 #####
def maisPartilhados() -> tuple[int,set[tuple[int,str]]]:
  maior_share = share_atual = 0
  # Conjunto para armazenar os pares (ano, categoria) com os prêmios atribuídos ao maior número de co-laureados
  share_maior = set()

  # Iterar pelos dados dos prêmios
  for prize in prizes:
    # Verificar se o prêmio tem laureados associados
    if 'laureates' in prize:
      # Calcular o número máximo de co-laureados para este prêmio
      for laureate in prize['laureates']:
        # Obter o valor da chave 'share' do dicionário 'laureate'
        share_atual = int(laureate.get('share'))
        if maior_share <= share_atual:
          if maior_share < share_atual:
            share_maior.clear()
          maior_share = share_atual
          share_maior.add((int(prize['year']), prize['category']))
  maisPartilhados = (maior_share, share_maior)
  
  return maisPartilhados

#print(maisPartilhados())



##### T1.F2 #####
def multiLaureados() -> dict[str,set[str]]:
  # Inicialização dos dicionários
  # Dicionário para armazenar todos os laureados e as categorias de prémios que receberam
  laureados = {}
  # Dicionário para armazenar os laureados que receberam prémios em mais de uma categoria
  multiLaureados = {}

  # Iterar pelos dados dos prémios
  for prize in prizes:

    # Verificar se o prémio tem laureados associados
    if 'laureates' in prize:
      # Calcular o número máximo de co-laureados para este prémio
      for laureate in prize['laureates']:
        # Obter o primeiro nome do laureado
        nome = laureate['firstname']
        # Verificar se o sobrenome está presente
        if 'surname' in laureate:
          # Adicionar o sobrenome, se presente, ao nome completo do laureado
          nome += ' ' + laureate['surname']

        # Verificar se o nome do laureado já está no dicionário de laureados
        if nome in laureados:
          # Adicionar a categoria do prémios ao laureado existente
          laureados[nome].add(prize['category'])
        else:
          # Criar um novo registro para o laureado com a categoria do prémios
          laureados[nome] = {prize['category']}

  # Iteração sobre os laureados para encontrar os que receberam prémios em mais de uma categoria
  for nome, categorias in laureados.items():
    if len(categorias) > 1:
      # Adicionar o laureado ao dicionário de múltiplos laureados e as respetivas categorias dos prémios ganhos alfabeticamente
      multiLaureados[nome] = set(sorted(categorias))

  # Retornar o dicionário de múltiplos laureados
  return multiLaureados

#print(multiLaureados())


##### T1.F3 #####
def anosSemPremio() -> tuple[int,int] :

  lista_anos, lista_anos_consecutivos, maior_lista_anos_consecutivos = [], [], []
  ano_anterior = None
  count_anterior = 0

  # Guardar todos os anos em que pelo menos um prémio da mesma categoria não foi entregue
  for prize in prizes:
    if "overallMotivation" in prize:
      if "No Nobel Prize was awarded this year" in prize["overallMotivation"]:
        if prize["year"] not in lista_anos:
          lista_anos.append(prize["year"])

  #Organizar a lista por ondem crescente
  lista_anos = sorted(lista_anos)

  # Organizar os anos consecutivos numa lista de listas
  for ano in lista_anos:

    # Primeiro ano sem prémio
    if ano_anterior == None:
        ano_anterior = ano

    else:
      # Verificar se são anos consecutivos
      if (int(ano) - int(ano_anterior)) == 1:
  
        # Verificar se o ano anterior já está na lista de anos consecutivos
        if ano_anterior in lista_anos_consecutivos:
          lista_anos_consecutivos.append(ano)
          ano_anterior = ano
        else:
            lista_anos_consecutivos.append(ano_anterior)
            lista_anos_consecutivos.append(ano)
            ano_anterior = ano
    
      else:
        # Guardar a lista de anos consecutivos anterior numa lista de listas
        maior_lista_anos_consecutivos.append(lista_anos_consecutivos)
        # Esvaziar a lista com os anos consecutivos
        lista_anos_consecutivos = []
        ano_anterior = ano

  # Itera sobre cada lista da lista de listas, para verificar qual é a maior
  for lista in maior_lista_anos_consecutivos:
    if len(lista) > count_anterior:
      count_anterior = len(lista)
      anos_sem_premio = (int(lista[0]), int(lista[len(lista) - 1]))

  return anos_sem_premio

#print(anosSemPremio())


##### T1.F4 #####
def rankingDecadas() -> dict[str,tuple[str,int]]:

  dict = {}
  rankingDecadas = {}

  # Iterar sobre os laureados
  for laureate in laureates:
    # Iterar sobre o prémio do laureado
    for prize in laureate["prizes"]:
      # Cálcular a década
      decada = str(int(prize["year"]) // 10) + 'x'

      for affiliation in prize["affiliations"]:

        if "country" in affiliation:
          country = affiliation["country"]

          # Verificar se a década já está no dicionário
          if decada in dict:

            # Verificar se o país já está na década
            if country in dict[decada]:
              # Incrementar a contagem do país naquela década
              dict[decada][country] += 1
  
            else:
              # Adicionar o país à década com contagem 1
              dict[decada][country] = 1
      
          else:
              # Criar um novo registro para a década com o país e a contagem 1
              dict[decada] = {country: 1}

  # Obter o dicionário com apenas o país com maior laureados da década
  for decada, countries_count in dict.items():

    # Encontrar o país com o maior valor no dicionário
    most_common_country = max(countries_count, key=countries_count.get)

    # Obter o número de vezes que o país aparece naquela década
    most_common_count = countries_count[most_common_country]

    # Adicionar as duas variáveis como valores às chaves decadas
    rankingDecadas[decada] = (most_common_country, most_common_count)

  return rankingDecadas

#print(rankingDecadas())


#####################################################################################
# T2
#####################################################################################


##### T2.F1 #####
def toGrayscale(rgb:np.ndarray) -> np.ndarray:

  # Obter a altura e largura da imagem
  imageHeight = len(rgb)
  imageWidth = len(rgb[0])

  # Cria uma matriz vazia para armazenar a imagem resultante com as dimensões da original
  gsc = np.empty([imageHeight, imageWidth], dtype=np.uint8)
  
  # Iterar sobre cada pixel da imagem
  for i in range(imageHeight):
    for j in range(imageWidth):
      # Converte o pixel para tons de cinza usando a fórmula de luminância
      gsc[i][j] = int(rgb[i][j][0]*0.21 + rgb[i][j][1]*0.72 + rgb[i][j][2] * 0.07)

  return gsc


def converteGrayscale(fromimg:str,toimg:str) -> None:
    # a 3D numpy array of type uint8
    rgb: np.ndarray = asarray(Image.open(fromimg))
    # a 2D numpy array of type uint8
    grayscale: np.ndarray = toGrayscale(rgb)
    Image.fromarray(grayscale, mode="L").save(toimg)



##### T2.F2 #####
def toBW(gray:np.ndarray,threshold:tuple[int,int]) -> np.ndarray:

  # Obter a altura e largura da imagem
  imageHeight = len(gray)
  imageWidth = len(gray[0])

  # Cria uma matriz vazia para armazenar a imagem resultante com as dimensões da original
  bw = np.empty([imageHeight, imageWidth], dtype=np.uint8)
  
  # Iterar sobre cada pixel da imagem
  for i in range(imageHeight):
    for j in range(imageWidth):
      # Verificar se o valor do pixel está dentro do intervalo definido pelo threshold
      if gray[i][j] >= threshold[0] and gray[i][j] <= threshold[1]:
        bw[i, j] = 255   # Se sim, definir como branco
      else:
        bw[i, j] = 0     # Se não, definir como preto
        
  return bw



def converteBW(fromimg:str,toimg:str,threshold:tuple[int,int]) -> None:
    # a 2D numpy array of type uint8
    grayscale : np.ndarray = asarray(Image.open(fromimg))
    # a 2D numpy array of type uint8 (but with values being only 0 or 255)
    bw : np.ndarray = toBW(grayscale,threshold)
    Image.fromarray(bw,mode="L").save(toimg)



##### T2.F3 #####
def autoThreshold(fromimg:str,tolerance:int) -> tuple[int,int]:
  grayscale: np.ndarray = asarray(Image.open(fromimg))

  # Obter a altura e largura da imagem
  imageHeight = len(grayscale)
  imageWidth = len(grayscale[0])

  # Dicionário para armazenar a contagem de ocorrências de cada valor de pixel
  detected_colors = {}
  
  # Iterar sobre cada pixel da imagem
  for i in range(imageHeight):
    for j in range(imageWidth):
      # Obter o valor do pixel atual
      vgs = grayscale[i, j]

      # Atualizar a contagem de ocorrências do valor de pixel
      if vgs in detected_colors:
        detected_colors[vgs] += 1
      else:
        detected_colors[vgs] = 1

  # Ordenar os valores de pixel pela contagem de ocorrências
  detected_colors = sorted(detected_colors.items(), key=lambda x:x[1], reverse=True) 

  # Obter a cor mais predominante na imagem
  cor = int(detected_colors[0][0])

  # Calcular os valores mínimos e máximos para o threshold com base na cor predominante e na tolerância
  vmax = cor + tolerance
  if vmax > 255:
    vmax = 255

  vmin = cor - tolerance
  if vmin < 0:
    vmin = 0
  
  # Retornar uma tupla contendo os valores mínimo e máximo do threshold
  return ((vmin, vmax))



##### T2.F4 #####
def toContour(bw:np.ndarray) -> np.ndarray:

  # Obter a altura e largura da imagem
  imageHeight = len(bw)
  imageWidth = len(bw[0])

  # Cria uma matriz vazia para armazenar a imagem resultante com as dimensões da original
  contorno = np.empty([imageHeight, imageWidth], dtype=np.uint8)

  # Iterar sobre cada pixel da imagem
  for i in range(imageHeight):
    for j in range(imageWidth):
      
      # Obter a cor do pixel atual
      current_pixel = bw[i, j]

      # Determinar os limites da matriz
      min_i = max(i - 1, 0)             # Garante que a coordenada mínima da linha não seja menor que 0
      max_i = min(i + 1, bw.shape[0])   # Garante que a coordenada máxima da linha não ultrapasse a altura da imagem
      min_j = max(j - 1, 0)             # Garante que a coordenada mínima da coluna não seja menor que 0
      max_j = min(j + 1, bw.shape[1])   # Garante que a coordenada máxima da coluna não ultrapasse a largura da imagem
      
      #Determinar a matriz dos pixeis circundantes e dele próprio
      surrounding_pixels = bw[min_i:max_i, min_j:max_j]

      # Verificar se algum dos pixeis circundantes tem cor diferente da cor do pixel atual
      if (surrounding_pixels != current_pixel).any():
        contorno[i, j] = 0      # Colocar o pixel como preto
      else:
        contorno[i, j] = 255    # Colocar o pixel como branco

  return contorno



def converteContour(fromimg:str,toimg:str) -> None:
    # a 2D numpy array of type uint8 (but with values being only 0 or 255)
    bw : np.ndarray = asarray(Image.open(fromimg).convert("L"))
    # a 2D numpy array of type uint8 (but with values being only 0 or 255)
    contour : np.ndarray = toContour(bw)
    Image.fromarray(contour,mode="L").save(toimg)



#####################################################################################
# T3
#####################################################################################

legislativas = pd.read_excel("dados_2/legislativas.xlsx",header=[0,1],sheet_name="Quadro")


##### T3.F1 #####
def eleitoresPorto() -> int:
  
  # Encontra os índices das linhas com NUTS III
  indices_nuts = legislativas.index[legislativas['Territórios', 'Âmbito Geográfico'] == 'NUTS III']
  
  # Encontra o índice em que NUTS III é 'Área Metropolitana do Porto'
  indice_porto = indices_nuts[legislativas.loc[indices_nuts, ('Territórios', 'Região')] == 'Área Metropolitana do Porto'].tolist()[0]

  # Obtém os anos de eleições e os seus respectivos números de eleitores para o Porto
  numeros_eleitores = legislativas.iloc[indice_porto][2:19].astype(int)
  
  # Encontra a tupla com o índice do ano com o maior número de eleitores
  indice_max_eleitores = numeros_eleitores.idxmax()
  
  # Extrai o ano da tupla
  ano_max_eleitores = indice_max_eleitores[1]
  
  return ano_max_eleitores

#print(eleitoresPorto())


##### T3.F2 #####
def taxaAbstencao() -> list[tuple[int,float]]:
  # Encontra o índices da linhas do NUTS 2024
  indice_2024 = legislativas.index[legislativas['Territórios', 'Âmbito Geográfico'] == 'NUTS 2024']

  # Encontra o índice em que NUTS 2024 é 'Portugal'
  indice_portugal = indice_2024[legislativas.loc[indice_2024, ('Territórios', 'Região')] == 'Portugal'].tolist()[0]
  
  # Obtém os anos de eleições e seus respectivos números de eleitores
  numeros_eleitores = legislativas.iloc[indice_portugal][2:19].astype(int)
  # Obtém os anos de eleições e seus respectivos números de votantes
  numeros_votantes = legislativas.iloc[indice_portugal][19:].astype(int)
  
  # Calcula a taxa de abstenção por ano em percentagem
  taxas_abstencao = []
  for ano, eleitores, votantes in zip(numeros_eleitores.index, numeros_eleitores, numeros_votantes):
    taxa = (1 - (votantes / eleitores)) * 100
    taxas_abstencao.append((ano[1], taxa))
  
  return taxas_abstencao

#taxaAbstencao()
#print(taxaAbstencao())


##### T3.F3 #####
def perdaGrandesMunicipios() -> dict[str,int]:

  # Encontra o índices das linhas com 'Âmbito geográfico' 'Município'
  indices_municipios = legislativas.index[legislativas['Territórios', 'Âmbito Geográfico'] == 'Município']
  # Ignorar os cabeçalhos que não são números
  indices_municipios = indices_municipios.tolist()

  # Obtém a lista de municípios
  municipios = legislativas['Territórios'][legislativas['Territórios']['Âmbito Geográfico'] == 'Município']['Região'].tolist()

  votos_por_municipio = {}    

  for municipio in municipios:
    # Obter os anos de eleições e seus respectivos números de votantes, relativos aos 'Municípios'
    votantes_municipio = legislativas[legislativas['Territórios']['Região'] == municipio].iloc[0, 2:].filter(like='Votantes').astype(int)

    # Verificar se em algum dos anos o número de votantes para o município em análise é maior ou igual a 10000
    if any(votantes_municipio >= 10000):

      # Inicializar as variáveis 
      primeiro_ano = None
      votos_ano_anterior = 0
      maior_perda = None
      ano_maior_perda = None

      # Iterar sobre cada ano e número de votos para o município em análise
      for ano, votos in votantes_municipio.items():
        # Extrai apenas o ano do formato em que ele está armazenado
        ano = ano[1]

        # Inicializar as variáveis primeiro_ano e votos_ano_anterior como as do primeiro ano
        if primeiro_ano is None:
          primeiro_ano = ano
          votos_ano_anterior = votos
          continue

        # Calcula a perda de votos em relação ao ano anterior
        perda = votos_ano_anterior - votos

        # Se esta for a primeira perda calculada, ela é atribuída como a maior perda até o momento
        if maior_perda is None:
          maior_perda = perda
          ano_maior_perda = ano

        # Atualiza o valor da maior perda se a perda atual for maior que a anterior
        else:
          if maior_perda < perda:
            maior_perda = perda
            ano_maior_perda = ano
          else:
            votos_ano_anterior = votos
            continue

        # Atualiza o número de votos do ano anterior para o próximo ciclo do loop
        votos_ano_anterior = votos

      # Armazena o município, como chave, e o ano da sua maior perda de votos, como valor, ao dicionário
      votos_por_municipio[municipio] = ano_maior_perda

  return votos_por_municipio

#print(perdaGrandesMunicipios())



##### T3.F4 #####
def demografiaMunicipios() -> dict[str,tuple[str,str]]:

  # Inicializar um dicionário vazio para armazenar provisoriamente os dados
  provisorio = {}

  # Encontra os índices das linhas com NUTS III
  indices_nuts = legislativas.index[legislativas['Territórios', 'Âmbito Geográfico'] == 'NUTS III'].tolist()

  # Obtém a lista de regiões NUTS III
  regiões_nuts = legislativas['Territórios'][legislativas['Territórios']['Âmbito Geográfico'] == 'NUTS III']['Região'].tolist()

  # Encontra os índices das linhas com Municípios
  indices_municipios = legislativas.index[legislativas['Territórios', 'Âmbito Geográfico'] == 'Município'].tolist()

  # Iterar sobre cada índice de região NUTS III
  for j in range (len(indices_nuts)):

    # Inicializar variáveis
    maior_perda = float('-inf')
    maior_ganho = float('-inf')
    região = regiões_nuts[j]
    municipio_ganho = None
    municipio_perda = None

    # Iterar sobre cada índice de município
    for i in range(len(indices_municipios)):
      # Obtém o número de eleitores para os anos de 2022 e 1975, convertendo-os para inteiros
      eleitores_2022 = legislativas.iloc[indices_municipios[i], 18].astype(int)
      eleitores_1975 = legislativas.iloc[indices_municipios[i], 2].astype(int)

      # Verificar se o índice do município atual está entre os índices da região NUTS III atual e da próxima região NUTS III
      if i+1 < len(indices_municipios):
        indice_municipio = indices_municipios[i]
        if indices_nuts[j] < indice_municipio < indices_nuts[j + 1]:

          # Calcula a perda e o ganho de eleitores
          perda = eleitores_1975 - eleitores_2022
          ganho = eleitores_2022 - eleitores_1975

          # Se esta for a primeira iteração, os maiores ganho e perda são inicializados com os valores do primeiro município
          if maior_perda == float('-inf') and maior_ganho == float('-inf'):
            maior_perda = perda
            maior_ganho = ganho
            municipio_ganho = legislativas.iloc[indices_municipios[i]][1]
            municipio_perda = legislativas.iloc[indices_municipios[i]][1]

          else:
            # Atualiza o valor de maior perda, e do município correspondente, se a perda atual for maior que a armazenado
            if maior_perda < perda:
              maior_perda = perda
              municipio_perda = legislativas.iloc[indices_municipios[i]][1]
            # Atualiza o valor de maior ganho, e do município correspondente, se o ganho atual for maior que o armazenado
            if maior_ganho < ganho:
              maior_ganho = ganho
              municipio_ganho = legislativas.iloc[indices_municipios[i]][1]
      else:
        if j == (len(indices_nuts) - 1):

          # Calcula a perda e o ganho de eleitores
          perda = eleitores_1975 - eleitores_2022
          ganho = eleitores_2022 - eleitores_1975

          # Se esta for a primeira iteração, os maiores ganho e perda são inicializados com os valores do primeiro município
          if maior_perda == float('-inf') and maior_ganho == float('-inf'):
            maior_perda = perda
            maior_ganho = ganho
            municipio_ganho = legislativas.iloc[indices_municipios[i]][1]
            municipio_perda = legislativas.iloc[indices_municipios[i]][1]
          else:
            # Atualiza o valor de maior perda, e do município correspondente, se a perda atual for maior que a armazenado
            if maior_perda < perda:
              maior_perda = perda
              municipio_perda = legislativas.iloc[indices_municipios[i]][1]
            # Atualiza o valor de maior ganho, e do município correspondente, se o ganho atual for maior que o armazenado
            if maior_ganho < ganho:
              maior_ganho = ganho
              municipio_ganho = legislativas.iloc[indices_municipios[i]][1]

    # Armazenar os nomes dos municípios com maior perda e ganho na região atual no dicionário provisorio
    provisorio[região] = (municipio_perda, municipio_ganho)

    # Ordenar o dicionário provisorio por ordem alfabética das chaves e atribuir o resultado a dicionário demografiaMunicipios
    demografiaMunicipios = dict(sorted(provisorio.items()))

  return demografiaMunicipios

#print(demografiaMunicipios())



#####################################################################################
# T4
#####################################################################################

nominations = pd.read_csv("dados_2/nominations.csv")


##### T4.F1 #####
def maisNomeado() -> tuple[str,int]:

  # Cria um grafo direcionado
  g = nx.DiGraph()

  # Iterar sobre as colunas de nomeados e nomeadores
  for nomeado, nomeador in zip(nominations["Nominee(s)"], nominations['Nominator(s)']):

    nomeado = nomeado.replace("v.", "\n")
    nomeador = nomeador.replace("v.", "\n")

    # Criar lista com nomeados
    nomeados_list = []
    for nomeado_individual in nomeado.split('\n'):
      nomeados_list.append(nomeado_individual)

    # Criar lista com nomeadores
    nomeadores_list = []
    for nomeador_individual in nomeador.split('\n'):
      nomeadores_list.append(nomeador_individual)

    # Adicionar arestas ao grafo apenas para as nomeações únicas
    for vnomeado in nomeados_list:
      for vnomeador in nomeadores_list:
        # Verificar se a nomeção (vnomeador, vnomeado) ainda não foi feita
        if not g.has_edge(vnomeador, vnomeado):
          # Adicionar a aresta ao grafo
          g.add_edge(vnomeador, vnomeado)

  # Inicializar variáveis
  max_degree = 0
  mais_nomeado = None

  # Encontrar o nomeado com o maior número de nomeações
  # Iterar sobre os nós
  for nomeado in g.nodes():
    # Guardar o número de arestas que entram em cada nó
    grau_entrada = g.in_degree(nomeado)
    # Encontrar o maior grau de entradas
    if grau_entrada > max_degree:
      max_degree = grau_entrada
      mais_nomeado = nomeado

  # Retornar o nomeado mais nomeado e o número de indicações recebidas
  return (mais_nomeado, max_degree)

#print(maisNomeado())


##### T4.F2 #####
def nomeacoesCruzadas() -> tuple[int,set[str]]:
  # Cria um grafo direcionado
  g = nx.DiGraph()

  # Iterar sobre as colunas de nomeados e nomeadores
  for nomeado, nomeador, categoria in zip(nominations["Nominee(s)"], nominations['Nominator(s)'], nominations['Category']):

    nomeado = nomeado.replace("v.", "\n")
    nomeador = nomeador.replace("v.", "\n")

    # Criar lista com nomeados
    nomeados_list = []
    for nomeado_individual in nomeado.split('\n'):
      nomeados_list.append(nomeado_individual)

    # Criar lista com nomeadores
    nomeadores_list = []
    for nomeador_individual in nomeador.split('\n'):
      nomeadores_list.append(nomeador_individual)

    # Adicionar arestas ao grafo apenas para as nomeações únicas
    for vnomeado in nomeados_list:
      for vnomeador in nomeadores_list:
        # Verificar se a nomeção (vnomeador, vnomeado) ainda não foi feita
        if not g.has_edge(vnomeador, vnomeado):
          # Adicionar a aresta ao grafo
          g.add_edge(vnomeador, vnomeado, categoria = categoria)

  max_cruzadas = 0
  max_categorias = set()

  # Itera sobre todos os nós (pessoas) no grafo
  for node in g.nodes():

    # Calcula os ancestrais de cada nó
    ancestors = nx.ancestors(g, node)
    # Calcula os descendentes de cada nó
    descendants = nx.descendants(g, node)
    # Calcula o número de nós que são tanto ancestrais quanto descendentes do nó de interesse, ou seja, o número de nós que formam uma rede de nomeações cruzadas com esse nó
    cruzadas = len(ancestors.intersection(descendants))

    # Encontra a maior rede de nomeações cruzadas
    if cruzadas > max_cruzadas:
      max_cruzadas = cruzadas
      max_categorias = set()
      # Iterar sobre os nós que são tanto ancestrais quanto descendentes do nó em análise
      for person in ancestors.intersection(descendants):
        # Iterar sobre as pessoas que nomearam o nó 
        for predecessor in g.predecessors(person):
          # Iterar sobre as pessoas que o nó nomeou
          for successor in g.successors(person):
            # Obter os dados da aresta (nomeação) entre o predecessor e o sucessor
            edge_data = g.get_edge_data(predecessor, successor)
            # Verificar se existem dados para a aresta e se há informações sobre a categoria associada a essa nomeação
            if edge_data is not None and 'categoria' in edge_data:
              # Adicionar a categoria à lista de categorias
              max_categorias.add(edge_data['categoria'])

  return(max_cruzadas, max_categorias)

#print(nomeacoesCruzadas())

##### T4.F3 #####
def caminhoEinsteinFeynman() -> list[str]:

  # Cria um grafo direcionado
  g = nx.DiGraph()

  # Iterar sobre as colunas de nomeados e nomeadores
  for nomeado, nomeador, ano in zip(nominations["Nominee(s)"], nominations['Nominator(s)'], nominations['Year']):

    nomeado = nomeado.replace("v.", "\n")
    nomeador = nomeador.replace("v.", "\n")

    # Criar lista com nomeados
    nomeados_list = []
    for nomeado_individual in nomeado.split('\n'):
      nomeados_list.append(nomeado_individual)

    # Criar lista com nomeadores
    nomeadores_list = []
    for nomeador_individual in nomeador.split('\n'):
      nomeadores_list.append(nomeador_individual)

    # Adicionar arestas ao grafo apenas para as nomeações únicas
    for vnomeado in nomeados_list:
      for vnomeador in nomeadores_list:
        # Verificar se a nomeção (vnomeador, vnomeado) ainda não foi feita
        if not g.has_edge(vnomeador, vnomeado):
          # Adicionar a aresta ao grafo associando o atributo ano
          g.add_edge(vnomeador, vnomeado, ano = ano)

  
  # Inicializar uma lista vazia que irá armazenar os caminhos filtrados que atendem a critérios específicos
  caminhos_filtrados = []

  # Calcula de todos os caminhos mais curtos no grafo g entre os nós "Albert Einstein" e "Richard Phillips Feynman"
  caminhos = nx.all_shortest_paths(g, source="Albert Einstein", target="Richard Phillips Feynman")

  # Iterar sobre cada caminho
  for caminho in caminhos:
    anos_caminho = []

    # Iterar sobre cada nó do caminho atual
    for i in range(len(caminho) - 1):

      # Atribui o valor do atributo 'ano' aresta do caminho em análise
      aresta_ano = g[caminho[i]][caminho[i+1]]['ano']
      # Adiciona o ano da aresta à lista dos anos do caminho
      anos_caminho.append(aresta_ano)

    # Verifica se todos os anos do caminho estão dentro do intervalo 1921-1965
    if all(1921 <= ano <= 1965 for ano in anos_caminho):
      # Adicionar o caminho atual (excluindo os nós inicial e final) à lista com os caminhos filtrados
      caminhos_filtrados.append(caminho[1:-1])

  # Escolher um dos menores caminhos 
  return caminhos_filtrados[0]

print(caminhoEinsteinFeynman())