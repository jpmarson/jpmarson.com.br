---
title: The backlog prioritization routine
date: 2022-05-26
tags: backlog, prioritization, product, agile
summary: Backlog prioritization is a routine and it never ends — it is like doing the dishes. Here is the cycle I use, step by step, with the tools for each stage.
draft: false
---

Backlog prioritization is a routine and it never ends. It is like washing the dishes or cutting your nails — that simple.

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
