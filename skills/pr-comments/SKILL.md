---
name: pr-comments
description: >-
    You should use this skill when:
    asked to handle or answer the comments on a pull request,
    asked which review comments are still open,
    asked to sort the feedback of reviewers or AI bots on a pull request
argument-hint: "Pull request number or URL"
---

# PR comments

Find the unanswered comments on a pull request, sort them by kind, and prepare an answer or a
decision for each one. Post a reply on GitHub only after the user confirms it.

## DependsOn

- [decision-flow](/skills/decision-flow/SKILL.md)

## Procedure

1. Take the pull request that the user names. If the user names none, take the pull request
   of the current branch
2. Read all review threads and all general comments of the pull request with the GitHub tools
3. Keep the unanswered comments
   - A review thread that is not resolved and whose last comment is by a reviewer
   - A general comment with no later comment by the author of the pull request
4. Mark a comment as AI when its author has `type: Bot` or a login that ends in `[bot]`,
   such as `copilot-pull-request-reviewer[bot]`
   - When the author data has no type, compare the login with the known AI logins:
     `Copilot`, `copilot-pull-request-reviewer`, `coderabbitai`, `gemini-code-assist`, `claude`
   - The mark only labels the comment in the decision tree. Handle an AI comment like any other
5. Sort each comment into one kind
   - Question: find the answer in the codebase and draft a reply
   - Suggestion, an optional idea or a GitHub `suggestion` block: ask the user whether to
     accept it
   - Code change request, a change that the reviewer requires: ask the user whether and where
     to change the code. Offer options that the codebase supports, such as the places that
     already follow the requested pattern
6. Run `decision-flow` on the suggestions and the code change requests
   - Each comment is one decision. Put `AI` in front of the decision for an AI comment
   - Give the author and a link to the comment in each decision
7. Show each draft reply to the user. Post a reply on GitHub only after the user confirms its
   text, and post it in the thread of its comment
