---
title: The manager who started building again (and what it changed)
date: 2026-09-27
tags: vibe coding, product management, leadership
summary: I spent years managing people who write code without writing a line myself. Going back to building — with AI alongside — changed my productivity less than it changed the quality of my questions.
draft: false
---

I am not a developer. For more than fifteen years my job has been something else: understanding why we are building a thing, aligning business and technology, making sure what was promised actually lands. Writing code was something I had done in another life, and badly.

That changed over the last few months. Not because I became an engineer, but because the barrier to entry dropped so far that not building stopped making sense.

## What I built

Nothing glamorous. Internal tools that solved problems I felt myself:

- A Python pipeline that watches a folder, detects when a portfolio report is updated, and fires a card into Teams with the traffic-light status of each group.
- A project complexity scoring instrument — a weighted matrix with override rules — that became an HTML page the team now uses for allocation decisions.
- A dashboard of priority projects that I open every Monday morning.

Each of those would otherwise have been a request to the engineering team. A request that would join a queue, compete with product delivery, and most likely never reach the top — correctly so, because product work comes before a manager's internal tooling.

## The part nobody talks about

The obvious gain is speed. The real gain is something else.

When you build, even badly, you start to understand the *shape* of the problem. And the shape of the problem is exactly what gets lost in translation between the person asking and the person implementing.

I used to ask "can we add this to the report?". Today I know the right question is almost always a different one: where does this data come from, how often does it change, what happens when it is missing. Questions I did not know to ask because I had never run into them.

> The skill that changed was not programming. It was knowing where complexity hides.

That changes the conversation with engineering. When a team says something is complex, I no longer treat it as a black box — nor, worse, with suspicion. I can ask where the complexity sits, and the answer becomes a shared decision instead of an estimate I either accept or push back on with no basis.

## The risk I take seriously

There is a bad side to this, and it is real.

A manager who builds quickly can start to believe building is easy. That is the trap: the prototype I put together in an evening has no tests, no error handling, does not scale, and has no one to maintain it. It solves my problem, for me, today. Calling that finished software would be dishonest — and turning that feeling into pressure on the team would be worse.

I learned this the predictable way. One of my automations sat broken for days without anyone noticing, because I had never built any failure alerting. It worked silently and it failed silently. An engineer would have anticipated that in the first hour.

So the line I hold is simple: what I build is management tooling, not product. The moment another person depends on it to do their job, it needs someone who knows what they are doing.

## What I would tell another manager

Start with something only you use. A spreadsheet you rebuild every week, a report you assemble by hand, a calculation you repeat. Build the ugly version. Use it daily for a month.

You will learn more about your own product in that month than in any architecture meeting — not because the meeting is useless, but because you now walk into it with context.

And above all: keep treating the work of people who do this professionally with the respect it deserves. AI collapsed the distance between an idea and a prototype. It has collapsed very little of the distance between a prototype and a system in production — and that is where the craft lives.
