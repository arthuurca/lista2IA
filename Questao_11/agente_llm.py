"""Assistente CLI de planejamento acadêmico com endpoint compatível com Chat Completions.

Usa Ollama local por padrão (qwen3:4b). Para outro endpoint, defina LLM_API_KEY,
LLM_MODEL e opcionalmente LLM_BASE_URL no ambiente.
O modelo extrai tarefas; o planejador local aplica horários e conflitos.
"""
import json, os, urllib.request
from prototipos_lista2 import schedule

def interpret_request(text,fixed=()):
    """Converte linguagem natural em tarefas estruturadas via endpoint configurado."""
    key=os.getenv("LLM_API_KEY","ollama")
    model=os.getenv("LLM_MODEL","qwen3:4b")
    base=os.getenv("LLM_BASE_URL","http://localhost:11434/v1").rstrip("/")
    fixed_text="; ".join(f"{name} fixo das {a//60:02d}:{a%60:02d} às {b//60:02d}:{b%60:02d} (não incluir como tarefa)" for a,b,name in fixed) or "nenhum"
    prompt=("Extraia somente as tarefas flexíveis da solicitação. Preserve o identificador e a descrição da tarefa no campo name. "
            "Retorne apenas JSON com a chave tasks; cada tarefa tem "
            "name, duration (minutos inteiro), priority (1 baixa a 3 alta), deadline (0 hoje, 1 amanhã, "
            "2 depois), e reason (justificativa curta baseada nos dados fornecidos). Não invente duração ou prazo; "
            "use 'confirmar duração/prazo' somente quando o dado estiver realmente ausente e não inclua essa tarefa no plano. "
            "Se o dado estiver explícito, copie-o sem pedir confirmação. Compromissos fixos não devem ser incluídos "
            "como tarefas nem movidos: "+fixed_text+". Solicitação: "+text)
    body_data={"model":model,"messages":[{"role":"user","content":prompt}],"response_format":{"type":"json_object"}}
    if "localhost:11434" in base or "127.0.0.1:11434" in base:
        body_data["reasoning_effort"]="none"  # extração simples não precisa de cadeia de raciocínio longa
    body=json.dumps(body_data).encode()
    req=urllib.request.Request(base+"/chat/completions",data=body,headers={"Authorization":"Bearer "+key,"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=300) as res: result=json.loads(res.read().decode())
    return json.loads(result["choices"][0]["message"]["content"]).get("tasks",[])

def minute_label(m): return f"{m//60:02d}:{m%60:02d}"

def main():
    print("Descreva suas tarefas e restrições em linguagem natural.")
    request=input("> ")
    start=int(input("Início da janela (hora cheia, ex. 14): "))*60
    end=int(input("Fim da janela (hora cheia, ex. 18): "))*60
    fixed=[]
    if input("Há compromisso fixo? (s/n): ").strip().lower()=="s":
        a=int(input("Hora inicial: "))*60; b=int(input("Hora final: "))*60
        fixed=[(a,b,input("Nome do compromisso: "))]
    tasks=interpret_request(request,fixed)
    plan,skipped=schedule(tasks,start,end,fixed)
    print("\nPlano proposto (confirme antes de usar):")
    for a,b,name in plan: print(f"{minute_label(a)}-{minute_label(b)}  {name}")
    if skipped:
        print("\nNão agendadas:")
        for name,why in skipped: print(f"- {name}: {why}")
    print("\nExplicação: o modelo estruturou o pedido; a checagem de duração e conflitos foi feita pelo planejador local.")
    print("Revise a extração e os horários. Nenhum compromisso é enviado a calendário.")

if __name__=="__main__": main()
