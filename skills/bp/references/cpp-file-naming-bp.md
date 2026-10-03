# Best Practices: C++ Project File Naming

## Naming

Name every C++ file and directory in lowercase `snake_case`, using only
`a-z`, `0-9`, and `_`, starting with a letter:

```plaintext
^[a-z][a-z0-9_]*\.(cpp|hpp|cppm|ipp)$
```

```plaintext
text_tools/
  http_server.hpp
  http_server.cpp
  http_server_test.cpp     # tests: <stem>_test.cpp, singular
  graph.cppm               # module `graph`
  graph-node.cppm          # partition `graph:node`
```

- A header, its source, and its test share the same stem.
- The hyphen appears only in module partition files, where it stands for
  the colon of `module:partition`.
- A module file is named after its module: `termgraph.graph_layout` →
  `termgraph/graph_layout.cppm`. Module names follow the same
  lowercase `snake_case` rule.
- No Windows reserved stems: `con`, `prn`, `aux`, `nul`, `com1`–`com9`,
  `lpt1`–`lpt9`.

## Reasoning: naming

- **Case-insensitive filesystems.** NTFS and APFS ignore case by default,
  ext4 does not. Uppercase letters make three failures possible:
  - `#include "HttpServer.h"` for a file named `HTTPServer.h` builds on
    Windows and macOS and fails on Linux.
  - Two paths that differ only by case break checkout on Windows and
    macOS.
  - A case-only rename made outside `git mv` goes unnoticed by git.

  A lowercase name has exactly one spelling, so these failures cannot
  occur.
- **Standard library.** Standard headers are lowercase, and multi-word
  ones use underscores: `<string_view>`, `<unordered_map>`,
  `<source_location>`. Project includes then read the same way as the
  standard ones next to them, and file names match the `snake_case` of
  standard identifiers.
- **Acronyms.** CamelCase has no single answer for `HTTPServer` vs
  `HttpServer`. `http_server` has one.
- **Predictability.** One convention for all files means the name can be
  guessed without opening the file. Choosing the style by content
  (CamelCase for classes, `snake_case` for functions) breaks that.
- **Underscore over hyphen.** File names leak into include guards, target
  names, and module names, where a hyphen is not a valid identifier
  character.
- **`_test` over `_tests`.** It is the more common suffix by a wide
  margin, and it sorts the test next to the file under test.
- **Module names.** Compilers name the compiled interface file after the
  module, so module names that differ only by case collide in the build
  directory.

## Extensions

| Extension | Use for |
| --------- | ------- |
| `.cpp`    | Source files, including module implementation units |
| `.hpp`    | Headers |
| `.cppm`   | Anything importable: module interfaces and partitions |
| `.ipp`    | Template definitions included at the end of a `.hpp` |

Never use `.h`, `.C`, `.H`, `.c++`, or `.h++`.

## Reasoning: extensions

- **Never `.h`.** It is the C header extension, and C and C++ are
  different languages. A `.h` file does not say which one it contains, so
  every tool without a compile command has to guess: editors, clangd,
  clang-format, GitHub syntax highlighting. `.hpp` has one meaning. A
  header that must compile as C is a C file and is outside this
  convention.
- **`.cppm` for importable units.** Editing one rebuilds all importers.
  That role should be visible in the file tree and in diffs, not only in
  `CMakeLists.txt`. The same argument justifies `.hpp` next to `.cpp`.
- **`.ipp` for template definitions.** Such a file cannot be included or
  compiled on its own, so it must stay out of both the header and the
  source sets.
- **Never `.C` / `.H`.** The meaning is carried by case, which
  case-insensitive filesystems discard.
- **Never `.c++` / `.h++`.** `+` needs escaping in regex, make, and URLs.

## Exceptions

- The language or tool dictates the name: QML components start with an
  uppercase letter; `CMakeLists.txt`, `README.md`.
- An existing codebase with one consistent convention keeps it. Report
  only deviations from the project's own convention and case-only path
  collisions.
