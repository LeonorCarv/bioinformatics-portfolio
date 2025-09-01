# Parte 1


# T1
def leParagrafos(ficheiro: str) -> list[str]:
  #cria uma lista texto com um elemento vazio inicial (string)
  list = ['']
  with open(ficheiro, "r", encoding="utf8") as f:
    #lê todas as linhas do arquivo de texto e armazena-as na variável paragrafos
    paragrafos = f.readlines()
    i = 0
    for line in paragrafos[1:]:
      #verifica se a primeira posição da linha é um caractere de nova linha ('\n')
      if line[0] == '\n':
        #Se a linha estiver em branco, adicionar um novo elemento vazio à lista texto
        list.append('')
        i += 1
        continue
      else:
        if len(list[i]) == 0:
          #Se a linha não estiver em branco, concatenar o conteúdo da linha ao parágrafo atual, removendo o último caractere, que é o caractere de nova linha
          list[i] += line[:-1]
        else:
          list[i] += ' '
          #Se a linha não estiver em branco, concatenar o conteúdo da linha ao parágrafo atual, removendo o último caractere, que é o caractere de nova linha
          list[i] += line[:-1]
  #Remover todas as aspas em excesso da lista
  while '' in list:
    list.remove('')

  return (list)

file_path = "dados_1/cidadeserras.txt"
#leParagrafos(file_path)
#print(leParagrafos(file_path))

# T2
def organizaCapitulos(paragrafos: list[str]) -> dict[str, list[str]]:
  list = leParagrafos('dados_1/cidadeserras.txt')
  # Cria um dicionário vazio para armazenar os capítulos
  dict = {}
  # Inicializa o índice para os números romanos
  i = -1
  # Lista de números romanos de I a XVI
  romanos = [
      'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII',
      'XIII', 'XIV', 'XV', 'XVI'
  ]
  # Itera sobre cada parágrafo da lista de parágrafos, começando do terceiro elemento
  for paragrafo in list[2:]:
    # Se o parágrafo for um número romano, incrementa o índice e adiciona o parágrafo à lista correspondente
    if paragrafo in romanos:
      i += 1
      #é o indicativo de novo capítulo, adicionar ao dicionário
      dict[paragrafo] = []
    else:
      # Se o parágrafo não for um número romano, adiciona-o à lista do capítulo atual
      dict[romanos[i]].append(paragrafo)
  return dict

#print(organizaCapitulos(list))

# T3
def menorCapitulo(capitulos: dict[str, list[str]]) -> str:
  dict = organizaCapitulos(leParagrafos('dados_1/cidadeserras.txt'))

  # Variáveis para acompanhar menor capítulo
  # Inicializa com um valor muito grande
  count_anterior = float('inf')
  # Inicializa com uma string vazia
  romano_anterior = ''

  # Variáveis para acompanhar o capítulo atual
  count_atual = 0
  romano_atual = ''

  # Itera sobre cada capítulo no dicionário de capítulos
  for romano, capitulo in dict.items():
    # Reinicia a contagem para cada novo capítulo
    count_atual = 0
    for paragrafo in capitulo:
      # Adiciona o comprimento de cada parágrafo ao contador
      count_atual += len(paragrafo)
      # Atualiza o número romano do capítulo atual
      romano_atual = romano
    # Verifica se o capítulo atual é menor que o anterior
    if count_atual < count_anterior:
      # Atualiza o menor total de caracteres
      count_anterior = count_atual
      # Atualiza o número romano do menor capítulo
      romano_anterior = romano_atual
  # Retorna o número romano do menor capítulo
  return romano_anterior

#print(menorCapitulo(dict))


def maiorDialogo(capitulos: dict[str, list[str]]) -> int:
  dict = organizaCapitulos(leParagrafos('dados/cidadeserras.txt'))

  # Variáveis para acompanhar o maior diálogo
  # Reinicia a contagem para cada novo capítulo
  count_anterior = count_atual = 0

  # Itera sobre cada capítulo no dicionário de capítulos
  for romano, capitulo in dict.items():
    # Reinicia a contagem para cada novo capítulo
    count_atual = 0
    for paragrafo in capitulo:
      # Verifica se o parágrafo é um diálogo
      if paragrafo.startswith('--'):
        # Incrementa o contador de diálogos
        count_atual += 1
      else:
        # Verifica se o número de diálogos é maior que o máximo encontrado até agora
        if count_atual > count_anterior:
          # Atualiza o número máximo de diálogos
          count_anterior = count_atual
        # Reinicia o contador para o próximo bloco de diálogo
        count_atual = 0
  # Retorna o número máximo de diálogos encontrado
  return count_anterior

#print(maiorDialogo(dict))

def mencoesPersonagens(capitulos: dict[str, list[str]],
                       personagens: set[str]) -> list[tuple[str, float]]:
  dict = organizaCapitulos(leParagrafos('dados_1/cidadeserras.txt'))
  # Lista para armazenar as menções aos personagens em cada capítulo
  mencoespers = []
  # Variáveis para acompanhar o número de menções
  count_atual = count_paragrafos = 0
  # Itera sobre cada capítulo no dicionário
  for romano, capitulo in dict.items():
    # Reinicia a contagem para cada novo capítulo
    count_paragrafos = 0
    for paragrafo in capitulo:
      # Reinicia a contagem para cada novo parágrafo
      count_atual = 0
      for personagem in personagens:
        if personagem in paragrafo:
          # Incrementa o contador se o personagem for mencionado no parágrafo
          count_atual += 1

      # Verifica se todos os personagens foram mencionados no parágrafo
      if len(personagens) == count_atual:
        # Incrementa o contador de parágrafos se todos os personagens foram mencionados
        count_paragrafos += 1
      else:
        # Reinicia o contador se nem todos os personagens foram mencionados no parágrafo
        count_atual = 0
    # Adiciona o número de menções de personagens no capítulo à lista de menções
    mencoespers.append((romano, count_paragrafos))
    # Ordena a lista de menções em ordem decrescente de contagem de menções
    mencoespers.sort(key=lambda x: (x[1]), reverse=True)
  return mencoespers

#print(mencoesPersonagens(dict, {"Jacintho"}))

import re

def ohJacinto(capitulos: dict[str, list[str]]) -> set[str]:
  # Inicializa um conjunto para armazenar os monólogos endereçados a Jacinto
  monologo = set()
  # Itera sobre cada capítulo no dicionário de capítulos
  for capitulo in capitulos.keys():
    # Itera sobre cada parágrafo no capítulo
    for paragrafo in capitulos[capitulo]:
      # Verifica se o parágrafo começa com '--', indicando um possível monólogo
      if paragrafo.startswith('--'):
        # Divide o parágrafo em frases terminadas em '.', '!' ou '?'
        for frase in re.split(r'(?<=[.!?])', paragrafo):
          # Verifica se a frase contém "Jacintho" e termina com '!' ou '?'
          if 'Jacintho' in frase and (frase.endswith('!')
                                      or frase.endswith('?')):
            # Se sim, adiciona o parágrafo inteiro ao conjunto de monólogos
            monologo.add(paragrafo)
            # Interrompe o loop de frases para evitar adicionar o mesmo parágrafo várias vezes
            break
  return (monologo)

#print(ohJacinto(organizaCapitulos(leParagrafos('dados_1/cidadeserras.txt'))))

# Parte 2

# T4

# the nucleotide complement of a DNA nucleotide in its bonded DNA strand
nucleotidePairs = {
    'A': 'T',
    'G': 'C',
    'Y': 'R',
    'W': 'W',
    'S': 'S',
    'K': 'M',
    'D': 'H',
    'V': 'B',
    'X': 'X',
    'N': 'N'
}
for k, v in list(nucleotidePairs.items()):
  nucleotidePairs[v] = k


def nucleotidePair(c):
  return nucleotidePairs[c]


def leDNA(ficheiro: str) -> tuple[str, str]:
  # Inicializa ambas as cadeias de DNA
  cadeia_original = ''
  cadeia_complementar = ''
  # Abre o arquivo de DNA para leitura
  with open(ficheiro, "r", encoding="utf8") as f:
    # Itera sobre cada linha do arquivo
    for linha in f:
      # Verifica se a linha não começa com '>', indicando que é uma linha de sequência
      if not linha.startswith('>'):
        # Remove espaços em branco e caracteres de nova linha e adiciona a linha à cadeia original
        cadeia_original += linha.rstrip()

  # Calcular o complemento reverso da cadeia
  for nucleótido in cadeia_original:
    # Adiciona o complemento do nucleotídeo atual à cadeia complementar
    cadeia_complementar += nucleotidePairs[nucleótido]

  # Cria uma tupla contendo as cadeias original e complementar
  tuple = (cadeia_original, cadeia_complementar)
  return (tuple)

dna = leDNA("dados_1/U49845.1.fasta")
#print(dna)

# T5


def encontraProteinas(code: str, dna: str) -> list[tuple[int, int, str]]:
  # Abre o arquivo de código de aminoácidos para leitura
  with open(code, "r", encoding="utf8") as f:
    # Ler o conteúdo do arquivo de código
    code = f.read()

    # Inicializar um dicionário para armazenar o código de aminoácidos
    database = {}

    # Listas para armazenar os aminoácidos, os códons de início e de fim e as bases
    aminoacidos = []
    start = []
    base1 = []
    base2 = []
    base3 = []

    # Iterar sobre cada linha do código de aminoácidos
    for linha in code.splitlines():
      #separar os caracateres,de cada linha, em listas, ignorando as suas informações iniciais
      for x in linha[11:]:
        if linha.startswith('    AAs  ='):
          aminoacidos.append(x)
        elif linha.startswith('  Starts ='):
          start.append(x)
        elif linha.startswith('  Base1  ='):
          base1.append(x)
        elif linha.startswith('  Base2  ='):
          base2.append(x)
        elif linha.startswith('  Base3  ='):
          base3.append(x)

    # Criar o dicionário de dados de códigos de aminoácidos
    for i in range(0, len(aminoacidos)):
      database[base1[i] + base2[i] + base3[i]] = [start[i], aminoacidos[i]]
    # Inicializar uma lista para armazenar as sequências de DNA encontradas
    sequencias_dna = []

    #Inicializa a variável para armazenar a sequência de DNA atual
    dna_completo = dna
    v_dna = ''

    # Armazenar todas as sequências de DNA encontradas
    for linha in dna_completo.splitlines():
      # Ignorar linhas que começam com ">"
      if not linha.startswith(">"):
        # Concatenar a linha à sequência atual
        v_dna += linha.strip()
      # Se houver uma sequência de DNA válida, armazená-la
      else:
        if v_dna:
          sequencias_dna.append(v_dna)
        v_dna = ''
    # Adicionar a última sequência de DNA
    if v_dna:
      sequencias_dna.append(v_dna)
  # Inicializar uma lista para armazenar todas as proteínas encontradas
  todas_proteinas = []
  # Iterar sobre cada sequência de DNA
  for sequencia in sequencias_dna:
    proteinas = ''
    codão = ''
    proteina = []

    #Determinar os codões correspondentes à sequência de DNA
    for init_pos in range(3):
      pos_inicio = pos_fim = 0
      proteinas = ''
      for pos in range(init_pos, len(sequencia) - 2, 3):
        # Obter o codão atual
        codão = sequencia[pos:pos + 3]

        #Determinar a posição inicial da proteina
        if len(proteinas) == 0:
          if database[codão][0] == 'M':
            pos_inicio = pos + 1
            #Adicionar os aminoácidos
            proteinas += database[codão][1]
            for x in range(pos + 3, len(sequencia) - 2, 3):
              codão = sequencia[x:x + 3]
              if database[codão][0] == '*':
                pos_fim = x + 3
                #Adicionar os aminoácidos, posições de inicio e fim
                proteina.append((pos_inicio, pos_fim, proteinas))
                pos_fim = pos_inicio = 0
                proteinas = ''
                break
              else:
                #Adicionar os aminoácidos
                proteinas += database[codão][1]
        else:
          continue
  # Adicionar a proteína à lista de proteínas
  todas_proteinas.extend(proteina)
  # Ordenar a lista pelo pos_inicio em ordem crescente
  todas_proteinas.sort(key=lambda x: x[0])
  # Retornar a lista de todas as proteínas encontradas
  return (todas_proteinas)

u49845 = ('GATCCTCCATATACAACGGTATCTCCACCTCAGGTTTAGATCTCAACAACGGAACCATTGCCGACATGAGACAGTTAGGTATCGTCGAGAGTTACAAGCTAAAACGAGCAGTAGTCAGCTCTGCATCTGAAGCCGCTGAAGTTCTACTAAGGGTGGATAACATCATCCGTGCAAGACCAAGAACCGCCAATAGACAACATATGTAACATATTTAGGATATACCTCGAAAATAATAAACCGCCACACTGTCATTATTATAATTAGAAACAGAACGCAAAAATTATCCACTATATAATTCAAAGACGCGAAAAAAAAAGAACAACGCGTCATAGAACTTTTGGCAATTCGCGTCACAAATAAATTTTGGCAACTTATGTTTCCTCTTCGAGCAGTACTCGAGCCCTGTCTCAAGAATGTAATAATACCCATCGTAGGTATGGTTAAAGATAGCATCTCCACAACCTCAAAGCTCCTTGCCGAGAGTCGCCCTCCTTTGTCGAGTAATTTTCACTTTTCATATGAGAACTTATTTTCTTATTCTTTACTCTCACATCCTGTAGTGATTGACACTGCAACAGCCACCATCACTAGAAGAACAGAACAATTACTTAATAGAAAAATTATATCTTCCTCGAAACGATTTCCTGCTTCCAACATCTACGTATATCAAGAAGCATTCACTTACCATGACACAGCTTCAGATTTCATTATTGCTGACAGCTACTATATCACTACTCCATCTAGTAGTGGCCACGCCCTATGAGGCATATCCTATCGGAAAACAATACCCCCCAGTGGCAAGAGTCAATGAATCGTTTACATTTCAAATTTCCAATGATACCTATAAATCGTCTGTAGACAAGACAGCTCAAATAACATACAATTGCTTCGACTTACCGAGCTGGCTTTCGTTTGACTCTAGTTCTAGAACGTTCTCAGGTGAACCTTCTTCTGACTTACTATCTGATGCGAACACCACGTTGTATTTCAATGTAATACTCGAGGGTACGGACTCTGCCGACAGCACGTCTTTGAACAATACATACCAATTTGTTGTTACAAACCGTCCATCCATCTCGCTATCGTCAGATTTCAATCTATTGGCGTTGTTAAAAAACTATGGTTATACTAACGGCAAAAACGCTCTGAAACTAGATCCTAATGAAGTCTTCAACGTGACTTTTGACCGTTCAATGTTCACTAACGAAGAATCCATTGTGTCGTATTACGGACGTTCTCAGTTGTATAATGCGCCGTTACCCAATTGGCTGTTCTTCGATTCTGGCGAGTTGAAGTTTACTGGGACGGCACCGGTGATAAACTCGGCGATTGCTCCAGAAACAAGCTACAGTTTTGTCATCATCGCTACAGACATTGAAGGATTTTCTGCCGTTGAGGTAGAATTCGAATTAGTCATCGGGGCTCACCAGTTAACTACCTCTATTCAAAATAGTTTGATAATCAACGTTACTGACACAGGTAACGTTTCATATGACTTACCTCTAAACTATGTTTATCTCGATGACGATCCTATTTCTTCTGATAAATTGGGTTCTATAAACTTATTGGATGCTCCAGACTGGGTGGCATTAGATAATGCTACCATTTCCGGGTCTGTCCCAGATGAATTACTCGGTAAGAACTCCAATCCTGCCAATTTTTCTGTGTCCATTTATGATACTTATGGTGATGTGATTTATTTCAACTTCGAAGTTGTCTCCACAACGGATTTGTTTGCCATTAGTTCTCTTCCCAATATTAACGCTACAAGGGGTGAATGGTTCTCCTACTATTTTTTGCCTTCTCAGTTTACAGACTACGTGAATACAAACGTTTCATTAGAGTTTACTAATTCAAGCCAAGACCATGACTGGGTGAAATTCCAATCATCTAATTTAACATTAGCTGGAGAAGTGCCCAAGAATTTCGACAAGCTTTCATTAGGTTTGAAAGCGAACCAAGGTTCACAATCTCAAGAGCTATATTTTAACATCATTGGCATGGATTCAAAGATAACTCACTCAAACCACAGTGCGAATGCAACGTCCACAAGAAGTTCTCACCACTCCACCTCAACAAGTTCTTACACATCTTCTACTTACACTGCAAAAATTTCTTCTACCTCCGCTGCTGCTACTTCTTCTGCTCCAGCAGCGCTGCCAGCAGCCAATAAAACTTCATCTCACAATAAAAAAGCAGTAGCAATTGCGTGCGGTGTTGCTATCCCATTAGGCGTTATCCTAGTAGCTCTCATTTGCTTCCTAATATTCTGGAGACGCAGAAGGGAAAATCCAGACGATGAAAACTTACCGCATGCTATTAGTGGACCTGATTTGAATAATCCTGCAAATAAACCAAATCAAGAAAACGCTACACCTTTGAACAACCCCTTTGATGATGATGCTTCCTCGTACGATGATACTTCAATAGCAAGAAGATTGGCTGCTTTGAACACTTTGAAATTGGATAACCACTCTGCCACTGAATCTGATATTTCCAGCGTGGATGAAAAGAGAGATTCTCTATCAGGTATGAATACATACAATGATCAGTTCCAATCCCAAAGTAAAGAAGAATTATTAGCAAAACCCCCAGTACAGCCTCCAGAGAGCCCGTTCTTTGACCCACAGAATAGGTCTTCTTCTGTGTATATGGATAGTGAACCAGCAGTAAATAAATCCTGGCGATATACTGGCAACCTGTCACCAGTCTCTGATATTGTCAGAGACAGTTACGGATCACAAAAAACTGTTGATACAGAAAAACTTTTCGATTTAGAAGCACCAGAGAAGGAAAAACGTACGTCAAGGGATGTCACTATGTCTTCACTGGACCCTTGGAACAGCAATATTAGCCCTTCTCCCGTAAGAAAATCAGTAACACCATCACCATATAACGTAACGAAGCATCGTAACCGCCACTTACAAAATATTCAAGACTCTCAAAGCGGTAAAAACGGAATCACTCCCACAACAATGTCAACTTCATCTTCTGACGATTTTGTTCCGGTTAAAGATGGTGAAAATTTTTGCTGGGTCCATAGCATGGAACCAGACAGAAGACCAAGTAAGAAAAGGTTAGTAGATTTTTCAAATAAGAGTAATGTCAATGTTGGTCAAGTTAAGGACATTCACGGACGCATCCCAGAAATGCTGTGATTATACGCAACGATATTTTGCTTAATTTTATTTTCCTGTTTTATTTTTTATTAGTGGTTTACAGATACCCTATATTTTATTTAGTTTTTATACTTAGAGACATTTAATTTTAATTCCATTCTTCAAATTTCATTTTTGCACTTAAAACAAAGATCCAAAAATGCTCTCGCCCTCTTCATATTGAGAATACACTCCATTCAAAATTTTGTCGTCACCGCTGATTAATTTTTCACTAAACTGATGAATAATCAAAGGCCCCACGTCAGAACCGACTAAAGAAGTGAGTTTTATTTTAGGAGGTTGAAAACCATTATTGTCTGGTAAATTTTCATCTTCTTGACATTTAACCCAGTTTGAATCCCTTTCAATTTCTGCTTTTTCCTCCAAACTATCGACCCTCCTGTTTCTGTCCAACTTATGTCCTAGTTCCAATTCGATCGCATTAATAACTGCTTCAAATGTTATTGTGTCATCGTTGACTTTAGGTAATTTCTCCAAATGCATAATCAAACTATTTAAGGAAGATCGGAATTCGTCGAACACTTCAGTTTCCGTAATGATCTGATCGTCTTTATCCACATGTTGTAATTCACTAAAATCTAAAACGTATTTTTCAATGCATAAATCGTTCTTTTTATTAATAATGCAGATGGAAAATCTGTAAACGTGCGTTAATTTAGAAAGAACATCCAGTATAAGTTCTTCTATATAGTCAATTAAAGCAGGATGCCTATTAATGGGAACGAACTGCGGCAAGTTGAATGACTGGTAAGTAGTGTAGTCGAATGACTGAGGTGGGTATACATTTCTATAAAATAAAATCAAATTAATGTAGCATTTTAAGTATACCCTCAGCCACTTCTCTACCCATCTATTCATAAAGCTGACGCAACGATTACTATTTTTTTTTTCTTCTTGGATCTCAGTCGTCGCAAAAACGTATACCTTCTTTTTCCGACCTTTTTTTTAGCTTTCTGGAAAAGTTTATATTAGTTAAACAGGGTCTAGTCTTAGTGTGAAAGCTAGTGGTTTCGATTGACTGATATTAAGAAAGTGGAAATTAAATTAGTAGTGTAGACGTATATGCATATGTATTTCTCGCCTGTTTATGTTTCTACGTACTTTTGATTTATAGCAAGGGGAAAAGAAATACATACTATTTTTTGGTAAAGGTGAAAGCATAATGTAAAAGCTAGAATAAAATGGACGAAATAAAGAGAGGCTTAGTTCATCTTTTTTCCAAAAAGCACCCAATGATAATAACTAAAATGAAAAGGATTTGCCATCTGTCAGCAACATCAGTTGTGTGAGCAATAATAAAATCATCACCTCCGTTGCCTTTAGCGCGTTTGTCGTTTGTATCTTCCGTAATTTTAGTCTTATCAATGGGAATCATAAATTTTCCAATGAATTAGCAATTTCGTCCAATTCTTTTTGAGCTTCTTCATATTTGCTTTGGAATTCTTCGCACTTCTTTTCCCATTCATCTCTTTCTTCTTCCAAAGCAACGATCCTTCTACCCATTTGCTCAGAGTTCAAATCGGCCTCTTTCAGTTTATCCATTGCTTCCTTCAGTTTGGCTTCACTGTCTTCTAGCTGTTGTTCTAGATCCTGGTTTTTCTTGGTGTAGTTCTCATTATTAGATCTCAAGTTATTGGAGTCTTCAGCCAATTGCTTTGTATCAGACAATTGACTCTCTAACTTCTCCACTTCACTGTCGAGTTGCTCGTTTTTAGCGGACAAAGATTTAATCTCGTTTTCTTTTTCAGTGTTAGATTGCTCTAATTCTTTGAGCTGTTCTCTCAGCTCCTCATATTTTTCTTGCCATGACTCAGATTCTAATTTTAAGCTATTCAATTTCTCTTTGATC', 'CTAGGAGGTATATGTTGCCATAGAGGTGGAGTCCAAATCTAGAGTTGTTGCCTTGGTAACGGCTGTACTCTGTCAATCCATAGCAGCTCTCAATGTTCGATTTTGCTCGTCATCAGTCGAGACGTAGACTTCGGCGACTTCAAGATGATTCCCACCTATTGTAGTAGGCACGTTCTGGTTCTTGGCGGTTATCTGTTGTATACATTGTATAAATCCTATATGGAGCTTTTATTATTTGGCGGTGTGACAGTAATAATATTAATCTTTGTCTTGCGTTTTTAATAGGTGATATATTAAGTTTCTGCGCTTTTTTTTTCTTGTTGCGCAGTATCTTGAAAACCGTTAAGCGCAGTGTTTATTTAAAACCGTTGAATACAAAGGAGAAGCTCGTCATGAGCTCGGGACAGAGTTCTTACATTATTATGGGTAGCATCCATACCAATTTCTATCGTAGAGGTGTTGGAGTTTCGAGGAACGGCTCTCAGCGGGAGGAAACAGCTCATTAAAAGTGAAAAGTATACTCTTGAATAAAAGAATAAGAAATGAGAGTGTAGGACATCACTAACTGTGACGTTGTCGGTGGTAGTGATCTTCTTGTCTTGTTAATGAATTATCTTTTTAATATAGAAGGAGCTTTGCTAAAGGACGAAGGTTGTAGATGCATATAGTTCTTCGTAAGTGAATGGTACTGTGTCGAAGTCTAAAGTAATAACGACTGTCGATGATATAGTGATGAGGTAGATCATCACCGGTGCGGGATACTCCGTATAGGATAGCCTTTTGTTATGGGGGGTCACCGTTCTCAGTTACTTAGCAAATGTAAAGTTTAAAGGTTACTATGGATATTTAGCAGACATCTGTTCTGTCGAGTTTATTGTATGTTAACGAAGCTGAATGGCTCGACCGAAAGCAAACTGAGATCAAGATCTTGCAAGAGTCCACTTGGAAGAAGACTGAATGATAGACTACGCTTGTGGTGCAACATAAAGTTACATTATGAGCTCCCATGCCTGAGACGGCTGTCGTGCAGAAACTTGTTATGTATGGTTAAACAACAATGTTTGGCAGGTAGGTAGAGCGATAGCAGTCTAAAGTTAGATAACCGCAACAATTTTTTGATACCAATATGATTGCCGTTTTTGCGAGACTTTGATCTAGGATTACTTCAGAAGTTGCACTGAAAACTGGCAAGTTACAAGTGATTGCTTCTTAGGTAACACAGCATAATGCCTGCAAGAGTCAACATATTACGCGGCAATGGGTTAACCGACAAGAAGCTAAGACCGCTCAACTTCAAATGACCCTGCCGTGGCCACTATTTGAGCCGCTAACGAGGTCTTTGTTCGATGTCAAAACAGTAGTAGCGATGTCTGTAACTTCCTAAAAGACGGCAACTCCATCTTAAGCTTAATCAGTAGCCCCGAGTGGTCAATTGATGGAGATAAGTTTTATCAAACTATTAGTTGCAATGACTGTGTCCATTGCAAAGTATACTGAATGGAGATTTGATACAAATAGAGCTACTGCTAGGATAAAGAAGACTATTTAACCCAAGATATTTGAATAACCTACGAGGTCTGACCCACCGTAATCTATTACGATGGTAAAGGCCCAGACAGGGTCTACTTAATGAGCCATTCTTGAGGTTAGGACGGTTAAAAAGACACAGGTAAATACTATGAATACCACTACACTAAATAAAGTTGAAGCTTCAACAGAGGTGTTGCCTAAACAAACGGTAATCAAGAGAAGGGTTATAATTGCGATGTTCCCCACTTACCAAGAGGATGATAAAAAACGGAAGAGTCAAATGTCTGATGCACTTATGTTTGCAAAGTAATCTCAAATGATTAAGTTCGGTTCTGGTACTGACCCACTTTAAGGTTAGTAGATTAAATTGTAATCGACCTCTTCACGGGTTCTTAAAGCTGTTCGAAAGTAATCCAAACTTTCGCTTGGTTCCAAGTGTTAGAGTTCTCGATATAAAATTGTAGTAACCGTACCTAAGTTTCTATTGAGTGAGTTTGGTGTCACGCTTACGTTGCAGGTGTTCTTCAAGAGTGGTGAGGTGGAGTTGTTCAAGAATGTGTAGAAGATGAATGTGACGTTTTTAAAGAAGATGGAGGCGACGACGATGAAGAAGACGAGGTCGTCGCGACGGTCGTCGGTTATTTTGAAGTAGAGTGTTATTTTTTCGTCATCGTTAACGCACGCCACAACGATAGGGTAATCCGCAATAGGATCATCGAGAGTAAACGAAGGATTATAAGACCTCTGCGTCTTCCCTTTTAGGTCTGCTACTTTTGAATGGCGTACGATAATCACCTGGACTAAACTTATTAGGACGTTTATTTGGTTTAGTTCTTTTGCGATGTGGAAACTTGTTGGGGAAACTACTACTACGAAGGAGCATGCTACTATGAAGTTATCGTTCTTCTAACCGACGAAACTTGTGAAACTTTAACCTATTGGTGAGACGGTGACTTAGACTATAAAGGTCGCACCTACTTTTCTCTCTAAGAGATAGTCCATACTTATGTATGTTACTAGTCAAGGTTAGGGTTTCATTTCTTCTTAATAATCGTTTTGGGGGTCATGTCGGAGGTCTCTCGGGCAAGAAACTGGGTGTCTTATCCAGAAGAAGACACATATACCTATCACTTGGTCGTCATTTATTTAGGACCGCTATATGACCGTTGGACAGTGGTCAGAGACTATAACAGTCTCTGTCAATGCCTAGTGTTTTTTGACAACTATGTCTTTTTGAAAAGCTAAATCTTCGTGGTCTCTTCCTTTTTGCATGCAGTTCCCTACAGTGATACAGAAGTGACCTGGGAACCTTGTCGTTATAATCGGGAAGAGGGCATTCTTTTAGTCATTGTGGTAGTGGTATATTGCATTGCTTCGTAGCATTGGCGGTGAATGTTTTATAAGTTCTGAGAGTTTCGCCATTTTTGCCTTAGTGAGGGTGTTGTTACAGTTGAAGTAGAAGACTGCTAAAACAAGGCCAATTTCTACCACTTTTAAAAACGACCCAGGTATCGTACCTTGGTCTGTCTTCTGGTTCATTCTTTTCCAATCATCTAAAAAGTTTATTCTCATTACAGTTACAACCAGTTCAATTCCTGTAAGTGCCTGCGTAGGGTCTTTACGACACTAATATGCGTTGCTATAAAACGAATTAAAATAAAAGGACAAAATAAAAAATAATCACCAAATGTCTATGGGATATAAAATAAATCAAAAATATGAATCTCTGTAAATTAAAATTAAGGTAAGAAGTTTAAAGTAAAAACGTGAATTTTGTTTCTAGGTTTTTACGAGAGCGGGAGAAGTATAACTCTTATGTGAGGTAAGTTTTAAAACAGCAGTGGCGACTAATTAAAAAGTGATTTGACTACTTATTAGTTTCCGGGGTGCAGTCTTGGCTGATTTCTTCACTCAAAATAAAATCCTCCAACTTTTGGTAATAACAGACCATTTAAAAGTAGAAGAACTGTAAATTGGGTCAAACTTAGGGAAAGTTAAAGACGAAAAAGGAGGTTTGATAGCTGGGAGGACAAAGACAGGTTGAATACAGGATCAAGGTTAAGCTAGCGTAATTATTGACGAAGTTTACAATAACACAGTAGCAACTGAAATCCATTAAAGAGGTTTACGTATTAGTTTGATAAATTCCTTCTAGCCTTAAGCAGCTTGTGAAGTCAAAGGCATTACTAGACTAGCAGAAATAGGTGTACAACATTAAGTGATTTTAGATTTTGCATAAAAAGTTACGTATTTAGCAAGAAAAATAATTATTACGTCTACCTTTTAGACATTTGCACGCAATTAAATCTTTCTTGTAGGTCATATTCAAGAAGATATATCAGTTAATTTCGTCCTACGGATAATTACCCTTGCTTGACGCCGTTCAACTTACTGACCATTCATCACATCAGCTTACTGACTCCACCCATATGTAAAGATATTTTATTTTAGTTTAATTACATCGTAAAATTCATATGGGAGTCGGTGAAGAGATGGGTAGATAAGTATTTCGACTGCGTTGCTAATGATAAAAAAAAAAGAAGAACCTAGAGTCAGCAGCGTTTTTGCATATGGAAGAAAAAGGCTGGAAAAAAAATCGAAAGACCTTTTCAAATATAATCAATTTGTCCCAGATCAGAATCACACTTTCGATCACCAAAGCTAACTGACTATAATTCTTTCACCTTTAATTTAATCATCACATCTGCATATACGTATACATAAAGAGCGGACAAATACAAAGATGCATGAAAACTAAATATCGTTCCCCTTTTCTTTATGTATGATAAAAAACCATTTCCACTTTCGTATTACATTTTCGATCTTATTTTACCTGCTTTATTTCTCTCCGAATCAAGTAGAAAAAAGGTTTTTCGTGGGTTACTATTATTGATTTTACTTTTCCTAAACGGTAGACAGTCGTTGTAGTCAACACACTCGTTATTATTTTAGTAGTGGAGGCAACGGAAATCGCGCAAACAGCAAACATAGAAGGCATTAAAATCAGAATAGTTACCCTTAGTATTTAAAAGGTTACTTAATCGTTAAAGCAGGTTAAGAAAAACTCGAAGAAGTATAAACGAAACCTTAAGAAGCGTGAAGAAAAGGGTAAGTAGAGAAAGAAGAAGGTTTCGTTGCTAGGAAGATGGGTAAACGAGTCTCAAGTTTAGCCGGAGAAAGTCAAATAGGTAACGAAGGAAGTCAAACCGAAGTGACAGAAGATCGACAACAAGATCTAGGACCAAAAAGAACCACATCAAGAGTAATAATCTAGAGTTCAATAACCTCAGAAGTCGGTTAACGAAACATAGTCTGTTAACTGAGAGATTGAAGAGGTGAAGTGACAGCTCAACGAGCAAAAATCGCCTGTTTCTAAATTAGAGCAAAAGAAAAAGTCACAATCTAACGAGATTAAGAAACTCGACAAGAGAGTCGAGGAGTATAAAAAGAACGGTACTGAGTCTAAGATTAAAATTCGATAAGTTAAAGAGAAACTAG')
#print(encontraProteinas("dados_1/standard_code.1", u49845))


def orfFinder(code: str, dna: tuple[str,
                                    str]) -> list[tuple[int, int, str, str]]:
  l = len(dna[0])
  res = []
  # Procurar proteínas na sequência original 5' -> 3'
  for i, j, seq in encontraProteinas(code, dna[0]):
    res.append((i, j, seq, "+"))
  # Procurar proteínas na sequência complementar 3' -> 5'
  for i, j, seq in encontraProteinas(code, dna[1][::-1]):
    res.append((l - i + 1, l - j + 1, seq, "-"))
  return res


# T6


def intergenicRegions(dna: tuple[str, str], cds: str) -> str:
  info_location_original = []
  info_location_complement = []
  current_intergenic_sequence = []

  with open(cds, "r") as ficheiro:
    cds = ficheiro.readlines()

  count = 1
  for linha in cds:
    if linha.startswith('>'):
      #String com o trecho a analisar
      vPosIni = linha.find('location')
      vTemp = linha[vPosIni:vPosIni + linha[vPosIni:].find(']')]
      pinicial = pfinal = ''
      #Determina a posição inicial
      for vItem in vTemp.split('..')[0][::-1]:
        if vItem.isdigit():
          pinicial = vItem + pinicial
        else:
          break
      #Determina a posição final
      for vItem in vTemp.split('..')[1]:
        if vItem.isdigit():
          pfinal += vItem
        else:
          break
      #Vamos guardar os complementos separados dos originais
      if 'complement' in vTemp:
        info_location_complement.append(
            (linha[1:linha.find(' ')], pinicial, pfinal, count))
      else:
        info_location_original.append(
            (linha[1:linha.find(' ')], pinicial, pfinal, count))

      count += 1

  #Constroi os originais
  #if len(info_location_original) > 1:
  for i in range(0, len(info_location_original) - 1):
    i1, i2, i3, i4 = info_location_original[i]
    f1, f2, f3, f4 = info_location_original[i + 1]

    i3 = int(i3)
    f2 = int(f2)

    if i3 + 1 < f2:
      current_intergenic_sequence.append(
          ('>' + i1 + '..' + f1 + f' [location={i3+1}..{f2-1}] +\n' +
           dna[0][i3 + 1:f2] + '\n', f4))

  #Constroi os complementos
  #if len(info_location_complement) > 1:
  for i in range(0, len(info_location_complement) - 1):
    i1, i2, i3, i4 = info_location_complement[i]
    f1, f2, f3, f4 = info_location_complement[i + 1]

    i3 = int(i3)
    f2 = int(f2)

    if i3 + 1 < f2:
      current_intergenic_sequence.append(
          ('>' + i1 + '..' + f1 +
           f' [location=complement({i3+1}..{f2-1})] -\n' + dna[1][i3 + 1:f2] +
           '\n', f4))

  # Ordena pela ordem de recolha
  print(current_intergenic_sequence)
  current_intergenic_sequence.sort(key=lambda item: item[1])

  #Retorna a string
  return ''.join(item[0] for item in current_intergenic_sequence)

#print(intergenicRegions(u49845,"dados_1/U49845.1.cds.fasta"))