"""Protótipos didáticos da Lista 2; Owlready2 é necessário para executar HermiT."""
from itertools import product
from pathlib import Path
import csv, json, re

# Q2: KNN categórico com distância de Hamming.
def knn_hamming(train, query, k=3, target="Risco"):
    attrs=[c for c in train[0] if c!=target]
    near=sorted((sum(r[a]!=query[a] for a in attrs),i,r[target]) for i,r in enumerate(train))[:k]
    votes={}
    for _,_,y in near: votes[y]=votes.get(y,0)+1
    return min(votes,key=lambda y:(-votes[y],y)),near

def load_credit(path):
    with open(path,encoding="utf-8-sig",newline="") as f: return list(csv.DictReader(f))

# Q6: pertinências triangulares/trapezoidais, regras Mamdani, máximo/mínimo e centroide.
def tri(x,a,b,c):
    if x<=a or x>=c:return 0.
    if x==b:return 1.
    return (x-a)/(b-a) if x<b else (c-x)/(c-b)
def trap(x,a,b,c,d):
    if x<a or x>d:return 0.
    if b<=x<=c:return 1.
    if x<b:return 1. if a==b else (x-a)/(b-a)
    return 1. if c==d else (d-x)/(d-c)
def fan_mamdani(temp,humidity):
    t={"low":trap(temp,0,0,12,20),"mid":tri(temp,15,24,32),"high":trap(temp,28,34,40,40)}
    h={"low":trap(humidity,0,0,25,50),"high":trap(humidity,40,65,100,100)}
    xs=range(101); out=[]
    for x in xs:
        mu={"low":trap(x,0,0,25,50),"mid":tri(x,25,50,75),"high":trap(x,50,75,100,100)}
        rules=[(min(t['low'],h['low']),'low'),(min(t['mid'],h['low']),'mid'),(max(t['high'],h['high']),'high'),(min(t['mid'],h['high']),'high')]
        out.append(max(min(v,mu[label]) for v,label in rules))
    return sum(x*y for x,y in zip(xs,out))/sum(out) if sum(out) else 0.

# Q7: quinze casos sintéticos; cada registro contém sintomas, diagnóstico e conduta.
SUPPORTIVE_TREATMENTS={"resfriado":"repouso e hidratação; procurar avaliação se houver piora ou persistência", "gripe":"repouso e hidratação; avaliação profissional, especialmente em pessoas de risco", "alergia":"reduzir exposição ao possível alérgeno e buscar orientação profissional", "faringite":"avaliação profissional, sobretudo com febre alta ou dificuldade para engolir", "gastroenterite":"manter hidratação e buscar avaliação se houver sinais de desidratação ou sintomas intensos"}
CASE_SEED=[("resfriado",{"coriza","tosse","garganta"}),("gripe",{"febre","tosse","mialgia"}),("gripe",{"febre","mialgia","garganta"}),("alergia",{"coriza","espirros","coceira"}),("faringite",{"garganta","febre","odinofagia"}),("gastroenterite",{"nausea","vomito","diarreia"}),("resfriado",{"coriza","tosse","espirros"}),("alergia",{"coriza","espirros","coceira","tosse"}),("faringite",{"garganta","odinofagia","febre"}),("gripe",{"febre","tosse","mialgia","calafrios"}),("resfriado",{"coriza","garganta","tosse"}),("gastroenterite",{"nausea","vomito","diarreia","febre"}),("alergia",{"coriza","espirros","coceira"}),("faringite",{"garganta","febre","tosse"}),("gripe",{"febre","mialgia","calafrios"})]
CASES=[{"id":f"C{i:02d}","diagnostico":d,"sintomas":s,"tratamento_recomendado":SUPPORTIVE_TREATMENTS[d]} for i,(d,s) in enumerate(CASE_SEED,1)]
def jaccard(a,b): return len(a&b)/len(a|b) if a|b else 1.
def retrieve_cases(symptoms,k=3): return sorted(((jaccard(set(symptoms),c["sintomas"]),c) for c in CASES),key=lambda item:(-item[0],item[1]["id"]))[:k]
def propose_case_diagnosis(symptoms,k=5):
    near=retrieve_cases(symptoms,k=k); scores={}
    for score,case in near:d=case["diagnostico"]; scores[d]=scores.get(d,0)+score
    return max(scores,key=scores.get),near
def case_report(symptoms,k=5):
    label,near=propose_case_diagnosis(symptoms,k=k)
    return {"hipotese":label,"tratamento_recomendado":SUPPORTIVE_TREATMENTS[label],"casos_proximos":near,"aviso":"Sugestão fictícia para demonstração acadêmica; não é indicação clínica."}
def revise_case(symptoms,validated_label=None):
    proposed,near=propose_case_diagnosis(symptoms); final=validated_label or proposed
    if final not in SUPPORTIVE_TREATMENTS: raise ValueError("Diagnóstico corrigido fora das categorias cadastradas.")
    return {"diagnostico_sugerido":proposed,"diagnostico_validado":final,"corrigido":final!=proposed,"tratamento_recomendado":SUPPORTIVE_TREATMENTS[final],"casos_proximos":near}
def retain_case(path,symptoms,validated_label):
    p=Path(path); db=json.loads(p.read_text(encoding='utf8')) if p.exists() else []
    if validated_label not in SUPPORTIVE_TREATMENTS: raise ValueError("Diagnóstico validado fora das categorias cadastradas.")
    db.append({"symptoms":sorted(set(symptoms)),"validated_label":validated_label,"treatment_recommended":SUPPORTIVE_TREATMENTS[validated_label]})
    p.write_text(json.dumps(db,ensure_ascii=False,indent=2),encoding='utf8')

# Q8: E->Gripe; Gripe->Febre/Tosse/Mialgia. Valores ilustrativos, não clínicos.
P_E=.25; P_G={False:.04,True:.20}; P_S={"febre":{False:.08,True:.80},"tosse":{False:.20,True:.70},"mialgia":{False:.05,True:.75}}
def bayes_flu(evidence):
    num=den=0.
    for e,g,f,t,m in product((False,True),repeat=5):
        vals={"exposicao":e,"gripe":g,"febre":f,"tosse":t,"mialgia":m}
        if any(vals[k]!=v for k,v in evidence.items()):continue
        p=(P_E if e else 1-P_E)*(P_G[e] if g else 1-P_G[e])
        for n,v in (("febre",f),("tosse",t),("mialgia",m)):
            q=P_S[n][g]; p*=q if v else 1-q
        den+=p
        if g:num+=p
    return num/den if den else float('nan')

# Q9/Q15: OWL/Turtle, 11 classes, 15 propriedades e indivíduos. Abrível no Protégé.
OWL='''@prefix : <http://example.org/leitura#> . @prefix owl: <http://www.w3.org/2002/07/owl#> . @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> . @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
:Livro a owl:Class . :Ficcao a owl:Class ; rdfs:subClassOf :Livro . :Ciencia a owl:Class ; rdfs:subClassOf :Livro . :Fantasia a owl:Class ; rdfs:subClassOf :Ficcao . :Leitor a owl:Class . :Interesse a owl:Class . :Autor a owl:Class . :Editora a owl:Class . :Idioma a owl:Class . :Formato a owl:Class . :Disponibilidade a owl:Class .
:temInteresse a owl:ObjectProperty ; rdfs:domain :Leitor ; rdfs:range :Interesse . :temGenero a owl:ObjectProperty ; rdfs:domain :Livro . :escritoPor a owl:ObjectProperty ; rdfs:domain :Livro ; rdfs:range :Autor . :publicadoPor a owl:ObjectProperty ; rdfs:domain :Livro ; rdfs:range :Editora . :formato a owl:ObjectProperty ; rdfs:domain :Livro ; rdfs:range :Formato . :idioma a owl:ObjectProperty ; rdfs:domain :Livro ; rdfs:range :Idioma . :leu a owl:ObjectProperty ; rdfs:domain :Leitor ; rdfs:range :Livro . :favoritou a owl:ObjectProperty ; rdfs:domain :Leitor ; rdfs:range :Livro . :recomendadoPara a owl:ObjectProperty ; rdfs:domain :Livro ; rdfs:range :Leitor . :disponivelEm a owl:ObjectProperty ; rdfs:domain :Livro ; rdfs:range :Disponibilidade . :publicadoEm a owl:DatatypeProperty ; rdfs:domain :Livro ; rdfs:range xsd:integer . :idadeMinima a owl:DatatypeProperty ; rdfs:domain :Livro ; rdfs:range xsd:integer . :avaliacao a owl:DatatypeProperty ; rdfs:domain :Livro ; rdfs:range xsd:decimal . :nomeAutor a owl:DatatypeProperty ; rdfs:domain :Autor ; rdfs:range xsd:string . :titulo a owl:DatatypeProperty ; rdfs:domain :Livro ; rdfs:range xsd:string .
:Leitor rdfs:subClassOf [ a owl:Restriction ; owl:onProperty :temInteresse ; owl:someValuesFrom :Interesse ] . :Livro rdfs:subClassOf [ a owl:Restriction ; owl:onProperty :titulo ; owl:someValuesFrom xsd:string ] . :Livro rdfs:subClassOf [ a owl:Restriction ; owl:onProperty :formato ; owl:allValuesFrom :Formato ] .
:Ana a :Leitor ; :temInteresse :Fantasia . :Bob a :Leitor ; :temInteresse :Ciencia . :Fantasia a :Interesse . :Ciencia a :Interesse . :F1 a :Fantasia ; :titulo "A Ilha das Brumas" ; :formato :Digital ; :idioma :Portugues . :C1 a :Ciencia ; :titulo "O Universo em Escala" ; :formato :Impresso ; :idioma :Portugues . :Digital a :Formato . :Impresso a :Formato . :Portugues a :Idioma .
'''
def save_ontology(path="recomendacao.owl.ttl"): Path(path).write_text(OWL,encoding='utf8')
def _reasoned_ontology(ontology_path):
    from owlready2 import get_ontology, onto_path, sync_reasoner
    path=Path(ontology_path).resolve(); onto_path.append(str(path.parent))
    onto=get_ontology(path.name).load(); sync_reasoner([onto],debug=0)
    return onto

def _recommend_by_interest(onto,interest,fmt=None):
    from owlready2 import ThingClass
    wanted=onto.search_one(iri=f"*#{interest}")
    if wanted is None: raise ValueError(f"Classe OWL não encontrada: {interest}")
    book_class=onto.search_one(iri="*#Livro")
    found=[]
    for book in onto.search(iri="*#*"):
        if isinstance(book,ThingClass) or not getattr(book,"titulo",[]): continue
        if book_class not in book.INDIRECT_is_a or wanted not in book.INDIRECT_is_a: continue
        formats=list(getattr(book,"formato",[]))
        if fmt and all(f.name!=fmt for f in formats): continue
        title=getattr(book,"titulo",[book.name])[0]
        found.append((book.name,title,formats[0].name if formats else "sem formato"))
    return found

def recommend(interest,fmt=None,ontology_path="recomendacao.owl"):
    """Usa HermiT/Owlready2 para classificar antes de recomendar por interesse."""
    return _recommend_by_interest(_reasoned_ontology(ontology_path),interest,fmt)

def recommend_for_user(user="Ana",fmt=None,ontology_path="recomendacao.owl"):
    """Obtém os interesses declarados do usuário e recomenda tipos inferidos."""
    onto=_reasoned_ontology(ontology_path)
    person=onto.search_one(iri=f"*#{user}")
    if person is None: raise ValueError(f"Usuário não encontrado: {user}")
    interests=list(getattr(person,"temInteresse",[]))
    results=[]
    for interest in interests:
        label=getattr(interest,"name",str(interest).rsplit("#",1)[-1])
        results.extend((label,item) for item in _recommend_by_interest(onto,label,fmt))
    return results

def owl_inference_summary(ontology_path="recomendacao.owl"):
    onto=_reasoned_ontology(ontology_path)
    f1=onto.search_one(iri="*#F1")
    return {"consistente":True,"tipos_F1":sorted(c.name for c in f1.INDIRECT_is_a if hasattr(c,"name")),"recomendacao_Ana":recommend_for_user("Ana",ontology_path=ontology_path)}

# Q12: planejador verificável; interpretação LLM pode fornecer tarefas estruturadas.
def schedule(tasks,start,end,fixed=()):
    occupied=list(fixed); placed=[]; skipped=[]
    for task in sorted(tasks,key=lambda t:(-t['priority'],t['deadline'],t['name'])):
        for m in range(start,end-task['duration']+1):
            if all(m+task['duration']<=a or m>=b for a,b,_ in occupied):
                block=(m,m+task['duration'],task['name']); occupied.append(block); placed.append(block); break
        else: skipped.append((task['name'],'sem janela contínua disponível'))
    return sorted(placed),skipped

if __name__=='__main__':
    print('Ventilador 34C/65%:',round(fan_mamdani(34,65),1),'%')
    for e in ({},{'febre':True},{'febre':True,'tosse':True},{'febre':True,'tosse':True,'mialgia':True}): print(e,round(bayes_flu(e),4))
    print('Recomendações:',recommend('Fantasia'),recommend('Ciencia'))
    save_ontology()
