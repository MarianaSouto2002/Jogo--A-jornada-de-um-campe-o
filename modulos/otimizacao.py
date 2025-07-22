import heapq#módulo que trabalha com filas de prioridade
from collections import defaultdict#defaultdict para retornar um valor padrão

#Módulo 2: Otimização de Recursos - Espaço é Poder
#O Pacto Compacto (Compressão RLE e Huffman):

class noHuffman:#classe que representa os nós da árvore
    def __init__(self, caractere, frequencia):
        self.caractere = caractere 
        self.frequencia = frequencia#armazena frequencia dos caracteres
        self.esquerda = None#filhos da esquerda 
        self.direita = None#filhos da direita 

    def __lt__(self, outro):#método que vai permitir a comparação entre os nós
        return self.frequencia < outro.frequencia#a fila de prioridade vai saber qual nó tem a menor freq
    
def calcularFrequencia(texto: str) -> dict:#conta a freq dos caracteres, retorna um dicionário {'a':5...}
        frequencia = defaultdict(int)#inicializa com 0
        for caractere in texto:
            frequencia[caractere] += 1

        return frequencia
        
def construirArvoreHuffaman(frequencia: dict) -> noHuffman:#usa a freq para construir a árvore, e retorna o nó
        filaDePrioridade = [noHuffman(char, freq) for char, freq in frequencia.items()]#cria um nó para cada caractere
        heapq.heapify(filaDePrioridade)#heapify tranforma a lista em uma fila de prioridade do menor valor, itens ordenados
        
        while len(filaDePrioridade) > 1:#constroi a árvore combinando os nós até sobrar apenas 1 nó raiz
            #pega os dois nós com menor frequencia
            noEsquerda = heapq.heappop(filaDePrioridade)#heappop remove e retorna o menor elemento
            noDireita = heapq.heappop(filaDePrioridade)
            freqSoma = noEsquerda.frequencia + noDireita.frequencia#cria um nó pai com a soma das freq dos filhos
            noPai = noHuffman(None, freqSoma)
            noPai.esquerda = noEsquerda
            noPai.direita = noDireita
            heapq.heappush(filaDePrioridade, noPai)#adiciona o nó pai de volta a fila, mantendo a ordem
        
        return filaDePrioridade[0]#retorna a raíz da árvore completa
    
def gerarCodigos(raizArvore: noHuffman) -> dict:#gera para cada caract os códigos binários
        codigos = {}

        def percorrer(no, codAtual):#percorre recursivamente a árvore
            if no is None:#se o nó tem 1 caractere ele é a folha
                return
            if no.caractere is not None:
                codigos[no.caractere] = codAtual if codAtual else "0"
                return
            percorrer(no.esquerda, codAtual + "0")
            percorrer(no.direita, codAtual + "1")

        percorrer(raizArvore, "")
        return codigos
    
def huffmanComprimir(texto: str) -> tuple[str, dict]:#recebe o textoOriginal que a main manda
        if not texto:
            return "", {}
        
        frequencia = calcularFrequencia(texto)#faz a contagem
        arvore = construirArvoreHuffaman(frequencia)
        codigos = gerarCodigos(arvore)#"dicionário" de códigos

        textoComprimido = "".join([codigos[caractere] for caractere in texto])#substitui cada caractere pelo seu código binário e junta o código 

        return textoComprimido, codigos#retorna o texto binário e o dicionário de códigos
    
def huffmanDescomprimir(textoComprimido: str, codigos: dict) -> str:#usa os códigos para descomprimir e retorna o texto original
        if not textoComprimido:
            return ""
        
        codInvertidos = {v: k for k, v in codigos.items()}#inverte o dicionário, agora a chave é o código binário
        codAtual = ""
        textoDescomprimido = ""

        for bit in textoComprimido:#lê bit por bit, acumulando até encontrar um código válido
            codAtual += bit
            if codAtual in codInvertidos:
                textoDescomprimido += codInvertidos[codAtual]#quando encontra adiciona o caractere que corresponde e reinicia
                codAtual = ""
        
        return textoDescomprimido

def empacotarBits(textoComprimidoStr: str) -> bytes:#converte os 0 e 1 em bytes reais
     padding = 8 -(len(textoComprimidoStr) % 8)
     textoComprimidoStr += '1' + '0' * (padding - 1)#adiciona 1 e 0 até que o comprimento da string seja um múltimplo de 8
     
     listaBytes = bytearray()#lista de bytes, cada byte é 8 bits
     for i in range(0, len(textoComprimidoStr), 8):
         byte = textoComprimidoStr[i:i+8]
         listaBytes.append(int(byte, 2))
     return bytes(listaBytes)

def desempacotarBits(dadosBytes: bytes) -> str:#converte de volta os bytes para 0 e 1
     listaBits = []
     for byte in dadosBytes:
          listaBits.append(format(byte, '08b'))#converte um num para sua representação binária com 8 dígitos

     stringBits = "".join(listaBits)
     # Remove o padding que adicionamos na hora de empacotar.
    # Procuramos pelo '1' que marca o fim dos dados e descartamos o resto.
     stringBitsSemPadding = stringBits.rstrip('0')
     if stringBitsSemPadding.endswith('1'):
         stringBitsSemPadding = stringBitsSemPadding[:-1]

     return stringBitsSemPadding

     
