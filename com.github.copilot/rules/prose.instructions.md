---
name: Technical Writing
applyTo: '**/*.md'
---

# Technical writing

Write and review developer-facing prose in a concise, project-aware way.
Base it on the [Google developer documentation style guide](https://developers.google.com/style)
and on the writing rules of [ASD Simplified Technical English](https://www.asd-ste100.org/)
(STE). Use the STE writing rules, not its dictionary of approved words.
These principles inform the writing. They do not require the result to be
"Google-compatible" or STE-compliant.

## Editorial hierarchy

1. Follow project-specific terminology and conventions.
2. Use the principles in this file when project guidance is silent.
3. Use third-party references only when the first two sources do not answer the
   question.

## Decide the scope

- Apply the full style guidance to READMEs, API references, runbooks,
  procedures, release notes, onboarding docs, error messages, and code comments.
- Apply structural guidance only to ADRs, design docs, RFCs, PR descriptions,
  commit messages, and technical articles. Preserve the argument, trade-offs,
  and appropriate voice these genres need.
- Do not apply these rules to conversational answers, brainstorming, opinion
  pieces, or a user-requested voice. Apply them there only when the user asks
  for a documentation-style rewrite.

## Write for the reader

- Lead with the answer or action the reader needs. Put background after it.
- Put conditions before instructions so readers can skip steps that do not
  apply.
- Start a warning with the command, then give the reason: `Stop the service
  before you edit the file. A running service overwrites the file.`
- Use numbered lists for sequences and bullets for unordered items.
- Keep one main idea per paragraph and at most six sentences.
- Use headings to organize content and enable scanning. Make each heading
  self-contained.
- Prefer active voice and present tense. Name the actor when it is known.
  Passive voice is fine when the actor is irrelevant or the object matters
  more, as in "The file is saved."
- Use simple tenses: present, past, and future. Give every `-ing` phrase a
  clear actor. Write `After you install it, the service restarts`, not
  `After installing, the service restarts`.
- Use real verbs instead of nominalizations.
- Address the reader directly when the language supports it. Avoid ambiguous
  uses of "we."
- Keep one idea per sentence. Limit a sentence to 20 words in an instruction
  and to 25 words in a description.
- Use one term per concept and one meaning per word throughout the document.
  If `follow` means "come after", write `apply` or `obey` for rules.
- Give each modal verb one meaning: `must` for a requirement, `should` for a
  recommendation, `can` for ability or permission. Write `can` instead of `may`.
- Be specific and avoid abstractions.
- Use at most three nouns in a row: write `the flag that overrides the cache
  path`, not `cache path override flag`.
- Cut filler, bureaucratic phrasing, and redundancy. Keep articles and
  conjunctions: write `Run the task and check the output`, not
  `Run task, check output`.
- Do not open with an intro that restates the title or close with a summary
  that repeats the sections.
- Remove excessive claims, hedges, unexplained jargon, idioms, and
  pre-announcements.
- Replace a phrasal verb with a one-word verb: write `configure`, not
  `set up`, and `find`, not `find out`.
- Use a conversational, friendly, respectful tone without slang or excessive
  formality.
- Avoid anthropomorphism and culture-specific references.
- Expand an abbreviation only at its first use in the document. Leave
  abbreviations that are common in the industry unexpanded, such as `CI`,
  `API`, or `LLM`.

### Prose style examples

```text
1. Remove bureaucratic and verbose phrases
   ✘ "For the purpose of increasing the efficiency of the system, a process of
       optimization is currently being conducted."
   ✔ "The team optimizes the system for speed."

2. Prefer active voice over passive voice
   ✘ "Logging is enabled in the configuration file by the installer."
   ✔ "The installer enables logging in the configuration file."

3. Replace noun-based verbs with actual verbs
   ✘ "The execution of the installation can be performed by the administrator."
   ✔ "The administrator installs the software."

4. Be specific and avoid abstractions
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
- Use descriptive link text instead of `click here` or a bare URL.
- Use unambiguous dates such as `2026-08-19` or `August 19, 2026`.
- Add alt text that describes what an image conveys.
- Use `and`, not `&`, in English prose and headings.
- Use a hyphen-minus `-`, not an em dash `—`.
- Use two sentences or a list, not a semicolon `;`.

## Choose the language

- Write in the language of the document.
- Use American spelling and grammar in English.

## Adapt for Russian

Transfer the structural and clarity principles. Do not mechanically apply
English-specific rules such as second-person pronouns, sentence case, serial
commas, contractions, or American spelling. Prefer a natural imperative or
impersonal construction, such as `Чтобы удалить документ, нажмите Delete`.

Replace passive voice and nominalizations when the actor is known:
`производится обработка запроса` becomes `сервис обрабатывает запрос`.

## Break the rules deliberately

Depart from a recommendation when the change makes the text clearer for the
intended audience. Keep the choice consistent throughout the document and related
documents, and be able to explain why.

## Example

Before:

> Note that in order to be able to make use of the incremental build feature,
> it is necessary that the cache directory has been configured beforehand.
> Simply set the `CACHE_DIR` variable and everything will just work. We are
> also planning to add remote caching in a future release.

After:

> To use incremental builds, set `CACHE_DIR` to a writable path before the first
> build. If `CACHE_DIR` is unset, every build starts from scratch.

The rewrite puts the condition before the instruction and uses an explicit
actor. It removes unsupported claims and a roadmap announcement, and adds the
consequence that matters to the reader.
