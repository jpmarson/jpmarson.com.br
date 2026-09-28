---
title: O gestor que voltou a codar (e o que isso mudou nas minhas decisões)
date: 2026-09-27
tags: vibe coding, gestão de produto, liderança
summary: Passei anos gerenciando quem escreve código sem escrever nenhuma linha. Voltar a construir — com IA do lado — mudou menos a minha produtividade e mais a qualidade das minhas perguntas.
draft: false
---

Não sou desenvolvedor. Faz mais de quinze anos que meu trabalho é outro: entender por que estamos construindo algo, alinhar negócio e tecnologia, garantir que o que foi prometido chegue. Escrever código era coisa que eu tinha feito em outra vida, e mal.

Nos últimos meses isso mudou. Não porque virei engenheiro, mas porque a barreira de entrada caiu tanto que deixou de fazer sentido não construir.

## O que eu construí

Nada glamouroso. Ferramentas internas que resolviam dores que eu mesmo sentia:

- Um pipeline em Python que observa uma pasta, detecta quando um relatório de portfólio é atualizado e dispara um cartão no Teams com a classificação de farol de cada grupo.
- Um instrumento de classificação de complexidade de projetos — uma matriz de pontuação com regras de exceção — que virou uma página HTML que o time usa para decidir alocação.
- Um painel dos projetos prioritários, que eu abro toda segunda-feira.

Cada uma dessas coisas teria virado um pedido para o time de engenharia. Um pedido que entraria numa fila, competiria com entregas de produto e provavelmente nunca chegaria ao topo — corretamente, porque produto vem antes de ferramenta interna de gestor.

## A parte que ninguém comenta

O ganho óbvio é de velocidade. O ganho real é outro.

Quando você constrói, mesmo mal, você passa a entender o formato do problema. E o formato do problema é exatamente o que se perde na tradução entre quem pede e quem implementa.

Antes, eu perguntava "dá para colocar isso no relatório?". Hoje eu sei que a pergunta certa quase sempre é outra: de onde vem esse dado, com que frequência ele muda, o que acontece quando ele falta. São perguntas que eu não sabia fazer porque nunca tinha esbarrado nelas.

> A habilidade que mudou não foi programar. Foi saber onde a complexidade se esconde.

Isso muda a conversa com engenharia. Quando um time diz que algo é complexo, eu já não trato como caixa-preta nem — pior — desconfio. Consigo perguntar onde está a complexidade, e a resposta vira uma decisão conjunta em vez de uma estimativa que eu aceito ou contesto sem base.

## O risco que eu levo a sério

Existe um lado ruim nisso, e ele é real.

Um gestor que constrói rápido pode começar a achar que construir é fácil. É a armadilha: o protótipo que eu faço numa noite não tem testes, não tem tratamento de erro, não escala, não tem quem mantenha. Ele resolve o meu problema, para mim, hoje. Chamar isso de software pronto seria desonesto — e transformar essa sensação em pressão sobre o time seria pior ainda.

Aprendi isso da maneira previsível: uma das minhas automações ficou quebrada por dias sem que ninguém percebesse, porque eu não tinha construído nenhum mecanismo de alerta de falha. Funcionava em silêncio e falhava em silêncio. Um engenheiro teria previsto isso na primeira hora.

Então a régua que uso é simples: o que eu construo é ferramenta de gestão, não produto. No momento em que outra pessoa depende daquilo para trabalhar, aquilo precisa de alguém que saiba o que está fazendo.

## O que eu recomendaria a outro gestor

Comece por algo que só você usa. Uma planilha que você refaz toda semana, um relatório que você monta na mão, um cálculo que você repete. Construa a versão feia. Use no seu dia a dia por um mês.

Você vai aprender mais sobre o seu próprio produto nesse mês do que em qualquer reunião de arquitetura — não porque a reunião seja inútil, mas porque agora você chega nela com contexto.

E, principalmente: continue tratando o trabalho de quem faz isso profissionalmente com o respeito que ele merece. A IA encurtou a distância entre a ideia e o protótipo. Ela não encurtou quase nada da distância entre o protótipo e o sistema em produção — e é aí que mora o ofício.
