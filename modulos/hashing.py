#Desafio 2, módulo 2: O Cofre Rápido (Hashing)
from dataclasses import dataclass#cria alguns métodos

@dataclass
class Atleta:#armazena dados de um atleta
    nome: str
    registro: str
    pais: str
    recorde_10k: str

class tabelaHashAtletas:#armazena e busca atletas
    def __init__(self, tamanho=17, funcaoHash='enlacamento'):#inicializa a tabela
        self.tamanho = tamanho#num primo para espalhar mais os dados (recomendado)
        self.tabela = [[] for _ in range(tamanho)]#lista de listas vazias
        self.metodoHash = funcaoHash#permite escolher qual o método hash vai ser usado

    def hashEnlacamentoDeslocado(self, chave: str) -> int:#quebra a chave em pedaços e soma
        soma = 0
        tamPedaco = 3#quebra em pedaços de 3 digitos
        chaveNumerica = int("".join(filter(str.isdigit, chave)))#converte a chave para num e ignora caracteres não numéricos

        while chaveNumerica > 0:
            soma += chaveNumerica % (10 ** tamPedaco)#pega um pedaço da chave
            chaveNumerica //=(10 ** tamPedaco)#remove o pedaço que ja foi somado

        return soma % self.tamanho
    
    def hashExtracao(self, chave: str) -> int:#extrai uma parte da chve que é considerada única
        try:
            parteExtraida = int(chave[-3:])#pega os 3 últimos caracteres e converte para inteiro
            return parteExtraida % self.tamanho
        except (ValueError, IndexError):#se a chave for curta ou não terminar com números
            return hash(chave) % self.tamanho
        
    def funcaoHash(self, chave: str) -> int:#direciona para a função de hash correta
        if self.metodoHash == 'enlacamento':
            return self.hashEnlacamentoDeslocado(chave)
        elif self.metodoHash == 'extracao':
            return self.hashExtracao(chave)
        else:
            return hash(chave) % self.tamanho#método padrão se for inválida

    def inserir(self, atleta: Atleta):#insere atleta na tabela
        indice = self.funcaoHash(atleta.registro)#calcula o índice usando o hash escolhido
        listaColisoes = self.tabela[indice]#hashs que colidiram

        for i, atl in enumerate(listaColisoes):
            if atl.registro == atleta.registro:#verifica se o atleta já existe
                listaColisoes[i] = atleta#se existir atualiza os dados
                return
        listaColisoes.append(atleta)#se não existir adiciona o novo atleta

    def buscar(self, registroAtleta: str) -> Atleta | None:#busca o atleta pelo numero
        indice = self.funcaoHash(registroAtleta)#calcula o índice onde o atleta está
        listaColisoes = self.tabela[indice]

        for atleta in listaColisoes:
            if atleta.registro == registroAtleta:
                return atleta#encontrou
        return None#não está lá
    
    def __str__(self) -> str:#cria a representação visual da tabela
        representacao = "-----Banco de dados da Federação dos Atletas-----\n"
        for i, listaColisoes in enumerate(self.tabela):
            representacao += f"Índice {i}: "
            if not listaColisoes:
                representacao += "Vazio\n"
            else:
                nomesAtletas = " -> ".join([f"{atl.nome} ({atl.registro})" for atl in listaColisoes])
                representacao += nomesAtletas + "\n"
        return representacao




