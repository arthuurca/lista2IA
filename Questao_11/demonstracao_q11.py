"""Compara baseline estruturado e extração LLM local no mesmo cenário."""
from pathlib import Path
import json
from agente_classico import plan_today, FIXED, TASKS
from agente_llm import interpret_request, minute_label
from prototipos_lista2 import schedule

OUT=Path(__file__).resolve().parent
fixed=FIXED
request=("Organize estas atividades acadêmicas para hoje: A, preparar aula de Inteligência Artificial, "
         "90 minutos, prioridade alta, vence hoje; B, corrigir trabalhos, 120 minutos, prioridade média, "
         "vence amanhã; D, revisar artigo, 60 minutos, prioridade baixa, vence na próxima semana. "
         "Minha janela de trabalho é das 14h às 18h.")
classic,classic_skipped=plan_today()
tasks=interpret_request(request,fixed)
llm_plan,llm_skipped=schedule(tasks,14*60,18*60,fixed)
lines=["QUESTÃO 11 — DEMONSTRAÇÃO COMPARATIVA", "", "1) Baseline clássico: entrada estruturada"]
for a,b,name in sorted(classic+fixed): lines.append(f"{minute_label(a)}–{minute_label(b)}  {name}")
lines.append("Não agendada: B — corrigir trabalhos; duração contínua de 120 min não cabe hoje sem conflitar com C. Transferir para amanhã, antes do prazo.")
lines += ["", "2) Agente baseado em LLM: interpretação local via Ollama / qwen3:4b", "Pedido em linguagem natural:", request, "", "Tarefas estruturadas pelo LLM:", json.dumps(tasks,ensure_ascii=False,indent=2), "", "Plano calculado e verificado localmente:"]
for a,b,name in llm_plan: lines.append(f"{minute_label(a)}–{minute_label(b)}  {name}")
if llm_skipped:
 lines.append("Não agendadas:")
 lines.extend(f"- {name}: {why}; conferir e reagendar antes do prazo." for name,why in llm_skipped)
lines += ["", "Comparação: o baseline recebe tarefas estruturadas; o LLM interpreta linguagem natural. Os dois usam o planejador local para checar intervalos e conflitos. A saída do LLM precisa de revisão humana, principalmente se a extração de prazos/durações divergir do pedido."]
text="\n".join(lines)+"\n"
print(text)
