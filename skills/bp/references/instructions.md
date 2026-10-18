# Instructions Files Best Practices

Checks for `*.instructions.md` files. Every check is pass/fail; cite findings by ID.

## Frontmatter

- FM01 The frontmatter has `applyTo` with a non-empty glob.
  Why: without `applyTo` the editor does not attach the file on its own, so its rules never apply.

  ✘ `applyTo: ''`
  ✔ `applyTo: '**/*.py'`

- FM02 The frontmatter has an explicit `name` for discoverability.

## Content

- CT01 Every rule translates to observable behavior: you can point to a concrete action or text
  that violates it. A vague aphorism without an example is a finding.
  Why: the agent cannot tell whether it followed a rule that no behavior contradicts.

  ✘ `Write clean code`
  ✔ `Split a function that needs a comment to explain what it does`

- CT02 A rule whose wrong form is easy to produce has an example pair of the wrong and the right
  form. The pair may be code or text. A rule whose wrong form is not a realistic mistake needs no
  example.
  Why: an example raises compliance more than a description of the rule does.

  ✘ `Name functions well`
  ✔ `Name a function after its result: ✘ doWork(), ✔ parseHeader()`
