---
name: pr-comments
description: >-
    You should use this skill when:
    asked to handle or answer the comments on a pull request,
    asked which review comments are still open,
    asked to sort the feedback of reviewers or AI bots on a pull request
argument-hint: "Pull request, issue, or nothing for the current branch"
---

# PR comments

Collect the unanswered comments on the pull requests of a task, sort them by kind, and prepare
an answer or a decision for each one in the chat. The skill publishes nothing: the user posts
the replies.

## DependsOn

- [decision-flow](/skills/decision-flow/SKILL.md)

## Procedure

1. Find the pull requests
   - Take the pull requests or the issue that the user names
   - If the user names nothing, start from the current branch. Find the pull request of the
     branch and the issue that the code implements, by the branch name, the pull request
     description, and the commit messages. Read the issue
   - When the issue links to more than one pull request, take all of them
2. Read all review threads and all general comments of each pull request with the tools of its
   platform. Put the comments of all pull requests into one queue and handle them in turn
3. Keep the unanswered comments
   - A review thread that is not resolved and whose last comment is by a reviewer
   - A general comment with no later comment by the author of the pull request
4. Mark a comment as AI when the name of its author contains `bot` or `ai`, or when the
   context of the project shows that the author is an AI agent
   - The mark only labels the comment in the decision tree. Handle an AI comment like any other
5. Sort each comment into one kind
   - Question: find the answer in the codebase and draft a reply
   - Suggestion, an optional idea or a ready replacement text: ask the user whether to
     accept it
   - Code change request, a change that the reviewer requires: ask the user whether and where
     to change the code. Offer options that the codebase supports, such as the places that
     already follow the requested pattern
6. Run `decision-flow` on the suggestions and the code change requests
   - A comment gives as many decisions as it holds. Put `AI` in front of each decision from
     an AI comment
   - Give the pull request, the author, and a link to the comment in each decision
7. Write each draft reply in the chat, with a link to its comment
