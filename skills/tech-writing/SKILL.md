---
name: tech-writing
description: >-
  Use this skill when writing or reviewing technical documentation or
  developer-facing prose, especially README files, API documentation, runbooks,
  and release notes. Use the structural guidance for ADRs, design docs, PR
  descriptions, and commit messages. Also use it when the user asks to rewrite
  or tighten technical text, or explicitly mentions Google style. Do not use it
  for general conversational answers unless the user asks for a documentation-
  style rewrite.
argument-hint: "Text to write or review, plus its intended audience and genre"
user-invocable: true
---

# Technical writing

Write and review developer-facing prose using a concise, project-aware approach
based on the [Google developer documentation style guide](https://developers.google.com/style).
These principles inform the writing; they do not require the result to be
"Google-compatible." Follow project-specific conventions and choose what best
serves the intended reader.

## Editorial hierarchy

1. Follow project-specific terminology and conventions.
2. Use the principles in this skill when project guidance is silent.
3. Use third-party references only when the first two sources do not answer the
   question.

## Decide the scope

- Apply the full style guidance to README files, API references, runbooks,
  procedures, release notes, onboarding docs, error messages, and code comments
  intended for other developers.
- Apply structural guidance only to ADRs, design docs, RFCs, PR descriptions,
  commit messages, and technical articles. Preserve the argument, trade-offs,
  and appropriate voice these genres need.
- Do not apply this skill to conversational answers, brainstorming, opinion
  pieces, or a user-requested voice unless the user asks for a documentation-
  style rewrite.

Follow project-specific terminology and conventions first. Treat the Google
guide as recommendations, not rigid rules. Depart from a recommendation when
doing so improves clarity, and stay consistent within the document.

## Write for the reader

- Lead with the answer or action the reader needs; put background afterward.
- Put conditions before instructions so readers can skip steps that do not
  apply.
- Use numbered lists for sequences and bullets for unordered items.
- Keep one main idea per paragraph and make headings self-contained.
- Prefer active voice and present tense. Name the actor when it is known.
  Passive voice is fine when the actor is irrelevant or the object matters
  more, as in "The file is saved."
- Use real verbs instead of nominalizations.
- Address the reader directly when the language supports it. Avoid ambiguous
  uses of "we."
- Keep sentences short, with one idea per sentence.
- Be specific and avoid abstractions.
- Cut filler, bureaucratic phrasing, and redundancy.
- Remove excessive claims, hedges, unexplained jargon, idioms, and
  pre-announcements.
- Use a conversational, friendly, respectful tone without slang or excessive
  formality.
- Avoid anthropomorphism and culture-specific references. Expand abbreviations
  on first use.

### Prose style examples

```text
1. Remove bureaucratic and verbose phrases
   ✘ "For the purpose of increasing the efficiency of the system, a process of
       optimization is currently being conducted."
   ✔ "We are optimizing the system."

2. Prefer active voice over passive voice
   ✘ "The configuration file was modified to enable logging."
   ✔ "Modify the configuration file to enable logging."

3. Replace noun-based verbs with actual verbs
   ✘ "The execution of the installation can be performed by the administrator."
   ✔ "The administrator installs the software."

4. Be specific, avoid abstractions
   ✘ "The system provides a wide range of options for the user."
   ✔ "The system lets you export data to CSV, JSON, or XML."

5. Keep sentences short and clear
   ✘ "When the application encounters a situation in which the required
       library is missing, it will, in accordance with the predefined logic,
       generate an error message that informs the user about the problem."
   ✔ "If the library is missing, the app shows an error."

6. Cut filler and empty phrases
   ✘ "It should be noted that the installation process will take some time."
   ✔ "The installation takes several minutes."

7. Use verbs to make instructions actionable
   ✘ "The activation of the service is possible via the dashboard."
   ✔ "Activate the service in the dashboard."

8. Remove redundancy and duplication
   ✘ "Each and every user must always follow the mandatory rules."
   ✔ "Each user must follow the rules."

9. Address the reader directly ("you")
   ✘ "The feature can be used by the end user for configuration."
   ✔ "You can configure this feature."

10. Prefer present tense for clarity
    ✘ "The system was designed to support multiple platforms."
    ✔ "The system supports multiple platforms."
```

## Format technical content

- Use code font for filenames, symbols, flags, status codes, output,
  placeholders, and configuration keys.
- Limit bold as MD5 in
  [markdown.instructions.md](../../rules/markdown.instructions.md) says; UI
  elements and run-in headings are not exceptions. Do not start every item of a
  list with a bold lead-in (`- **Term:** description`). Use italics sparingly,
  and reserve underlining for links.
- Use descriptive link text instead of `click here` or a bare URL.
- Use unambiguous dates such as `2026-08-19` or `August 19, 2026`.
- Add alt text that describes what an image conveys.
- Use `and`, not `&`, in English prose and headings.
- Use a hyphen-minus `-`, not an em dash `—`.

## Adapt for Russian

Transfer the structural and clarity principles, but do not mechanically apply
English-specific rules such as second-person pronouns, sentence case, serial
commas, contractions, or American spelling. Prefer a natural imperative or
impersonal construction, such as `Чтобы удалить документ, нажмите Delete`.

Replace passive voice and nominalizations when the actor is known:
`производится обработка запроса` becomes `сервис обрабатывает запрос`.

## Rewrite or review

1. Identify the genre and choose the scope tier. State the tier if it is not
   obvious.
2. Fix ordering: answer first, then context; conditions before instructions.
3. Correct list structure, paragraph boundaries, voice, and terminology.
4. Fix technical formatting, links, dates, and image descriptions.
5. Read the result for a natural, helpful tone.

When reviewing existing text, show the proposed change and name the principle
behind it. This teaches the author how to apply the improvement next time.

## Break the rules deliberately

These are guidelines, not absolute rules. Depart from a recommendation when
doing so improves clarity for the intended audience. Keep the choice
consistent throughout the document and be able to explain why.

## Example

Before:

> Note that in order to be able to make use of the incremental build feature,
> it is necessary that the cache directory has been configured beforehand.
> Simply set the `CACHE_DIR` variable and everything will just work. We are
> also planning to add remote caching in a future release.

After:

> To use incremental builds, set `CACHE_DIR` to a writable path before the first
> build. If `CACHE_DIR` is unset, every build starts from scratch.

The rewrite puts the condition before the instruction, uses an explicit actor,
removes unsupported claims and a roadmap announcement, and adds the consequence
that matters to the reader.
