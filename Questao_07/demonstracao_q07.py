"""Executa demonstração reproduzível do ciclo de RBC (Questão 7)."""
from pathlib import Path
from prototipos_lista2 import CASES, case_report, revise_case, retain_case

OUT = Path(__file__).resolve().parent
lines = []
def say(s=""): lines.append(str(s))

say("DEMONSTRAÇÃO — QUESTÃO 7: RBC")
symptoms = {"febre", "tosse", "mialgia"}
report = case_report(symptoms)
say("Consulta: febre, tosse, mialgia")
say(f"Base: {len(CASES)} casos; {len({c['diagnostico'] for c in CASES})} categorias")
say("Retrieve / Reuse — casos mais próximos:")
for score, case in report["casos_proximos"]:
    say(f"  {case['id']} | Jaccard={score:.2f} | diagnóstico={case['diagnostico']} | sintomas={', '.join(sorted(case['sintomas']))}")
say(f"Hipótese: {report['hipotese']}")
say(f"Conduta de suporte associada: {report['tratamento_recomendado']}")
review = revise_case(symptoms, validated_label="gripe")
say(f"Revise: hipótese confirmada pelo revisor? {not review['corrigido']}; diagnóstico validado={review['diagnostico_validado']}")
retained = OUT / "casos_retidos_demonstracao.json"
if retained.exists():
    retained.unlink()
retain_case(retained, symptoms, review["diagnostico_validado"])
say(f"Retain: registro validado gravado em {retained.name}")
say("Nota: dados e conduta são fictícios e não substituem avaliação médica.")

text = "\n".join(lines) + "\n"
print(text)
