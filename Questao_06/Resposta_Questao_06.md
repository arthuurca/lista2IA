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
