# Best Practices: C++ Project File Naming

## Naming

Name every C++ file and directory in lowercase `snake_case`, starting with a
letter. Use only `a-z`, `0-9`, and `_`; module partition filenames may also
contain one hyphen as described below. File names follow:

```plaintext
^(?:[a-z][a-z0-9_]*\.(?:cpp|hpp|ipp)|[a-z][a-z0-9_]*(?:-[a-z][a-z0-9_]*)?\.cppm)$
```

```plaintext
text_tools/
  http_server.hpp
  http_server.cpp
  http_server_test.cpp     # tests: <stem>_test.cpp, singular
  graph.cppm               # module `Graph`
  graph-node.cppm          # partition `Graph:Node`
```

- A header, its source, and its test share the same stem.
- The hyphen appears only in module partition files, where it stands for
  the colon of `module:partition`.
- Module names are `CamelCase`, like the types they export. The file name
  is the `snake_case` form of the module name (acronyms count as words):
  `Graph.GraphLayout` → `graph/graph_layout.cppm`.
- Two module names must not differ only by case.
- No Windows reserved stems: `con`, `prn`, `aux`, `nul`, `com1`–`com9`,
  `lpt1`–`lpt9`.

## Reasoning: naming

- Case-insensitive filesystems. NTFS and APFS ignore case by default,
  ext4 does not. Uppercase letters make three failures possible:
  - `#include "HttpServer.h"` for a file named `HTTPServer.h` builds on
    Windows and macOS and fails on Linux.
  - Two paths that differ only by case break checkout on Windows and
    macOS.
  - A case-only rename made outside `git mv` goes unnoticed by git.

  A lowercase name has exactly one spelling, so these failures cannot
  occur.
- Standard library. Standard headers are lowercase, and multi-word
  ones use underscores: `<string_view>`, `<unordered_map>`,
  `<source_location>`. Project includes then read the same way as the
  standard ones next to them, and file names match the `snake_case` of
  standard identifiers.
- Acronyms. CamelCase has no single answer for `HTTPServer` vs
  `HttpServer`. `http_server` has one.
- Predictability. One convention for all files means the name can be
  guessed without opening the file. Choosing the style by content
  (CamelCase for classes, `snake_case` for functions) breaks that.
- Underscore over hyphen. File names leak into include guards and target
  names, where a hyphen is not a valid identifier character.
- `_test` over `_tests`. On GitHub, files named `_test` outnumber files
  named `_tests` roughly four to one, and the suffix sorts the test next
  to the file under test.
- CamelCase module names. Unlike `#include`, `import Graph;` does not
  name a file, so a module name does not have to follow the file name
  rules. Composite project types should stand out in code, so modules are
  named like the types they export. Only the file system needs `snake_case`.
- Module names must not differ only by case. Compilers name the compiled
  interface file after the module, so `Graph` and `graph` collide on
  case-insensitive filesystems.

## Extensions

| Extension | Use for |
| --------- | ------- |
| `.cpp`    | Source files, including module implementation units |
| `.hpp`    | Headers |
| `.cppm`   | Anything importable: module interfaces and partitions |
| `.ipp`    | Template definitions included at the end of a `.hpp` |

Never use `.h`, `.cc`, `.C`, `.H`, `.c++`, or `.h++`.

## Reasoning: extensions

- Never `.h`. It is the C header extension, and C and C++ are
  different languages. A `.h` file does not say which one it contains, so
  every tool without a compile command has to guess: editors, clangd,
  clang-format, GitHub syntax highlighting. `.hpp` has one meaning. A
  header that must compile as C is a C file and is outside this
  convention.
- `.cppm` for importable units. An importable unit is a file that starts
  with `export module ...;`, such as a module interface or a partition, so
  other files can `import` it. Editing one rebuilds all importers.
  That role should be visible in the file tree and in diffs, not only in
  `CMakeLists.txt`. The same argument justifies `.hpp` next to `.cpp`.
- `.ipp` for template definitions. Such a file cannot be included or
  compiled on its own, so it must stay out of both the header and the
  source sets.
- Never `.cc`. It is a second spelling of `.cpp`, and mixing the two in
  one tree makes globs and tooling configs list both.
- Never `.C` / `.H`. The meaning is carried by case, which
  case-insensitive filesystems discard.
- Never `.c++` / `.h++`. `+` needs escaping in regex, make, and URLs.

## Exceptions

- The language or tool dictates the name: QML components start with an
  uppercase letter; `CMakeLists.txt`, `README.md`.
- An existing codebase with one consistent convention keeps it. Report
  only deviations from the project's own convention and case-only path
  collisions.
