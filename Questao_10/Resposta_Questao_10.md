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
