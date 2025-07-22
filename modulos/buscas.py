#TRABALHO FINAL: A JORNADA DE UM CAMPEÃO, jogo de gerenciamento e simulação estratégica com o tema de atletismo
#Desafio 1: A Pilha de Pergaminhos Desorganizados (Busca Sequencial)

import random #biblioteca que gera nums aleatórios

def gerarListaInscritos(quantAtletas: int) -> list[int]: 
    valorMaximo = quantAtletas + 1000#numeros suficientes e únicos
    numPeito = random.sample(range(1001, valorMaximo + 1), quantAtletas)#cria sequencia que vai do 1001 até o valor maximo
    return numPeito #retorna a lista

def buscaSequencial(numPeito: list[int], atletaProcurado: int) -> tuple[int, int]:#busca o atleta passando o numPeito
    comp = 0
    for indice, numAtual in enumerate(numPeito):#enumerete retorna o indice e o valor de cada elem
        comp += 1#incrementa
        if numAtual == atletaProcurado:
            return indice, comp#encontrado
    return -1, comp#não encontrado


#Desafio 2: Os Catálogos Ordenados (Busca Binária)

def gerarListaOrdenada(quantAtletas: int) -> list[int]:
    numPeito = gerarListaInscritos(quantAtletas)#reutiliza a função de cima
    numPeito.sort()#ordena a lista
    return numPeito

def buscaBinaria(numPeito: list[int], atletaProcurado: int) -> tuple[int, int]:
    inicio = 0#ponteiro inicio
    fim = len(numPeito) - 1#ponteiro fim
    comp = 0
    while inicio <= fim:
        comp += 1
        meio = (inicio + fim) // 2#acha a metade da lista
        numMeio = numPeito[meio]

        if numMeio == atletaProcurado:
            return meio, comp#meio é o numero procurado
        elif numMeio < atletaProcurado:
            inicio = meio + 1#começa do meio para frente
        else:
            fim = meio -1
    return -1, comp#não encontrado


#Desafio 3: Decifrando os Códigos do Vazio (Rabin-Karp Matcher) - busca padrões em textos, utilizando hashing para comparar strings

def buscaRabinKarp(texto: str, padrão: str) -> list[int]:
    N = len(texto)#comprimento da string da busca
    M = len(padrão)#comprimento da string que vai encontrar

    if N < M:#se o texto for menor que o padrão
        return[]#retorna vazio
    
    b = 256#caracteres do alfabeto ASCII
    c = 101#num primo grande para calcular o hash
    hashPadrao = 0
    hashTexto = 0#primeira janela de texto que vai ser comparada

    h = 1#valor usado para a remoção do primeiro caractere da janela
    for i in range(M - 1):
        h = (h * b) % c #calcula o valor de h = base^(m-1) % primo.
    for i in range (M):#calcula o hash do padão e da primeira janela de texto
        hashPadrao = (b * hashPadrao + ord(padrão[i])) % c#ord(caractere) pega o valor ASCII
        hashTexto = (b * hashTexto + ord(texto[i])) % c
    
    posicoesEncontradas = []#lista para armazenar os índices onde é encontrado o padão

    for i in range(N - M + 1):#percorre as possíveis janelas de tamanho M dentro do texto
        if hashPadrao == hashTexto:#compara
            if padrão == texto[i : i + M]:#compara as strings caractere por caractere se eles forem iguais
                posicoesEncontradas.append(i)#se encontrar adciona o indice na lista

        #cálculo do hash da próxima janela(janela deslizante)
        if i < N - M:#garantia de que tem caractere
            hashTexto = (b * (hashTexto - ord(texto[i]) * h) + ord(texto[i + M])) % c#remove o caractere da esquerda que está saindo e multiplica por h, e adiciona o da direita(novo caractere)
        #usa o %c para manter o número pequeno            
            if hashTexto < 0:#se for negativo
                hashTexto = hashTexto + c#corrige e garante que o hash seja positivo, soma com c
    return posicoesEncontradas#retorna a lista com os indíces que o padrão é encontrado