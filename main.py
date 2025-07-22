import time
import locale
import os#verifica tamanho dos arquivos
import json#salva o dicionário de códigos
import csv
from modulos.buscas import gerarListaInscritos, buscaSequencial, gerarListaOrdenada, buscaBinaria, buscaRabinKarp
from rich.console import Console
from modulos.otimizacao import huffmanComprimir, huffmanDescomprimir, empacotarBits, desempacotarBits
from modulos.hashing import Atleta, tabelaHashAtletas

try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')
    except locale.Error:
        print("Aviso: Locale 'pt_BR' não foi encontrado. A formatação de números pode usar vírgulas.")

console = Console()

def modulo1Desafio1():
    console.print("\n[bold yellow]Seja bem vindo(a) ao módulo 1 do desafio 1 do jogo: A JORNADA DE UM CAMPEÃO[/bold yellow]")
    console.print("[italic]A lista de pré-inscrição, com milhares de nomes dos atletas, acaba de ser liberada![/italic]")
    console.print("[italic]Essa lista é um arquivo bruto e sem ordem e como técnico, você precisa garantir que a inscrição do seu atleta foi efetivada para que ele avance de fases.[/italic]")
    console.print("\n[bold cyan]Desafio 01: Confirmar a Inscrição na lista[/bold cyan]")

    totalInscritos = 50_000#50.000
    console.print(f"A lista contém [bold]{totalInscritos:n}[/bold] atletas pré-inscritos.")
    listaInscritos = gerarListaInscritos(totalInscritos)

    try:
        numAtleta = int(console.input("\n[bold]Qual o número de peito do seu atleta que você precisa confirmar? [/bold]"))
    except ValueError:
        console.print("[bold red]Número inválido. Por favor, insira um número de peito.[/bold red]")
        return
    console.print(f"\n[yellow]Procurando o número [bold]{numAtleta}[/bold] na lista de inscritos, um por um...[/yellow]")   

    tempoInicio = time.time()
    posicaoNaLista, numComparacoes = buscaSequencial(listaInscritos, numAtleta)
    tempoFim = time.time()
    tempoTotal = tempoFim - tempoInicio

    console.print("\n----- [bold]Resultado da verificação do atleta:[/bold] -----")
    if posicaoNaLista != -1:#existe na lista
        console.print(f"[bold green]Inscrição Confirmada![/bold green] Seu atleta está na lista.")
        console.print(f"A posição na lista de divulgação é: {posicaoNaLista + 1:n}")
    else:
        console.print(f"[bold red]Atenção!![/bold red] O número {numAtleta:n} não foi encontrado na lista de pré-inscrição.")

    console.print(f"Atletas verificados um a um: [bold cyan]{numComparacoes:n}[/bold cyan]")
    console.print(f"Tempo da consulta: [bold magenta]{tempoTotal:.6f} segundos[/bold magenta]")
    
    if numComparacoes > (totalInscritos / 2):#precisou olhar mais de metade da lista, busca foi longa
        console.print("[italic red]\nPode ficar tranquilo jogador, deu tudo certo! Mas para a próxima grande maratona, preciso de um método de busca mais rápido e inteligente...'[/italic red]")

    console.print("\n[bold]Pressione Enter para avançar para o próximo desafio...[/bold]", end="")
    input()
    console.print("\n" + "="*50)

def modulo1Desafio2():
    console.print("\n\n" + "="*50)
    console.print("\n[bold yellow]Seja bem vindo(a) de volta ao módulo 1 do desafio 2 do jogo: A JORNADA DE UM CAMPEÃO - A eficiência da Maratona do Rio! [/bold yellow]")
    console.print("[italic]A lista de pré-inscrição, com milhares de nomes, acaba de ser liberada! Dessa vez você está treinando um grupo de atletas e a lista de inscritos está ORDENADA por número de peito.[/italic]")
    console.print("\n[bold cyan]Seu desafio é: Validar as incrições dos seus corredores nessa lista ordenada.[/bold cyan]")

    totalInscritos = 50_000
    console.print(f"A lista da Maratona do Rio contém [bold]{totalInscritos:n}[/bold] atletas.")
    listaOrdenada = gerarListaOrdenada(totalInscritos)

    atletasParaEncontrar = []#cria lista
    try:
        quantAtletas = int(console.input("\n[bold]Quantos atletas do seu grupo você deseja verificar? [/bold]"))
        for i in range(quantAtletas):#se repete até a quantAtletas
            numAtletas = int(console.input(f"  Digite o número de peito do [bold]{i + 1}º[/bold] atleta: "))#contagem começa do 1
            atletasParaEncontrar.append(numAtletas)#adiciona o numero na lista
    except ValueError:
        console.print("[bold red]Entrada inválida. Desafio cancelado.[/bold red]")
        return
    
    for atleta in atletasParaEncontrar:
        console.print(f"\n[yellow]Buscando pelo atleta [bold]{atleta:n}[/bold] usando a Busca Binária...[/yellow]")
        posicaoEncontrada, comparacoes = buscaBinaria(listaOrdenada, atleta)
        console.print(f"Comparações realizadas: [bold cyan]{comparacoes:n}[/bold cyan]")
    
    atletasParaComparar = atletasParaEncontrar[0]#compara com a primeira posicao
    console.print("\n\n-----[bold]Painel comparativo de performance[/bold] -----")
    console.print(f"Para encontrar o atleta [bold]{atletasParaComparar:n}[/bold] na lista ordenada de [bold]{totalInscritos:n}[/bold] pessoas:")
    posicaoEncontradaBinaria, compBinaria = buscaBinaria(listaOrdenada, atletasParaComparar)
    posicaoEncontradaSequencial, compSequen = buscaSequencial(listaOrdenada, atletasParaComparar)#usa a lista ordenada para a comparação ser justa

    console.print(f"Busca [bold red]Sequencial[/bold red]: [cyan]{compSequen:n}[/cyan] comparações.")
    console.print(f"Busca [bold green]Binária[/bold green]:    [cyan]{compBinaria:n}[/cyan] comparações.")

    if compBinaria > 0:#evita divisao por zero
        diferenca = compSequen / compBinaria
        console.print(f"\n[bold]A Busca binária foi [yellow]{diferenca:.2f} vezes[/yellow] mais eficiente![/bold]")#resultado
    console.print("[italic]Pode sorrir técnico! Nessa fase, graças à organização e um bom algoritmo você alcançou a eficiência  na sua procura.[/italic]")

    console.print("\n[bold]Pressione Enter para avançar para o próximo desafio...[/bold]", end="")
    input()
    console.print("\n" + "="*50)

def modulo1Desafio3():
    console.print("\n\n" + "="*50)
    console.print("[bold yellow]Seja bem vindo(a) de volta ao módulo 1 do desafio 3 do jogo: A JORNADA DE UM CAMPEÃO - Preparação para a Corrida[/bold yellow]")
    console.print("[italic]Seu atleta está se preparando para uma grande competição. Verifique se todos os equipamentos estão prontos.[/italic]")

    console.print("\n[bold cyan]Seu desafio é: Encontrar rapidamente os equipamentos na lista de inventário.[/bold cyan]")

    inventarioEquipamentos = (
        "Lista de equipamentos para a corrida de domingo:\n"
        "10 pares de tênis de corrida modelo Velocity X2, 5 garrafas esportivas, "
        "3 cronômetros profissionais, 8 uniformes oficiais da equipe, "
        "2 kits de primeiros socorros, 12 toalhas esportivas, "
        "6 óculos esportivos com proteção UV, 4 pares de meias de compressão, "
        "1 caixa de géis energéticos, 3 bandeiras da equipe, "
        "5 coletes refletivos para treino noturno, 2 termômetros esportivos."
    )

    console.print(f"\n[bold]Inventário completo:[/bold]\n[grey50]{inventarioEquipamentos}[/grey50]")

    #interação com o usuário
    while True:
        try:
            console.print("\n" + "-"*50)
            equipamento = console.input("[bold]Digite o equipamento que deseja verificar (ou 'sair' para terminar): [/bold]").strip().lower()
            
            if equipamento == 'sair':
                break

            if not equipamento:
                console.print("[bold red]Por favor, digite um equipamento válido.[/bold red]")
                continue

            
            console.print(f"\n[yellow]Buscando '[bold]{equipamento}[/bold]' no inventário...[/yellow]")

            posicoes = buscaRabinKarp(inventarioEquipamentos.lower(), equipamento.lower())#executa o algorítmo

            if posicoes: # retorna os índices lineares na string
                console.print(f"[bold green]Equipamento encontrado![/bold green] Aparece nas posições (índices): [bold cyan]{posicoes}[/bold cyan]")
               
                for pos in posicoes:#mostra onde ele foi encontrado
                    inicio = max(0, pos-20)
                    fim = min(len(inventarioEquipamentos), pos + len(equipamento) + 20)
                    contexto = inventarioEquipamentos[inicio:fim].replace('\n', ' ')
                    console.print(f"    ...{contexto}...")
            else:
                console.print(f"[bold red]Atenção![/bold red] O equipamento '[bold]{equipamento}[/bold]' não foi encontrado na lista.")

        except Exception as e:
            console.print(f"[bold red]Erro na busca: {str(e)}[/bold red]")

    console.print("\n[italic]Após a confirmação dos equipamentos está tudo pronto para a corrida![/italic]")

    console.print("\n[bold]Pressione Enter para avançar para o próximo desafio...[/bold]", end="")
    input()
    console.print("\n" + "="*50)


def modulo2Desafio1():
    console.print("\n\n" + "="*50)
    console.print("[bold yellow]Seja bem vindo(a) de volta ao módulo 2 do desafio 1 do jogo: A JORNADA DE UM CAMPEÃO - Relatório do atleta[/bold yellow]")
    console.print("[italic]Seu atleta completou a maratona! O relógio GPS gerou o arquivo 'relatorio_maratona.txt' com a análise da performance.[/italic]")

    console.print("\n[bold cyan]Seu desafio é: Comprimir este arquivo para enviá-lo pela rede.[/bold cyan]")

    arquivoOriginal = "relatorio_maratona.txt"
    arquivoComprimido = "relatorio.huff"
    arquivoCodigos = "codigos.json" 
    arquivoDescomprimido = "relatorio_descomprimido.txt"

    try:
        
        with open(arquivoOriginal, 'r', encoding='utf-8') as f:#ler arquivo
            textoOriginal = f.read()#o relatorio_maratona.txt é carregado e armazenado aqui
        console.print(f"\nArquivo '[bold]{arquivoOriginal}[/bold]' lido com sucesso!")

        
        console.print("[yellow]Iniciando a compressão com o algoritmo de Huffman...[/yellow]")#comprimir os dados
        textoComprimido, codigos = huffmanComprimir(textoOriginal)

        dadosEmBytes = empacotarBits(textoComprimido)#empacota a string de 0 e 1

        with open(arquivoComprimido, 'wb') as f:#arquivo salvo em modo binário
            f.write(dadosEmBytes)

        
        with open(arquivoCodigos, 'w', encoding='utf-8') as f:
            json.dump(codigos, f)#salva o dicionario
        console.print(f"Arquivo comprimido salvo como '[bold]{arquivoComprimido}[/bold]'.")
        console.print(f"Mapa de códigos salvo como '[bold]{arquivoCodigos}[/bold]'.")#arquivoCódigos é a chave para descomprimir

        console.print("\n[yellow]Recebimento... Lendo arquivo comprimido para descompressão...[/yellow]")

        with open(arquivoComprimido, 'rb') as f:#ler o arquivo comprimido em binário
            dadosComprimidosRecebidos = f.read()
        with open(arquivoCodigos, 'r', encoding='utf-8') as f:
            codigosRecebidos = json.load(f)

        textoComprimidoRecebidoStr = desempacotarBits(dadosComprimidosRecebidos)#volta para a string de 0 e 1

        textoDescomprimido = huffmanDescomprimir(textoComprimidoRecebidoStr, codigosRecebidos)

        with open(arquivoDescomprimido, 'w', encoding='utf-8') as f:
            f.write(textoDescomprimido)#salva o arq descomprimido
        console.print(f"Arquivo descomprimido salvo como '[bold]{arquivoDescomprimido}[/bold]' para verificação.")

        
        tamanhoOriginalBytes = os.path.getsize(arquivoOriginal)#os.path.getsize dá o tamanho real do arquivo em bytes.
        tamanhoComprimidoBytes = os.path.getsize(arquivoComprimido)
        tamanhoTransmissao = tamanhoComprimidoBytes + os.path.getsize(arquivoCodigos)#tamanho total = arq comprimido + códigos

        taxaCompressao = (1 - (tamanhoTransmissao / tamanhoOriginalBytes)) * 100

        console.print("\n--- [bold]Painel de Compressão de Arquivo[/bold] ---")
        console.print(f"Tamanho Original....: [bold red]{tamanhoOriginalBytes:n}[/bold red] bytes")
        console.print(f"Tamanho Transmitido.: [bold green]{tamanhoTransmissao:n}[/bold green] bytes (dados + códigos)")
        console.print(f"Taxa de Compressão..: [bold yellow]{taxaCompressao:.2f}%[/bold yellow]")

        console.print("\n[bold]Verificação de Integridade dos Dados:[/bold]")
        if textoOriginal == textoDescomprimido:
            console.print("[bold green]Sucesso! O arquivo restaurado é idêntico ao original.[/bold green]")
        else:
            console.print("[bold red]Falha! Houve perda de dados no processo.[/bold red]")

    except FileNotFoundError:
        console.print(f"[bold red]Erro: Arquivo '{arquivoOriginal}' não encontrado. Por favor, crie-o antes de rodar o desafio.[/bold red]")

    console.print("\n[italic]Foi enviado o relatório compactado em segundos. A otimização é a chave para a performance, dentro e fora das pistas.[/italic]")
    
    console.print("\n[bold]Pressione Enter para avançar para o próximo desafio...[/bold]", end="")
    input()
    console.print("\n" + "="*50)

def modulo2Desafio2():
    console.print("\n\n" + "="*50)
    console.print("[bold yellow]Seja bem vindo(a) de volta ao módulo 2 do desafio 2 do jogo: A JORNADA DE UM CAMPEÃO - Hashing - O Cofre Rápido.[/bold yellow]")
    console.print("[italic]Você obteve acesso ao banco de dados da Federação de Atletas! Agora pode consultar e gerenciar informações de forma instantânea.[/italic]")

    while True:
        console.print("\n[bold cyan]Desafio: Testar diferentes funções de hash para organizar o banco de dados.[/bold cyan]")
        
        escolha = console.input("Qual função de hash deseja usar?\n[1] Enlaçamento Deslocado\n[2] Extração\n[3] Sair do Módulo\nEscolha: ")

        if escolha == '3':
            console.print("\n[bold green]Obrigado por utilizar o banco de dados da Federação![/bold green]")
            console.print("[italic]Módulo 2 concluído com sucesso![/italic]")
            break 

        if escolha == '1' or escolha == '2':
            if escolha == '1':
                metodoHash = 'enlacamento'
                console.print("\n[yellow]Usando a função de hash: Enlaçamento Deslocado.[/yellow]")
            else: 
                metodoHash = 'extracao'
                console.print("\n[yellow]Usando a função de hash: Extração.[/yellow]")
            
            tabelaAtletas = tabelaHashAtletas(tamanho=17, funcaoHash = metodoHash)#carregando os dados
            try:
                with open('atletas.csv', mode='r', encoding='utf-8') as f:
                    leitor_csv = csv.DictReader(f)
                    for linha in leitor_csv:
                        novoAtleta = Atleta(
                            registro=linha['registro'],
                            nome=linha['nome'],
                            pais=linha['pais'],
                            recorde_10k=linha['recorde_10k']
                        )
                        tabelaAtletas.inserir(novoAtleta)
                console.print(f"\n[bold green]Banco de dados com {sum(len(b) for b in tabelaAtletas.tabela)} atletas carregado com sucesso![/bold green]")
                console.print(str(tabelaAtletas))#mostra o estado da tabela
            except FileNotFoundError:
                console.print("[bold red]Erro: Arquivo 'atletas.csv' não encontrado.[/bold red]")
                return

            while True:
                console.print("\n--- [bold]Gerenciamento da Federação[/bold] ---")
                console.print("1. Buscar atleta por Nº de registro")
                console.print("2. Adicionar novo atleta")
                console.print("3. Voltar ao menu anterior")
                
                escolhaAcao = console.input("Escolha uma ação: ").strip()

                if escolhaAcao == '1': 
                    idBusca = console.input("  Digite o Nº de Registro do atleta para buscar: ").strip()

                    tempoInicio = time.time()
                    atletaEncontrado = tabelaAtletas.buscar(idBusca)
                    tempoTotal = time.time() - tempoInicio

                    if atletaEncontrado:
                        console.print(f"  [bold green]Atleta encontrado![/] {atletaEncontrado}")
                        console.print(f"  (Busca realizada em [magenta]{tempoTotal * 1000:.4f} milissegundos[/magenta])")
                    else:
                        console.print("  [bold red]Atleta não encontrado no banco de dados.[/bold red]")

                elif escolhaAcao == '2':
                    console.print("\n--- [bold]Cadastro de Novo Atleta[/bold] ---")
                    try:
                        
                        reg = console.input("  Nº de Registro: ").strip()
                        nom = console.input("  Nome: ").strip()
                        pa = console.input("  País: ").strip()
                        rec = console.input("  Recorde 10k (mm:ss): ").strip()

                        
                        atleta_para_adicionar = Atleta(registro=reg, nome=nom, pais=pa, recorde_10k=rec)#cria o objeto atleta

                        tabelaAtletas.inserir(atleta_para_adicionar)#insere o atleta na tabela para as buscas

                        with open('atletas.csv', mode='a', newline='', encoding='utf-8') as f:#adiciona o atleta no arquivo modo 'a' (append), sem apagar o que ja tinha
                            escritor_csv = csv.writer(f)
                            escritor_csv.writerow([reg, nom, pa, rec])#escreve dados como uma nova linha
                        
                        console.print(f"\n[bold green]Sucesso![/bold green] Atleta '{nom}' adicionado ao banco de dados e ao arquivo .csv!")
                        console.print("\n[bold]Tabela Hash Atualizada:[/bold]")
                        console.print(str(tabelaAtletas))#mostra o estado da tabela

                    except Exception as e:
                        console.print(f"[bold red]Ocorreu um erro ao adicionar o atleta: {e}[/bold red]")

                elif escolhaAcao == '3':
                    console.print("[yellow]Voltando ao menu de seleção de hash...[/yellow]")
                    break 
                
                else:
                    console.print("[bold red]Opção inválida. Por favor, escolha 1, 2 ou 3.[/bold red]")
        
        else: 
            console.print("[bold red]Opção inválida. Por favor, escolha 1, 2 ou 3.[/bold red]")

    console.print("\n[italic]Você como técnico tem o poder da informação na ponta dos dedos. Planejar estratégias nunca foi tão rápido e prático.[/italic]")
def main():
    console.print("[bold green]=== JOGO: A JORNADA DE UM CAMPEÃO ===[/bold green]")
    modulo1Desafio1()
    modulo1Desafio2()
    modulo1Desafio3()
    modulo2Desafio1()
    modulo2Desafio2()

if __name__ == "__main__":
    main()