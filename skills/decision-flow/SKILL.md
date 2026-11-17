---
name: decision-flow
description: >-
    You should use this skill when:
    asked to help make decisions based on the conversation so far,
    asked what is left to decide before work starts,
    a discussion ends with several open options and no chosen one
---

# Decision flow

Walk the user through the open decisions of the conversation in short rounds of 1-3 questions,
with a summary after each round, until no decision is left open. The skill sets the format of
the rounds. The decisions themselves come from the conversation.

## Procedure

1. Read the whole conversation and list the open decisions: questions without an answer,
   options offered but not chosen, and assumptions nobody confirmed
   - Drop a decision the user already made, and a fact you can find with tools yourself
2. When two or more decisions remain, show the decision tree before the first round
   - One nested markdown list: a decision is an item, its options are child items, and a
     decision that only one option opens sits under that option
   - Give each option its amount of work: `S` (minutes), `M` (about an hour), `L` (a day or
     more), with a few words on what the work is
   - Mark the decisions of the current round with `(now)`
3. Ask one round of 1-3 questions in one form of the question tool, with options to pick
   - Take decisions from the top of the tree first: their answers prune the branches below
   - Put the recommended option first and make it the default. Name the work in its label
4. After the answers, write a summary of 1-2 paragraphs: what the user chose, what it means for
   the work, and which branches dropped out
5. Show the remaining tree with the decisions added by the answers, and start the next round
   from step 3
6. When no decision is left, list every decision in one line each and name the next action.
   Start the work only when the user asks

## Tree example

```markdown
- Storage for the cache (now)
  - SQLite - M: schema and migration
    - Clear old entries on start or by a timer? (now)
      - On start - S
      - By a timer - M: a background task
  - Files on disk - S: one directory per key
- Expose the cache in the settings UI? (now)
  - No - S
  - Yes - L: a new page and its tests
```
