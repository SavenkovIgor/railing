# Best Practices: CMake Project Config

This document describes how to distribute config across the layers
of a CMake project so that the config is readable, extensible, and does not
collapse into a pile of copy-paste when adding a new compiler or platform.

## Config Layers

A CMake project is configured at several levels. Each layer has its own
responsibility. Mixing responsibilities is the main source of unreadable
and unmaintainable build systems.

### CMakeLists.txt - project description

Owner: project developer. In git, changes go through PRs.

What the project is, what targets it has, which C++ standard it uses, what
policies apply (warnings, optimizations, sanitizers as an option), what
internal dependencies it has. Code that must work identically for anyone
who clones the repo.

### CMakePresets.json - shared invocation recipes

Owner: project developer. In git, changes go through PRs.

Composable recipes that make sense for everyone: hidden building-block presets
(`clang_compiler`, `release_build`), named compositions for standard build
variants, CI presets. *How* to run the build - which compiler, which generator,
which build type, where to find dependencies on a specific system.

Presets in this file can reference env vars as a contract with users
(`$penv{SDK_ROOT}`). That's fine - it means: "you must have this
variable, see the README". What must not appear here: hard-coded
personal paths or machine-specific values. See the
[CMake Presets reference](https://cmake.org/cmake/help/latest/manual/cmake-presets.7.html).

### CMakeUserPresets.json - personal local overrides

Owner: end user. In `.gitignore`, never committed.

Personal combinations not needed by others:

- SDK paths on a personal machine (if env vars are not being used).
- Flag experiments not yet ready for the team.
- Personal IDE configurations.
- Activating additional options that are disabled in shared presets.

Can inherit from `CMakePresets.json` presets, but not the other way around -
shared presets must not depend on personal ones.

**Rule:** if something is needed by the team or CI - put it in
`CMakePresets.json`. If only for you - put it in `CMakeUserPresets.json`.
If personal paths leak into a shared preset, a new developer won't be
able to configure the project without editing a git-tracked file. See the
[CMake Presets reference](https://cmake.org/cmake/help/latest/manual/cmake-presets.7.html).

### Toolchain file (`*.cmake`, via `CMAKE_TOOLCHAIN_FILE`)

Owner: SDK vendor or package manager (rarely the project itself).
See the section "Toolchain files: where they live" for details.

A description of a specific toolchain, especially for cross-compilation.
Target triple, sysroot, paths to compilers, `CMAKE_FIND_ROOT_PATH`,
`find_package` behavior. Usually provided by a third party
(e.g. Android NDK, iOS toolchain, or other cross-compilation SDK vendors).

### CMake modules (`cmake/*.cmake`, via `include()`)

Owner: project developer. In git.

Custom functions, config fragments, custom find-modules. This is where
conditional logic goes, such as "configure warnings for the current
compiler", utility macros, reusable pieces.

### Environment variables

Owner: end user (on their machine or in CI). The project documents the required
variables (e.g. in the README), but does not set their values.

The last resort, for things that physically have no place in the repo files.
SDK paths that depend on the user's machine (e.g. `ANDROID_NDK`, custom SDK roots).

### Dependency manager (Conan profiles)

Owner: project developer for dependency manifest
(`conanfile.py`/`conanfile.txt`, in git);
end user for build profile (`~/.conan2/profiles/*`) on their machine or CI.

A separate world that describes dependencies and how to build them. The
profile for dependencies usually differs from the profile for your code.

## Rule of thumb: what goes where

| Question                                          | Where                    |
| ------------------------------------------------- | ------------------------ |
| What we build and by what rules                   | CMakeLists               |
| With what and where we build (shared recipes)     | CMakePresets.json        |
| With what and where we build (personal overrides) | CMakeUserPresets.json    |
| Where the toolchain is and how it works           | Toolchain file           |
| Reusable logic, conditional branches              | In-project CMake modules |
| Where things are installed on the user's machine  | Environment vars         |
| Which dependencies and how to build them          | Conan profile            |

## The key mental distinction: Policy vs. Plumbing

Most of the confusion in CMake configs comes from mixing two different
things in one variable:

- Policy (project policy) - a decision like "we are strict with
  warnings", "we use C++23", "we have RTTI disabled",
  "we don't use exceptions". Does not depend on who builds or where.
  This is part of the project itself.

- Plumbing (build wiring) - specific paths, compiler names,
  output directory locations, cache isolation flags. Depends on the
  machine, environment, and specific invocation.

Policy → `CMakeLists.txt`.
Shared plumbing → `CMakePresets.json`.
Personal plumbing → `CMakeUserPresets.json`.

If it's unclear which category a flag belongs to, ask yourself:
"Would this decision change if I rebuilt the project tomorrow with the
same compiler but in a different folder?" If yes - plumbing. If no - policy.

## Reasoning: what should be possible without editing CMakeLists

The goal of a well-structured config is that typical changes to
"how we build" do not require editing "what we build".
A good config passes the following scenarios without changes to the
committed build files (`CMakeLists.txt`, `CMakePresets.json`, and cmake modules):

Without touching the project code, the following should be possible:

- Add a new compiler for the same platform - new compiler-preset in
  `CMakeUserPresets.json`.
- Switch Debug ↔ Release - choose a different preset.
- Add a sanitizer build - a new preset inheriting the existing one
  and adding the needed flags via infrastructure the project already
  provides (interface target, option).
- Adjust SDK paths for a new developer - their personal
  `CMakeUserPresets.json` with env vars.
- Add a new CI config - new preset in `CMakePresets.json`.
- Bump a dependency version - edit `conanfile`, not CMakeLists.
- Build with a different set of features - preset with different
  `cacheVariables` for options the project already defines.
- Try a newer compiler that emits new warnings without failing the
  build - `cmake --compile-no-warning-as-error`.
- Enable a compiler cache - `CMAKE_CXX_COMPILER_LAUNCHER` in a preset
  (see "Compiler cache: a preset setting").
- Collect build timings - a query and a callback script written by the CI
  wrapper or by the developer (see "Build time: measure, then optimize").
- Try another generator or a distributed build - a different `generator`
  in a preset (see "Scaling beyond one machine").

Requires editing CMakeLists / cmake modules:

- Add a new source file or new target.
- Add a new dependency (declared in `conanfile` + located via
  `find_package` in CMake).
- Change the project's minimum C++ standard.
- Change the set of warnings (this is policy).
- Add a new optional feature flag (the option needs to be defined).
- Change the install structure - what goes where.

If adding a new build config requires touching CMakeLists - that
is a signal that something is either in the wrong place or not
parameterized. For example, warning flags hard-coded in CMakeLists for
a specific compiler without conditional logic are a seam that will
eventually require code edits when a new toolchain is added.

CMakePresets as a contract. This is not just convenience - it is the
interface between the project and tooling. IDEs (CLion, VS Code, Visual
Studio) read `CMakePresets.json` and surface presets in their UI.
CI scripts reference presets by name. When presets are meaningfully
composed, the project and its users speak the same language.

## Examples

### Warning flags

A classic case of "compiler-specific syntax, but project policy". The
flag names differ (`-Wall` vs `/W4`), but the decision "be strict" is shared.

```cmake
# cmake/Warnings.cmake
add_library(project_warnings INTERFACE)

if(MSVC)
  target_compile_options(project_warnings INTERFACE
    /W4 /permissive-)
elseif(CMAKE_CXX_COMPILER_ID MATCHES "Clang|GNU")
  target_compile_options(project_warnings INTERFACE
    -Wall -Wextra -Wpedantic
    -Wconversion -Wsign-conversion
    -Wcast-qual -Wcast-align
    -Wformat=2 -Wundef
    -Wunused -Wdouble-promotion
    -Wimplicit-fallthrough
    -Wextra-semi
    -Woverloaded-virtual -Wnon-virtual-dtor
    -Wold-style-cast)
endif()
```

In `CMakeLists.txt`:

```cmake
include(cmake/Warnings.cmake)

add_executable(my_app ...)
target_link_libraries(my_app PRIVATE project_warnings)
```

Why not globally via `CMAKE_CXX_FLAGS`:

- `CMAKE_CXX_FLAGS` applies to everything compiled in the build tree,
  including third-party code that Conan or `add_subdirectory` may build.
  `-Werror` on someone else's code is a classic way to get random CI
  failures after bumping a dependency that added a new deprecation warning.
- `cacheVariables` in presets **does not compose**: when inheriting,
  the last one to set a variable wins - no merging happens. Spreading
  warnings across compiler-presets leads to them drifting apart quickly.
- An INTERFACE target gives explicit opt-in: tests or experimental targets
  can avoid linking to it if you need to temporarily relax warnings.

### Warnings as errors

Instead of hand-written `-Werror` / `/WX`, set
[`CMAKE_COMPILE_WARNING_AS_ERROR`](https://cmake.org/cmake/help/latest/variable/CMAKE_COMPILE_WARNING_AS_ERROR.html)
(CMake 3.24+) in `CMakeLists.txt`:

```cmake
set(CMAKE_COMPILE_WARNING_AS_ERROR ON)
```

CMake picks the right flag per compiler, and anyone can relax it for one
run with `cmake --compile-no-warning-as-error` - no edits to git-tracked
files.

- It is not an `INTERFACE_*` property, so linking `project_warnings`
  does not propagate it. Set the variable; keep the warning list in the
  INTERFACE target.
- Like other `CMAKE_*` defaults it leaks into `add_subdirectory` /
  `FetchContent` deps - set it after them or wrap them in `block()`.

### Language standard

Set `CMAKE_CXX_STANDARD`, `CMAKE_CXX_STANDARD_REQUIRED ON`, and
`CMAKE_CXX_EXTENSIONS OFF` in `CMakeLists.txt`. This is a project decision,
not a per-run decision - everyone who builds the project should get the same
language version regardless of the preset.

A library that other projects consume through `find_package` also needs
`target_compile_features(<lib> PUBLIC cxx_std_NN)`: `CMAKE_CXX_STANDARD`
does not reach the exported package (see "Target-based alternative").

### `compile_commands.json` for clangd

Set [`CMAKE_EXPORT_COMPILE_COMMANDS`](https://cmake.org/cmake/help/latest/variable/CMAKE_EXPORT_COMPILE_COMMANDS.html)
to `ON` in `CMakeLists.txt` - needed always, not per-preset. clangd expects
this file; without it IDE integration does not work.

## Toolchain files: where they live and who writes them

A toolchain file is a recipe for "how to use a specific compiler for
a specific target platform". In most projects you don't need to write
one by hand - it comes ready-made. Three sources, in descending order
of frequency:

### 1. SDK / compiler vendor

The most common case. The toolchain is shipped with the SDK and lives
inside its installation:

- Android NDK:
  `$ANDROID_NDK/build/cmake/android.toolchain.cmake`
- iOS via CMake - typically `ios.toolchain.cmake` from a
  community project or Apple's own.
- Other cross-compilation SDKs ship a `<sdk>.toolchain.cmake` inside
  their installation directory.

Owner: SDK vendor. The project only specifies the path.

### 2. Package manager

Conan generates its own toolchain files when installing dependencies:

- Conan 2: `<build-dir>/conan_toolchain.cmake`, generated by
  `conan install`. Contains `CMAKE_PREFIX_PATH` for deps found by
  Conan, flags from the profile, build_type selection.

Owner: package manager. The project configures
the manager (profiles, manifest); it does not write the file itself.

### Combining toolchain files

CMake accepts only one `CMAKE_TOOLCHAIN_FILE`. If you need to combine
several (e.g. vendor toolchain + Conan toolchain), options include:

- `tools.cmake.cmaketoolchain:user_toolchain` - the recommended
  Conan 2 approach ([documentation](https://docs.conan.io/2/reference/tools/cmake/cmaketoolchain.html#using-a-custom-toolchain-file)).
  A list of external toolchain files that Conan includes via `include()`
  as the first block inside its `conan_toolchain.cmake`.
  `CMAKE_TOOLCHAIN_FILE` points to `conan_toolchain.cmake`; the vendor
  toolchain is pulled in via Conan config:

  ```ini
  # Conan profile or global.conf
  [conf]
  tools.cmake.cmaketoolchain:user_toolchain=["/path/to/vendor/toolchain.cmake"]
  ```

- `CMAKE_PROJECT_TOP_LEVEL_INCLUDES` (CMake 3.24+) - a CMake-native
  mechanism for additional files included after the toolchain. Not
  Conan-specific.
- Chain via `include()` in your own toolchain wrapper - a thin
  custom wrapper that includes the needed toolchains in sequence.

In a typical setup (vendor toolchain + Conan), the canonical approach is
to set the vendor toolchain via
`tools.cmake.cmaketoolchain:user_toolchain` in the Conan profile, with
`CMAKE_TOOLCHAIN_FILE` pointing to `conan_toolchain.cmake`, which in turn
includes the vendor toolchain.

## Conan: separating profiles and who initiates what

When a project has a package manager and third-party dependencies,
there are two possible ways to build them:

1. Via the package manager - Conan resolves and builds
   deps before CMake even runs.
2. Via CMake itself - `FetchContent_MakeAvailable()`,
   `ExternalProject_Add()`, `add_subdirectory(third_party/...)`.

If Conan is already in the project - all external dependencies go through it.
No exceptions in normal cases.

Why:

- Binary cache: Conan caches built dependencies between builds and
  between machines (via remote). CMake's FetchContent rebuilds from scratch.
- Separate profile for deps: dependencies can be built in Release
  even when your project is in Debug, without `-Werror`, with a different
  C++ standard. With `add_subdirectory`, all of that inherits from the
  parent CMakeLists (see the section on `CMAKE_*` leaks).
- Cross-compilation: Conan correctly knows that a cross-compiled build needs
  target dependencies and a host build needs host ones. CMake
  FetchContent requires manual logic for each dependency.
- Versioning: Conan has a lockfile; builds are reproducible.
- Diamond resolution: if dependencies A and B both pull in
  different versions of zlib, Conan resolves that. A mix of
  conan+FetchContent does not - you end up with two zlиbs in one binary.

Typical workflow:

```bash
conan install . --output-folder=build/my_preset --build=missing
cmake --preset my_preset
cmake --build --preset my_preset
```

Conan:

- Resolves `conanfile.txt`/`conanfile.py`.
- Builds or downloads dependencies.
- Generates `build/my_preset/conan_toolchain.cmake` and
  CMake package files.

CMake:

- Uses the Conan toolchain (via `CMAKE_PROJECT_TOP_LEVEL_INCLUDES`
  or `CMAKE_TOOLCHAIN_FILE`).
- In its `CMakeLists.txt` writes a normal
  `find_package(SomeLib REQUIRED)`, which finds the Conan artifacts.
- Links via
  `target_link_libraries(my_app PRIVATE SomeLib::SomeLib)`.

From CMakeLists this looks like a standard find_package integration -
Conan is "invisible" to the project description itself. This is correct:
the project knows it needs `OpenSSL`, and does not know (and should not
need to know) whether it came from the system, from Conan, or was built locally.

Exceptions where FetchContent is justified:

- A header-only utility not available in Conan, where adding it there
  for a single use is overkill.
- Build-time tools (code generators, formatters) that are not linked
  into your binary. Though `tool_requires` in Conan 2 handles this too.
- The project has no package manager at all.

Conan profiles for deps vs. your code:

The build profile for dependencies is not the profile for your code.
Dependencies are typically built:

- Without `-Werror` (third-party code, third-party deprecation warnings).
- Often in Release, even when your project is in Debug (faster, and
  you usually don't debug dependencies).
- With their own warning settings, not yours.

Conan by default uses one profile (`host`) for everything, but you can
explicitly split it via `--profile:host` and `--profile:build` or via
custom settings in the profile. For most projects the default behavior
is sufficient; what matters is not poisoning it with global flags from CMake.

In presets the integration looks like this:

```json
"CMAKE_PREFIX_PATH":
  "${sourceDir}/build/${presetName}/conan-dependencies"
```

Dependencies live in the build directory, built by Conan, found via
`find_package` in CMake.

## `CMAKE_*` leaks into dependencies

A sharp edge that is easy to miss. The `CMAKE_*` prefix does not mean
"private CMake system variable". Most `CMAKE_*` variables are
directory-scoped defaults that are inherited by nested CMakeLists.

`set(CMAKE_CXX_STANDARD 23)` in the root CMakeLists leaks into:

- `add_subdirectory(third_party/foo)` → yes, it leaks. If `foo`
  was written for C++17 and uses something removed or broken in C++23 -
  it will break.
- `FetchContent_MakeAvailable(...)` → same, uses `add_subdirectory`
  internally.
- `find_package(...)` for already-built libs → no leak; the library
  is already compiled.
- `ExternalProject_Add(...)` → no leak; launches CMake as a
  subprocess with a clean environment.
- Conan-built deps → no leak; Conan builds them separately with its
  own profile, before your CMake runs.

So leaks are real for in-tree source deps. This is one more argument for
"dependencies via Conan, not via `add_subdirectory`".

Also leaks in the same way: `CMAKE_CXX_FLAGS`, `CMAKE_CXX_EXTENSIONS`,
`CMAKE_POSITION_INDEPENDENT_CODE`,
`CMAKE_INTERPROCEDURAL_OPTIMIZATION`, and most compiler defaults.

### Local protection via `block()`

CMake 3.25+ lets you create a variable scope:

```cmake
block()
  set(CMAKE_CXX_STANDARD 17)
  set(CMAKE_CXX_EXTENSIONS OFF)
  add_subdirectory(third_party/legacy_lib)
endblock()
```

After exiting `block()`, `CMAKE_CXX_STANDARD` reverts to your value.

### Target-based alternative

Modern CMake suggests: don't set `CMAKE_CXX_STANDARD` globally at all;
instead declare the requirement at the target level:

```cmake
add_library(my_lib ...)
target_compile_features(my_lib PUBLIC cxx_std_23)
```

`cxx_std_23` is a minimum requirement, not a forced value. Consumers
via PUBLIC get "I need a compiler with at least C++23", but the specific
standard can be raised higher.

It also works on INTERFACE libraries:
`target_compile_features(my_iface INTERFACE cxx_std_23)`.

`CMAKE_CXX_STANDARD` only initializes the `CXX_STANDARD` property of
targets in this build. It is not a usage requirement, so
`install(EXPORT)` does not record it. A consumer of the installed package
compiles with its own default standard: with GCC 13 that is C++17, and a
public header that uses C++20 fails to compile there. A requirement set
with `target_compile_features(... PUBLIC ...)` is exported as
`INTERFACE_COMPILE_FEATURES` and reaches every consumer.

Pragmatic compromise:

- `set(CMAKE_CXX_STANDARD 23)` globally as a default for your own code -
  convenient and readable.
- `target_compile_features(<lib> PUBLIC cxx_std_23)` on every library
  that is installed or exported, in addition to the global default.
- `block()` for cases where a dep needs something different and
  `add_subdirectory` can't be avoided.
- First priority - **don't use `add_subdirectory` for third-party**,
  so the question of leaks doesn't arise at all. Conan covers this
  for most cases.

## Source tree mirrors the target graph

Targets are the logical structure of the project; directories are the
physical one. They must describe the same thing. A reader should be able
to predict the list of targets from `tree`, and find any target's code
without reading CMake. When the two diverge, every basic question -
"which target is this file part of", "what rebuilds if I change it",
"who is allowed to include this header" - requires reverse-engineering
`CMakeLists.txt`.

Rules:

- One target - one directory. Each library or executable is defined
  in its own directory's `CMakeLists.txt`, pulled in via
  `add_subdirectory`. The directory name matches the target name
  (modulo a namespace prefix like `myproj_`).
- A target's sources live under its directory. No `../` paths in
  `add_library` / `add_executable` / `target_sources`, and no sources
  from other directories listed in the root `CMakeLists.txt`.
- A file belongs to exactly one target. If two targets need the same
  source, it is a third target - link it, don't compile it twice.
- Headers are reached through linking, not through paths. Public
  headers live in `<target_dir>/include/<target_name>/`, private ones
  next to the sources. Declare the public ones as a header file set
  (CMake 3.23+):
  `target_sources(foo PUBLIC FILE_SET HEADERS BASE_DIRS include FILES ...)`.
  The file set adds `include` to the include path of `foo` and its
  consumers, and `install(TARGETS foo FILE_SET HEADERS)` installs exactly
  these files. `#include <foo/bar.hpp>` tells the reader where the
  header comes from. Pointing
  `target_include_directories` into another target's directory is a
  hidden dependency that bypasses `target_link_libraries`.
- Subdirectories inside a target are only grouping. Once a
  subdirectory becomes a separate target, it gets its own
  `CMakeLists.txt`.

```plaintext
CMakeLists.txt          # project(), options, add_subdirectory() only
cmake/                  # modules, INTERFACE policy targets (warnings)
libs/
  core/                 # target: core
    CMakeLists.txt
    include/core/*.hpp  # public API
    src/*.cpp, *.hpp    # implementation + private headers + unit tests
    tests/              # component tests of core, see "Test layout"
  net/                  # target: net, links core
    CMakeLists.txt
    include/net/*.hpp
    src/*.cpp
apps/
  server/               # target: server, links net
    CMakeLists.txt
    main.cpp
tests/                  # tests spanning several targets
```

Legitimate exceptions - the rule relaxes to "a directory holds one
*kind* of target", created by a loop or a helper function:

- `examples/`, `tools/` with many small homogeneous executables.
- Top-level `tests/` with tests that span several targets (see
  "Test layout").
- INTERFACE policy targets (`project_warnings`) in `cmake/`: they are
  config, not code.
- Generated sources, which live in the build directory.

## Test layout

Tests live next to the code they test. Most languages that leave the
choice open converge on this: Go enforces `foo_test.go` in the same
package, Rust keeps unit tests in the same file, Google-style C++
(Abseil, Chromium) puts `foo_test.cc` next to `foo.cc`. Separate test
trees appear where the toolchain forces them (Maven classpath, .NET
assemblies, Python tests run against the installed package). CMake
forces nothing: a target contains exactly the files listed for it, and
install works per target, so a test file next to a source file never
ends up in the library.

Why colocation is the default:

- Access to internals without breaking encapsulation. A test in the
  component's directory includes its private headers directly. A test
  in a separate tree needs `target_include_directories` into another
  target's sources - the hidden dependency described in "Source tree
  mirrors the target graph".
- A missing test is visible. `parser.cpp` without
  `parser_test.cpp` next to it stands out in a listing and in review.
- No drift. A mirrored `tests/` tree goes stale: a source file is
  renamed or deleted, its test stays under the old path. A colocated
  test moves with the code.
- One owner. CODEOWNERS, reviewers, and history are shared by the
  component and its tests.

### Where a test goes

The granularity is the subject of the test - what it makes
assertions about - not every class it touches. A unit test may use
collaborators; that does not make it an integration test.

| Subject of the test                   | Location                                 | List                         |
| ------------------------------------- | ---------------------------------------- | ---------------------------- |
| One class / one source file           | `<stem>_test.cpp` next to `<stem>.cpp`   | `<target>_unit_tests`        |
| Several classes of one target         | `<target_dir>/tests/<scenario>_test.cpp` | `<target>_integration_tests` |
| Several targets together, or a binary | Top-level `tests/`                       | Its own target there         |

The file name makes the first rule checkable: a `<stem>_test.cpp` next
to sources must have a matching `<stem>.cpp` or `<stem>.hpp`. A test
named after no file in its directory is in the wrong place.

```plaintext
libs/core/
  CMakeLists.txt
  include/core/parser.hpp
  src/
    parser.cpp
    parser_test.cpp         # unit: subject is Parser
    lexer.cpp
    lexer_test.cpp          # unit: subject is Lexer
  tests/
    parse_pipeline_test.cpp # component: Lexer + Parser together
tests/
  request_roundtrip_test.cpp  # cross-target: core + net
```

### Two lists per component, runners chosen by the consumer

Each component exposes its tests as two `OBJECT` libraries with no
`main()` - one per kind. The list of test files lives in the
component's own `CMakeLists.txt`: adding a test touches only the
component, which matters when the component is a git submodule - the
parent repository only moves the submodule commit.

```cmake
# libs/core/CMakeLists.txt
add_library(core src/parser.cpp src/lexer.cpp)
target_sources(core PUBLIC
  FILE_SET HEADERS BASE_DIRS include FILES include/core/parser.hpp)

if(BUILD_TESTING)
  add_library(core_unit_tests OBJECT
    src/parser_test.cpp
    src/lexer_test.cpp)
  target_link_libraries(core_unit_tests PUBLIC core GTest::gtest)

  add_library(core_integration_tests OBJECT
    tests/parse_pipeline_test.cpp)
  target_link_libraries(core_integration_tests PUBLIC core GTest::gtest)
endif()
```

The consumer decides how to run them: one runner per component, one
per kind across components, unit tests only under sanitizers,
integration tests with longer timeouts. Separate lists make this a
change in one place instead of sorting files out of a common pile.

```cmake
# parent CMakeLists.txt: one runner per kind
include(GoogleTest)

add_executable(unit_tests)
target_link_libraries(unit_tests PRIVATE
  core_unit_tests net_unit_tests GTest::gtest_main)
gtest_discover_tests(unit_tests PROPERTIES LABELS unit)

add_executable(integration_tests)
target_link_libraries(integration_tests PRIVATE
  core_integration_tests net_integration_tests GTest::gtest_main)
gtest_discover_tests(integration_tests PROPERTIES LABELS integration)
```

`ctest -L unit` then runs only unit tests. One runner per kind (or per
component) keeps the number of link steps low; one executable per test
file means dozens of slow C++ links.

### Pitfall: tests that silently disappear

Test frameworks register tests through static initializers in files
nothing else references. Both of the following build without errors
and produce a runner with zero tests:

- `STATIC` test library. The linker pulls an object file out of a
  static archive only to resolve a referenced symbol; test files have
  none, so they are dropped. Use `OBJECT`, or link the archive with
  `$<LINK_LIBRARY:WHOLE_ARCHIVE,core_unit_tests>` (CMake 3.24+).
- `OBJECT` library linked transitively. Its objects are added only
  to the target that links it directly. Collecting test libraries in an
  `INTERFACE` aggregator and linking that to the runner loses them all.
  Link the test libraries to the runner directly, or use the helper
  below.

Guard against both: CI compares the number of discovered tests with the
previous run, or at least fails on a runner that reports zero tests.

### Transitive test sets: `source_set()`

GN has `source_set`: a set of object files that reaches every final
binary through any chain of dependencies. An `OBJECT` library is the
same set without the transitive part. Adding the objects to the
library's own interface sources makes it transitive:

```cmake
# cmake/SourceSet.cmake
function(source_set name)
  add_library(${name} OBJECT ${ARGN})
  target_sources(${name} INTERFACE $<TARGET_OBJECTS:${name}>)
endfunction()
```

With `source_set(core_unit_tests ...)`, test sets can be collected
through an `INTERFACE` aggregator or a chain of other test sets, and a
set reachable by two paths is linked once.

Use `source_set()` only for targets that nothing links except a final
binary: the `<target>_unit_tests` and `<target>_integration_tests`
sets. CMake has no notion of a `SHARED` library as a boundary for
interface sources. If a `source_set()` target sits below a `SHARED`
library, its objects go into the shared library and again into every
binary that links it: two copies of the code and of every global, and no
link error. With `-fvisibility=hidden`, the usual setting for shared
libraries, each copy then works with its own state. Make shared test
helpers (fixtures, mocks) `STATIC` libraries instead.

### Test sets belong to the component

Do not let the component add its tests to the parent's runner itself
(`target_sources(unit_tests ...)` from the submodule, or a global
property registry). It works, but the component then depends on the
name of its consumer's target and cannot be reused elsewhere. One
`target_link_libraries` line per component in the parent is the right
price: adding a component touches the parent anyway (`add_subdirectory`),
adding a test does not.

## Installable libraries

A library that another project consumes through `find_package` carries
its usage requirements in the exported package. Everything the consumer
needs has to be a usage requirement of the target: include paths, compile
features, link dependencies. Directory-scoped settings and
`CMAKE_CXX_STANDARD` stay behind in the build tree.

```cmake
include(GNUInstallDirs)
include(CMakePackageConfigHelpers)

add_library(image src/image.cpp)
add_library(Imaging::image ALIAS image)
target_compile_features(image PUBLIC cxx_std_20)
target_sources(image PUBLIC
  FILE_SET HEADERS
  BASE_DIRS include
  FILES include/image/image.hpp)

install(TARGETS image EXPORT ImagingTargets FILE_SET HEADERS)
install(EXPORT ImagingTargets
  NAMESPACE Imaging::
  DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/Imaging)
write_basic_package_version_file(ImagingConfigVersion.cmake
  COMPATIBILITY SameMajorVersion)
# plus ImagingConfig.cmake that includes ImagingTargets.cmake,
# installed next to it together with ImagingConfigVersion.cmake
```

The consumer:

```cmake
find_package(Imaging 1.0 CONFIG REQUIRED)
target_link_libraries(viewer PRIVATE Imaging::image)
```

- Header file set over `target_include_directories`. A plain include
  path into the source tree makes `install(EXPORT)` fail; the
  workaround is a pair of `$<BUILD_INTERFACE:...>` and
  `$<INSTALL_INTERFACE:...>` expressions plus a separate
  `install(DIRECTORY)`. A `FILE_SET HEADERS` gives the right path in
  both trees and installs exactly the declared headers.
- Namespace and `ALIAS`. The installed target is `Imaging::image`;
  `add_library(Imaging::image ALIAS image)` gives in-tree consumers the
  same name, so moving a consumer between the build tree and an installed
  package changes no `target_link_libraries` line. A name with `::`
  that does not resolve to a target is an error at generate time, while
  a plain name silently turns into a `-limage` linker flag.
- `CONFIG` mode in `find_package` for packages that ship a CMake config.
  Without it, CMake first looks for a `FindImaging.cmake` module.
- Verify with a separate consumer project. Install into a staging prefix
  (`cmake --install build --prefix stage`), then configure a small
  project with `-DCMAKE_PREFIX_PATH=stage` that links the package. This
  catches requirements that exist only in the build tree: a missing
  compile feature, an include path into the sources, an undeclared
  dependency.
- CPS (Common Package Specification) metadata is an addition, not a
  replacement. `install(PACKAGE_INFO <name> EXPORT <export>)` (CMake
  4.3+) writes a JSON description that tools other than CMake can read;
  keep the CMake config files for consumers that do not read CPS yet.
  See "CPS" below.

### CPS

CPS describes a binary library as data: headers, libraries, compile
definitions, and required packages. A CMake config file describes the same
as code, for example a `find_dependency(ZLIB)` call, and only CMake can run
it.

```cmake
install(TARGETS zwrap EXPORT zwrap)
install(PACKAGE_INFO zwrap EXPORT zwrap)   # install tree
export(PACKAGE_INFO zwrap EXPORT zwrap)    # build tree
```

If `zwrap` links `zlib-ng::zlib`, the CPS file records `zlib-ng` in a
`requires` entry. A consumer calls `find_package(zwrap REQUIRED)` and links
`zwrap::zwrap`; it does not mention `zlib-ng`, and CMake still finds it.

- `find_package()` (4.3+) searches for and imports CPS packages the same
  way as CMake configs. The consumer's `CMakeLists.txt` does not change.
- `export(PACKAGE_INFO <name> EXPORT <export>)` writes the CPS file into
  the `cps/<name>` subdirectory of the build tree, for consumers that use
  your build directory without installing. `install(PACKAGE_INFO ...)`
  writes the install-tree file; the two files can differ.
- Header file sets are exported to CPS (4.5+), and `find_package()` imports
  CPS executable components.
- Package metadata can come from `project()`: its `COMPAT_VERSION` and
  `SPDX_LICENSE` options are inherited by the CPS file, and
  `install(PACKAGE_INFO)` has `LICENSE` and `DEFAULT_LICENSE` of its own.
- Dependencies of a package are data (a `requires` entry), so a runtime a
  library needs, such as the Fortran runtime for a BLAS built from Fortran,
  travels with the package instead of being rediscovered by the consumer.
- Package managers (Conan, Spack) generate CPS for the packages they
  provide. For a project that does not ship CPS yet, the packager's file is
  the source.
- A CPS file is machine-readable, so an audit script can check it. A script
  that rejects warning flags in the usage requirements of a package is
  trivial for JSON and hard for CMake code.
- CMake config files keep working. Ship both until the consumers you care
  about read CPS.

### SBOM

A software bill of materials lists what a binary is built from: packages,
versions, relationships. `install(SBOM <name> EXPORTS <export>...)` (CMake
4.5+) generates it at install time from the target graph, next to the
installed exports; `export(SBOM)` does the same for the build tree. The
default format is SPDX 3.0.1 in JSON-LD (`FORMAT`).

A packager can switch SBOM generation on without editing the project:
`cmake -DCMAKE_INSTALL_SBOM_FORMATS=spdx` generates one SBOM for every
export set created by `install(TARGETS ... EXPORT ...)` and installs it
under `<libdir>/sbom/<export-name>`. Export sets with an explicit
`install(SBOM)` are skipped. Use the command itself when you need your own
metadata, format, or destination.

```cmake
install(TARGETS image EXPORT ImagingTargets FILE_SET HEADERS)
install(SBOM Imaging EXPORTS ImagingTargets
  DATA_LICENSE CC0-1.0
  DEFAULT_LICENSE MIT)
```

- The SBOM covers the targets of the listed exports only. A test framework
  linked into test executables that are not in an export set does not
  appear, while a tool that works from the installed file list cannot tell.
  Keep test targets out of the exports so the list stays accurate.
- Name, version, and description are inherited from `project()` when the
  SBOM name matches the project name. Options of the command override them.
- License of a component comes from the `SPDX_LICENSE` target property, and
  from `DEFAULT_LICENSE` where the property is unset. A target without
  either has no license in the document, so set one of them and read the
  output for imported dependencies.
- A target cannot be described if its `LINK_LIBRARIES` or
  `INTERFACE_LINK_LIBRARIES` contain generator expressions, unless they are
  guarded by `LINK_ONLY`.
- A typical use for open-source projects is the license question ("did I
  link a GPL library statically"), more than the CVE question.
- The SBOM is data about one build. CMake does not scan for vulnerabilities
  and does not look at releases already shipped. Generate the SBOM in CI as
  a byproduct of the install step, store it next to the release artifact,
  and run the CVE scan in a separate job against the stored files, so old
  releases can be scanned again when a new CVE appears.
- The package identity ("which CVE entry applies to this zlib") is not
  solved by CMake. Set `PACKAGE_URL` where you know it, or enrich the SBOM
  after generation.

## C++20 modules

Module interface units go into a file set of type `CXX_MODULES`. CMake
scans these sources during the build and orders compilation so that each
built module interface (BMI) exists before the units that import it.

```cmake
add_library(graph)
target_compile_features(graph PUBLIC cxx_std_20)
target_sources(graph PUBLIC
  FILE_SET CXX_MODULES
  FILES src/graph.cppm src/graph-node.cppm)
```

Requirements (CMake 3.28+): the Ninja generators with `ninja` 1.11+ or
Visual Studio 2022+, and Clang 16+, GCC 14+, or MSVC toolset 14.34+.
Header units are not supported.

- `PUBLIC` file set for modules that consumers import, `PRIVATE` for
  internal ones. Import a `PRIVATE` module only from implementation units
  (`module M;`), not from a module interface: a consumer of the interface
  would need the private module too. CMake rejects this, except with the
  Visual Studio generators, which do not diagnose it.
- Implementation units declare `module M;`. `module M:part;` declares an
  internal partition, which must be in the `CXX_MODULES` file set.
- Installing: `install(TARGETS)` needs an explicit `DESTINATION` for the
  `CXX_MODULES` file set, and `install(EXPORT)` needs
  `CXX_MODULES_DIRECTORY`; without it, consumers cannot import the
  modules. The Visual Studio generators do not support exporting modules.
- The toolchain must provide the module scanner. GCC and MSVC scan through
  an option of the compiler itself; Clang uses a separate `clang-scan-deps`
  program. Some packagings place it where CMake does not find it, and
  scanning then fails. Check that `clang-scan-deps` of the same LLVM
  installation is available next to the compiler.
- Modules turn compilation into a scheduling problem: a module interface
  must be built before every unit that imports it, so a module with many
  importers becomes the long pole of the build. Keep interfaces small, move
  definitions into implementation units, and check the trace (see "Build
  time: measure, then optimize") for modules that block the build.
- Macros still need `#include`; header units are not supported, so a
  project that moves to `import` keeps a thin macro header.
- A C++20 project that does not use modules yet: put
  `set(CMAKE_CXX_SCAN_FOR_MODULES 0)` near the top of the top-level
  `CMakeLists.txt`, not in the cache. Otherwise every source is scanned,
  and scanned sources are excluded from unity builds.

### `import std`

CMake 4.5 (a release candidate on 2026-10-18) makes `import std`
available in every target with C++20 or newer and module scanning
enabled. Up to CMake 4.4 it required the
`CMAKE_EXPERIMENTAL_CXX_IMPORT_STD` gate, `CXX_MODULE_STD ON` on each
target, and C++23.

- Toolchains: Clang 18.1.2+ with libc++ or libstdc++, MSVC toolset
  14.36+, GCC 15+ (GCC 16+ on macOS). Only the Ninja generators support
  it.
- `CMAKE_CXX_STDLIB_MODULES_JSON` (CMake 4.5+) points CMake at the
  standard library module metadata instead of asking the compiler. The
  path depends on the machine, so it belongs in the toolchain file or a
  preset.

## Preprocessor definitions: scope and volatility

A `-D` flag is part of the compile command of every translation unit
that sees it. Change its value and every such TU is recompiled, and
every compiler cache (ccache, sccache, remote caches) misses. A global
define that changes on every commit - git hash, build number, build
date - turns every build into a full rebuild and drops the CI cache hit
rate to zero.

The same applies to a header: moving the value from `-D` into
`inline constexpr auto git_hash = "..."` in a header replaces a
preprocessor macro with a language construct, but every includer still
recompiles on every commit. What protects the cache is not the syntax
but how many TUs depend on the value.

Classify each definition by how often it changes and what it affects:

| Kind                    | Examples                          | Where                                      |
| ----------------------- | --------------------------------- | ------------------------------------------ |
| Volatile build metadata | git hash, build number, version   | One generated `.cpp` in a dedicated target |
| Stable feature flags    | `WITH_TLS`, `ENABLE_TRACING`      | Owning target, `PRIVATE` by default        |
| ABI-affecting           | `_GLIBCXX_ASSERTIONS`, `NOMINMAX` | Toolchain / Conan profile, uniform         |

### Volatile metadata: compilation firewall

Declaration in a stable header, value in exactly one generated source.
A new commit recompiles one file and relinks; nothing else changes.

```cpp
// libs/buildinfo/include/buildinfo/buildinfo.hpp - never changes
namespace buildinfo {
std::string_view version();
std::string_view git_hash();
}
```

```cmake
# libs/buildinfo/CMakeLists.txt
set(out ${CMAKE_CURRENT_BINARY_DIR}/buildinfo.cpp)
add_custom_target(buildinfo_gen
  COMMAND ${CMAKE_COMMAND}
    -DIN=${CMAKE_CURRENT_SOURCE_DIR}/buildinfo.cpp.in
    -DOUT=${out}
    -DVERSION=${PROJECT_VERSION}
    -P ${CMAKE_CURRENT_SOURCE_DIR}/GenBuildInfo.cmake
  BYPRODUCTS ${out})

add_library(buildinfo STATIC ${out})
add_dependencies(buildinfo buildinfo_gen)
target_include_directories(buildinfo PUBLIC include)
```

`GenBuildInfo.cmake` gets the hash via `execute_process(git rev-parse)`
and writes the file via `configure_file`, which leaves the output
untouched when the content is the same - no spurious rebuilds. Running
at build time (not configure time) keeps the hash from going stale
after a commit without re-running CMake.

Avoid `__DATE__` / `__TIME__`: they make every build unique, which
breaks both caching and reproducible builds. If a timestamp is needed,
take it from `SOURCE_DATE_EPOCH` in the same generated source.

### Stable flags: target scope, language over preprocessor

- Scope to the target that needs the flag, with explicit visibility:
  `PRIVATE` unless the flag changes the target's public headers.
- Prefer a generated config header of the owning target with
  `inline constexpr bool with_tls = ...;` and `if constexpr` over
  `#ifdef`: both branches are type-checked, typos are compile errors,
  and the flag is a named, scoped symbol instead of a global token.
- Keep `#if` only where the disabled branch cannot compile at all
  (missing platform headers or APIs).

### Not per source file

`set_source_files_properties(... COMPILE_DEFINITIONS ...)` looks like
the tightest possible scope, but it is an ODR hazard: two TUs of one
target that include the same header with an `inline` function or a
class definition see different code under the same name. The linker
silently picks one. The smallest safe scope for a definition that can
reach a header is the target.

### ABI-affecting definitions: the exception

Definitions that change layouts or inline code in standard or system
headers must be identical for everything linked into one binary,
dependencies included. Scoping them per target causes ODR violations,
not isolation. Set them in the toolchain file or Conan profile so that
dependencies get them too, or project-wide if no prebuilt code is
affected. These values are stable per build config, so they do not
hurt caching.

### Compiler cache: a preset setting

The rules above keep compile commands stable; a compiler cache turns that
into reused results. Which cache to use, and whether to use one at all,
depends on the machine and the CI, so it is plumbing: set it in a preset,
not in `CMakeLists.txt`.

```json
"cacheVariables": {
  "CMAKE_C_COMPILER_LAUNCHER": "sccache",
  "CMAKE_CXX_COMPILER_LAUNCHER": "sccache"
}
```

Put it in a shared CI preset or in `CMakeUserPresets.json`. To check the
hit rate, delete the build directory, keep the cache, rebuild, and read
`sccache --show-stats` (or `ccache -s`). A low hit rate on an unchanged
tree points at a volatile compile command, such as a global define.
Record the hit rate together with the build timings, see "Build time:
measure, then optimize".

The compile command contains the absolute paths of the source and build
directories, so a CI job that checks out into a different directory each
time misses the cache of the previous job. Give the checkout a fixed path
(GitLab runners do this with `GIT_CLONE_PATH`), or set the cache's base
directory (`base_dir` in ccache). Share the cache between runners, for
example through a Redis backend for sccache, so that a new runner starts
warm.

## Build time: measure, then optimize

A build is a graph, and its duration is set by the longest chain through
it, not by the sum of the steps. Guessing which step to fix usually hits the
wrong one: typical findings are one dependency (a test framework) that
everything waits for, tests that run serially, and an `install` step that
takes longer than the build. Collect timings first.

CMake instrumentation (4.3+, see `cmake-instrumentation(7)`) records every
command CMake runs during configure, generate, build, test, and install.
It works with the Makefile, Ninja, and FASTBuild generators, not with the
Visual Studio generators.

### What instrumentation collects

- CMake wraps each compile, link, and custom command in a launcher that
  writes a JSON snippet. Snippets are also written for configure, generate,
  a whole `cmake --build`, a whole `cmake --install`, each `ctest` run, and
  each test.
- A snippet holds the role (`compile`, `link`, `custom`, `test`, `install`,
  ...), the target, `timeStart` and `duration` in milliseconds, the source
  file, the outputs and their sizes, the configuration, the test name, and
  the exit code.
- A query decides what is collected. It is a JSON file or a
  `cmake_instrumentation()` call with three parts: hooks, options, and
  callbacks.
- Hooks say when indexing runs: `postGenerate`, `preBuild` and `postBuild`
  (for a direct `ninja` or `make` run, not triggered by `cmake --build`),
  `preCMakeBuild`, `postCMakeBuild`, `postCMakeInstall`,
  `postCMakeWorkflow`, `postCTest`. A hook fires only for the matching
  entry point, so run the build through `cmake --build`, the tests through
  `ctest`, and the install through `cmake --install`. The `postBuild` hook
  runs its callback in the background, so the callback's console output is
  lost; for a summary printed at the end of a developer's build use
  `postCMakeBuild`.
- Indexing writes an index file that lists the snippets created since the
  previous indexing, runs every callback with the index path appended as the
  last argument, and then deletes the index and the snippets. The index
  also holds the hook name, the build directory, and the path of the trace
  file.
- Options add data: `dynamicSystemInformation` (host memory and CPU load
  average before and after each command), `staticSystemInformation` (host
  name, CPU count, memory, in the index), `trace` (a Google Trace Event file
  you open in Perfetto or `chrome://tracing`), `compileTrace` (4.4+, the
  per-file `-ftime-trace` JSON of Clang, copied next to the data),
  `captureOutput` (4.4+), and `processMetrics` (4.5+, peak memory and CPU
  time per command).
- `CUSTOM_CONTENT` of `cmake_instrumentation()` puts configure-time values
  (string, bool, list, JSON) into a content file that every snippet
  references, next to the type and labels of its target. Use it to tag
  records with the optimization level or a coverage build.
- The data version is requested explicitly: `DATA_VERSION 1.2` needs 4.5,
  and `compileTrace` needs data version 1.1. `cmake -E capabilities` (4.5+)
  reports what the installed CMake supports.

### Where each piece lives

Follow the policy and plumbing split: what to collect and where to send it
depends on the machine and the CI, so it is plumbing.

- The callback script is code. It lives in the repository (`tools/` or
  `cmake/`) and goes through review.
- A query is switched on per environment, without touching a committed
  build file: the CI wrapper writes a query file into
  `<build>/.cmake/instrumentation/v1/query/`, and a developer puts one into
  `<config_dir>/instrumentation/v1/query/` of their CMake user config
  directory.
- All queries are merged. If any query has hooks, every callback of every
  query runs at every hook, and an option requested by one query adds its
  data to all snippets. A callback must tolerate fields it did not ask for.
- Do not make a project-level callback upload anything. A callback declared
  in `CMakeLists.txt` runs arbitrary commands on every build of every
  developer. Let it at most write a local summary into the build directory.
- Collecting from developer machines (for example to find out whether five
  minute links are everyone's problem or one laptop) needs the team's
  agreement. Tag each record with the preset, the compiler, the linker, the
  compiler cache state (`CUSTOM_CONTENT`), and the host (`staticSystemInformation`);
  without tags, laptop and CI numbers mix into noise.

### Wiring it into CI

1. Before the build, the CI job writes a query into the build tree:

   ```json
   {
     "version": 1,
     "hooks": ["postCMakeBuild", "postCTest", "postCMakeInstall"],
     "options": ["staticSystemInformation", "dynamicSystemInformation", "trace"],
     "callbacks": ["python3 /abs/path/to/tools/build_report.py"]
   }
   ```

2. The build runs from a named preset through `cmake --build`, `ctest`, and
   `cmake --install` (or one `cmake --workflow`, hook `postCMakeWorkflow`),
   so a record can be compared with the previous record of the same preset.
   For before-and-after comparisons of a change, build clean
   (`--clean-first`) with a fixed `--parallel <jobs>` and compare the two
   traces.
3. The callback reads the index file and builds a summary: total `duration`
   per `role`, the slowest `compile` and `link` snippets with their
   `target` and `source`, and the slowest `test` snippets by `testName`.
   It writes the summary to the job report.
4. CMake deletes the index, the snippets, and the previous trace after the
   callbacks finish, so the callback copies what the job must keep: the
   index, the snippets, and the trace file named in the index. It uploads
   the copies as artifacts.
5. CI compares the totals with the last successful run of the main branch
   and reports regressions. Compare relatively (a percentage over the
   baseline), not against a fixed number, and discard runs where the CPU
   load recorded in the snippets shows a busy runner.
6. Keep the history in one table keyed by commit and preset.

Start with steps 3 and 4. Add the regression check after a few weeks of
data, when you know how noisy your runners are. Instrumentation data can
also go to CDash (the `cdashSubmit` option, or the `CTEST_USE_INSTRUMENTATION`
environment variable in a CTest dashboard run).

A build served from a compiler cache measures the cache, not the compiler.
Record the hit rate (see "Compiler cache: a preset setting") next to the
timings and compare only builds with a similar rate.

### Acting on the data

| What the data shows                           | Lever                                                                                                      |
| --------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| Idle cores in the trace while work is waiting | Unneeded build-order edges, see "Waiting for work that is not needed yet"                                  |
| One target is a long pole, others wait for it | Get it prebuilt from the package manager                                                                   |
| `install` takes minutes                       | Stripping and RPATH rewriting run at install time: parallel install, see below                              |
| Tests run one after another                   | `ctest --parallel` (or `CTEST_PARALLEL_LEVEL`, or `jobs` in a test preset); `RESOURCE_LOCK` only for real conflicts |
| A few translation units dominate compile time | `compileTrace` (Clang, 4.4+): the per-file trace shows the headers and templates behind the time           |
| CI builds everything to run one test          | `test_prep/<test-name>` and `install_prep/<component>` (on by default in 4.5+) build only what that step needs |
| The same tests rerun though nothing changed   | `ctest --out-of-date` (4.5+), see below                                                                    |
| Link time dominates                           | A faster linker (lld, mold) as preset plumbing; compare two presets in one trace                           |
| Compile time dominates, cache misses          | A volatile compile command, see "Preprocessor definitions: scope and volatility"                           |
| Configure time dominates                      | See "Configure time"                                                                                       |

### Waiting for work that is not needed yet

Open the trace and look for idle jobs while the build is not finished. The
cause is often not a slow command but an order that CMake enforces
conservatively, because a target might need a file that an upstream target
produces. Two fixes remove most of these waits.

Declare the visibility of generated headers. Before policy CMP0154 (3.28),
CMake assumes any generated file may be a public header of its target, so
Ninja holds back the compilation of every consumer until the generating
command finishes, even when the file is a private detail. With CMP0154 NEW
(`cmake_minimum_required` 3.28 or newer), a generated file in a target that
uses file sets is private unless it is in a `PUBLIC` or `INTERFACE` file
set. Put a private generated header into a private file set, and a public
one into a public file set:

```cmake
target_sources(config PRIVATE
  FILE_SET implementation_headers TYPE HEADERS
  BASE_DIRS ${generated_dir}
  FILES ${generated_dir}/config.hpp)
```

Enable `OPTIMIZE_DEPENDENCIES` (3.19+) for static and object libraries. A
static library that links to another target gets a build-order dependency on
it, although creating the archive needs nothing from that target. So the
code generation of a library waits for all upstream archives, and a chain of
libraries builds one at a time. With the option, CMake drops the
dependencies the library does not need and keeps explicit
`add_dependencies()`, custom commands that produce its sources, and
languages with side effects. The final executable still waits for the
libraries it links.

```cmake
set(CMAKE_OPTIMIZE_DEPENDENCIES ON)   # initializes the property of new targets
set_property(TARGET schema_1 PROPERTY OPTIMIZE_DEPENDENCIES ON)   # one target
```

Apply both to the places the trace points at, then compare the clean builds
with the same `--parallel` value.

### Tests only for what changed

`ctest --out-of-date` (4.5+) runs only the tests whose recorded build
dependencies are newer than the last run of the test. The dependencies are
the executables and targets in the `COMMAND`, plus the targets and files
given in `BUILD_DEPENDS` of `add_test()` or `discover_tests()`;
`gtest_discover_tests()` records the test executable itself. A test without
known build dependencies is excluded whenever the option is given, so add
`BUILD_DEPENDS` for tests that run scripts or read generated files.
Combine it with `test_prep/all` so that only the needed targets are built.

### Parallel install

A parallel install needs two steps. Enable the global property
`INSTALL_PARALLEL` (3.30+) in the project, then run
`cmake --install <build> --parallel <jobs>` (3.31+); the environment
variable `CMAKE_INSTALL_PARALLEL_LEVEL` sets a default. Install rules of
different directories then run in no fixed order. Do not enable it if an
`install(CODE)` or `install(SCRIPT)` depends on files or variables from an
earlier `install()` in another directory. Before 4.5, `cmake --install`
reported success for a parallel install even when an install script failed;
on older versions, check the installed files instead of the exit code.

## Configure time

Configure runs on every change of a `CMakeLists.txt` or `*.cmake` file,
including adding one source file to one target, and it re-runs for the whole
project. CMake cannot skip parts of it: generator expressions are evaluated
over the whole target graph, and a change anywhere is visible everywhere.
The cost is paid by every developer on every edit, so keep configure cheap
and repeatable.

- Profile it before changing anything:
  `cmake --profiling-format=google-trace --profiling-output=configure.json`
  and open the file in Perfetto.
- Put expensive probing behind a cache variable: `execute_process` that
  inspects the machine, `try_compile`, SDK discovery. CMake already caches
  `try_compile` and platform checks; custom code does not get this for free.
- Keep the network out of configure. A toolchain file or provider that
  queries a package manager on every run (some do) costs time on every
  edit; report it upstream and ask for the result to be cached.
- Keep the build tree between CI runs on a dedicated agent. A clean tree
  repeats compiler detection and feature checks every time. A reused tree
  can go stale when the image changes: set the environment variable
  `CMAKE_SYSTEM_ENVIRONMENT_ID` (4.5+) to the image version, and CMake warns
  when it differs from the cached value. `CMAKE_SYSTEM_ENVIRONMENT_ACTION=REFRESH`
  runs `--fresh` instead, which drops every cache variable that a configure
  preset or the command line does not set again.
- Do not look for a way to reconfigure "only the changed target". Remove
  work from configure instead.

### Debugging CMake code

- `cmake --debugger --debugger-pipe <path>` (3.27+) starts CMake as a
  Debug Adapter Protocol server. VS Code, CLion, and any editor with a DAP
  client can set breakpoints, step through CMake code, and inspect
  variables. A failed configure in a supporting IDE offers the call stack.
- `cmake_language(PRINT_VARIABLES)`, `PRINT_TARGETS`, and `PRINT_PROPERTIES`
  (4.5+) print variables, existing targets, and properties in readable form;
  they replace `cmake_print_variables()` and `cmake_print_properties()`.
- `--trace-expand` on a big project writes gigabytes. Narrow it with
  `--trace-source=<file>`, or use the debugger.
- Never expose the debug port to a network: the debugger runs any CMake
  code the client sends.

## Scaling beyond one machine

Order of effort: first stable compile commands and a compiler cache (see
"Compiler cache: a preset setting"), then measurement, then distribution.
Distribution without the first two spends hardware on rebuilding what a
cache would give for free.

The generator is plumbing, so choose it in a preset, never in
`CMakeLists.txt`.

- Ninja is the default for local and CI builds. Module scanning works with
  the Ninja generators and Visual Studio 2022+; `import std` only with
  Ninja.
- The FASTBuild generator (4.2+) adds parallel and distributed builds with
  caching and little setup: set `CMAKE_FASTBUILD_CACHE_PATH` (or the
  `FASTBUILD_CACHE_PATH` environment variable) and build with
  `cmake --build <dir> -- -cache`; FASTBuild's own `-dist` flag turns on
  distribution, and the target properties `FASTBUILD_CACHING` and
  `FASTBUILD_DISTRIBUTION` opt a single target out. It is not in the list
  of generators that scan C++ modules, so a project that uses modules stays
  on Ninja. Instrumentation works with it.
- Remote execution (a compiler wrapper such as Rex CC with a BuildGrid and
  BuildBox cluster, or a hosted remote execution service) needs a fleet.
  On two laptops the scheduling and cache overhead dominates and the build
  gets slower than a local one. Decide by trial on the real project with the
  instrumentation from this document, not by the vendor's numbers.
- CMake itself does not distribute and will not: it describes the build and
  hands it to a generator. Do not plan around a "CMake server".

## Anti-patterns

### Target defined far from its sources

```cmake
# BAD: root CMakeLists.txt describes everything
add_library(core src/core/a.cpp src/core/b.cpp)
add_library(net  src/net/socket.cpp src/core/utils.cpp)  # shared file
target_include_directories(net PRIVATE ${CMAKE_SOURCE_DIR}/src/core)

# GOOD: each target in its own directory, sharing via linking
add_subdirectory(libs/core)
add_subdirectory(libs/net)   # target_link_libraries(net PUBLIC core)
```

The `net` → `core` dependency in the bad version is invisible:
it exists only as an include path and a compiled-twice file.

### `CMAKE_CXX_FLAGS` in presets with everything in it

```json
"CMAKE_CXX_FLAGS": "-Werror -Wall -Wextra ... -fsanitize=address ..."
```

- Applies globally, catches warnings from third-party code.
- Does not compose - if another preset also touches `CMAKE_CXX_FLAGS`,
  they overwrite each other.
- Hides project policy in build configs where it is hard to find.

### Hard-coded paths

```json
"CMAKE_PREFIX_PATH": "/home/user/my-sdk/1.0/linux"
```

Only works for the author. Better:

```json
"CMAKE_PREFIX_PATH": "$env{MY_SDK_ROOT}/linux"
```

With explicit documentation of which env vars the user must set, or
with a reasonable fallback via `$penv{X}`.

### Duplicating flags across presets

If the same `-Werror` lives in `clang_native_dev`,
`clang_native_release`, `gcc_dev`, `gcc_release` - sooner or later
they will drift apart. Single source of truth: `CMAKE_COMPILE_WARNING_AS_ERROR`
in CMakeLists (see "Warnings as errors").

### Old-style directory commands instead of targets

```cmake
# BAD: Cuz applies globally to the directory
include_directories(${CMAKE_SOURCE_DIR}/include)  # bad
add_definitions(-DFEATURE_X=1)                    # bad

# GOOD: Explicitly per-target, no leaks and with explicit visibility
target_include_directories(my_lib PUBLIC include)
target_compile_definitions(my_lib PRIVATE FEATURE_X=1)
```

With explicit visibility (`PRIVATE`/`PUBLIC`/`INTERFACE`).

CMake 4.5 reports these commands with the `CMD_NON_TARGET_DIRECTIVE`
diagnostic: `-Wnon-target-directive` on the command line, or
`"warnings": { "nonTargetDirective": true }` in a configure preset
(schema version 13).

### Specifying compilers without a toolchain file for cross-compilation

```json
"CMAKE_C_COMPILER": "$penv{SDK_ROOT}/bin/cross-gcc"
```

This works in simple cases but skips important platform variables:
`CMAKE_SYSTEM_NAME`, sysroot, `CMAKE_FIND_ROOT_PATH`, `find_package`
behavior. For cross-compilation it is better to specify the toolchain
file explicitly:

```json
"CMAKE_TOOLCHAIN_FILE":
  "$penv{SDK_ROOT}/cmake/toolchain.cmake"
```

The vendor's toolchain file knows all the required details.

## Project checklist

Project level (`CMakeLists.txt`):

- [ ] `cmake_minimum_required` is set; the version is not ancient.
- [ ] C++ standard is set in CMakeLists, not via flags.
- [ ] Every installed or exported library declares
      `target_compile_features(<lib> PUBLIC cxx_std_NN)`.
- [ ] Warnings are extracted into an INTERFACE target and applied explicitly.
- [ ] Warnings-as-errors via `CMAKE_COMPILE_WARNING_AS_ERROR`, not a
      hand-written `-Werror` / `/WX`.
- [ ] `CMAKE_EXPORT_COMPILE_COMMANDS ON`.
- [ ] Dependencies via `target_link_libraries` with explicit visibility.
- [ ] Public headers via `FILE_SET HEADERS`; other include paths via
      `target_include_directories`, never directory-wide.
- [ ] LTO/sanitizers - per-target and conditional, not via a global flag.
- [ ] If `add_subdirectory` is used for in-tree source deps - wrapped
      in `block()` to protect against `CMAKE_*` leaks.

Source layout:

- [ ] Each library/executable target is defined in its own directory,
      named after the target (exceptions: `examples/`, `tools/`, top-level `tests/`).
- [ ] No `../` paths or foreign-directory sources in target definitions.
- [ ] No source file is compiled into more than one target.
- [ ] Public headers in `<target>/include/<target>/`; no
      `target_include_directories` pointing into another target's tree.

Tests:

- [ ] Unit tests are `<stem>_test.cpp` next to `<stem>.cpp`; tests of
      several classes are in `<target_dir>/tests/`; cross-target tests
      in top-level `tests/`. No mirrored test tree.
- [ ] Each component exposes `<target>_unit_tests` and
      `<target>_integration_tests` as `OBJECT` libraries without `main()`,
      listed in the component's own `CMakeLists.txt`.
- [ ] Test libraries reach runners directly or through `source_set()`
      (no `STATIC` without `WHOLE_ARCHIVE`, no plain `OBJECT` behind an
      `INTERFACE` aggregator).
- [ ] `source_set()` only for test sets; shared test helpers are `STATIC`.
- [ ] One runner per component or per kind, not per test file; tests
      carry `unit` / `integration` labels.
- [ ] CI fails on a runner that reports zero tests.

Preprocessor definitions:

- [ ] No `add_definitions` / `add_compile_definitions` / `-D` in
      `CMAKE_CXX_FLAGS` for project-specific values.
- [ ] Git hash, build number, version string are not passed via `-D` or
      a widely included header; they live in one generated `.cpp`.
- [ ] No `__DATE__` / `__TIME__`.
- [ ] No per-source-file `COMPILE_DEFINITIONS`.
- [ ] ABI-affecting definitions are identical across the project and
      its dependencies (toolchain file or Conan profile).

Installable libraries:

- [ ] Installed targets have a namespace (`Pkg::target`) and an `ALIAS`
      with the same name for in-tree consumers.
- [ ] Headers are installed through `install(TARGETS ... FILE_SET HEADERS)`.
- [ ] A separate consumer project builds against a staging install.
- [ ] CPS is installed next to the CMake config with `install(PACKAGE_INFO)`.
- [ ] If an SBOM is generated with `install(SBOM)`: test-only targets are
      not in the listed exports, licenses are set (`SPDX_LICENSE` or
      `DEFAULT_LICENSE`), and the SBOM is stored with the release artifact.

Build and configure time:

- [ ] The CI job records instrumentation data (index, snippets, trace) as
      an artifact, copied by the callback before CMake deletes it, and
      tagged with the preset and the compiler cache hit rate.
- [ ] A project-level instrumentation callback does not upload anything;
      uploads happen only in CI or by a developer's own choice.
- [ ] Regressions are checked against the last main-branch run as a
      percentage, not against a fixed number.
- [ ] Tests run with `ctest --parallel`; when install shows up in the
      trace, `INSTALL_PARALLEL` is enabled and `cmake --install --parallel`
      is used.
- [ ] Idle jobs in the trace are explained: generated headers are in a
      private or public file set (CMP0154 NEW), and
      `OPTIMIZE_DEPENDENCIES` is enabled for chains of static libraries.
- [ ] Expensive configure-time probing is behind cache variables, and
      configure does not use the network.

C++20 modules:

- [ ] Module interface units are in a `CXX_MODULES` file set; `PRIVATE`
      modules are imported only from implementation units.
- [ ] A C++20 project without modules sets
      `CMAKE_CXX_SCAN_FOR_MODULES 0` in the top-level `CMakeLists.txt`.
- [ ] A Clang toolchain has `clang-scan-deps` of the same installation next
      to the compiler.
- [ ] Generator is chosen in a preset; a project with modules uses Ninja.

Invocation level (`CMakePresets.json`):

- [ ] `CMakeUserPresets.json` is in `.gitignore`.
- [ ] `CMAKE_CXX_FLAGS` in presets - only thin toolchain-specific
      wiring (e.g. module cache path).
- [ ] Dependency paths via env vars with documentation.
- [ ] Cross-compilation via `CMAKE_TOOLCHAIN_FILE`, not by manually
      specifying compilers.
- [ ] Composition via `inherits`, no copy-paste between presets.
- [ ] `binaryDir` is unique per preset.
- [ ] Compiler cache via `CMAKE_<LANG>_COMPILER_LAUNCHER` in a preset,
      not in `CMakeLists.txt`.
- [ ] No personal paths in shared presets; everything via env vars
      or UserPresets.

Dependencies:

- [ ] All third-party goes through a package manager (Conan),
      not via `add_subdirectory`/`FetchContent`.
- [ ] Conan profile is separate from the project profile.
- [ ] Third-party does not inherit `-Werror` and other strict policies.
- [ ] Dependency versions are pinned in a lock file / manifest.
- [ ] `conan_toolchain.cmake` is included via
      `CMAKE_PROJECT_TOP_LEVEL_INCLUDES` when stacked on top of a
      vendor toolchain (e.g. Android NDK, iOS, etc.).

## General principle

A preset should be thin and read like a simple sentence:
"take the project → build it with this compiler → in this config
→ put the output here". Everything that describes *how the project should
be structured* lives in the project. Everything that describes *how the
build is currently invoked* lives in the preset.

When you read someone else's `CMakePresets.json` and see long lists of
warning flags, sanitizer settings, and project include paths - that means
project policy has leaked into build invocation. The fix is to move it
back into CMakeLists.
