#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera os currículos em PDF (PT e EN) de João Paulo Marson.

Uso:
    pip install weasyprint
    python3 tools/build_cv.py

Saída:
    cv/joao-paulo-marson-cv-pt.pdf
    cv/joao-paulo-marson-resume-en.pdf

O conteúdo fica todo neste arquivo (dicionários PT e EN). Para atualizar o CV,
edite o texto aqui e rode o script de novo.
"""
import os
import html as _h
from weasyprint import HTML

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "cv")

CSS = """
@page { size: A4; margin: 14mm 15mm 12mm 15mm;
  @bottom-center { content: "joão paulo marson · jpmarson.com.br · " string(pg) " " counter(page) " / " counter(pages);
    font-family: 'DejaVu Sans Mono', monospace; font-size: 7pt; color: #93a3bd; } }
body { string-set: pg attr(data-pg); }
* { box-sizing: border-box; }
body { font-family: 'DejaVu Sans', sans-serif; font-size: 9.2pt; line-height: 1.45; color: #1e293b; margin: 0; }
a { color: #0a66ff; text-decoration: none; }
.name { font-size: 24pt; font-weight: bold; letter-spacing: -0.5pt; color: #0f172a; }
.headline { font-size: 11pt; color: #0a66ff; font-weight: bold; margin-top: 3pt; }
.contact { font-family: 'DejaVu Sans Mono', monospace; font-size: 7.8pt; color: #5b6b83; margin-top: 7pt; }
.contact span { margin-right: 9pt; }
.rule { height: 2.5pt; background: #0a66ff; margin: 9pt 0 11pt; border-radius: 2pt; }
h2 { font-size: 9.5pt; text-transform: uppercase; letter-spacing: 1.1pt; color: #0a66ff;
     margin: 13pt 0 6pt; padding-bottom: 2.5pt; border-bottom: 0.6pt solid #d7dfec; }
.summary { text-align: justify; margin: 0; }
.metrics { margin: 9pt 0 0; }
.metrics td { padding: 5pt 4pt; border: 0.6pt solid #dbe3f0; text-align: center; width: 20%; vertical-align: top; }
.metrics b { font-family: 'DejaVu Sans Mono', monospace; font-size: 11.5pt; color: #0a66ff; display: block; }
.metrics span { font-size: 6.8pt; color: #5b6b83; }
.job { margin-bottom: 9pt; }
.job-title { font-size: 10pt; font-weight: bold; color: #0f172a; }
.job-co { font-size: 9.2pt; color: #0a66ff; font-weight: bold; }
.job-meta { font-family: 'DejaVu Sans Mono', monospace; font-size: 7.5pt; color: #5b6b83; }
.job p { margin: 3pt 0 0; text-align: justify; }
.bt { font-weight: bold; color: #0f172a; margin-top: 4pt; font-size: 8.8pt; }
ul { margin: 3pt 0 0; padding-left: 12pt; }
li { margin-bottom: 1.8pt; text-align: justify; }
.skills td { padding: 2.5pt 0; vertical-align: top; }
.skills .lbl { font-weight: bold; color: #0f172a; width: 28%; padding-right: 8pt; }
.two td { vertical-align: top; width: 50%; padding-right: 10pt; }
.early { font-size: 8.6pt; color: #475569; margin-bottom: 2pt; }
.early b { color: #0f172a; }
.muted { color: #93a3bd; }
"""


def esc(t):
    return _h.escape(t)


def render(d, out):
    jobs = ""
    for j in d["jobs"]:
        bt = '<div class="bt">%s</div>' % esc(j["bt"]) if j.get("bt") else ""
        bullets = "".join("<li>%s</li>" % esc(b) for b in j.get("bullets", []))
        jobs += """<div class="job">
          <div><span class="job-title">%s</span> &nbsp;<span class="job-co">%s</span></div>
          <div class="job-meta">%s</div>
          <p>%s</p>%s%s</div>""" % (esc(j["title"]), esc(j["co"]), esc(j["meta"]), esc(j["desc"]),
                                    bt, ("<ul>%s</ul>" % bullets) if bullets else "")
    early = "".join("<div class='early'><b>%s</b> — %s <span class='muted'>(%s)</span></div>"
                    % (esc(a), esc(b), esc(c)) for a, b, c in d["early"])
    skills = "".join("<tr><td class='lbl'>%s</td><td>%s</td></tr>" % (esc(k), esc(v)) for k, v in d["skills"])
    metrics = "".join("<td><b>%s</b><span>%s</span></td>" % (esc(a), esc(b)) for a, b in d["metrics"])
    edu = "".join("<div class='early'><b>%s</b><br>%s <span class='muted'>· %s</span></div>"
                  % (esc(a), esc(b), esc(c)) for a, b, c in d["edu"])
    langs = "".join("<div class='early'><b>%s</b> — %s</div>" % (esc(a), esc(b)) for a, b in d["langs"])

    doc = """<!DOCTYPE html><html lang="%(lang)s"><head><meta charset="utf-8"><style>%(css)s</style></head>
    <body data-pg="%(pg)s">
    <div class="name">João Paulo Marson</div>
    <div class="headline">%(headline)s</div>
    <div class="contact"><span>%(loc)s</span><span>jp@jpmarson.com.br</span><span>jpmarson.com.br</span><span>linkedin.com/in/jpmarson</span></div>
    <div class="rule"></div>
    <h2>%(t_summary)s</h2>
    <p class="summary">%(summary)s</p>
    <table class="metrics" width="100%%" cellspacing="4"><tr>%(metrics)s</tr></table>
    <h2>%(t_exp)s</h2>%(jobs)s
    <h2>%(t_early)s</h2>%(early)s
    <h2>%(t_skills)s</h2><table class="skills" width="100%%">%(skills)s</table>
    <table class="two" width="100%%"><tr>
      <td><h2>%(t_edu)s</h2>%(edu)s</td>
      <td><h2>%(t_lang)s</h2>%(langs)s</td>
    </tr></table>
    </body></html>""" % dict(
        lang=d["lang"], css=CSS, pg=d["pg"], headline=esc(d["headline"]), loc=esc(d["loc"]),
        t_summary=d["t_summary"], summary=esc(d["summary"]), metrics=metrics,
        t_exp=d["t_exp"], jobs=jobs, t_early=d["t_early"], early=early,
        t_skills=d["t_skills"], skills=skills, t_edu=d["t_edu"], edu=edu, t_lang=d["t_lang"], langs=langs)
    HTML(string=doc).write_pdf(out)
    print("gerado:", os.path.relpath(out, ROOT))


PT = dict(
    lang="pt-BR", pg="página", loc="São Paulo, Brasil",
    headline="Gestão de Projetos & Produtos Digitais · Fintech e Meios de Pagamento",
    t_summary="Resumo", t_exp="Experiência Profissional", t_early="Trajetória Anterior",
    t_skills="Competências", t_edu="Formação", t_lang="Idiomas",
    summary=("Líder de projetos e produtos digitais com 16 anos de experiência, mais de 6 deles em fintechs. "
             "Lidero equipes em projetos e na operação de produtos digitais em diversos mercados, integrando times "
             "de negócio, produto e engenharia. Meu papel é dar clareza: reduzir o gap entre negócios e tecnologia, "
             "ler os dados e o ambiente, desenhar a estratégia e garantir que todos enxerguem e sigam a mesma direção. "
             "Acredito que confiança vem antes de processo e que bons resultados são construídos em equipe. "
             "Experiência sólida em métodos ágeis (Scrum, Kanban, LeSS), integrações via API, priorização orientada "
             "a dados e gestão de stakeholders."),
    metrics=[("16+", "anos de experiência"), ("-40%", "custo de onboarding"), ("-30%", "fraude no onboarding"),
             ("24h → 0", "resposta de underwriting"), ("3.8 → 4.9", "nota do app nas lojas")],
    jobs=[
        dict(title="Manager, Technical Project Management", co="Fiserv",
             meta="ago/2025 — atual · São Paulo, Brasil",
             desc=("Estruturando, junto com os líderes de cada frente, a capacidade de gestão de projetos cross-team "
                   "no Brasil, com foco em execução, compliance e impacto de negócio mensurável. Lidero três grupos "
                   "de project managers."),
             bullets=[
                 "Compliance regulatório e de bandeiras em produtos e operações.",
                 "Entrega e evolução de produtos e funcionalidades core.",
                 "Habilitação de novos adquirentes pela plataforma Acquiring as a Service (AQaaS).",
                 "Priorização de projetos alinhada aos objetivos de negócio, com mais previsibilidade de entrega e retorno financeiro.",
                 "Foco atual: eficiência operacional, priorização por valor, métricas claras, melhoria contínua e governança pragmática — padronizar apenas o que escala."]),
        dict(title="Technical Product Owner", co="novutech · cartão de crédito novücard",
             meta="jan/2020 — jul/2025 · Remoto · 5 anos e 7 meses",
             desc=("Product Owner técnico do cartão de crédito novücard, trabalhando lado a lado com times de negócio, "
                   "engenharia, dados e atendimento. Meu papel: ligar os dados de produção às decisões de produto, "
                   "conduzir o fórum de prioridades entre negócio e tecnologia e manter a empresa informada sobre cada "
                   "entrega, para que o time inteiro seguisse na mesma direção."),
             bt="Resultados do time:",
             bullets=[
                 "Redução de 40% no custo de onboarding e de 30% na fraude no onboarding.",
                 "Resposta de underwriting reduzida de 24 horas para imediata.",
                 "Nota do app nas lojas de 3.8 para 4.9.",
                 "Migração completa da empresa processadora em 6 meses.",
                 "Mais de 1.000 chamados mensais a menos no atendimento.",
                 "Aumento de 20% na ativação de cartões físicos."]),
        dict(title="Technical Product Owner", co="ITS Soluções",
             meta="jun/2018 — jan/2020 · São Paulo · 1 ano e 8 meses",
             desc=("Product Owner de um produto SaaS de automação de chamados de TI, levantando dores dos clientes e "
                   "desenhando soluções junto com desenvolvedores e arquitetos. Também atuei como consultor de pré-vendas."),
             bullets=[
                 "Definição e priorização de funcionalidades; construção de MVP e roadmap.",
                 "Gestão de riscos para assegurar qualidade, boa experiência de uso e viabilidade técnica.",
                 "Validação das soluções com clientes e comunicação transparente via release notes."]),
    ],
    early=[
        ("Scrum Master · StratioBD", "Transformação digital no Banco Carrefour Brasil: apoio a dois times na adoção de Scrum, trilha de capacitação (Scrum, Kanban, MVP, LeSS) e KPIs de fluxo.", "jul/2017 — jun/2018"),
        ("Scrum Master · Nextel Telecomunicações", "Definição de metodologia, processos e boas práticas para a área digital de aplicativos móveis, junto a dois times.", "abr/2017 — jul/2017"),
        ("Product Owner / Scrum Master · ITS Soluções", "Metodologia de gestão de projetos, pré-vendas, levantamento de requisitos, user stories, release planning e KPIs ágeis.", "jun/2015 — 2017"),
        ("Project Manager MS Dynamics AX/CRM · AX4B e SAGlobal", "Gestão de projetos de ERP e CRM: cronograma, escopo, marcos, coordenação de times e relacionamento com clientes.", "2010 — jun/2015"),
        ("Consultor de Pré-vendas e CRM · Metrics Information System", "Mapeamento de processos comerciais, implantação e treinamento de Dynamics CRM e atendimento a clientes na América Latina.", "ago/2008 — abr/2010"),
    ],
    skills=[
        ("Liderança", "Liderança de Times, Construção de Confiança, Colaboração entre Áreas, Comunicação e Alinhamento de Stakeholders"),
        ("Gestão", "Gestão de Projetos e Programas, Governança de Portfólio, Gestão de Riscos, Priorização por Valor"),
        ("Produto", "Product Ownership, Discovery, Roadmap, MVP, Métricas de Produto, Análise de Dados"),
        ("Métodos Ágeis", "Scrum, Kanban, LeSS, Facilitação, KPIs de Fluxo, Melhoria Contínua"),
        ("Domínio", "Fintech, Meios de Pagamento, Adquirência (AQaaS), Cartões de Crédito, Prevenção a Fraudes, Compliance Regulatório"),
        ("Tecnologia", "Integrações via API, SaaS, ERP/CRM (MS Dynamics)"),
    ],
    edu=[
        ("Pós-graduação em Análise de Sistemas de TI", "Faculdade de Tecnologia de São Paulo (FATEC-SP)", "2010 — 2011"),
        ("Pós-graduação em Marketing", "Universidade Presbiteriana Mackenzie", "2007 — 2008"),
        ("Bacharelado em Administração de Empresas", "Universidade Estadual de Londrina", "2002 — 2006"),
    ],
    langs=[("Português", "nativo"), ("Inglês", "profissional"), ("Espanhol", "intermediário")],
)

EN = dict(
    lang="en", pg="page", loc="São Paulo, Brazil",
    headline="Project & Digital Product Management · Fintech and Payments",
    t_summary="Summary", t_exp="Professional Experience", t_early="Earlier Career",
    t_skills="Skills", t_edu="Education", t_lang="Languages",
    summary=("Project and digital product leader with 16 years of experience, more than 6 of them in fintech. "
             "I lead teams on projects and in the operation of digital products across several markets, bringing "
             "business, product and engineering teams together. My role is to bring clarity: close the gap between "
             "business and technology, read the data and the environment, shape the strategy and make sure everyone "
             "sees and follows the same direction. I believe trust comes before process, and that strong results are "
             "built as a team. Solid background in agile methods (Scrum, Kanban, LeSS), API integrations, data-driven "
             "prioritization and stakeholder management."),
    metrics=[("16+", "years of experience"), ("-40%", "onboarding cost"), ("-30%", "onboarding fraud"),
             ("24h → 0", "underwriting response"), ("3.8 → 4.9", "app store rating")],
    jobs=[
        dict(title="Manager, Technical Project Management", co="Fiserv",
             meta="Aug 2025 — Present · São Paulo, Brazil",
             desc=("Building, together with the leads of each front, a cross-team project management capability in "
                   "Brazil, focused on execution, compliance and measurable business impact. I lead three project "
                   "management groups."),
             bullets=[
                 "Regulatory and card scheme compliance across products and operations.",
                 "Delivery and evolution of core products and features.",
                 "Enabling new acquirers through the Acquiring as a Service (AQaaS) platform.",
                 "Project prioritization aligned with business goals, improving delivery predictability and financial return.",
                 "Current focus: operational efficiency, value-driven prioritization, clear metrics, continuous improvement and pragmatic governance — standardize only what scales."]),
        dict(title="Technical Product Owner", co="novutech · novücard credit card",
             meta="Jan 2020 — Jul 2025 · Remote · 5 years 7 months",
             desc=("Technical Product Owner for the novücard credit card, working side by side with business, "
                   "engineering, data and customer support teams. My role: connect production data to product "
                   "decisions, run the priority forum between business and technology, and keep the company informed "
                   "about every delivery so the whole team moved in the same direction."),
             bt="Team outcomes:",
             bullets=[
                 "40% lower onboarding cost and 30% less onboarding fraud.",
                 "Underwriting response cut from 24 hours to immediate.",
                 "App store rating up from 3.8 to 4.9.",
                 "Full card processor migration delivered in 6 months.",
                 "Over 1,000 fewer support contacts per month.",
                 "20% increase in physical card activation."]),
        dict(title="Technical Product Owner", co="ITS Soluções",
             meta="Jun 2018 — Jan 2020 · São Paulo · 1 year 8 months",
             desc=("Product Owner for an IT ticket automation SaaS product, uncovering customer pain points and designing "
                   "solutions together with developers and architects. Also acted as a pre-sales consultant."),
             bullets=[
                 "Defined and prioritized features; built the MVP and product roadmap.",
                 "Managed risk to ensure product quality, effective UX and technical feasibility.",
                 "Validated solutions with clients and kept transparent communication through release notes."]),
    ],
    early=[
        ("Scrum Master · StratioBD", "Digital transformation at Banco Carrefour Brasil: supported two teams in adopting Scrum, with a training track (Scrum, Kanban, MVP, LeSS) and flow KPIs.", "Jul 2017 — Jun 2018"),
        ("Scrum Master · Nextel Telecomunicações", "Defined methodology, processes and best practices for the mobile apps digital area, working with two teams.", "Apr 2017 — Jul 2017"),
        ("Product Owner / Scrum Master · ITS Soluções", "Project management methodology, pre-sales, requirements gathering, user stories, release planning and agile KPIs.", "Jun 2015 — 2017"),
        ("Project Manager MS Dynamics AX/CRM · AX4B and SAGlobal", "ERP and CRM project management: scheduling, scope, milestones, team coordination and client relationship.", "2010 — Jun 2015"),
        ("Pre-sales and CRM Consultant · Metrics Information System", "Mapped commercial processes, implemented and trained Dynamics CRM, and served clients across Latin America.", "Aug 2008 — Apr 2010"),
    ],
    skills=[
        ("Leadership", "Team Leadership, Trust Building, Cross-functional Collaboration, Communication and Stakeholder Alignment"),
        ("Management", "Project & Program Management, Portfolio Governance, Risk Management, Value-Driven Prioritization"),
        ("Product", "Product Ownership, Discovery, Roadmap, MVP, Product Metrics, Data Analysis"),
        ("Agile", "Scrum, Kanban, LeSS, Facilitation, Flow KPIs, Continuous Improvement"),
        ("Domain", "Fintech, Payments, Merchant Acquiring (AQaaS), Credit Cards, Fraud Prevention, Regulatory Compliance"),
        ("Technology", "API Integrations, SaaS, ERP/CRM (MS Dynamics)"),
    ],
    edu=[
        ("Postgraduate Degree, IT Systems Analysis", "Faculdade de Tecnologia de São Paulo (FATEC-SP)", "2010 — 2011"),
        ("Postgraduate Degree, Marketing", "Universidade Presbiteriana Mackenzie", "2007 — 2008"),
        ("Bachelor's Degree, Business Administration", "Universidade Estadual de Londrina", "2002 — 2006"),
    ],
    langs=[("Portuguese", "native"), ("English", "professional working proficiency"), ("Spanish", "intermediate")],
)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    render(PT, os.path.join(OUT, "joao-paulo-marson-cv-pt.pdf"))
    render(EN, os.path.join(OUT, "joao-paulo-marson-resume-en.pdf"))
