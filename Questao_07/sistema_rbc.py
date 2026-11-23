"""CLI interativa para demonstrar as quatro etapas de RBC da questão 7."""
from prototipos_lista2 import case_report, revise_case, retain_case, CASES, SUPPORTIVE_TREATMENTS

def main():
    print("Apoio didático por casos; não substitui atendimento médico.")
    print(f"Base: {len(CASES)} casos, {len(SUPPORTIVE_TREATMENTS)} categorias.")
    print("Informe sintomas separados por vírgula: febre, tosse, mialgia, coriza, garganta, espirros, coceira, odinofagia, nausea, vomito, diarreia, calafrios")
    symptoms={s.strip().lower() for s in input("Sintomas: ").split(",") if s.strip()}
    result=case_report(symptoms)
    print("\nRetrieve — casos mais próximos:")
    for score,case in result["casos_proximos"]:
        print(f"{case['id']} | Jaccard {score:.2f} | {case['diagnostico']} | {sorted(case['sintomas'])}")
    print(f"\nReuse — hipótese: {result['hipotese']}")
    print(f"Conduta de suporte: {result['tratamento_recomendado']}")
    corrected=input("Revise — confirme com Enter ou digite uma categoria corrigida: ").strip().lower()
    label=corrected or result["hipotese"]
    final=revise_case(symptoms,validated_label=label)
    print(f"Diagnóstico validado: {final['diagnostico_validado']}")
    if input("Retain — gravar este caso validado? (s/n): ").strip().lower()=="s":
        retain_case("casos_usuario.json",symptoms,final["diagnostico_validado"])
        print("Caso armazenado em casos_usuario.json")

if __name__=="__main__": main()
