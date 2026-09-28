---
title: A rotina de priorização do Backlog
date: 2022-05-26
tags: backlog, priorização, produto, agilidade
summary: A priorização do backlog é uma rotina e nunca acaba — é como lavar louça. Aqui está o ciclo que eu uso, passo a passo, com as ferramentas de cada etapa.
draft: false
---

A priorização do backlog é uma rotina e ela nunca acaba, é como lavar louça ou cortar a unha, simples assim.

Nesse post eu tento passar para vocês detalhes dessa rotina, passo a passo, ideias e ferramentas de como faço. Espero ajudar!

A rotina de priorização de Backlog é como o ciclo abaixo:

![](https://static.wixstatic.com/media/b92f60_52807f66d4154e2583de5e31d3c1db6e~mv2.png/v1/fill/w_980,h_648,al_c,q_90,usm_0.66_1.00_0.01,enc_avif,quality_auto/b92f60_52807f66d4154e2583de5e31d3c1db6e~mv2.png)

Exemplo de um app de venda de ingresso de cinema — [Miro criado para isso aqui](https://miro.com/app/board/uXjVON9t52U=/?share_link_id=365207571910).

## 1 — Entender a situação

A melhor maneira para entender a situação é conversar com as pessoas de cada área interessada no produto ou etapa do produto pela qual você é responsável como PO/PM.

Busque entender coisas como:

- Se a visão do produto mudou.
- Se a estratégia da empresa para atingir os objetivos mudou.
- Se os objetivos do produto de curto ou médio prazo mudaram.
- Se uma coisa que vocês planejaram deu errado.
- Se algum fornecedor mudou alguma integração e isso vai quebrar o produto, exigindo ação.
- Se surgiram novas demandas legais vindas de órgãos do governo.
- Se surgiu alguma nova campanha de marketing que vai demandar ação do seu time.
- Se alguma função que você deixou coletando dados deu algum resultado razoável para desligar ou ligar, mudar, melhorar ou criar algo.
- Se as pessoas que estão fazendo discovery descobriram alguma dor nova ou algo que possa ser melhorado.
- Se o time de desenvolvimento está com alguma demanda que eles não aguentam mais ficar sem — pode ser uma automação, testes, refatoração, atualização ou adoção de uma nova biblioteca.
- Se houve um pico de reclamações no time de atendimento ao cliente; acompanhe a lista de itens mais solicitados ou reclamados e pense junto com o time como vocês podem ajudar.
- Se o time de QA encontrou algum bug urgente; entenda também a lista de bugs e suas prioridades.
- Se seu concorrente lançou algo interessante.
- Se algum outro stakeholder possui demanda nova que seja importante para a empresa e para o produto — pode ser de vendas, operações ou outra área.

### Dicas

- Você precisa monitorar muita coisa. Tente manter uma reunião semanal com as principais pessoas de cada área para ter um termômetro da situação.
- A conversa cara a cara (pode ser virtual) é a melhor forma de levantar a situação.
- Monitore o seu produto: as métricas também vão te dar alguns insights.
- Converse do CEO ao atendente. Exercite a empatia.
- Compare a situação levantada com o seu plano de trabalho e se sinta confortável caso tenha que mudar algo.

## 2 — Ter uma visão geral e classificada

Depois que você levantou a situação, é hora de atualizar ou montar o seu mapa da visão geral.

**Recomendo fortemente você criar um mapa de features.** Eu uso um inspirado em User Story Mapping.

![](https://static.wixstatic.com/media/b92f60_8b11deb0ff4444a48d30da419706948d~mv2.png/v1/fill/w_980,h_314,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/b92f60_8b11deb0ff4444a48d30da419706948d~mv2.png)

Os blocos azuis são grandes funções ou pequenos projetos, e os amarelos são funções que precisamos desenvolver e entregar (cards).

Você não precisa priorizar as demandas nessa etapa de visão geral, só precisa classificá-las. Minha sugestão é usar o método **MoSCoW**:

![](https://static.wixstatic.com/media/b92f60_a2ad9bd2cd1a4f57b7055b866a7fb6c6~mv2.png/v1/fill/w_980,h_163,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/b92f60_a2ad9bd2cd1a4f57b7055b866a7fb6c6~mv2.png)

Depois de classificá-las, eu coloco os complementos abaixo para facilitar a minha leitura:

![](https://static.wixstatic.com/media/b92f60_957e49cb8b36434684b272be63742f84~mv2.png/v1/fill/w_980,h_113,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/b92f60_957e49cb8b36434684b272be63742f84~mv2.png)

Daí seu mapa vai ficar assim:

![](https://static.wixstatic.com/media/b92f60_fb17201bfcef4a7d852f2b16cb74d35f~mv2.png/v1/fill/w_980,h_223,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/b92f60_fb17201bfcef4a7d852f2b16cb74d35f~mv2.png)

### Dicas

- Valide sua classificação com as pessoas das áreas interessadas no produto: atendimento ao cliente, diretoria, operações, vendas, etc.
- Faça desse mapa o seu backlog.
- Mantenha esse mapa atualizado.
- Utilize o backlog do Jira ou outra ferramenta apenas para bugs e outras demandas que não entreguem valor para o cliente final.
- Eu usei o [Miro](https://miro.com/) para fazer esse mapa.

## 3 — Priorizar e planejar

Reveja a classificação que você fez na etapa anterior. Veja se ainda faz sentido; se não fizer, reclassifique alguns cards.

Existem vários métodos para priorizar (RICE, Kano, etc.). Eu gosto da matriz de esforço vs. impacto (valor) e da lista priorizada em conjunto.

![](https://static.wixstatic.com/media/b92f60_fadcbc8d82a445e2b51ca14e3d24b1ce~mv2.png/v1/fill/w_806,h_758,al_c,q_90,enc_avif,quality_auto/b92f60_fadcbc8d82a445e2b51ca14e3d24b1ce~mv2.png)

**IMPORTANTE:** nem sempre você poderá seguir o resultado da matriz, pois uma função pode depender de outra estar pronta primeiro. Por causa disso, você deverá checar essa sequência fazendo uma lista priorizada:

![](https://static.wixstatic.com/media/b92f60_5fbc46d789714990b7b701c0aca0310c~mv2.png/v1/fill/w_980,h_513,al_c,q_90,usm_0.66_1.00_0.01,enc_avif,quality_auto/b92f60_5fbc46d789714990b7b701c0aca0310c~mv2.png)

Repare que o primeiro colocado na matriz de esforço vs. impacto nem sempre será o primeiro quando você for priorizar, pois existem as dependências.

> Leve em consideração as dependências entre os cards e tente priorizar os cards de maior valor para o negócio ou cliente com maior risco de encontrar problemas durante o desenvolvimento.

Agora que você tem uma lista priorizada, é hora de arrumar um jeito fácil de mostrar a sua visão de priorização. Eu gosto de fazer assim:

![](https://static.wixstatic.com/media/b92f60_29b8a13b15314ad39a37c8f325214374~mv2.png/v1/fill/w_980,h_382,al_c,q_90,usm_0.66_1.00_0.01,enc_avif,quality_auto/b92f60_29b8a13b15314ad39a37c8f325214374~mv2.png)

Sprints com datas embaixo e os cards que acredito que caibam nas sprints — use e abuse de marcos como o exemplo do Go-live acima.

### Dicas

- Chame pelo menos uma pessoa de QA, uma de Desenvolvimento e uma de Negócio para priorizar as demandas na matriz de esforço vs. impacto.
- Chame pelo menos uma pessoa de Desenvolvimento para fazer a lista priorizada após ter preenchido a matriz. Se possível, faça as duas etapas juntas com o maior número de pessoas.
- Apresente a sua ideia de cronograma para os desenvolvedores do seu time. Não queira uma estimativa assinada com sangue: a ideia aqui é ter uma noção de grandeza, do tipo é 8 ou 80, uma ou duas sprints.
- Não planeje mais do que 3 sprints para frente. Vai por mim, não vale a pena, pois tudo pode mudar — e vai mudar.

## 4 — Validar a proposta de priorização e cronograma

A essa altura essa proposta já nem é mais sua, é da empresa como um todo, pois você já vem trazendo sugestões, validando e melhorando as ideias com outras pessoas como QAs, devs e pessoas de negócio.

Mas agora é a hora de dar uma última validada no cronograma que você montou. Valide com o seu chefe, com diretores, com parceiros de áreas, com fornecedores — aqui quanto mais, melhor.

Esse cronograma é fundamental para te dar um pouco de paz de espírito para trabalhar, pois uma vez validado, vocês vão trabalhar no discovery e no refinamento de cada uma dessas demandas antes delas entrarem em desenvolvimento.

### Dicas

- Valide com o máximo de pessoas possível.
- Deixe esse cronograma público: ninguém pode alegar que não teve visibilidade (retire muletas).
- Mantenha esse cronograma atualizado.
- Não planeje mais do que 3 sprints para frente.

## 5 — Passar a prioridade adiante e colher novidades

Essa última etapa do ciclo é quando você vai de fato apresentar os cards para o time de desenvolvimento. Em muitas empresas é a hora da Planning.

Eu espero que entre a etapa 4 e a 5 você tenha criado todos os cards com todas as informações necessárias para um bom desenvolvimento e testes.

Durante a passagem de prioridade para o time de desenvolvimento podem surgir algumas ideias. Seja flexível, escute atentamente, veja se faz sentido e não tenha medo de mudar algo em cima da hora.

Veja o resultado da Sprint anterior: talvez alguma coisa tenha que ser terminada na próxima Sprint, e isso vai impactar o seu cronograma e quem sabe a sua priorização. Esse resultado é uma das fontes para entender a situação.

Pronto — agora você volta para a etapa um e começa tudo de novo para as próximas sprints!

### Dicas

- Dica para o seu time: durante a planning, mostre qual é o norte, para onde queremos ir, qual é o objetivo de negócio e o impacto que esses novos cards levarão para os clientes.
- Deixe pelo menos 8h de trabalho para o time de desenvolvimento fazer o plano de como construir a solução, e só então devolver o que cabe ou não cabe na Sprint.
