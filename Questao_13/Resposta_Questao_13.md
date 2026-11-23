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
