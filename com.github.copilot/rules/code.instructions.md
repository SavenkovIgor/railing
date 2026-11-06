---
name: Coding Style
applyTo: '**/*.{h,hpp,cc,cpp,cppm,ipp,py,js,ts}'
---

# Coding style

- Readability and maintainability are primary concerns
- Code should always be self-documenting first; comments explain *why*, not *what*
  - Delete a comment that retells the next line: ✘ `// increase the retry counter` above `++retries;`, ✔ `// the server drops the first request after a reconnect`
- Prefer small, focused, pure functions - if a function needs a comment to explain what it does, consider splitting it
  - A check function verifies one condition on the inputs it owns and nothing out of its scope, so checks compose into a sequence of validators (e.g. when constructing a validated type) without repeating each other
- Follow single responsibility principle in classes and functions
- Prefer explicit over implicit: make dependencies, side effects, and control flow visible at the call site
- Prefer deterministic over stochastic: avoid randomness unless the feature requires it; when needed, make it explicit and seedable
  - *Deviate when:* ML/AI training, fuzzing, generative features
- Prefer stateless over stateful: functions and components should derive output purely from their inputs
  - *Deviate when:* caches (performance), sessions, streaming protocols
  - A cache that grows from external input (requests, files, user data) has a size limit or an eviction policy. Without one, memory grows with the input until the process runs out of it
- Prefer idempotent operations: running the same operation multiple times should produce the same result as running it once
  - *Deviate when:* intentional side-effectful operations (financial transactions, hardware I/O)
- Fail fast: detect and surface errors as close to their source as possible
- Write bitmasks as binary literals with digit separators (`0b0111'0000` in C++, `0b0111_0000` in Python), not hex, when the bit layout matters
- Never cut corners on: input validation at trust boundaries, error handling that prevents data loss, security measures, accessibility basics, or anything explicitly requested

## 1. Think Before Coding

Don't assume. Don't hide confusion. Surface tradeoffs.

Before implementing:
- State your assumptions explicitly. If uncertain, ask
- If multiple interpretations exist, present them - don't pick silently
- If a simpler approach exists, say so. Push back when warranted
- Question the requirement itself: sometimes the best version of a task is not doing it. Say so when that's the case
- If something is unclear, at planning, stop. Name what's confusing. Ask

## 2. Simplicity First

Minimum code that solves the problem. Nothing speculative.

Before writing any new code, walk the ladder in order - stop at the first step that works:

1. Does this task actually need to exist? (YAGNI) → if not, skip it and say why
2. Does the standard library solve it? → reach for stdlib before anything else
3. Can a native platform feature handle it? → use the built-in instead of reimplementing
4. Does an already-installed dependency cover it? → reuse it; don't add a new dependency
5. Can it be one line of code? → write the one-liner
6. Only then: write a minimal working implementation → smallest version that passes

Additional constraints:
- No features beyond what was asked
- No abstractions for single-use code
- No "flexibility" or "configurability" that wasn't requested
- No error handling for impossible scenarios
- Prefer deleting over adding: if removing code (a branch, a flag, a special case) solves the problem, do that instead of layering more on - within the code your change already touches (§3 still governs unrelated code)
- If you write 200 lines and it could be 50, rewrite it

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify

## 3. Surgical Changes, Engineering Proposals

Touch only what you must. Clean up only your own mess. Propose improvements when necessary.

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting. But highlight it if below standards
- Don't refactor things that aren't broken automatically. But propose refactors if see clear improvements
- Match existing style, even if you'd do it differently. But remember that bad style is also a smell
- If you notice unrelated dead code, mention it - don't delete it

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused
- Don't remove pre-existing dead code - highlight it for future cleanup

The test: Every changed line should trace directly to the user's request

## 4. Goal-Driven Execution

Define success criteria. Loop until verified.

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

Expected values in tests come from literals or an independent implementation, never from the code under test. A test that recomputes the result with the same formula mirrors the implementation and cannot fail

For multi-step tasks, state a brief plan:
```text
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently
It doesn't mean you can't ask questions or help you if stuck
It means you have to have a clear definition of "done" and keep it in mind as you work

## 5. Surface approach conflicts, don't silently pick one

If two patterns or paradigms are contradict, pick one and state it explicitly.
Explain why. Flag the other for future cleanup directly in the code.
Don't silently blend conflicting patterns.

## API design

Make an API easy to use correctly and hard to use incorrectly: a developer does the right thing by default, with minimal thought or memorization.

> If developers are smart, motivated, have experience with programming, are willing
> to read documentation, and want to succeed - yet they still fail to use
> your API correctly, it's the API's fault, not theirs.

### Least astonishment

- Review the names of functions, classes, and endpoints: guess what a developer expects and compare the names with that guess
- Write error messages that tell the developer what to do next
- Follow the naming of the standard library when naming new types
- Make custom types behave like built-in types

### Names

- Name descriptively and concisely
- Keep names consistent within their context (class, namespace, module)
- Do not repeat the class name in a method name
- Do not repeat the type of an argument in its name when the type is obvious
- Write a well-known abbreviation as an ordinary word, not in capitals
- Do not prefix a cheap read with `get`

### Arguments

- Order arguments by how often they are used, most common first
- Keep the argument order the same across similar functions
- Group related arguments into one type
- Use at most 4 arguments in a function
- Use two or more arguments of the same type only in well-known cases such as width and height; otherwise give them distinct types or group them

### Path variables

- Name a variable that holds a directory with the suffix `dir`, a full path to a file with `file`, and a file name without a path with `filename`

### API completeness

- When you add or change an entity, check which CRUD operations (create, read, update, delete) its API has, and propose the missing ones instead of adding them
- Protect destructive operations or mark them clearly

### Successful path and common tasks

- Check that the successful path is the obvious one
- Check that a common task through the API is straightforward

## Code organization

- Code should be modular (and testability is a good proxy for modularity)
- Modules should have clear, intuitive APIs that are hard to misuse
- Modules should not have cyclic dependencies

- Component is a minimum unit of code cohesive both logically and physically
- Package - the primary unit of code (components), organization in a repository
is the package. A package is a collection of related files (cohesive) and a
specification of dependencies between them.
- Dependency is a relationship between two components where one could
not work/compile without the other.

## Domain modeling

Make invalid states impossible to express in types: model a set of mutually exclusive states as one enum or variant, not as independent flags.

```text
✘ isLoading: bool, hasError: bool    isLoading and hasError can both be true
✔ state: Loading | Failed | Ready    only the valid states exist
```

An invariant is a condition on the members of an object that every public member function relies on without checking it:

- The constructor establishes the invariant; when it cannot, construction fails with an error. LLMs often add a separate `init()` or `isValid()` instead, and then every caller has to remember the call and every member function has to check the state
- Every public member function keeps the invariant on each exit, an exit by exception included, so the invariant also holds on entry to the destructor
- Inside a member function the invariant may break; restore it before the function calls a public member function of the same object, a callback, or a virtual function, since each of them can observe the object
- A setter exists only for a member outside the invariant, or checks the invariant and rejects a value that breaks it

```text
✘ Range with setMin() and setMax()    setMin(10) while max is 5 breaks min <= max
✔ Range with setBounds(min, max)      one call checks min <= max
```

## Logging

Choose the level of each log call by who reads the message and what they must do:

- `fatal`: an error after which the application cannot continue and stops. For users and developers
- `error`: an operation failed, someone has to act to fix it, and the application keeps running. For users and developers
- `warning`: something unexpected happened that can degrade a feature, but the application keeps working. For users and developers
- `info`: a rare lifecycle event that users and developers care about: start, stop, a changed configuration
- `debug`: detail a developer needs to diagnose a problem
- `trace`: the step-by-step flow of execution, for developers only

An expected outcome that the code handles is not an error: ✘ `error: cache miss for key 42`, ✔ `debug: cache miss for key 42`

On a hot path (a loop over items, a per-frame or per-packet handler), log at `debug` or `trace` only: ✘ `info: packet received` for each packet, ✔ `trace: packet received`
