"""Executa demonstração reproduzível da Ontologia OWL 2 + HermiT (Questão 9)."""
from pathlib import Path
import json
from prototipos_lista2 import owl_inference_summary

OUT = Path(__file__).resolve().parent
lines = []
def say(s=""): lines.append(str(s))

say("DEMONSTRAÇÃO — QUESTÃO 9: OWL 2 + HermiT")
summary = owl_inference_summary(str(OUT / "recomendacao.owl"))
say(f"Consistência: {'consistente' if summary['consistente'] else 'inconsistente'}")
say("Tipos inferidos para F1: " + ", ".join(summary["tipos_F1"]))
say("Recomendação para Fantasia: " + json.dumps(summary["recomendacao_Ana"], ensure_ascii=False))
say("Mecanismo: Owlready2 executa HermiT; a consulta filtra os indivíduos por tipo inferido e formato.")
say("Requer Java e `pip install -r requirements.txt`.")

text = "\n".join(lines) + "\n"
print(text)
