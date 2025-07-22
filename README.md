Fase 2: O Desafio da Organização Digital - Modulo 1

O tema escolhido para o Software foi de um jogo de gerenciamento e simulação estratégica com o tema de atletismo, nomeado de:  A Jornada de um Campeão, a  ideia principal é colocar o usuário no papel de um técnico
A Fase 2 foca na exploração e comparação de algoritmos de busca, aplicados a situações do dia a dia de um treinador esportivo.

Arquitetura do projeto:
-> main.py: ponto de entrada do jogo. Organiza os desafios em três módulos e gerencia a interação com o jogador utilizando a biblioteca rich para exibição estilizada.

-> buscas.py: contém as implementações dos algoritmos de busca usados nos desafios.

-> modulos/: pasta onde ficam agrupadas as funcionalidades modulares.

-> README.md: documentação geral do projeto e desta fase.

                *Busca Sequencial (Desafio 1: A Pilha de Pergaminhos Desorganizados)
-Contexto: verificar se um número de peito específico está presente em uma lista desordenada de 50.000 atletas.
-Implementação: percorre a lista do início ao fim até encontrar o valor ou terminar.
-Integração: usada no módulo modulo1Desafio1() da main.py.
Complexidade:
-Melhor caso: O(1) (alvo é o primeiro elemento)
-Pior caso: O(n) (alvo está no fim ou não está na lista)
-Eficiência observada: em listas grandes, o número de comparações foi alto quando o número estava no fim ou não existia.

                *Busca Binária (Desafio 2: Os Catálogos Ordenados)
-Contexto: verificar a inscrição de múltiplos atletas em uma lista ordenada.
-Implementação: algoritmo clássico que divide a lista ao meio repetidamente.
-Integração: utilizada em modulo1Desafio2().
Complexidade:
-Todos os casos: O(log n)
-Eficiência observada: drasticamente superior à busca sequencial — em muitos testes, a busca binária foi mais de 20 vezes mais rápida.

                *Rabin-Karp Matcher (Desafio 3: Decifrando os Códigos do Vazio)
-Contexto: localizar um equipamento dentro de um grande texto de inventário.
-Implementação: algoritmo de busca de string com uso de hashes para comparação rápida.
-Integração: usada em modulo1Desafio3().
Complexidade:
-Melhor caso (sem colisões): O(n + m).Rápido, sem colisões, Como não há colisões de hash, não é necessário comparar caractere por caractere.
-Pior caso (com muitas colisões): O(n*m).Isso acontece quando o hash não é bom ou quando o texto tem padrões muito parecidos com o padrão buscado.
-Eficiência observada: muito eficaz para buscas curtas em textos grandes, com excelente performance para inventários moderados.


Fase 2: Otimização de Recursos - Módulo 2

O módulo 2 do desafio foca em otimizar como esses dados, agora organizados, são armazenados e acessados. A otimização de recursos é crucial para a performance de qualquer software, e nesta fase vamos utilizar a compressão de dados para economizar espaço e o hashing para acesso em tempo constante.

Arquiteturas adicionais do projeto:
-> otimizacao.py: Novo módulo contendo a implementação do algoritmo de compressão/descompressão de Huffman.

->hashing.py: Novo módulo com a implementação da Tabela Hash e das funções de hash customizadas.

->atletas.csv: Arquivo de dados externo para simular o banco de dados da federação.

->relatorio_maratona.txt: Arquivo de texto usado como base para o desafio de compressão.


                *Compressão de Dados com Huffman (Desafio 1: O Pacto Compacto)
-Contexto: Comprimir um arquivo de texto grande (relatorio_maratona.txt) que simula a telemetria bruta (dados de performance) de um GPS, a fim de otimizar sua transmissão por uma rede lenta e instável.
-Implementação: O algoritmo foi implementado em Python do zero. O processo inclui:
    1. Contagem da frequência de cada caractere no arquivo de texto.
    2. Construção de uma árvore binária (Árvore de Huffman) utilizando uma fila de prioridade (módulo heap`) para sempre combinar os dois nós de menor frequência.
    3. Geração de um dicionário de códigos binários (0 e 1) percorrendo a árvore.
    4. "Tradução" do texto original para a nova sequência de bits.
    5. Implementação de funções de empacotamento de bits para converter a string de '0's e '1's em bytes reais, permitindo uma compressão efetiva.
    6. O processo inverso para descompressão, garantindo a integridade dos dados.
-Integração: Toda a lógica de compressão está no arquivo modulos/otimizacao.py. A função modulo2Desafio1() em main.py orquestra o desafio, lendo o arquivo de texto, chamando as funções de otimização, salvando os resultados e exibindo um painel comparativo.
-Complexidade:
    -Tempo: O(n + k log k), onde n é o número total de caracteres no texto e k é o número de caracteres únicos. O(n) para contar as frequências e O(k log k) para construir a árvore de Huffman.
-Eficiência observada: Extremamente eficiente em textos com baixa variedade de caracteres e alta repetição. No teste final com o arquivo de telemetria otimizado, a taxa de compressão alcançou 56.77%, demonstrando a grande economia de espaço. A verificação de integridade confirmou que não houve perda de dados, provando a robustez do algoritmo.



Tabela Hash (Desafio 2: O Cofre Rápido)
-Contexto: Armazenar e consultar instantaneamente os dados de atletas em um grande banco de dados simulado da federação, utilizando o número de registro como chave única para acesso imediato.
-Implementação:
    1. Uma classe TabelaHashAtletas foi criada para encapsular toda a lógica.
    2. Tratamento de Colisões: Utiliza a técnica de Encadeamento Separado, onde cada posição da tabela é uma lista ("balde") que pode conter múltiplos atletas se uma colisão de hash ocorrer.
    3. Funções de Hash: Duas funções diferentes foram implementadas, permitindo ao jogador escolher qual testar:
        - Enlaçamento Deslocado (Shift Folding): Quebra a chave numérica do registro do atleta em pedaços de 3 dígitos e os soma para gerar o índice.
        - Extração (Extraction): Para chaves formatadas (ex: AnoMesID), extrai os últimos 3 dígitos (considerados a parte mais única) para gerar o índice.
    4. O sistema permite não apenas a busca, mas também a nserção de novos atletas, que são adicionados tanto à tabela em memória quanto ao arquivo atletas.csv para persistência dos dados.
-Integração: A classe TabelaHashAtletas e a classe Atleta estão definidas em modulos/hashing.py. A função modulo2Desafio2() em main.py gerencia a interação, permitindo ao jogador escolher a função de hash, carregar os dados do .csv e realizar buscas ou inserções em um menu interativo.
-Complexidade:
    -Inserção, Busca e Remoção:
        - Melhor/Caso Médio: O(1) (tempo constante). Com uma boa função de hash e poucas colisões, a operação é praticamente instantânea.
        - Pior Caso: O(n)`. Ocorre no cenário improvável em que todas as chaves geram o mesmo índice, transformando a tabela hash em uma única lista e a busca em uma busca sequencial.
-Eficiência observada: A busca por atletas foi instantânea, com o tempo de resposta medido em frações de milissegundos. A performance O(1) foi claramente demonstrada. O menu interativo permitiu observar como as duas diferentes funções de hash distribuíam os mesmos atletas de formas distintas pela tabela, evidenciando o impacto direto da escolha da função de hash na organização dos dados.