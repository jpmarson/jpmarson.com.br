-- ============================================================================
-- Migração dos 5 posts do antigo blog Ciclo de PO (Wix) para o Supabase.
-- Gerado a partir de posts/*.md. Idempotente: não sobrescreve posts existentes.
-- ============================================================================
insert into public.posts
  (slug, status, published_at,
   title_pt, summary_pt, body_pt, tags_pt,
   title_en, summary_en, body_en, tags_en)
values
(
  $md$rotina-de-priorizacao-do-backlog$md$, 'published', $md$2022-05-26$md$::date,
  $md$A rotina de priorização do Backlog$md$,
  $md$A priorização do backlog é uma rotina e nunca acaba — é como lavar louça. Aqui está o ciclo que eu uso, passo a passo, com as ferramentas de cada etapa.$md$,
  $md$A priorização do backlog é uma rotina e ela nunca acaba, é como lavar louça ou cortar a unha, simples assim.

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
$md$,
  array[$md$backlog$md$,$md$priorização$md$,$md$produto$md$,$md$agilidade$md$]::text[],
  $md$The backlog prioritization routine$md$,
  $md$Backlog prioritization is a routine and it never ends — it is like doing the dishes. Here is the cycle I use, step by step, with the tools for each stage.$md$,
  $md$Backlog prioritization is a routine and it never ends. It is like washing the dishes or cutting your nails — that simple.

In this post I try to walk you through the details of that routine, step by step, with the ideas and tools I use. I hope it helps!

The backlog prioritization routine looks like the cycle below:

![](https://static.wixstatic.com/media/b92f60_52807f66d4154e2583de5e31d3c1db6e~mv2.png/v1/fill/w_980,h_648,al_c,q_90,usm_0.66_1.00_0.01,enc_avif,quality_auto/b92f60_52807f66d4154e2583de5e31d3c1db6e~mv2.png)

Example based on a cinema ticket app — [the Miro board is here](https://miro.com/app/board/uXjVON9t52U=/?share_link_id=365207571910).

## 1 — Understand the situation

The best way to understand the situation is to talk to people from every area with a stake in the product, or in the part of the product you are responsible for as a PO/PM.

Try to find out things like:

- Whether the product vision has changed.
- Whether the company's strategy for reaching its goals has changed.
- Whether the product's short or medium-term objectives have changed.
- Whether something you planned went wrong.
- Whether a vendor changed an integration in a way that will break the product and requires action.
- Whether new legal requirements have come from government bodies.
- Whether a new marketing campaign will demand something from your team.
- Whether a feature you left collecting data produced a reasonable result — enough to turn something on or off, change it, improve it or build something new.
- Whether the people doing discovery found a new pain point or something that could be improved.
- Whether the development team has work they cannot stand to go without any longer: automation, tests, refactoring, an upgrade, or adopting a new library.
- Whether there was a spike in complaints to customer support; track the most requested or complained-about items and think with the team about how you can help.
- Whether QA found an urgent bug; also understand the bug list and its priorities.
- Whether a competitor launched something interesting.
- Whether another stakeholder has new work that matters to the company and the product — sales, operations or any other area.

### Tips

- You need to monitor a lot. Try to keep a weekly meeting with the key people from each area to take the temperature.
- A face-to-face conversation (virtual counts) is the best way to assess the situation.
- Monitor your product: metrics will also give you insights.
- Talk to everyone from the CEO to the support agent. Practice empathy.
- Compare what you learned against your work plan, and be comfortable changing something if you need to.

## 2 — Get a classified overview

Once you have assessed the situation, it is time to update or build your overview map.

**I strongly recommend creating a feature map.** I use one inspired by User Story Mapping.

![](https://static.wixstatic.com/media/b92f60_8b11deb0ff4444a48d30da419706948d~mv2.png/v1/fill/w_980,h_314,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/b92f60_8b11deb0ff4444a48d30da419706948d~mv2.png)

The blue blocks are large features or small projects; the yellow ones are features we need to build and deliver (cards).

You do not need to prioritize the work at this overview stage — you only need to classify it. My suggestion is the **MoSCoW** method:

![](https://static.wixstatic.com/media/b92f60_a2ad9bd2cd1a4f57b7055b866a7fb6c6~mv2.png/v1/fill/w_980,h_163,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/b92f60_a2ad9bd2cd1a4f57b7055b866a7fb6c6~mv2.png)

After classifying them, I add the markers below to make the map easier to read:

![](https://static.wixstatic.com/media/b92f60_957e49cb8b36434684b272be63742f84~mv2.png/v1/fill/w_980,h_113,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/b92f60_957e49cb8b36434684b272be63742f84~mv2.png)

Then your map ends up like this:

![](https://static.wixstatic.com/media/b92f60_fb17201bfcef4a7d852f2b16cb74d35f~mv2.png/v1/fill/w_980,h_223,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/b92f60_fb17201bfcef4a7d852f2b16cb74d35f~mv2.png)

### Tips

- Validate your classification with people from the areas that care about the product: customer support, leadership, operations, sales, and so on.
- Make this map your backlog.
- Keep the map up to date.
- Use the Jira backlog — or another tool — only for bugs and other work that does not deliver value to the end customer.
- I used [Miro](https://miro.com/) to build this map.

## 3 — Prioritize and plan

Revisit the classification from the previous stage. See whether it still makes sense; if not, reclassify some cards.

There are many prioritization methods (RICE, Kano, and others). I like the effort vs. impact (value) matrix combined with a prioritized list.

![](https://static.wixstatic.com/media/b92f60_fadcbc8d82a445e2b51ca14e3d24b1ce~mv2.png/v1/fill/w_806,h_758,al_c,q_90,enc_avif,quality_auto/b92f60_fadcbc8d82a445e2b51ca14e3d24b1ce~mv2.png)

**IMPORTANT:** you will not always be able to follow the matrix result, because one feature may depend on another being ready first. Because of that, you should check the sequence by building a prioritized list:

![](https://static.wixstatic.com/media/b92f60_5fbc46d789714990b7b701c0aca0310c~mv2.png/v1/fill/w_980,h_513,al_c,q_90,usm_0.66_1.00_0.01,enc_avif,quality_auto/b92f60_5fbc46d789714990b7b701c0aca0310c~mv2.png)

Notice that whatever ranks first in the effort vs. impact matrix will not always be first when you actually prioritize, because dependencies exist.

> Take dependencies between cards into account, and try to prioritize the cards with the highest business or customer value that carry the highest risk of running into problems during development.

Now that you have a prioritized list, it is time to find an easy way to show your prioritization view. I like to do it like this:

![](https://static.wixstatic.com/media/b92f60_29b8a13b15314ad39a37c8f325214374~mv2.png/v1/fill/w_980,h_382,al_c,q_90,usm_0.66_1.00_0.01,enc_avif,quality_auto/b92f60_29b8a13b15314ad39a37c8f325214374~mv2.png)

Sprints with dates underneath and the cards I believe fit into them — make heavy use of milestones, like the Go-live above.

### Tips

- Bring at least one person from QA, one from Development and one from the business to prioritize work in the effort vs. impact matrix.
- Bring at least one person from Development to build the prioritized list after filling in the matrix. If possible, do both steps together with as many people as you can.
- Present your draft schedule to the developers on your team. Do not ask for an estimate signed in blood — the idea is to get a sense of magnitude: is it 8 or 80, one sprint or two.
- Do not plan more than 3 sprints ahead. Trust me, it is not worth it, because everything can change — and it will.

## 4 — Validate the prioritization and the schedule

By this point the proposal is not really yours anymore, it belongs to the company as a whole, because you have been bringing suggestions, validating and improving ideas with QAs, devs and business people along the way.

But now it is time for one last validation of the schedule you put together. Validate it with your boss, with directors, with partner areas, with vendors — here, the more the better.

This schedule is essential to give you some peace of mind to work, because once validated, you will work on discovery and refinement of each item before it enters development.

### Tips

- Validate with as many people as possible.
- Make the schedule public: nobody can claim they had no visibility (remove the excuses).
- Keep the schedule up to date.
- Do not plan more than 3 sprints ahead.

## 5 — Hand the priority over and gather what is new

This last stage of the cycle is when you actually present the cards to the development team. At many companies this is Planning.

I hope that between stages 4 and 5 you have created all the cards with the information needed for good development and testing.

While handing priority over to the development team, some ideas may come up. Be flexible, listen carefully, check whether they make sense, and do not be afraid to change something at the last minute.

Look at the result of the previous Sprint: something may need to be finished in the next one, and that will affect your schedule and perhaps your prioritization. That result is one of the inputs for understanding the situation.

And that is it — now you go back to stage one and start again for the next sprints!

### Tips

- A tip for your team: during planning, show the direction, where we want to go, what the business objective is, and the impact these new cards will have on customers.
- Leave at least 8 hours of work for the development team to plan how to build the solution, and only then come back with what does and does not fit in the Sprint.
$md$,
  array[$md$backlog$md$,$md$prioritization$md$,$md$product$md$,$md$agile$md$]::text[]
),
(
  $md$apague-cards-com-mais-de-6-meses$md$, 'published', $md$2022-05-28$md$::date,
  $md$Apague cards com mais de 6 meses$md$,
  $md$Se um card está parado no backlog há mais de seis meses, ele não dói o suficiente. Apague — você vai se sentir livre depois disso.$md$,
  $md$Apague todos os cards que foram criados há mais de 6 meses que ainda estão no seu Backlog.

Vai por mim, vai lá e apaga tudo. Se está com receio, apague os com mais de 7 ou 8 meses. Se eles ainda não entraram em desenvolvimento é porque não doem tanto, não prometem tanto resultado ou tem outra coisa de errado com eles.

Você vai se sentir livre depois disso!

![](https://static.wixstatic.com/media/b92f60_07845cee4a1742858b49324e67e63f98~mv2.png/v1/fill/w_374,h_629,al_c,q_85,enc_avif,quality_auto/b92f60_07845cee4a1742858b49324e67e63f98~mv2.png)
$md$,
  array[$md$backlog$md$,$md$priorização$md$,$md$produto$md$]::text[],
  $md$Delete every card older than 6 months$md$,
  $md$If a card has been sitting in your backlog for more than six months, it does not hurt enough. Delete it — you will feel free afterwards.$md$,
  $md$Delete every card in your backlog that was created more than 6 months ago.

Trust me, go there and delete all of it. If you are nervous about it, start with the ones older than 7 or 8 months. If they still have not gone into development, it is because they do not hurt that much, they do not promise much of a result, or there is something else wrong with them.

You will feel free afterwards!

![](https://static.wixstatic.com/media/b92f60_07845cee4a1742858b49324e67e63f98~mv2.png/v1/fill/w_374,h_629,al_c,q_85,enc_avif,quality_auto/b92f60_07845cee4a1742858b49324e67e63f98~mv2.png)
$md$,
  array[$md$backlog$md$,$md$prioritization$md$,$md$product$md$]::text[]
),
(
  $md$nao-existe-apenas-um-caminho-certo$md$, 'published', $md$2022-10-06$md$::date,
  $md$Não existe apenas um caminho certo!$md$,
  $md$Fique de orelha em pé quando quiserem te vender uma verdade absoluta sobre como desenvolver produto. Não existe bala de prata.$md$,
  $md$Não existe um único caminho certo para se desenvolver e entregar um produto digital!

![](https://static.wixstatic.com/media/b92f60_d005e79ee3d945a48408d7cfb0a947c6~mv2.jpeg/v1/fill/w_980,h_442,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/b92f60_d005e79ee3d945a48408d7cfb0a947c6~mv2.jpeg)

Faça um paralelo, pense que você está fazendo uma trilha a pé, seu objetivo é chegar no topo de uma montanha para ver a vista de lá, a trilha é cheia de pedras, tem um caminho já traçado que você consegue perceber, mas em alguns momentos você e seus amigos tomam diferentes decisões sobre onde pisar, no fim todos chegam lá, alguns com mais ou menos esforço, mas todos chegaram lá.

Vejo muita discussão em sites e blogs com coisas como:

- Não faça daily
- Não escreva user story
- Faça 3 reuniões X com o seu time
- Ao invés disso faça aquilo
- Etc…

Acredito que temos que trocar ideias e aprender uns com os outros, mas fique de orelha em pé quando quiserem te vender uma verdade absoluta, pergunte o porquê daquilo e quais foram os prós e contras.

## Não existe apenas um caminho certo!

Cada um de nós trabalha em uma empresa diferente, com times, níveis de maturidade, orçamentos e quantidade de pessoas diferentes. Não existe bala de prata.

Escute de verdade seus clientes e parceiros, busque melhorar a eficiência do processo do seu trabalho, troque ideias com profissionais de outras empresas e construa o seu caminho junto com o seu time!
$md$,
  array[$md$agilidade$md$,$md$produto$md$,$md$liderança$md$]::text[],
  $md$There is not just one right path!$md$,
  $md$Be wary when someone tries to sell you an absolute truth about how to build product. There is no silver bullet.$md$,
  $md$There is no single right path to develop and deliver a digital product!

![](https://static.wixstatic.com/media/b92f60_d005e79ee3d945a48408d7cfb0a947c6~mv2.jpeg/v1/fill/w_980,h_442,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/b92f60_d005e79ee3d945a48408d7cfb0a947c6~mv2.jpeg)

Think of it as a hike. Your goal is to reach the top of a mountain for the view. The trail is full of rocks, there is a visible path already traced out, but at various points you and your friends make different decisions about where to step. In the end everyone gets there — some with more effort, some with less, but everyone gets there.

I see a lot of discussion on sites and blogs along the lines of:

- Do not run a daily
- Do not write user stories
- Run 3 X meetings with your team
- Do that instead of this
- And so on…

I believe we should exchange ideas and learn from each other, but be wary when someone tries to sell you an absolute truth. Ask why, and ask what the trade-offs were.

## There is not just one right path!

Each of us works at a different company, with different teams, maturity levels, budgets and headcount. There is no silver bullet.

Really listen to your customers and partners, work on the efficiency of your own process, exchange ideas with people at other companies, and build your own path together with your team!
$md$,
  array[$md$agile$md$,$md$product$md$,$md$leadership$md$]::text[]
),
(
  $md$aprendizados-para-quem-usa-ou-quer-usar-scrum$md$, 'published', $md$2022-12-22$md$::date,
  $md$Aprendizados para quem usa ou quer usar Scrum$md$,
  $md$Quinze aprendizados práticos sobre Sprints, priorização, cerimônias e escopo — coisas que eu gostaria de ter sabido antes de errar.$md$,
  $md$![](https://static.wixstatic.com/media/b92f60_555fd61b7efa43f2981c227f41e1bbea~mv2.jpg/v1/fill/w_640,h_427,al_c,q_80,enc_avif,quality_auto/b92f60_555fd61b7efa43f2981c227f41e1bbea~mv2.jpg)

**1.** Não espere 100% dos cards entregues de uma Sprint, mas uma taxa entre 85% e 110%. **Por quê?** Porque a vida muda, coisas acontecem, fornecedores pisam na bola, pessoas ficam doentes, tecnologias falham, etc… Uma taxa como essa já vai te dar uma ótima previsibilidade.

**2.** Deixe clara a **prioridade dos cards dentro da sua Sprint**. Se não der para entregar todos, que sejam entregues os mais importantes. **Por quê?** Mesma resposta do item acima, mas com uma dica: certifique-se de que todos do time entenderam isso.

**3.** Scrum não é bom para quem **não tem um objetivo**. **Por quê?** Porque se a sua empresa não tiver um objetivo claro de onde quer chegar e como, a chance de alterarem o escopo no meio da Sprint porque alguma coisa aconteceu é enorme.

**4.** Scrum não é bom para times **orientados a gambiarra**. **Por quê?** Porque quando esse produto entrar em produção vai aparecer uma enxurrada de bugs todos os dias, e isso vai atropelar o planejamento da Sprint, alterando muito o escopo e deixando o time meio maluco. **Os bugs serão corrigidos com mais gambiarras que gerarão mais bugs, levando à loucura ao infinito.**

**5.** Tente levar para a Sprint um escopo **equilibrado** entre demandas de front, de back e de outra tecnologia que vocês tiverem. **Por quê?** Porque o time de desenvolvimento vai montar uma estratégia para entregar o máximo da Sprint baseado no conhecimento e no perfil das pessoas. Aqui é importante reforçar a prioridade da Sprint, para não entregarem cards menos importantes por causa do conhecimento do dev em vez de um do topo da lista.

**6.** Um escopo dos sonhos de uma Sprint seria algo **equilibrado** entre novas features, melhorias, bugs e débitos técnicos. **Por quê?** Para que tudo caminhe lado a lado: os devs ficariam felizes com os débitos técnicos sendo resolvidos, os clientes com os bugs tratados e novas funções, etc… Mas o mundo não é tão perfeito assim, logo você terá sprints mais focadas em um ou outro tipo de demanda — e está tudo bem.

**7.** Uma demanda pode não caber em apenas uma Sprint, e está tudo bem. Imagino que você já saiba o conceito de quebrar e refinar as demandas para que sejam do menor tamanho possível. Agora imagine que você já discutiu com o time e não dá para quebrar mais: a demanda é grande mesmo e não vai caber na sua Sprint de 2 semanas. Faça um acordo com o time de **entregar em 2 sprints**.

**8.** Não aumente a quantidade de dias da sua Sprint para atingir um objetivo específico ou por causa de um momento de **crise na sua empresa**. Eu já fiz isso com a minha equipe em algumas situações e todas se mostraram erradas. Mantenha o tamanho da sua Sprint — as Sprints são curtas exatamente para você poder avaliar se estão no caminho correto, se o que foi feito foi efetivo ou não, conhecer novidades que surgiram nos últimos dias e ajustar as demandas para a próxima rodada.

**9.** Mantenha a consistência das suas cerimônias de demonstração e retrospectiva. **Por quê?** Só a consistência vai te levar no caminho da melhoria contínua, seja do produto desenvolvido ou dos processos internos do time. Não subestime o poder disso no médio prazo. Se vocês não tiverem consistência, a cerimônia cai em **descrédito**.

**10.** Não quer fazer **reunião diária**, quer fazer só alguns dias por semana ou só por texto? Está tudo bem, desde que:

- O time esteja entregando na taxa esperada (item 1).
- A comunicação do time funcione, dando visibilidade dos problemas para pedir ajuda o quanto antes (às vezes dá tempo de salvar e entregar um item que estava com impedimento) e informar com antecedência as pessoas que esperavam uma funcionalidade que não será entregue, tentando uma negociação.

**11.** Faça a reunião de planejamento com o time em um **nível mais alto**: explique quais problemas serão resolvidos, o impacto na vida do cliente e leve requisitos claros. Sempre que possível, apresente previamente para alguns devs o que será levado para a reunião de planejamento, para refinar as demandas. **Por quê?** Porque as suas demandas vão chegar refinadas e as pessoas vão saber o motivo de estar trabalhando na demanda A ou B.

**12.** Após a reunião de planejamento, **dê um dia ou algumas horas** para o time de desenvolvimento:

- Planejar o desenvolvimento de cada item (a solução técnica).
- Quebrar as demandas em sub-tasks.
- Definir responsáveis para cada sub-task.
- Pontuar as demandas, se eles quiserem. Particularmente não vejo sentido em pontuar — acredito mais em comprometimento da equipe em entregar o que ela prometeu.
- Definir quais demandas caberão ou não na Sprint.

**13.** Tente fazer com que o time de desenvolvimento apresente a reunião de demonstração. **Por quê?** **Porque a entrega foi desse time** — nada mais justo que eles apresentarem. Ajude o time se estiverem falando muito **"tecniquês"**: explique que é uma reunião para qualquer pessoa da empresa interessada naquele assunto, e elas não são devs. Anote as sugestões dadas durante a reunião.

**14.** Se você tiver que mudar o escopo da Sprint colocando um novo card, reúna o time e negocie. Veja se cabe sem tirar nenhum outro card ou definam juntos qual vai sair. **Por quê?** Porque se tudo correu como o previsto não vai caber mais trabalho no mesmo prazo, e você já precisa **comunicar** quem está esperando a função do card que sairá da Sprint.

**15.** Registre os bugs de uma demanda ainda dentro da Sprint em uma **sub-task** do tipo bug. **Por quê?** Às vezes identificamos vários pequenos problemas durante o desenvolvimento de uma função, e registrá-los nos comentários do card não é legal — pode ficar difícil identificar se o erro já foi corrigido ou não, e a quantidade de retrabalho entre dev e QA.

## Vai por mim

- Scrum é bom (um dia vou escrever por que Scrum é bom).
- A diretoria esquece dos débitos técnicos combinados e vai te cobrar depois: "por que isso está assim e não assado?".
- Sempre, sempre desenhe uma funcionalidade da melhor maneira possível. Alguns débitos técnicos se vingam depois de lançados.

Quero manter esse post vivo e ir adicionando coisas aqui. Se sentiu falta de algo ou tem dúvida, por favor me envie.
$md$,
  array[$md$scrum$md$,$md$agilidade$md$,$md$liderança$md$,$md$produto$md$]::text[],
  $md$Lessons for anyone using — or about to use — Scrum$md$,
  $md$Fifteen practical lessons about Sprints, prioritization, ceremonies and scope — things I wish I had known before getting them wrong.$md$,
  $md$![](https://static.wixstatic.com/media/b92f60_555fd61b7efa43f2981c227f41e1bbea~mv2.jpg/v1/fill/w_640,h_427,al_c,q_80,enc_avif,quality_auto/b92f60_555fd61b7efa43f2981c227f41e1bbea~mv2.jpg)

**1.** Do not expect 100% of a Sprint's cards to be delivered — expect a rate between 85% and 110%. **Why?** Because life changes, things happen, vendors drop the ball, people get sick, technology fails. A rate like that already gives you excellent predictability.

**2.** Make the **priority of the cards inside your Sprint** explicit. If not everything can be delivered, let the most important things be delivered. **Why?** Same answer as above, with one tip: make sure everyone on the team understood it.

**3.** Scrum is not good for teams **without a goal**. **Why?** Because if your company has no clear objective of where it wants to go and how, the chance of someone changing scope mid-Sprint because "something happened" is enormous.

**4.** Scrum is not good for teams **oriented toward quick hacks**. **Why?** Because once that product hits production, a flood of bugs will show up every day, running over the Sprint plan, changing scope heavily and driving the team a little crazy. **The bugs get fixed with more hacks, which generate more bugs, leading to madness without end.**

**5.** Try to bring a **balanced** scope into the Sprint across front end, back end and whatever other technology you have. **Why?** Because the development team will build a strategy to deliver as much of the Sprint as possible based on people's knowledge and profile. Here it is important to reinforce the Sprint priority, so they do not deliver less important cards because of a given dev's expertise instead of one from the top of the list.

**6.** A dream Sprint scope would be **balanced** across new features, improvements, bugs and technical debt. **Why?** So everything moves forward side by side: devs are happy seeing tech debt resolved, customers are happy with bugs fixed and new features. But the world is not that perfect, so you will have Sprints more focused on one type of work than another — and that is fine.

**7.** A piece of work may not fit into a single Sprint, and that is fine. I assume you already know the idea of splitting and refining work into the smallest possible size. Now imagine you have already discussed it with the team and it cannot be split further: the work really is big and will not fit into your 2-week Sprint. Agree with the team to **deliver it across 2 sprints**.

**8.** Do not extend the length of your Sprint to hit a specific goal or because of a **crisis at your company**. I have done this with my team in a few situations and every one of them turned out to be a mistake. Keep your Sprint length — Sprints are short precisely so you can assess whether you are on the right track, whether what was built was effective, learn what is new from the last few days, and adjust the work for the next round.

**9.** Keep your review and retrospective ceremonies consistent. **Why?** Only consistency takes you down the path of continuous improvement, whether of the product or of the team's internal processes. Do not underestimate the power of that over the medium term. Without consistency, the ceremony loses **credibility**.

**10.** Do not want to run a **daily**? Want to run it only a few days a week, or only in writing? That is fine, as long as:

- The team is delivering at the expected rate (item 1).
- Team communication works, giving visibility of problems so people can ask for help as early as possible (sometimes there is still time to rescue a blocked item) and warn in advance the people who were expecting a feature that will not be delivered, so a negotiation is possible.

**11.** Run the planning meeting with the team at a **higher level**: explain which problems will be solved, the impact on the customer's life, and bring clear requirements. Whenever possible, walk some devs through what you plan to bring to the meeting beforehand, so the work gets refined. **Why?** Because your items will arrive refined and people will know why they are working on A or B.

**12.** After the planning meeting, **give the development team a day or a few hours** to:

- Plan the implementation of each item (the technical solution).
- Split the work into sub-tasks.
- Assign owners for each sub-task.
- Point the items, if they want to. Personally I do not see the point in story points — I believe more in the team's commitment to deliver what it promised.
- Decide what will and will not fit in the Sprint.

**13.** Try to have the development team run the review meeting. **Why?** **Because the delivery was theirs** — it is only fair they present it. Help the team if they drift into **jargon**: explain that this is a meeting for anyone in the company interested in the topic, and they are not developers. Write down the suggestions raised during the meeting.

**14.** If you have to change Sprint scope by adding a new card, gather the team and negotiate. See whether it fits without removing anything, or decide together what comes out. **Why?** Because if everything went as planned, no extra work fits in the same timeframe — and you now need to **communicate** with whoever was waiting on the card that is leaving the Sprint.

**15.** Record bugs found during the Sprint as a **sub-task** of type bug on the item itself. **Why?** Sometimes we spot several small problems while a feature is being built, and logging them in the card's comments is not great — it becomes hard to tell whether an error was already fixed, and hard to see how much rework is happening between dev and QA.

## Trust me on these

- Scrum is good (one day I will write about why Scrum is good).
- Leadership forgets about the technical debt that was agreed and will come back later asking "why is this like that?".
- Always, always design a feature the best way you can. Some technical debt takes its revenge after launch.

I want to keep this post alive and keep adding to it. If you feel something is missing, or you have a question, please send it over.
$md$,
  array[$md$scrum$md$,$md$agile$md$,$md$leadership$md$,$md$product$md$]::text[]
),
(
  $md$instrumento-para-priorizar-o-backlog$md$, 'published', $md$2023-01-18$md$::date,
  $md$Um instrumento para te ajudar a priorizar o backlog$md$,
  $md$O instrumento EOC — Estratégia, Objetivos e Clientes. Um questionário com pesos que torna explícito o raciocínio por trás de cada decisão de priorização.$md$,
  $md$![](https://static.wixstatic.com/media/b92f60_d2c25afe33b04263985048006388211e~mv2.jpg/v1/fill/w_640,h_427,al_c,q_80,enc_avif,quality_auto/b92f60_d2c25afe33b04263985048006388211e~mv2.jpg)

**Fiz esse instrumento com 4 objetivos:**

1. Tentar encontrar o peso ideal entre estratégia, objetivos do negócio e dores dos clientes na tomada de decisão.
2. Evitar abstrações, ser o mais objetivo possível e de fácil entendimento.
3. Deixar claro o raciocínio adotado na priorização para qualquer pessoa da empresa interessada no assunto.
4. Ajudar POs e PMs na priorização de novas funções ou melhorias em um sistema ou produto digital que já está em uso.

## O Instrumento EOC

[Acesse a planilha aqui](https://docs.google.com/spreadsheets/d/1ybEQn5jOlXdaWz1YmbQB6DEQKucwEkThg7TcT41yA44/edit?usp=sharing)

### Explicação rápida

Sim, parece que é só um questionário no Google Spreadsheets, mas preste atenção nos detalhes.

**Primeira aba**

*As perguntas.* Aqui devem estar as perguntas que representam os problemas e expectativas dos clientes, e os objetivos do seu time, empresa ou produto.

*Interessados.* Deixe claro quem tem interesse ou vai ser impactado com a pergunta.

*Os pesos.* Processos de tomada de decisão são baseados no que mais importa para alguém. Algumas coisas importam mais que outras, e assim as pessoas tomam as suas decisões. Os pesos aqui representam isso: o que mais importa nesse momento na estratégia da sua empresa.

*Os indicadores.* Tente encontrar perguntas que vão mexer em algum indicador do seu negócio e deixe claro esse vínculo — lembre-se de que é um instrumento para todos os interessados.

**Segunda aba — Questionário e priorização**

Aqui você cadastra as suas demandas com o assunto, título e uma breve descrição com a situação e características do que você quer fazer. Responda apenas "Sim" ou "Não" para cada pergunta; cada resposta influencia na priorização da demanda.

Ao final, informe os componentes envolvidos nessa demanda (exemplo: back, front, back e front) e o esforço — trata-se apenas de uma noção de grandeza que você mesmo pode informar com base na sua experiência.

Todos os itens dessa aba são importantes para te ajudar a priorizar. Os dois últimos te ajudam a visualizar o equilíbrio entre componentes e esforço das suas demandas.

Pareceu simples? Era para ser simples mesmo.

### Sugestão de como implementar no seu time

Em primeiro lugar, levante as perguntas mais relevantes para o seu time. Converse com o máximo de pessoas e faça seu filtro. Sugestão: tente manter em torno de 10 perguntas.

Itens importantes na hora de levantar as perguntas:

**1. Quais são os objetivos do meu time?** Exemplos: aumentar o faturamento; reduzir o custo; suportar escala de X requisições por dia; atingir X mil clientes até o mês Y; lançar o produto Z até o mês A.

**2. O que é mais importante para a minha empresa nesse momento e em que meu time pode ajudar?** Exemplos: reduzir o CAC; aumentar o TPV; reduzir churn.

**3. Como eu sei o que o cliente quer?** Exemplos: entrevistas; reclamações no suporte; reclamações nas lojas de aplicativos; benchmark.

Tente equilibrar essas perguntas entre cliente, empresa e tecnologia — ou outra área que você atenda.

Definiu as perguntas junto com as pessoas interessadas? O segundo passo é levar esse grupo de perguntas aos interessados no assunto (o time, superiores, diretoria, marketing, atendimento) e definir o peso que cada uma terá no processo de tomada de decisão.

O terceiro e último passo é preencher a segunda aba com as suas demandas e ordená-las. Faça isso frequentemente para manter uma visão atualizada. Dica: preencha, ordene e veja se faz sentido — provavelmente vocês vão recalibrar os pesos depois da primeira visão ordenada.

Lembre-se: esse instrumento é para te ajudar. Você ainda sempre terá que olhar para diversas áreas e informações dentro da sua empresa e decidir o que é melhor na hora de pedir algo novo para o time.

---

**Obs. 1:** fique à vontade para copiar, editar e divulgar esse instrumento; peço apenas que cite a fonte.

**Obs. 2:** apelidei o instrumento de EOC para lembrar de Estratégia, Objetivos e Clientes.

**Última obs.:** já estou gerando outro instrumento desse para priorizar débitos técnicos e bugs.
$md$,
  array[$md$backlog$md$,$md$priorização$md$,$md$produto$md$,$md$ferramentas$md$]::text[],
  $md$An instrument to help you prioritize the backlog$md$,
  $md$The EOC instrument — Strategy, Objectives and Customers. A weighted questionnaire that makes the reasoning behind every prioritization decision explicit.$md$,
  $md$![](https://static.wixstatic.com/media/b92f60_d2c25afe33b04263985048006388211e~mv2.jpg/v1/fill/w_640,h_427,al_c,q_80,enc_avif,quality_auto/b92f60_d2c25afe33b04263985048006388211e~mv2.jpg)

**I built this instrument with 4 goals:**

1. To find the right balance between strategy, business objectives and customer pain in decision making.
2. To avoid abstractions — to be as objective and easy to understand as possible.
3. To make the reasoning behind prioritization clear to anyone in the company who cares about it.
4. To help POs and PMs prioritize new features or improvements in a system or digital product already in use.

## The EOC instrument

[Open the spreadsheet here](https://docs.google.com/spreadsheets/d/1ybEQn5jOlXdaWz1YmbQB6DEQKucwEkThg7TcT41yA44/edit?usp=sharing)

### Quick explanation

Yes, it looks like just a questionnaire in Google Sheets, but pay attention to the details.

**First tab**

*The questions.* These should be the questions that represent customer problems and expectations, and the objectives of your team, company or product.

*Stakeholders.* Make it clear who has an interest in, or will be affected by, each question.

*The weights.* Decision-making processes are based on what matters most to someone. Some things matter more than others, and that is how people decide. The weights represent exactly that: what matters most right now in your company's strategy.

*The indicators.* Try to find questions that move some indicator of your business, and make that link explicit — remember this is an instrument for all stakeholders.

**Second tab — Questionnaire and prioritization**

Here you register your work items with a subject, a title and a short description of the situation and characteristics of what you want to do. Answer only "Yes" or "No" to each question; every answer influences the item's priority.

At the end, note the components involved (for example: back end, front end, or both) and the effort — just a sense of magnitude that you can provide yourself based on experience.

Every item on this tab helps you prioritize. The last two help you see the balance between components and effort across your work.

Looked simple? It was meant to be.

### How to roll this out with your team

First, gather the questions most relevant to your team. Talk to as many people as you can and then filter. Suggestion: aim for around 10 questions.

Important things to consider while gathering the questions:

**1. What are my team's objectives?** Examples: increase revenue; reduce cost; support a scale of X requests per day; reach X thousand customers by month Y; launch product Z by month A.

**2. What matters most to my company right now, and where can my team help?** Examples: reduce CAC; increase TPV; reduce churn.

**3. How do I know what the customer wants?** Examples: interviews; support complaints; app store reviews; benchmarking.

Try to balance these questions across customer, company and technology — or whatever other area you serve.

Defined the questions together with your stakeholders? The second step is to take that set of questions to the people who care (the team, your managers, leadership, marketing, support) and define the weight each one carries in the decision-making process.

The third and final step is to fill in the second tab with your work items and rank them. Do this regularly to keep an up-to-date view. Tip: fill it in, rank it, and see whether it makes sense — you will most likely recalibrate the weights after the first ranked view.

Remember: this instrument is there to help you. You will still always have to look across several areas and sources of information inside your company and decide what is best when asking the team for something new.

---

**Note 1:** feel free to copy, edit and share this instrument; I only ask that you credit the source.

**Note 2:** I nicknamed it EOC as a reminder of Strategy (*Estratégia*), Objectives and Customers.

**Last note:** I am already building another version of this instrument to prioritize technical debt and bugs.
$md$,
  array[$md$backlog$md$,$md$prioritization$md$,$md$product$md$,$md$tools$md$]::text[]
)
on conflict (slug) do nothing;
