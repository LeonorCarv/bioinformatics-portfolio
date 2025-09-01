import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely import *
from shapely.plotting import *
import math
import networkx as nx
from matplotlib.widgets import CheckButtons, RadioButtons
from matplotlib import gridspec

# Tarefa 1

# um tuplo (axioma,regras de expansão,ângulo inicial em graus,ângulo de rotação em graus)
lsystem = tuple[str,dict[str,str],float,float]

tree1 : lsystem = ("F",{"F":"F[-F]F[+F][F]"},90,30)
tree2 : lsystem = ("X",{"F":"FF","X":"F-[[X]+X]+F[+FX]-X"},90,22.5)
bush1 : lsystem = ("Y",{"X":"X[-FFF][+FFF]FX","Y":"YFX[+Y][-Y]"},90,25.7)
bush2 : lsystem = ("VZFFF",{"V":"[+++W][---W]YV","W":"+X[-W]Z","X":"-W[+X]Z","Y":"YZ","Z":"[-FFF][+FFF]F"},90,20)
plant1 : lsystem = ("X",{"X":"F+[[X]-X]-F[-FX]+X)","F":"FF"},60,25)

def expandeLSystem(l:lsystem,n:int) -> str:
    
    # Desempacotar a tupla
    axiomas, regras_expansão, ângulo_inicial, ângulo_rotação = l

    # Iterar, através do método de re-escrita, n vezes
    for x in range(n):

        # String temporária para construir a nova string
        new_axioma = ''
        # Iterar sobre cada caracter
        for axioma in axiomas:

            # Se a regra de expansão existir, substituir o caracter atual por ela e adicionar ao novo axioma
            if axioma in regras_expansão:
                new_axioma += regras_expansão[axioma]
            # Se a regra de expansão não existir, adicionar apenas o caracter atual ao novo axioma
            else:
                new_axioma += axioma
        # Juntar a nova string à string inicial
        axiomas = new_axioma

    return axiomas

#print(expandeLSystem(tree1,2))


def desenhaTurtle(steps:str,start_pos:(float,float),start_angle:float,side:float,theta:float) -> list[list[(float,float)]]:
    pos = start_pos
    angle = start_angle
    lines = [[pos]]
    stack = []
    for s in steps:
        if s=="F":
            pos = (pos[0] + side * math.cos(math.radians(angle)),pos[1] + side * math.sin(math.radians(angle)))
            lines[-1].append(pos)
        elif s=="-": angle = angle-theta
        elif s=="+": angle = angle+theta
        elif s=="[": stack.append((pos,angle))
        elif s=="]": pos,angle = stack.pop() ; lines.append([pos])
    return lines



def desenhaLSystem(l:lsystem,n:int):
    """
    Desenha uma representação gráfica de um L-System expandido.

    Argumentos:
        l (tuple): Tupla contendo as informações do L-System:
            - axiomas (str): O axioma inicial do sistema.
            - regras_expansão (dict): Dicionário que contém as regras de expansão do sistema.
            - ângulo_inicial (float): O ângulo inicial de direção para a tartaruga.
            - ângulo_rotação (float): O ângulo de rotação utilizado pelo sistema.
        n (int): O número de iterações para expandir o L-System.

    Returns:
        None: Exibe o gráfico do sistema L desenhado.

    """

    s = expandeLSystem(l,n)

    # Desempacotar a tupla
    axiomas, regras_expansão, ângulo_inicial, ângulo_rotação = l

    # Definir os parâmetros iniciais para desenhaTurtle
    start_pos = (0.0, 0.0)
    side = 5.0

    # Chamar a função desenhaTurtle para obter os segmentos de reta
    draw = desenhaTurtle(s, start_pos, ângulo_inicial, side, ângulo_rotação)

    # Configurações do gráfico
    plt.figure(figsize=(10, 12))
    ax = plt.gca()

    # Definir as cores para os segmentos de reta (ramos)
    colors = plt.cm.viridis_r([i / len(draw) for i in range(len(draw))])    # Mapeia cores com base no número de ramos

    # Iterar sobre cada linha do desenho e atribuir-lhe uma cor
    for linha, color in zip(draw, colors):
        x, y = zip(*linha)              # Desempacotar os pontos de cada segmento de reta
        ax.plot(x, y, color=color)      # Coordenadas x e y dos pontos passam a estar em tuplas


   # Adicionar um colorbar
    cb = plt.colorbar(plt.cm.ScalarMappable(cmap=plt.cm.viridis_r), ax=ax)
    cb.set_label('Coloração dos Ramos *', fontsize=14)
    cb.set_ticks([])                    # Remove os marcadores (ticks) do colorbar

    # Ajustar a exibição do gráfico
    ax.set_aspect('equal')              # Define a proporção dos eixos x e y como iguais
    plt.axis('off')                     # Desativa a exibição dos eixos no gráfico

    # Adicionar uma legenda informativa
    plt.text(0.0, 0, '* Num L-System cada iteração adiciona\n mais detalhes à estrutura, portanto a\n escala contínua de cores representa uma\n visualização mais fluída do processo de\n expansão e não uma cor específica para\n cada novo nível.', fontsize=10, transform=ax.transAxes, bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))

    # Adicionar um título ao gráfico
    plt.subplots_adjust(bottom=0.2)        # Ajusta a distância entre o título e o limite superior do plot
    plt.title('Árvore fractal', fontsize = 20, loc='center')

    plt.show()

#print(desenhaLSystem(tree1,5))


# Tarefa 2

packaging_waste = pd.read_csv('dados_3/env_waspac.tsv',na_values=":")
municipal_waste = pd.read_csv('dados_3/env_wasmun.tsv',na_values=":")

def desenhaReciclagemPaisIndice(ax,pais,indice):

    # Converter o argumento país para maiúsculas
    pais = pais.upper()
    # Converter o argumento índice para minúsculas
    indice = indice.lower()

    # Eliminar as linhas com países que não existem/ não pertencem à UE
    if indice == 'packaging':
        waste_pack = packaging_waste.drop([16, 18, 24, 31])
        waste_mun = None
    elif indice == 'municipal':
        waste_pack = None
        waste_mun = municipal_waste.drop([0, 2, 5, 19, 24, 25, 28, 32, 36, 37])
    else:
        waste_pack = packaging_waste.drop([16, 18, 24, 31])
        waste_mun = municipal_waste.drop([0, 2, 5, 19, 24, 25, 28, 32, 36, 37])


    if waste_pack is not None:

        categorical_data = waste_pack.select_dtypes(include=['int', 'float'])
        colunas_numericas = categorical_data.columns.tolist()

        # Converter os valores numéricos em falta pela média dos valores da sua coluna
        for coluna_num in colunas_numericas:

            # Calcular a média da coluna excluindo NaNs em packaging_waste
            media_coluna_pack = waste_pack[coluna_num].mean()
            # Substituir os valores ausentes pela média da coluna
            waste_pack[coluna_num] = waste_pack[coluna_num].fillna(media_coluna_pack)

        # Filtrar os dados apenas para o país desejado
        vpais_pack = waste_pack[waste_pack['geo\TIME_PERIOD'] == pais]

        # Plotar os dados
        ax.plot(colunas_numericas, vpais_pack.iloc[0][colunas_numericas], label=f'{pais} Packaging Waste', marker='o', color='blue')


    if waste_mun is not None:

        categorical_data = waste_mun.select_dtypes(include=['int', 'float'])
        colunas_numericas = categorical_data.columns.tolist()

        # Converter os valores numéricos em falta pela média dos valores da sua coluna
        for coluna_num in colunas_numericas:
            # Calcular a média da coluna excluindo NaNs em numeric_waste
            media_coluna_mun = waste_mun[coluna_num].mean()
            # Substituir os valores ausentes pela média da coluna
            waste_mun[coluna_num] = waste_mun[coluna_num].fillna(media_coluna_mun)

        # Filtrar os dados apenas para o país desejado
        vpais_mun = waste_mun[waste_mun['geo\TIME_PERIOD'] == pais]

        # Plotar os dados
        ax.plot(colunas_numericas, vpais_mun.iloc[0][colunas_numericas], label=f'{pais} Municipal Waste', marker='s', color='orange')

    # Adicionar legenda
    ax.legend()

    # Adicionar rótulos aos eixos
    ax.set_xlabel('Anos')
    ax.set_ylabel('Quantidade de Resíduos')

    # Adicionar título ao gráfico
    ax.set_title("Reciclagem UE")

    return None

#fig, ax = plt.subplots(figsize=(10, 6))
#print(desenhaReciclagemPaisIndice(ax, 'FR', 'muniCIPAL'))
#plt.show()


def testeDesenhaReciclagemPaisIndice():
  _,ax = plt.subplots()
  desenhaReciclagemPaisIndice(ax,'Russia',"packaging")
  plt.show()


def desenhaReciclagem():
    
    # Criar a figura e os eixos
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.subplots_adjust(left=0.30, bottom=0.2, right=0.9)

    # Função chamada quando um novo país é selecionado na caixa de seleção de países
    def on_pais_change(label):
        ax.clear()                                                              # Limpa o gráfico

        # Iterar sobre os checkboxes de tipo de reciclagem
        for i, selected in enumerate(tipo_checkboxes.get_status()):
            if selected:
                desenhaReciclagemPaisIndice(ax, label, tipo_reciclagem[i])      # Desenha o gráfico com o país selecionado
        plt.draw()                                                              # Redesenhar o gráfico

    # Função chamada quando um botão de tipo de reciclagem é selecionado
    def tipo_button_callback(label):
        ax.clear()                                                              # Limpa o gráfico

        # Verificar se algum país foi selecionado
        if pais_dropdown.value_selected is not None:
            for i, selected in enumerate(tipo_checkboxes.get_status()):
                if selected == True:
                    desenhaReciclagemPaisIndice(ax, pais_dropdown.value_selected, tipo_reciclagem[i])
        plt.draw()                                                              # Redesenha o gráfico

    # Lista dos países
    paises = packaging_waste.drop([16, 18, 24, 31])['geo\TIME_PERIOD'].unique().tolist()
    # Lista do tipos de reciclagem
    tipo_reciclagem = ['packaging', 'municipal']

    # Posição da caixa de seleção de países
    pais_dropdown_pos = plt.axes([0.03, 0.02, 0.18, 0.95]) # Posição da caixa de seleção de países
    # Posição dos checkboxes de tipo de reciclagem
    tipo_checkboxes_pos = plt.axes([0.25, 0.01, 0.15, 0.15], frameon=False)  # Posição dos checkboxes de tipo de reciclagem    

    # Dropdown de países
    pais_dropdown = RadioButtons(pais_dropdown_pos, paises)
    # Criação dos checkboxes
    tipo_checkboxes = CheckButtons(tipo_checkboxes_pos, tipo_reciclagem, actives=[False, False])

    # Atribui as funções de callback aos eventos de clique nos widgets
    pais_dropdown.on_clicked(on_pais_change)
    tipo_checkboxes.on_clicked(tipo_button_callback)

    # Mostrar o gráfico
    plt.show()
    
    return None

#desenhaReciclagem()


# Tarefa 3

listings = pd.read_csv('dados_3/listings.csv')

neighbourhoods = gpd.read_file("dados_3/neighbourhoods.geojson")

import contextily as ctx

def desenhaZonas():

    # Filtrar linhas com avaliações não nulas
    filtered_listings = listings.dropna(subset=['number_of_reviews'])

    # Juntar os dados dos dois ficheiros num só GeoDataFrame
    geodf = pd.merge(filtered_listings, neighbourhoods, on='neighbourhood', how='left')

    # Agrupar todas as linhas pela coluna 'neighbourhood' e selecionar a coluna 'number_of_reviews' dentro de cada grupo
    neighbourhood_reviews = geodf.groupby('neighbourhood')['number_of_reviews'].sum().reset_index()

    # Juntar o número total de reviews com o GeoDataFrame
    geodf = pd.merge(neighbourhoods, neighbourhood_reviews, left_on='neighbourhood', right_on='neighbourhood', how='left')


    # Desenhar o mapa
    fig, ax = plt.subplots(figsize=(15, 10))

    # Altera os limites
    ax.set_xlim(-8.9, -7.9)
    ax.set_ylim(40.7, 41.5)
    ax.axis('off')

    # Acrescentar o mapa com rótolos
    colors = ctx.providers.CartoDB.VoyagerNoLabels
    labels = ctx.providers.CartoDB.PositronOnlyLabels
    ctx.add_basemap(ax, crs=geodf.crs.to_string(), source=colors)
    ctx.add_basemap(ax, crs=geodf.crs.to_string(), source=labels)

    # Plotar as zonas com cor proporcional ao número total de reviews
    geodf.plot(column='number_of_reviews', cmap='rainbow', ax=ax, legend=True, legend_kwds={'orientation': "vertical"})

    # Ajustar o tamanho da fonte do colorbar
    cbar = ax.get_figure().get_axes()[1]
    cbar.set_ylabel('Número total de Reviews', fontsize=16)

    # Exibir o mapa
    plt.title('Número total de reviews na Zona Metropolitana do Porto', fontsize=15)
    plt.show()

#desenhaZonas()


def desenhaAlojamentos():

    # Extrair a coluna 'neighbourhood_group' do DataFrame listings
    neighb_groups = listings['neighbourhood_group']

    # Inicializar uma lista vazia para armazenar os dados dos alojamentos no Porto
    dados = []

    # Itera sobre as cidades e verifica se são o Porto, adicionando os dados correspondentes à lista
    for index, cidade in enumerate(neighb_groups):
        if cidade == 'PORTO':
            dados.append(listings.iloc[index])

    # Converter a lista de dados num DataFrame
    df_dados = pd.DataFrame(dados)

    
    # FORMATO
    # Definir os tipos de quarto presentes nos dados
    room_types = df_dados['room_type'].unique()
    # Definir os marcadores para cada tipo de quarto
    markers = {'Entire home/apt': 'x', 'Private room': '^', 'Shared room': '.', 'Hotel room': 's'}

    # TAMANHO
    # Calcular os tamanhos dos marcadores proporcionalmente à disponibilidade
    availabel = df_dados['availability_365']
    sizes = availabel / 5

    # COR
    # Calcular as cores dos marcadores proporcionalmente ao preço
    price = df_dados['price']
    #price = price.dropna()
    vprices = price / (price.max() - price.min())
    colors = plt.cm.plasma_r(vprices)

    # Latitude e Longitude dos alojamentos
    latitude = df_dados['latitude']
    longitude = df_dados['longitude']


    # Criar um novo gráfico
    fig, ax = plt.subplots(figsize=(20, 8))

    # Definir os limites
    ax.set_xlim(-8.69, -8.56)
    ax.set_ylim(41.13, 41.19)
    ax.axis('off')

    # Adicionar o mapa de fundo com contextily
    ctx.add_basemap(ax, crs='EPSG:4326', source=ctx.providers.OpenStreetMap.Mapnik)

    # Iterar sobre os dados para adicionar marcadores personalizados para cada alojamento
    for indice, row in df_dados.dropna(subset=['price']).iterrows():
        marcador = row['room_type']
        ax.scatter(row['longitude'], row['latitude'], marker=markers[marcador],
                    s=row['availability_365'] // 5, c=plt.cm.plasma_r((row['price'] / (price.max() - price.min()))), label=marcador, alpha=0.5)

    # Adicionar uma legenda
    legend_elements = [
        plt.Line2D([0], [0], marker='x', color='black', markersize=15, label='Entire home/apt'),
        plt.Line2D([0], [0], marker='^', color='black', markersize=15, label='Private room'),
        plt.Line2D([0], [0], marker='.', color='black', markersize=15, label='Shared room'),
        plt.Line2D([0], [0], marker='s', color='black', markersize=15, label='Hotel room')
    ]
    ax.legend(handles=legend_elements, fontsize=15, loc='upper left')

    # Adicionar uma legenda explicativa
    plt.text(-8.69, 41.125,'* O tamanho dos marcadores é proporcional à disponibilidade.', fontsize=12)

    # Adicionar a colorbar e definir o rótulo
    sm = plt.cm.ScalarMappable(cmap='plasma_r', norm=plt.Normalize(vmin=price.min(), vmax=price.max()))
    sm._A = []  # hack para que a escala de cores funcione corretamente
    cbar = fig.colorbar(sm, ax=ax, orientation='vertical')
    cbar.set_label('Price (€)', fontsize=15)

    # Adicionar título ao gráfico
    plt.title('Alojamentos disponíveis no Porto', fontsize=20)
    
    plt.show()

desenhaAlojamentos()


def topLocation() -> tuple[str,str,float,float]:

    # Determinar qual o anfitrião com mais alojamentos registados
    # Inicializar o dicionário que irá conter todos os host e o número de alojamentos de cada
    id_counts = {}

    # Contar o número de alojamentos para cada host
    for host in listings['host_name']:
        if host in id_counts:
            id_counts[host] += 1
        else:
            id_counts[host] = 1

    # Ordenar o dicionário por ordem decrescente dos valores
    sorted_id_count = sorted(id_counts.items(), key=lambda item: item[1], reverse=True)

    # Selecionar o elemento que aparece mais vezes (host com mais alojamentos)
    most_frequent_id = sorted_id_count[0][0]

    # Filtrar DataFrame para incluir as linhas correspondentes aos alojamnetos do host_id mais frequente
    df_freq_host = listings[listings['host_name'] == most_frequent_id].reset_index(drop=True)


    # Definir as coordenadas do centro
    x = -8.6308
    y = 41.1647

    # Criar GeoDataFrames com os dois pontos (representa o centro)
    centro = gpd.GeoDataFrame(geometry=gpd.points_from_xy([x], [y]))

    # Inicializar a menor distância como infinito
    menor_dist = float('inf')
    # Definir o número de casas decimais
    num_casas_decimais = 6

    # Iterar sobre os alojamentos do host mais frequente para encontrar o mais próximo do centro
    for indice, id in enumerate(df_freq_host['id']):

        latitude = round(df_freq_host['latitude'][indice], num_casas_decimais)
        longitude = round(df_freq_host['longitude'][indice], num_casas_decimais)

        # Criar um GeoDataFrame para representar o alojamento atual
        aloj = gpd.GeoDataFrame(geometry=gpd.points_from_xy([longitude], [latitude]))

        # Calcular a distância entre o centro e o alojamento
        distance = centro.geometry.distance(aloj.geometry)

        # Atualizar a menor distância se a nova distância for menor
        if menor_dist > distance.values[0]:
            menor_dist = distance.values[0]
            loc = (longitude, latitude)                 # Coordenadas do alojamento mais próximo ao centro
            host_name = df_freq_host['host_name'][indice]    # Nome do host do alojamento mais próximo
            name = df_freq_host['name'][indice]

    tuple = (name, host_name, loc[1], loc[0])
    
    return tuple




def desenhaTop():
    name,host_name,latitude,longitude = topLocation()

    # Definir as coordenadas do centro
    x = -8.6308
    y = 41.1647

    # Criar o gráfico
    fig, ax = plt.subplots(figsize=(10, 8))

    # Definir os limites
    ax.set_xlim(-8.635, -8.625)
    ax.set_ylim(41.16, 41.17)
    ax.axis('off')

    # Adicionar o mapa de fundo com Contextily
    ctx.add_basemap(ax, crs='EPSG:4326', source=ctx.providers.OpenStreetMap.Mapnik)

    # Adicionar o ponto do Centro
    ax.scatter(x, y, alpha=0.5, marker='.', color='red', s=500)
    ax.plot(x, y, 'ok', markersize=1)
    #ax.text(x, y, 'Centro')

    # Adicionar o ponto do alojamento mais próximo ao centro
    ax.scatter(longitude, latitude, alpha=0.5, marker='*', color='blue', s=600)
    ax.plot(longitude, latitude, 'ok', markersize=1)
    #ax.text(longitude, latitude, name)

    # Adicionar uma legenda
    legend_elements = [
        plt.Line2D([0], [0], marker='.', color='red', markersize=15, label='Centro'),
        plt.Line2D([0], [0], marker='*', color='blue', markersize=15, label=name),
    ]
    ax.legend(handles=legend_elements, fontsize=12, loc='upper left')

    # Adicionar título ao gráfico
    plt.title(f'Alojamento de {host_name} mais central no Porto')
    
    # Exibir o gráfico
    plt.show()

#desenhaTop()


# Tarefa 4

bay = pd.read_csv('dados_3/bay.csv')

def constroiEcosistema() -> nx.DiGraph:

    # Criar um grafo direcionado
    g = nx.DiGraph()

    # Selecionar as colunas 'Names' e 'TrophicLevel'
    names_trophic_level = bay[['Names', 'TrophicLevel']]

    # Iterar sobre as linhas do DataFrame selecionado
    for index, row_1 in names_trophic_level.iterrows():
        name = row_1['Names']
        level = row_1['TrophicLevel']

        # Adicionar o nó ao grafo com o atributo level
        g.add_node(name, level=level)

    # Selecionar as colunas com transferências de biomassa
    trans_biomassa = bay[['Diatoms', 'Flagellates', 'Bacteria', 'HM plankton', 'Small copepods', 'Medium copepods', 'Large copepods', 'Other lg zooplankton', 'Sm macrobenthos', 'Lg suspension feeder', 'Echinoderm', 'Mollusc', 'Prawn & shrimp', 'Large crustacean', 'Cuttlefish', 'Other cephalopod', 'Flatfish', 'Gurnard', 'Other benthic carnivorous fish', 'Lizardfish', 'Red tjor-tjor', 'Pinky', 'Other benthopelagic fish', 'Sm pelagic fish', 'Lg pelagic fish', 'Skates and rays', 'Sm benthic shark', 'Large sharks', 'Cetaceans', 'Susp POC', 'Sed POC', 'DOC', 'DIC']]

    # Iterar sobre as linhas do DataFrame de transferência de biomassa
    for i, row_2 in trans_biomassa.iterrows():
        for j, transfer in enumerate(row_2):
            if transfer > 0:
                # Obter os nomes dos organismos relacionados à transferência
                name_i = trans_biomassa.columns[i]
                name_j = trans_biomassa.columns[j]
                # Adicionar a aresta ao grafo com o atributo de transferência
                g.add_edge(name_i, name_j, transfer=transfer)

    return g

def desenhaEcosistema():
    
    g = constroiEcosistema()
    
    # Criar um dicionário para armazenar os rótulos dos nós, mapeando os nomes das espécies para índices
    label_dict = {}
    for indice, nome in enumerate(bay['Names']):
        label_dict[nome] = indice + 1

    # Criar a figura
    fig = plt.figure(figsize=(15, 10))

    # Definir uma grade com 1 linha e 2 colunas (para o gráfico e o colorbar)
    gs = gridspec.GridSpec(1, 2, width_ratios=[5, 1])

    # Gráfico
    ax = plt.subplot(gs[0])

    # Definir o layout dos nós com formato circular
    pos = nx.circular_layout(g)

    # Definir o tamanho dos nós baseado no nível trófico
    node_size = [g.nodes[node]['level'] * 100 for node in g.nodes]

    # Definir as cores das arestas com base na transferência de biomassa
    edge_colors = [g[x][y]['transfer'] for x, y in g.edges]

    # Encontrar os valores máximo e mínimo de biomassa para normalização
    max_biomassa = max(edge_colors)
    min_biomassa = min(edge_colors)

    # Normalizar as cores das arestas
    norm = plt.Normalize(vmin=min_biomassa, vmax=max_biomassa)
    cmap = plt.cm.cool

    # Aplicar o mapeamento de cores normalizado às arestas
    edge_colors_normalized = [cmap(norm(biomassa)) for biomassa in edge_colors]

    # Desenhar os nós
    nx.draw_networkx_nodes(g, pos, node_size=node_size, node_color='pink')
    # Desenhar as arestas com as cores normalizadas
    nx.draw_networkx_edges(g, pos, width=2.0, edge_color=edge_colors_normalized, arrows=True, alpha=0.5)
    # Desenhar os rótulos dos nós
    nx.draw_networkx_labels(g, pos, labels=label_dict, font_size=12, font_color='black', font_weight='bold', verticalalignment='bottom')
    # Desenhar os rótulos das arestas
    nx.draw_networkx_edge_labels(g, pos, font_size=10, edge_labels=nx.get_edge_attributes(g, 'transfer'))

    # Adicionar uma legenda
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='pink', markersize=10, label='Nível Trófico (Tamanho dos Nós)'),
        plt.Line2D([0], [0], color='black', lw=4, label='Transferência de Biomassa (Largura das Arestas)')
    ]
    # Posicionar a legenda no gráfico
    ax.legend(handles=legend_elements, fontsize=12, loc='upper left', bbox_to_anchor=(-0.2, 0.99)) #-0.2, 0.99

    # Adicionar o texto com as informações do dicionário de rótulos
    dict_text = "\n".join([f"{value}: {key}" for key, value in label_dict.items()])
    plt.text(-0.2, 0.8, dict_text, fontsize=10, verticalalignment='top', transform=ax.transAxes)

    # Criar a barra de cores para mostrar a quantidade de biomassa transferida
    ax_cb = plt.subplot(gs[1])
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, cax=ax_cb)
    cbar.set_label('Quantidade de Biomassa Transferida', fontsize=15)

    # Definir o título do gráfico
    ax.set_title("Distribuição da Biomassa entre Espécies num Ecossistema", fontsize=20)
    # Remover os eixos do gráfico
    ax.axis('off')
    
    plt.show()

#desenhaEcosistema()