"""Baseline clássico: recebe dados estruturados e agenda com regras explícitas."""
from prototipos_lista2 import schedule
TASKS=[
 {"name":"A — preparar aula de IA","duration":90,"priority":3,"deadline":0,"reason":"alta prioridade; vence hoje"},
 {"name":"B — corrigir trabalhos","duration":120,"priority":2,"deadline":1,"reason":"prioridade média; vence amanhã"},
 {"name":"D — revisar artigo","duration":60,"priority":1,"deadline":2,"reason":"baixa prioridade; vence na próxima semana"},
]
FIXED=[(16*60,17*60,"C — reunião de pesquisa")]
def plan_today(): return schedule(TASKS,14*60,18*60,FIXED)
if __name__=="__main__":
 plan,skipped=plan_today()
 print("Baseline clássico (entrada estruturada):")
 for start,end,name in sorted(plan+FIXED): print(f"{start//60:02d}:{start%60:02d}-{end//60:02d}:{end%60:02d}  {name}")
 print("Não agendadas:")
 for name,reason in skipped: print(f"- {name}: {reason}; transferida para amanhã, antes do prazo")
