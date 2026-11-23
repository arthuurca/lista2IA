"""Executa demonstração reproduzível da Rede Bayesiana (Questão 8)."""
from pathlib import Path
from prototipos_lista2 import bayes_flu

OUT = Path(__file__).resolve().parent
lines = []
def say(s=""): lines.append(str(s))

say("DEMONSTRAÇÃO — QUESTÃO 8: REDE BAYESIANA")
scenarios = [
    ("sem evidência", {}),
    ("febre=sim", {"febre": True}),
    ("febre=sim, tosse=sim", {"febre": True, "tosse": True}),
    ("febre=sim, tosse=sim, mialgia=sim", {"febre": True, "tosse": True, "mialgia": True}),
]
prior = bayes_flu({})
say(f"P(Gripe) a priori = {prior:.4f}")
previous = prior
for label, evidence in scenarios:
    posterior = bayes_flu(evidence)
    say(f"Evidência: {label:38s} | prior de referência={previous:.4f} | posterior P(Gripe|e)={posterior:.4f}")
    if label != "sem evidência":
        say(f"  Interpretação: nesta rede didática, a evidência altera a probabilidade em {posterior - previous:+.4f} em relação ao cenário anterior.")
    previous = posterior
say("Valores condicionais são hipóteses educacionais; a rede não faz diagnóstico real.")

text = "\n".join(lines) + "\n"
print(text)
