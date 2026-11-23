# RESOLUÇÃO DA LISTA 2

**Disciplina:** Inteligência Artificial (PPGI 2026.2)  
**Professor:** Evandro Costa  
**Integrantes:** Ana Leticia Nobre da Silva e Arthur Vinicius Fernandes de Carvalho  

## 1. Sistemas baseados em Ontologias e Grafos de Conhecimento

Uma ontologia define formalmente os conceitos de um domínio suas classes, propriedades, relações e restrições lógicas. Por exemplo numa aplicação médica, Doenca e Sintoma podem ser definidos como classes enquanto temSintoma atua como uma propriedade relacionando essas entidades, além disso axiomas formais permitem estabelecer que toda instância de Gripe também pertence à classe Doenca. Na linguagem OWL essa semântica formal possibilita que um motor de raciocínio deduza novas informações implícitas e verifique possíveis inconsistências na base. A abordagem por ontologia prioriza o rigor do significado e as regras estruturais do domínio, porém sua construção costuma exigir bastante cuidado técnico e o processamento pode ficar pesado quando a expressividade lógica aumenta muito.

Por outro lado um grafo de conhecimento organiza a informação na forma de uma rede onde as entidades são representadas como nós e as relações aparecem como arestas direcionadas. Seguindo o mesmo contexto de saúde podemos registrar fatos como (Ana, temSintoma, Febre) ou (Gripe, podeCausar, Febre). Essa estrutura é bem flexível para juntar dados vindos de fontes diferentes e facilita consultas que percorrem conexões entre vizinhos. Apesar dessa praticidade para exploração e busca rápida uma aresta isolada no grafo não impõe por conta própria toda a semântica lógica nem as restrições formais que encontramos em uma ontologia.

Na prática as duas abordagens funcionam muito bem juntas, já que a ontologia fornece o vocabulário padronizado e as regras do esquema enquanto o grafo armazena a grande massa de fatos concretos sobre os indivíduos. Como exemplo de mapeamento considere um domínio de biblioteca contendo as classes Pessoa, Livro, Autor e Genero com as propriedades escreveu e temGenero além do axioma indicando que Autor é subclasse de Pessoa. Ao mapear essa ontologia para um grafo de conhecimento cada classe e cada indivíduo passa a ser um nó identificado e cada propriedade declarada vira uma aresta rotulada. Assim a afirmação escreveu(Clarice, A Paixao Segundo GH) na ontologia se transforma numa ligação direta entre o nó Clarice e o nó do livro através da relação escreveu, enquanto o axioma de subclasse permite associar ao nó Clarice tanto o rótulo Autor quanto o rótulo Pessoa. Os arquivos referentes a esta questão estão organizados na pasta Questao_01.

## 2. Algoritmo dos K vizinhos mais próximos (KNN) na base de 30 instâncias

Na primeira lista de exercícios trabalhamos com uma base composta por 30 instâncias categóricas voltadas para classificar o atributo alvo Risco em três níveis possíveis que são Baixo, Moderado ou Alto. O algoritmo KNN funciona como um método supervisionado baseado em instâncias onde não há ajuste prévio de parâmetros complexos, pois diante de uma nova consulta o sistema mede a distância entre o novo caso e todos os exemplos já rotulados da base selecionando os k vizinhos mais próximos para decidir a classe final por votação majoritária. Como os cinco atributos preditores dessa base são todos categóricos utilizamos a distância de Hamming, na qual cada atributo com valor diferente entre dois registros soma 1 ponto na distância total podendo variar de 0 até 5. Quando ocorre empate de distância entre vizinhos o desempate segue a ordem original das linhas na tabela.

Para demonstrar o funcionamento tomamos a consulta com Historia igual a Boa, Divida igual a Alta, Garantia igual a Nenhuma, Renda de 0 a 15k e TempoEmprego igual a Longo. Comparando essa entrada com as 30 linhas da base observamos que as instâncias 11 (Risco Alto), 13 (Risco Baixo), 22 (Risco Alto) e 27 (Risco Moderado) ficam todas com distância de Hamming igual a 1 pois diferem em apenas um atributo. Adotando k igual a 3 os três primeiros vizinhos selecionados são as instâncias 11, 13 e 22 que fornecem dois votos para Alto e um voto para Baixo resultando na classificação Alto com proporção de 2 em 3. Se ampliarmos a vizinhança para k igual a 5 entram também instâncias de distância seguinte mantendo a maioria favorável à classe Alto com 3 votos em 5. A base completa com as 30 instâncias e o código da função knn_hamming encontram se dentro da pasta Questao_02 nos arquivos credito_ampliado.csv e prototipos_lista2.py.

## 3. O chatbot ELIZA regras algoritmo e evoluções

O programa ELIZA foi desenvolvido por Joseph Weizenbaum em 1966 com o propósito de simular a condução de uma entrevista clínica no estilo de um psicoterapeuta rogeriano. Mesmo sem possuir compreensão real sobre o mundo ou sobre os sentimentos humanos o sistema conseguia manter conversas convincentes porque identificava palavras chave nas frases digitadas aplicava regras de decomposição e remontagem do texto e devolvia perguntas abertas que incentivavam o próprio usuário a continuar falando. Quando uma frase seguia uma estrutura conhecida como Eu estou preocupado com X o mecanismo trocava os pronomes para ajustar a perspectiva do interlocutor e montava uma resposta como Por que você está preocupado com X.

Para ilustrar considere o seguinte trecho de diálogo entre um estudante e o sistema. Usuário diz: Estou muito ansioso com a apresentação do trabalho amanhã. ELIZA responde: Por que você diz que está muito ansioso com a apresentação do trabalho amanhã? Usuário diz: Acho que vou esquecer partes importantes na hora de falar. ELIZA responde: Você realmente acredita que vai esquecer partes importantes na hora de falar? Usuário diz: Sim isso já aconteceu antes na faculdade. ELIZA responde: Conte mais sobre isso por favor. As duas primeiras trocas são tecnicamente interessantes porque mostram como o casamento de padrões captura o trecho após o verbo ou expressão inicial realiza a inversão pronominal de primeira para segunda pessoa e devolve uma questão coerente sem precisar analisar o significado profundo da frase. Já a última resposta evidencia a limitação técnica do método, visto que diante de uma frase sem palavra chave prioritária o programa recorre a uma frase genérica de escape que ignora a informação histórica trazida pelo usuário.

O algoritmo interno do ELIZA opera em etapas bem definidas: primeiro faz a leitura e limpeza da sentença removendo pontuações que atrapalhem a busca, depois procura palavras chave cadastradas no roteiro ordenando as encontradas pela prioridade atribuída a cada termo. Em seguida a regra de decomposição associada à palavra de maior peso quebra a frase em partes usando curingas e a regra de remontagem reconstrói a resposta aplicando as substituições pronominais necessárias. Nos anos seguintes surgiram evoluções importantes a partir dessa ideia inicial. Em 1972 Kenneth Colby apresentou o PARRY na Universidade de Stanford para simular um paciente com esquizofrenia paranoica, indo além dos moldes puramente reativos do ELIZA ao manter variáveis internas de estado afetivo como nível de medo raiva e desconfiança que alteravam o rumo das respostas. Mais tarde a linguagem AIML criada por Richard Wallace para o robô ALICE padronizou a escrita de bases conversacionais em XML por meio de categorias padrões de entrada e modelos de saída além de tags para redução recursiva de frases (srai) e memória de tópico, ampliando bastante a escala das regras embora ainda permanecesse fundamentada em correspondência simbólica de padrões. O material desta questão está na pasta Questao_03.

## 4. Taxonomia de agentes em 5 categorias e descrição PEAS

Conforme apresentado por Russell e Norvig no Capítulo 2 os agentes inteligentes podem ser organizados em cinco categorias principais de acordo com a forma como processam percepções e escolhem ações: agente reativo simples, agente baseado em modelo (com estado), agente baseado em objetivo, agente baseado em utilidade e agente adaptativo (com aprendizado). Para cada aplicação a especificação PEAS define a Medida de Desempenho (P), o Ambiente (E), os Atuadores (A) e os Sensores (S) acompanhada das propriedades do respectivo ambiente de tarefa.

| Categoria de Agente | Aplicação | Descrição PEAS e Propriedades do Ambiente |
|***|***|***|
| Reativo simples | Termostato residencial automático | P: manter temperatura na faixa desejada e economizar energia. E: cômodo fechado, parcialmente observável, estocástico, dinâmico e contínuo. A: chave de acionamento do aquecedor ou ar condicionado. S: termômetro local. |
| Reativo simples | Sensor de presença para iluminação | P: garantir iluminação quando houver pessoas e reduzir gasto elétrico. E: corredor ou sala, parcialmente observável, estocástico e dinâmico. A: relé da lâmpada. S: sensor infravermelho e célula fotoelétrica. |
| Baseado em modelo | Aspirador robótico com mapa de limpeza | P: porcentagem da área limpa, tempo gasto e ausência de colisões. E: piso residencial com móveis, parcialmente observável, sequencial, dinâmico e discreto na grade. A: motores das rodas e escova de sucção. S: detector de sujeira, pára choque e odometria. |
| Baseado em modelo | Monitoramento de faixa em veículo | P: manter o carro centralizado na faixa com segurança. E: rodovia, parcialmente observável, estocástico, sequencial e contínuo. A: assistência na direção e alerta no painel. S: câmeras frontais e sensores de velocidade. |
| Baseado em objetivo | Sistema GPS de navegação urbana | P: chegar ao endereço solicitado cumprindo o trajeto válido. E: malha viária urbana, parcialmente observável, estocástico, sequencial e dinâmico. A: tela com mapa e instruções por voz. S: receptor de satélite e dados de trânsito. |
| Baseado em objetivo | Braço robótico de montagem industrial | P: encaixar a peça corretamente na posição final sem danos. E: célula de manufatura, observável localmente, determinístico ou pouco estocástico e sequencial. A: juntas motorizadas e garra pneumática. S: câmeras de visão e sensores de força. |
| Baseado em utilidade | Roteador inteligente de pacotes em rede | P: maximizar vazão minimizando atraso e perda de pacotes. E: rede de computadores, parcialmente observável, estocástico, dinâmico e multiagente. A: encaminhamento de pacotes pelas interfaces. S: contadores de fila e medidores de latência. |
| Baseado em utilidade | Escalonador de cargas em nuvem | P: equilibrar tempo de resposta, consumo energético e custo financeiro. E: cluster de servidores, parcialmente observável, estocástico e dinâmico. A: alocador de máquinas virtuais e filas. S: monitores de uso de processador memória e prazos. |
| Adaptativo | Filtro classificador de mensagens spam | P: minimizar falsos positivos e falsos negativos ao longo do tempo. E: caixa de entrada de correio eletrônico, parcialmente observável, estocástico e mutável. A: mover mensagem para pasta spam ou entrada. S: leitor de texto cabeçalhos e marcações do usuário. |
| Adaptativo | Sistema de recomendação de catálogo | P: aumentar taxa de acerto e satisfação do usuário nas sugestões. E: plataforma digital com milhares de itens, parcialmente observável, estocástico e dinâmico. A: exibição ordenada de itens na interface. S: registro de cliques buscas tempo de leitura e avaliações. |

Enquanto o agente reativo simples responde apenas à percepção imediata através de regras diretas de condição e ação, o agente baseado em modelo guarda um estado interno para lidar com ambientes parcialmente observáveis. O agente baseado em objetivo avalia sequências de ações futuras para atingir uma meta definida ao passo que o agente baseado em utilidade compara diferentes estados possíveis através de uma função numérica que mede o grau de qualidade quando há conflitos entre metas. Por fim o agente adaptativo incorpora um componente de aprendizagem que analisa o retorno das experiências para melhorar o comportamento futuro. A resposta individual também está salva na pasta Questao_04.

## 5. Resumo estendido: Inferência em Modelos de Linguagem (LLM)

### 5.1 Introdução e Conceituação de Inferência

O treinamento de um modelo de linguagem de ponta (Frontier Model) exige investimentos na casa das centenas de milhões de dólares e meses de processamento intensivo. No entanto ao término do treinamento o modelo resultante é essencialmente um conjunto estático de pesos, isto é números especializados ajustados durante o processo de aprendizado que ficam armazenados na memória. Por si só o modelo treinado é inerte e não realiza nenhuma ação.

A inferência é o processo técnico que traz o modelo à vida. Ela consiste em pegar o modelo previamente treinado e executá lo contra novas entradas (prompts) fornecidas pelos usuários para gerar saídas correspondentes. A inferência é a tecnologia fundamental por trás de todos os chatbots modernos assistentes de código e aplicações agênticas utilizadas atualmente.

### 5.2 Dinâmica Econômica e Custos Operacionais

Ao contrário do treinamento que ocorre apenas uma vez, a inferência ocorre a cada vez que uma mensagem é enviada ao modelo. Por ser um processo recorrente e executado continuamente em larga escala o custo acumulado da inferência ao longo do tempo frequentemente supera o custo total de treinamento do modelo. Consequentemente garantir a máxima eficiência no fornecimento (serving) de modelos tornou se o fator crítico para viabilizar financeiramente e operacionalmente o uso da inteligência artificial generativa.

### 5.3 Motores de Inferência e Padronização de Endpoints

O software responsável por orquestrar todo o ciclo de vida da execução de um modelo é denominado Motor de Inferência (Inference Engine). O objetivo central do motor de inferência é transformar uma coleção de pesos estáticos em um serviço capaz de responder a requisições de forma confiável rápida e em escala industrial. Entre as principais funções do motor estão gerenciar e agendar a fila de requisições recebidas, alocar e otimizar os recursos de hardware (GPUs) e determinar a melhor estratégia de processamento conjunto dos dados. Soluções amplamente adotadas na indústria como vLLM, Ollama e Llama.cpp são exemplos práticos de motores de inferência modernos.

A maioria dos motores de inferência expõe uma interface de programação (API) padronizada e compatível com o formato da OpenAI. Essa padronização traz uma vantagem estratégica fundamental para desenvolvedores pois a estrutura do formato de requisição permanece idêntica independentemente do modelo específico que esteja sendo executado na infraestrutura. Dessa forma é possível substituir o modelo subjacente em uma aplicação sem a necessidade de reescrever o código do sistema cliente.

### 5.4 Pré Processamento: Tokenização e Roteamento de Hardware

Antes que a consulta de um usuário entre no servidor ou atinja a GPU ela passa por um fluxo de pré processamento obrigatório que transforma o texto em um formato computável pelo modelo. Os modelos de linguagem não processam palavras ou caracteres diretamente. O texto de entrada é submetido à tokenização que divide a mensagem em tokens os quais podem ser palavras inteiras fragmentos de palavras ou sinais de pontuação e mapeia cada token para um identificador numérico único (Token ID). O modelo opera exclusivamente sobre essa sequência de identificadores.

Embora a tokenização consuma uma quantidade insignificante de capacidade computacional ela define diretamente o custo financeiro da consulta uma vez que a cobrança nos serviços de inferência é realizada por token. Existe também um compromisso importante no tamanho do vocabulário: modelos projetados com vocabulários maiores conseguem representar o texto de forma mais eficiente utilizando menos tokens por prompt, contudo um vocabulário expandido aumenta a complexidade computacional durante o processo de treinamento.

Assim que a requisição formatada chega ao data center ela passa por dois estágios iniciais. No primeiro estágio ocorre a autenticação, em que a requisição é validada por meio de uma chave de API (API Key) ou token de acesso para verificar a permissão de uso dos recursos de hardware. No segundo estágio atua o roteamento de inferência, onde o roteador (Inference Router) analisa os atributos do prompt como tamanho e tipo de conteúdo e direciona a requisição para o hardware físico disponível que esteja mais otimizado para atendê la naquele momento.

### 5.5 Estratégias de Agendamento e Batching (Loteamento)

Em um ambiente de produção múltiplas requisições chegam simultaneamente ao data center. Processar cada requisição individualmente na GPU seria extremamente ineficiente. A analogia utilizada no vídeo é a de uma padaria que liga um forno industrial gigantesco para assar um único pão por vez, o que geraria um enorme desperdício de energia e capacidade reduzindo drasticamente a vazão (throughput) medida pela quantidade de requisições processadas por unidade de tempo.

Para maximizar o aproveitamento do hardware a inferência utiliza o conceito de Batching (Loteamento) agrupando requisições diversas para que a GPU as processe como uma única unidade de trabalho coordenada e mais eficiente. Como as consultas dos usuários possuem tamanhos e tempos de resposta variados os motores modernos utilizam o Continuous Batching (Loteamento Contínuo). No momento exato em que uma requisição no lote é concluída o agendador (Scheduler) aloca imediatamente uma nova requisição para ocupar o espaço vago. Isso garante que as GPUs operem continuamente próximas da capacidade máxima de utilização sem ociosidade.

### 5.6 As Duas Fases Cruciais da Inferência: Prefill e Decode

Quando a requisição agendada chega ao modelo na GPU a execução da inferência é dividida em duas fases distintas e com características computacionais opostas: a fase de Prefill (Pré preenchimento) e a fase de Decode (Decodificação).

Na fase de Prefill o modelo lê e processa todo o prompt de entrada de uma só vez para compreender o contexto. Durante esse processo o modelo constrói o KV Cache (Key Value Cache) que funciona como uma memória de trabalho contínua de tudo o que foi lido até o momento. Sem o KV Cache o modelo precisaria reprocessar todo o histórico da conversa a cada novo token gerado, portanto essa memória evita que o tempo de resposta cresça de forma exponencial conforme a conversa se prolonga. O Prefill exige rajadas massivas de cálculos matemáticos paralelos sendo limitado por processamento (Compute Bound), de modo que sua velocidade depende estritamente da capacidade bruta de cálculo (FLOPS) do hardware.

Após a conclusão do Prefill o KV Cache é passado para a fase de Decode. Nesta etapa a resposta do modelo é gerada de forma autorregressiva, isto é um token por vez. Em cada passo do Decode o modelo realiza uma passagem direta (forward pass) e produz uma distribuição de probabilidade sobre todo o vocabulário gerando uma lista ranqueada dos possíveis próximos tokens. Assim que um token é selecionado ele é anexado à sequência e o processo se repete. Para gerar cada token o modelo precisa consultar o histórico acumulado no KV Cache e ler todos os seus pesos na memória. Por isso a velocidade do Decode não é limitada pela capacidade de cálculo matemático mas sim pela largura de banda de memória (Memory Bandwidth Bound) ou seja quão rápido os dados conseguem ser transferidos da memória para o processador.

| Fase de Inferência | Modo de Processamento | Principal Recurso Gerado ou Usado | Gargalo de Hardware | Métrica de Desempenho |
|***|***|***|***|***|
| Prefill | Paralelo (lê todo o prompt de uma vez) | Criação do KV Cache | Compute Bound (Processamento Bruto) | Time to First Token (TTFT) |
| Decode | Sequencial (geração token a token) | Consulta ao KV Cache existente | Memory Bandwidth Bound (Largura de Banda) | Inter Token Latency (ITL) |

### 5.7 Métricas de Benchmark, Latência e Síntese do Fluxo

A avaliação do desempenho de um sistema de inferência baseia se em duas métricas principais de latência que medem diretamente a velocidade percebida pelo usuário final. O Time to First Token (TTFT) indica o tempo total transcorrido desde o envio da requisição até o recebimento do primeiro token da resposta pelo usuário refletindo diretamente a eficiência e a duração da fase de Prefill. Já o Inter Token Latency (ITL) indica o tempo decorrido entre a emissão de cada token sucessivo na resposta medindo a velocidade com que cada etapa da fase de Decode é executada. A combinação do TTFT com o ITL compõe a latência total observada nas aplicações de inteligência artificial.

Em síntese o fluxo completo de transformação de um modelo de linguagem estático em uma resposta interativa compreende seis etapas coordenadas: (1) recebimento e tokenização convertendo o texto do prompt em identificadores numéricos. (2) autenticação e roteamento validando a chave e enviando a consulta para a GPU mais adequada pelo Inference Router. (3) agendamento em lote inserindo a requisição em lote contínuo (Continuous Batching) para maximizar a ocupação do hardware. (4) execução do Prefill realizando o processamento paralelo intensivo do prompt e gerando a memória KV Cache. (5) execução do Decode gerando a resposta token por token com consulta ao KV Cache em cada passo. (6) emissão da resposta convertendo os tokens gerados de volta em texto entregue ao usuário em tempo real. Este resumo estendido também está salvo na pasta Questao_05.

## 6. Sistema baseado em regras fuzzy com inferência de Mamdani

Desenvolvemos um sistema de controle nebuloso seguindo a metodologia de Mamdani para regular a velocidade de um ventilador com base em duas variáveis de entrada que são a temperatura ambiente (universo de discurso de 0 a 40 graus Celsius) e a umidade relativa do ar (universo de discurso de 0 a 100 por cento) produzindo como saída a velocidade do motor (universo de 0 a 100 por cento). A implementação está disponível na função fan_mamdani do arquivo prototipos_lista2.py localizado na pasta Questao_06.

| Variável | Conjunto Fuzzy | Função de Pertinência e Parâmetros |
|***|***|***|
| Temperatura (0 a 40 °C) | baixa | Trapezoidal (0, 0, 12, 20) |
| Temperatura (0 a 40 °C) | média | Triangular (15, 24, 32) |
| Temperatura (0 a 40 °C) | alta | Trapezoidal (28, 34, 40, 40) |
| Umidade (0 a 100 %) | baixa | Trapezoidal (0, 0, 25, 50) |
| Umidade (0 a 100 %) | alta | Trapezoidal (40, 65, 100, 100) |
| Velocidade (0 a 100 %) | baixa | Trapezoidal (0, 0, 25, 50) |
| Velocidade (0 a 100 %) | média | Triangular (25, 50, 75) |
| Velocidade (0 a 100 %) | alta | Trapezoidal (50, 75, 100, 100) |

Na etapa de fuzzificação os valores numéricos de entrada são mapeados nos graus de pertinência de cada conjunto. A base de conhecimento utiliza quatro regras Mamdani: Regra 1 define que se a temperatura é baixa e a umidade é baixa então a velocidade é baixa; Regra 2 define que se a temperatura é média e a umidade é baixa então a velocidade é média; Regra 3 estabelece que se a temperatura é alta ou a umidade é alta então a velocidade é alta; Regra 4 estabelece que se a temperatura é média e a umidade é alta então a velocidade é alta. O operador lógico E utiliza o mínimo entre os antecedentes, o operador OU utiliza o máximo, a implicação de cada regra corta o conjunto de saída pelo mínimo e a agregação combina as curvas resultantes pelo operador máximo. Por fim a etapa de defuzzificação calcula o centroide (média ponderada ao longo do domínio discretizado de 0 a 100) fornecendo por exemplo velocidade de 77,5 por cento quando a temperatura vale 34 graus e a umidade vale 65 por cento.

## 7. Sistema de Apoio ao Diagnóstico Médico Baseado em Casos (RBC)

O sistema de raciocínio baseado em casos foi construído com uma base de 15 casos médicos fictícios distribuídos em cinco condições clínicas distintas (gripe, resfriado, alergia, faringite e gastroenterite) abrangendo 12 sintomas observáveis possíveis. Cada caso da base armazena seu código identificador, o conjunto de sintomas observados, o diagnóstico associado e uma orientação geral de cuidado. O código fonte interativo está em Questao_07/sistema_rbc.py acompanhado do módulo Questao_07/prototipos_lista2.py, do script de demonstração Questao_07/demonstracao_q07.py, do arquivo de retenção Questao_07/casos_retidos_demonstracao.json e dos slides de apresentação em Questao_07/apresentacao_demonstracoes.pptx.

O cálculo de similaridade entre o conjunto de sintomas informados pelo paciente A e os sintomas de cada caso armazenado B utiliza o índice de Jaccard definido pela razão entre o tamanho da interseção e o tamanho da união dos dois conjuntos. As quatro etapas fundamentais do ciclo de RBC foram implementadas da seguinte forma: na Recuperação (Retrieve) o sistema percorre os 15 registros calcula a similaridade de Jaccard e retorna os casos mais semelhantes ordenados; na Reutilização (Reuse) os casos recuperados do topo votam ponderados pela similaridade para sugerir o diagnóstico mais compatível e o tratamento de suporte correspondente; na Revisão (Revise) o profissional ou usuário avalia a sugestão podendo confirmar a hipótese ou informar uma correção; e na Retenção (Retain) o novo atendimento validado é gravado em formato JSON para enriquecer consultas futuras.

Em um teste prático com os sintomas febre, tosse e mialgia o sistema recupera no topo o caso C02 (gripe) com similaridade 1,00 seguido pelo caso C10 (gripe com calafrios) com similaridade 0,75 e pelos casos C03 (0,50), C14 (0,50) e C15 (0,50). A etapa de reuso sugere o diagnóstico de gripe com recomendação educacional de repouso hidratação e acompanhamento médico. Após a confirmação na etapa de revisão o caso validado fica salvo em casos_retidos_demonstracao.json. A demonstração visual do funcionamento encontra se nos slides de Questao_07/apresentacao_demonstracoes.pptx.

## 8. Sistema de Diagnóstico Médico Utilizando Redes Bayesianas

Para representar o raciocínio diagnóstico sob incerteza modelamos uma Rede Bayesiana voltada para a avaliação de síndrome gripal contendo cinco variáveis binárias: Exposicao (fator de risco epidemiológico indicando contato recente), Gripe (doença principal a ser diagnosticada) e três sintomas observáveis que são Febre, Tosse e Mialgia. A estrutura causal assume que a exposição prévia influencia a probabilidade de contrair gripe, enquanto a presença ou ausência de gripe condiciona diretamente o surgimento de febre, tosse e dor muscular. Dado o estado da variável Gripe os três sintomas são considerados condicionalmente independentes entre si e também independentes da exposição inicial.

![Diagrama da Rede Bayesiana](figura_rede_bayesiana.png)

| Variável (Nó) | Pais na Rede | Tabela de Probabilidade Condicional (CPT) |
|***|***|***|
| Exposicao | Nenhum | P(Exposicao = sim) = 0,25 ; P(Exposicao = não) = 0,75 |
| Gripe | Exposicao | P(Gripe = sim | Exposicao = sim) = 0,20 ; P(Gripe = sim | Exposicao = não) = 0,04 |
| Febre | Gripe | P(Febre = sim | Gripe = sim) = 0,80 ; P(Febre = sim | Gripe = não) = 0,08 |
| Tosse | Gripe | P(Tosse = sim | Gripe = sim) = 0,70 ; P(Tosse = sim | Gripe = não) = 0,20 |
| Mialgia | Gripe | P(Mialgia = sim | Gripe = sim) = 0,75 ; P(Mialgia = sim | Gripe = não) = 0,05 |

A implementação em Python realiza inferência exata por enumeração sobre a distribuição conjunta fatorada da rede. Partindo das probabilidades a priori sem nenhuma evidência observada a probabilidade marginal inicial da doença é P(Gripe = sim) = 0,25 x 0,20 + 0,75 x 0,04 = 0,0800 (8,00 por cento). Realizamos os experimentos inserindo evidências progressivamente: no Cenário 1 com Febre igual a sim a probabilidade a posteriori sobe para 0,4651 pois a febre é muito mais frequente na presença de gripe do que sem ela; no Cenário 2 acrescentando Tosse igual a sim a probabilidade atualiza para 0,7527; e no Cenário 3 com Febre, Tosse e Mialgia todas positivas a probabilidade a posteriori atinge 0,9786.

Em comparação com sistemas baseados apenas em regras rígidas as Redes Bayesianas oferecem a vantagem de tratar evidências parciais ou incompletas de maneira gradual atualizando a crença diagnóstica sem travar quando falta algum sintoma. Como limitações desta modelagem didática destacam se o uso de variáveis estritamente binárias a presença de uma única doença alvo e a suposição de independência condicional entre todos os sintomas. Para tornar o modelo mais realista em ambiente clínico seria indicado acrescentar diagnósticos diferenciais como resfriado e alergia, incluir variáveis de faixa etária e vacinação e calibrar as tabelas com dados epidemiológicos reais. Todos os arquivos código diagrama e a apresentação em slides Questao_08/apresentacao_demonstracoes.pptx estão na pasta Questao_08.

## 9. Sistema de Recomendação Baseado em Ontologias (OWL 2.0)

Escolhemos o domínio de recomendação de livros em uma biblioteca digital e desenvolvemos uma ontologia formal em OWL 2.0 armazenada nos arquivos recomendacao.owl (formato RDF/XML compatível com Protégé) e recomendacao.owl.ttl dentro da pasta Questao_09. A modelagem cumpre todos os requisitos mínimos contendo 11 classes (Livro, Ficcao, Ciencia, Fantasia, Leitor, Interesse, Autor, Editora, Idioma, Formato e Disponibilidade) organizadas hierarquicamente com Fantasia subclasse de Ficcao e ambas subclasses de Livro bem como Ciencia subclasse de Livro.

Foram definidas 15 propriedades sendo 10 propriedades de objeto (temInteresse, temGenero, escritoPor, publicadoPor, formato, idioma, leu, favoritou, recomendadoPara e disponivelEm) e 5 propriedades de dados (publicadoEm, idadeMinima, avaliacao, nomeAutor e titulo) acompanhadas de axiomas de domínio alcance e restrições existenciais e universais que exigem por exemplo que todo leitor possua algum interesse associado e que todo livro tenha título e formato válido. Na base de indivíduos cadastramos leitores como Ana (que tem interesse em Fantasia) e Bob (interesse em Ciencia), além das obras F1 intitulada A Ilha das Brumas (instância de Fantasia em formato Digital) e C1 intitulada O Universo em Escala (instância de Ciencia em formato Impresso).

O sistema de recomendação implementado em Questao_09/prototipos_lista2.py e executado por Questao_09/demonstracao_q09.py utiliza a biblioteca Owlready2 integrada ao motor de raciocínio HermiT. Ao carregar recomendacao.owl e acionar o reasoner HermiT o sistema verifica automaticamente a consistência lógica da ontologia e realiza a classificação automática dos indivíduos deduzindo que o indivíduo F1 por pertencer à classe Fantasia também é instância implícita das superclasses Ficcao e Livro. Quando o usuário informa o perfil de Ana o mecanismo consulta as classes inferidas pelo reasoner e recomenda a obra F1 apresentando como justificativa o vínculo semântico entre o interesse declarado e a hierarquia deduzida. A apresentação do funcionamento está disponível em Questao_09/apresentacao_demonstracoes.pptx.

## 10. Planejamento de rotas para entregas urbanas (BFS, DFS, UCS e A*)

Na formulação clássica deste problema de busca os estados correspondem às nove localidades do mapa {A, B, C, D, E, F, G, H, I}, sendo o estado inicial a origem A e o teste de objetivo verificar se o agente chegou ao destino I. As ações disponíveis em cada estado consistem em percorrer qualquer trecho adjacente existente no grafo não direcionado, a função de transição retorna a localidade vizinha alcançada pela aresta escolhida e a função de custo soma os tempos de deslocamento em minutos definidos na tabela do problema.

Como o enunciado menciona Busca em Profundidade junto com a sigla BFS apresentamos tanto a busca em profundidade (DFS) quanto a busca em largura (BFS) adotando desempate em ordem alfabética e controle de estados visitados. Na Busca em Profundidade (DFS) a ordem de expansão segue o ramo mais profundo primeiro visitando A, B, C, F, E, D, G, H até alcançar I, o que produz a rota A para B para C para F para E para D para G para H para I com custo total de 29 minutos. Já na Busca em Largura (BFS) a exploração ocorre nível por nível na ordem A, B, D, C, E, G, F, H chegando ao objetivo I pela rota A para B para C para F para I com custo total de 4 + 5 + 2 + 4 = 15 minutos.

Na Busca de Custo Uniforme (UCS) a fronteira é expandida pelo menor custo acumulado g(n). A ordem de expansão percorre A (g=0), D (g=3), B (g=4), E via B (g=6), C (g=9), F via E (g=9), G (g=9) e H via E (g=11), alcançando I pelo caminho ótimo A para B para E para H para I (ou equivalentemente A para B para E para F para I) com custo total mínimo de 13 minutos. Na busca informada A* utilizamos a função de avaliação f(n) = g(n) + h(n) com a heurística fornecida no enunciado:

| Nó Expandido ou Avaliado | g(n) | h(n) | f(n) = g(n) + h(n) | Observação no Algoritmo A* |
|***|***|***|***|***|
| A | 0 | 10 | 10 | Estado inicial expandido primeiro |
| B | 4 | 8 | 12 | Gerado a partir de A; expandido por desempate alfabético com D |
| D | 3 | 9 | 12 | Gerado a partir de A; caminho por D até E teria g=7 pior que via B |
| E | 6 | 6 | 12 | Alcançado via B com g=6; gera F (f=13) e H (f=13) |
| F | 9 | 4 | 13 | Alcançado via E; gera o destino I com g=13 e f=13 |
| H | 11 | 2 | 13 | Alcançado via E; também alcança I com g=13 e f=13 |
| I | 13 | 0 | 13 | Objetivo selecionado com custo ótimo de 13 minutos |

| Algoritmo | Custo da Solução | Nós Expandidos antes de I | Completo? | Ótimo? |
|***|***|***|***|***|
| Busca em Profundidade (DFS) | 29 min | 8 nós expandidos | Sim (em grafo finito com visitados) | Não |
| Busca em Largura (BFS) | 15 min | 8 nós expandidos | Sim (em grafo finito) | Não para custos variados nas arestas |
| Custo Uniforme (UCS) | 13 min | 8 nós expandidos | Sim (custos positivos) | Sim |
| Busca A* | 13 min | 6 nós expandidos | Sim | Sim (heurística admissível e consistente) |

Para a modificação que obriga o entregador a passar por D e por F antes de chegar a I em qualquer ordem propomos uma nova representação de estado na forma da tripla (localidade_atual, visitou_D, visitou_F) onde os dois últimos componentes são valores booleanos. O estado inicial passa a ser (A, Falso, Falso), a função de transição atualiza os marcadores para Verdadeiro sempre que o agente passa por D ou por F e o teste de objetivo passa a exigir o estado (I, Verdadeiro, Verdadeiro). Executando a busca de menor custo nesse espaço de estados ampliado encontramos a rota ótima A para D para E para F para I com custo total de 3 + 4 + 3 + 4 = 14 minutos. A resolução individual está na pasta Questao_10.

## 11. Comparação entre Agentes Inteligentes Clássicos e Agentes baseados em LLMs

Na concepção clássica de agentes inteligentes apresentada no Capítulo 2 de Russell e Norvig o projeto do agente parte de uma definição formal dos perceptos das ações do estado interno e da função de transição ou utilidade que guia a tomada de decisão. Considerando o cenário do assistente acadêmico para organizar o expediente do professor das 14h às 18h o agente clássico recebe as tarefas já estruturadas em campos fixos (duração em minutos, nível de prioridade e prazo) verifica as restrições temporais rígidas como a reunião de pesquisa C fixada das 16h às 17h e aloca as atividades sem permitir sobreposição nem quebra de tarefas indivisíveis. Essa abordagem garante previsibilidade e correção matemática no cumprimento das restrições mas exige que toda entrada seja previamente traduzida para estruturas formais.

Por sua vez o agente baseado em Grandes Modelos de Linguagem (LLMs) recebe o pedido diretamente em linguagem natural livre, exatamente como o professor falaria no dia a dia: Preciso preparar uma aula de Inteligência Artificial corrigir trabalhos de alunos e participar de uma reunião de pesquisa. O LLM atua interpretando a intenção do texto extraindo os parâmetros das tarefas para uma estrutura JSON e gerando explicações compreensíveis para o usuário. Na arquitetura implementada na pasta Questao_11 combinamos o modelo local qwen3:4b via Ollama com o verificador temporal determinístico em Python demonstrando a comparação prática entre Questao_11/agente_classico.py e Questao_11/demonstracao_q11.py além dos slides em Questao_11/apresentacao_demonstracoes.pptx.

Respondendo diretamente à questão proposta: um agente baseado em LLM oferece claras vantagens quando a entrada é aberta ambígua ou em linguagem natural quando é necessário integrar instruções textuais variadas dialogar para pedir esclarecimentos ao usuário ou redigir justificativas em linguagem acessível. Entretanto capacidades como verificação exata de restrições temporais e de recursos, garantia de ausência de conflitos na agenda, otimização combinatória de utilidade e manutenção rigorosa da consistência de estado ainda dependem fortemente de mecanismos explícitos de raciocínio planejamento e verificação algorítmica, visto que modelos generativos puros podem sofrer alucinações numéricas ou violar restrições duras.

| Horário Planejado | Atividade Alocada | Duração e Prioridade | Justificativa da Decisão |
|***|***|***|***|
| 14h00 às 15h30 | A: Preparar aula de IA | 90 min (Prioridade Alta, prazo hoje) | Alocada no primeiro bloco disponível por vencer hoje e ser urgente |
| 15h30 às 16h00 | Janela livre de transição | 30 min | Nenhuma tarefa pendente cabe em apenas 30 minutos contínuos |
| 16h00 às 17h00 | C: Reunião de pesquisa | 60 min (Prioridade Alta, horário fixo) | Compromisso fixo obrigatório das 16h às 17h respeitado |
| 17h00 às 18h00 | D: Revisar artigo | 60 min (Prioridade Baixa, próxima semana) | Aproveita a hora final disponível de 60 minutos exatos |

A atividade B (Corrigir trabalhos, 120 minutos, prioridade média e prazo amanhã) não pode ser iniciada hoje porque exige duas horas contínuas e a janela das 14h às 16h já é ocupada pela preparação urgente da aula A (90 minutos) enquanto a reunião fixa C bloqueia o horário das 16h às 17h restando apenas 60 minutos ao final da tarde. Por isso o plano transfere justificadamente a correção B para o dia seguinte cumprindo seu prazo até amanhã e maximizando a utilidade das tarefas entregues hoje.

## 12. Especificação e desenvolvimento de aplicação de agente baseado em LLM

Desenvolvemos um aplicativo completo de assistente inteligente para planejamento acadêmico disponível na pasta Questao_12 no arquivo Questao_12/agente_llm.py junto com o módulo de escalonamento Questao_12/prototipos_lista2.py. A aplicação foi projetada em três módulos integrados que atendem aos componentes exigidos no enunciado: interface em linguagem natural, etapa de inferência e componente de explicabilidade.

Na interface de usuário em linguagem natural o programa solicita via terminal que o usuário descreva livremente suas tarefas durações prioridades e prazos bem como o intervalo de trabalho disponível e eventuais compromissos de horário fixo. Em seguida o módulo de inferência se conecta ao servidor local Ollama (utilizando por padrão o modelo qwen3:4b na porta 11434 ou qualquer endpoint compatível configurado por variável de ambiente) enviando um prompt estruturado que extrai as entidades do texto para objetos JSON validados e aciona o algoritmo de planejamento temporal para montar o cronograma livre de conflitos. Caso alguma tarefa não tenha duração ou prazo informados no texto o sistema não inventa valores e sinaliza a pendência.

Por fim o módulo de explicabilidade apresenta ao usuário tanto o cronograma detalhado minuto a minuto quanto a lista de atividades que não puderam ser alocadas na janela acompanhada do motivo exato de cada decisão (como falta de bloco contínuo suficiente ou conflito com compromisso fixo) esclarecendo qual parte foi interpretada pelo modelo de linguagem e qual parte foi validada pelo planejador determinístico.

## 13. Ensaio sobre a arquitetura Transformers

### 13.1 Introdução e Transição das Sequências para a Atenção

O Transformer é a arquitetura por trás de quase todos os grandes modelos de linguagem atuais como GPT, Claude, Gemini, Llama e BERT. Foi proposto em 2017 por Vaswani e colegas no artigo Attention Is All You Need com uma ideia ousada: abandonar redes recorrentes e convolucionais e deixar que um único mecanismo, a atenção, decida quais partes do texto importam para cada palavra. Este ensaio apresenta os conceitos essenciais da arquitetura e em seguida acompanha uma frase concreta ao longo do modelo mostrando o que acontece entre a entrada do texto e a previsão da próxima palavra.

Antes do Transformer o padrão para processamento de linguagem natural eram as redes recorrentes (RNN, LSTM e GRU), que leem o texto token a token e carregam um estado oculto responsável por resumir tudo o que foi lido até aquele ponto. Isso trazia dois problemas graves: a informação distante se diluía ao longo da sequência e o treinamento não podia ser paralelizado pois cada passo dependia do cálculo do passo anterior. O mecanismo de atenção introduzido para tradução automática por Bahdanau e colegas em 2014 permitia ao modelo olhar de volta para posições anteriores em vez de depender só de um vetor resumo. O Transformer levou essa ideia ao limite ao processar toda a sequência de uma só vez fazendo cada posição consultar diretamente todas as outras, de modo que dependências longas ficam a um passo de distância e o treinamento aproveita todo o paralelismo das GPUs.

### 13.2 Conceitos Principais da Arquitetura

O funcionamento da arquitetura apoia se em dez componentes fundamentais que operam em conjunto:

1. Tokenização e Embeddings: o texto de entrada é dividido em tokens (palavras ou subpalavras) e cada token recebe um número inteiro de um vocabulário fixo. Em seguida cada identificador é mapeado para um vetor denso de números reais (512 dimensões no artigo original), posicionando palavras de uso parecido próximas nesse espaço vetorial.

2. Codificação posicional: como a operação de atenção por si só não distingue a ordem das palavras soma se ao embedding um vetor que informa a posição de cada token na frase, utilizando funções de seno e cosseno no modelo original ou variantes rotacionais como RoPE em modelos recentes.

3. Autoatenção (Self Attention): cada token gera três vetores por meio de projeções lineares aprendidas que são a consulta (Query, Q), a chave (Key, K) e o valor (Value, V). A consulta de um token é comparada por produto escalar com as chaves de todos os tokens, os resultados são divididos pela raiz quadrada da dimensão das chaves (raiz de dk) para evitar saturação e normalizados pela função softmax gerando pesos que misturam os vetores de valor V: Atenção(Q, K, V) = softmax(Q . K^T / raiz(dk)) . V.

4. Atenção multicabeça e Máscara causal: em vez de calcular uma única atenção o modelo executa várias cabeças em paralelo (8 no original) permitindo que uma cabeça capture relações sintáticas enquanto outra foca em referências a entidades para depois concatenar e projetar os resultados. Nos modelos geradores aplica se também uma máscara causal que impede cada posição de atender a tokens futuros durante o treinamento.

5. Rede feed forward, conexões residuais, normalização e camada de saída: após a atenção cada posição passa individualmente por duas camadas lineares com ativação não linear. Cada subcamada utiliza conexão residual (somando a entrada à saída) seguida de normalização de camada para estabilizar redes profundas empilhadas em dezenas de blocos. Ao final o vetor da última posição passa por uma projeção linear do tamanho do vocabulário e por um softmax que fornece a distribuição de probabilidade da próxima palavra.

### 13.3 Funcionamento Passo a Passo com Exemplo Concreto

Considere um modelo gerador do tipo GPT que recebe o prompt O banco aprovou o e precisa prever a próxima palavra. Primeiro ocorre a tokenização dividindo a frase em quatro tokens: O, banco, aprovou, o. Cada token é convertido em seu vetor de embedding somado à respectiva codificação posicional (posições 1, 2, 3 e 4). Nesse instante inicial o vetor da palavra banco ainda é ambíguo pois isoladamente pode representar tanto uma instituição financeira quanto um assento.

Ao entrar na autoatenção da primeira camada cada token projeta seus vetores Q, K e V e compara sua consulta com as chaves anteriores respeitando a máscara causal. Para o verbo aprovou a atenção atribuída à chave de banco é elevada porque banco exerce o papel de sujeito da ação. Com a mistura dos vetores de valor V a representação de aprovou incorpora características de banco e nas camadas seguintes o contexto do verbo aprovar desloca a representação de banco para o sentido financeiro desfazendo a ambiguidade inicial. Na última posição o token o consulta todo o contexto acumulado distribuindo seus pesos de atenção de forma ilustrativa conforme a tabela abaixo:

| Token Atendido no Contexto | Peso de Atenção (Softmax) | Papel Semântico Capturado |
|***|***|***|
| O | 0,05 | Artigo inicial com baixo peso informativo direto |
| banco | 0,25 | Sujeito que estabelece o domínio financeiro da frase |
| aprovou | 0,60 | Verbo transitivo que exige um objeto compatível com aprovação |
| o | 0,10 | Artigo masculino singular que antecede o substantivo esperado |

Os pesos somam 1,00 conforme garantido pelo softmax. O vetor atualizado do último token o passa então pela rede feed forward pelas conexões residuais e pela normalização ao longo de toda a pilha de camadas saindo com uma representação rica que indica a expectativa de um substantivo masculino ligado a aprovação bancária. Na camada de saída a projeção sobre o vocabulário seguida de softmax atribui probabilidades altas para palavras como empréstimo (41 por cento), pedido (18 por cento), crédito (12 por cento) e projeto (6 por cento). Selecionado o token empréstimo ele é anexado à frase formando O banco aprovou o empréstimo e o ciclo recomeça de modo autorregressivo.

### 13.4 Treinamento, Inferência, Variantes e Conclusão

No treinamento o modelo ajusta seus pesos minimizando a entropia cruzada entre a distribuição prevista e o próximo token real para todas as posições da frase simultaneamente graças à máscara causal. Na inferência a geração ocorre um token por vez guardando se os vetores K e V já calculados no KV Cache para evitar retrabalho. A partir da arquitetura original surgiram três famílias principais: modelos somente codificador como BERT voltados para classificação e busca bidirecional; modelos somente decodificador como GPT, Claude e Llama voltados para geração textual; e modelos codificador e decodificador como T5 aplicados em tradução e sumarização. Embora o custo quadrático da atenção em relação ao tamanho do contexto ainda exija otimizações como FlashAttention e atenção esparsa o Transformer consolidou se por unir expressividade contextual direta e alto paralelismo de treinamento. O texto deste ensaio encontra se também na pasta Questao_13.

## 14. Knowledge Graph: representação, inferência, aprendizagem e aplicação

Um Grafo de Conhecimento (Knowledge Graph ou KG) estrutura informações complexas na forma de triplas relacionais (sujeito, predicado, objeto) onde os nós representam entidades do mundo real ou conceitos e as arestas representam relações semânticas tipadas, como na tripla (Marie Curie, descobriu, Polonio). Para manter a coerência quando dados de várias origens são integrados o grafo costuma apoiar se em um esquema ou vocabulário que define os tipos válidos de nós as propriedades permitidas e as restrições de domínio e alcance.

A inferência sobre um Knowledge Graph permite descobrir fatos novos que não estavam explícitos na base original percorrendo caminhos relacionais e aplicando regras lógicas ou hierarquias de tipos. Por exemplo se o grafo registra que Marie Curie pertence ao tipo Cientista e o esquema define que todo Cientista é um Pesquisador o motor deduz que ela também é pesquisadora; de modo semelhante regras de composição de caminho permitem inferir relações indiretas e checagens de domínio ajudam a apontar arestas contraditórias. Já os métodos de aprendizagem de máquina atuam tanto na construção quanto no completamento do grafo: técnicas de processamento de linguagem natural extraem novas entidades e relações a partir de textos brutos enquanto modelos de representação vetorial (Knowledge Graph Embeddings como TransE, DistMult e redes neurais em grafos) aprendem vetores para nós e arestas a fim de prever conexões ausentes (link prediction) e alinhar entidades equivalentes.

Uma aplicação prática bastante consolidada é o uso de Grafos de Conhecimento em motores de busca e recomendação cultural como o Google Knowledge Graph ou bases em Neo4j para plataformas de filmes. Em um grafo audiovisual que conecta usuários, filmes, diretores, atores e gêneros através de arestas como assistiu, atuouEm, dirigiu e temGenero a inferência por regras de caminho pode operar com a cláusula: se gostou(Usuario, Filme1) e temGenero(Filme1, Genero) e dirigiu(Diretor, Filme1) e dirigiu(Diretor, Filme2) e temGenero(Filme2, Genero) então recomendar(Usuario, Filme2). Dessa maneira o sistema não apenas deduz uma recomendação altamente relevante como também consegue exibir o caminho percorrido no grafo como explicação transparente para o usuário. O arquivo individual desta questão está na pasta Questao_14.

## 15. Aplicação de Ontologia com OWL 2.0 e raciocínio no Protégé

Para demonstrar de forma completa uma aplicação baseada em OWL 2.0 com foco em representação do conhecimento e raciocínio automático utilizamos a ontologia de recomendação de livros recomendacao.owl (e sua versão em sintaxe Turtle recomendacao.owl.ttl) organizada na pasta Questao_15 junto com o script de inferência Questao_15/demonstracao_q15.py e os slides em Questao_15/apresentacao_demonstracoes.pptx. O domínio modela uma livraria e biblioteca digital onde leitores possuem perfis de interesse literário e obras possuem gêneros, formatos, idiomas, autores e restrições formais.

A representação do conhecimento em OWL 2.0 explora axiomas de subclasse (Fantasia subclasse de Ficcao e Ficcao subclasse de Livro; Ciencia subclasse de Livro), axiomas de domínio e alcance nas 15 propriedades definidas e restrições de quantificação existencial (owl:someValuesFrom garantindo que todo indivíduo da classe Leitor tenha pelo menos um interesse e que todo Livro possua título) e universal (owl:allValuesFrom garantindo que a propriedade formato de um Livro aponte somente para indivíduos da classe Formato).

Quando abrimos o arquivo recomendacao.owl na ferramenta Protégé (ou executamos o script demonstracao_q15.py que aciona o mesmo motor HermiT via Owlready2) e selecionamos o reasoner HermiT clicando em Start reasoner a máquina de inferência realiza três tarefas essenciais: primeiro valida a consistência global da ontologia confirmando que nenhum indivíduo viola as restrições de domínio alcance ou quantificação; segundo executa a classificação taxonômica deduzindo que o livro F1 (A Ilha das Brumas), declarado apenas como instância de Fantasia, pertence automaticamente às classes superiores Ficcao e Livro; e terceiro apoia a consulta semântica de recomendação associando o interesse de Ana em Fantasia aos indivíduos classificados nessa categoria. A pasta Questao_15 contém todos os arquivos necessários e a apresentação em slides.

## Organização das Pastas na Entrega

Cada questão possui sua própria pasta independente (Questao_01 até Questao_15) contendo a resposta individual e todos os códigos bases ontologias diagramas e apresentações em slides (.pptx) correspondentes.
