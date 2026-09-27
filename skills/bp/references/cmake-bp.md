# Best Practices: CMake Project Config

This document describes how to distribute config across the layers
of a CMake project so that the config is readable, extensible, and does not
collapse into a pile of copy-paste when adding a new compiler or platform.

## Config Layers

A CMake project is configured at several levels. Each layer has its own
responsibility. Mixing responsibilities is the main source of unreadable
and unmaintainable build systems.

### CMakeLists.txt — project description

Owner: project developer. In git, changes go through PRs.

What the project is, what targets it has, which C++ standard it uses, what
policies apply (warnings, optimizations, sanitizers as an option), what
internal dependencies it has. Code that must work identically for anyone
who clones the repo.

### CMakePresets.json — shared invocation recipes

Owner: project developer. In git, changes go through PRs.

Composable recipes that make sense for everyone: hidden building-block presets
(`clang_compiler`, `release_build`), named compositions for standard build
variants, CI presets. *How* to run the build — which compiler, which generator,
which build type, where to find dependencies on a specific system.

Presets in this file can reference env vars as a contract with users
(`$penv{SDK_ROOT}`). That's fine — it means: "you must have this
variable, see the README". What must not appear here: hard-coded
personal paths or machine-specific values. See the
[CMake Presets reference](https://cmake.org/cmake/help/latest/manual/cmake-presets.7.html).

### CMakeUserPresets.json — personal local overrides

Owner: end user. In `.gitignore`, never committed.

Personal combinations not needed by others:

- SDK paths on a personal machine (if env vars are not being used).
- Flag experiments not yet ready for the team.
- Personal IDE configurations.
- Activating additional options that are disabled in shared presets.

Can inherit from `CMakePresets.json` presets, but not the other way around —
shared presets must not depend on personal ones.

**Rule:** if something is needed by the team or CI — put it in
`CMakePresets.json`. If only for you — put it in `CMakeUserPresets.json`.
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
profile for **dependencies** usually differs from the profile for **your code**.

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

- **Policy (project policy)** — a decision like "we are strict with
  warnings", "we use C++23", "we have RTTI disabled",
  "we don't use exceptions". Does not depend on who builds or where.
  This is part of **the project itself**.

- **Plumbing (build wiring)** — specific paths, compiler names,
  output directory locations, cache isolation flags. Depends on the
  machine, environment, and specific invocation.

Policy → `CMakeLists.txt`.
Shared plumbing → `CMakePresets.json`.
Personal plumbing → `CMakeUserPresets.json`.

If it's unclear which category a flag belongs to, ask yourself:
"Would this decision change if I rebuilt the project tomorrow with the
same compiler but in a different folder?" If yes — plumbing. If no — policy.

## Reasoning: what should be possible without editing CMakeLists

The goal of a well-structured config is that typical changes to
"how we build" do not require editing "what we build".
A good config passes the following scenarios without changes to the
committed build files (`CMakeLists.txt`, `CMakePresets.json`, and cmake modules):

Without touching the project code, the following should be possible:

- Add a new compiler for the same platform — new compiler-preset in
  `CMakeUserPresets.json`.
- Switch Debug ↔ Release — choose a different preset.
- Add a sanitizer build — a new preset inheriting the existing one
  and adding the needed flags via infrastructure the project already
  provides (interface target, option).
- Adjust SDK paths for a new developer — their personal
  `CMakeUserPresets.json` with env vars.
- Add a new CI config — new preset in `CMakePresets.json`.
- Bump a dependency version — edit `conanfile`, not CMakeLists.
- Build with a different set of features — preset with different
  `cacheVariables` for options the project already defines.
- Try a newer compiler that emits new warnings without failing the
  build — `cmake --compile-no-warning-as-error`.

Requires editing CMakeLists / cmake modules:

- Add a new source file or new target.
- Add a new dependency (declared in `conanfile` + located via
  `find_package` in CMake).
- Change the project's minimum C++ standard.
- Change the set of warnings (this is policy).
- Add a new optional feature flag (the option needs to be defined).
- Change the install structure — what goes where.

If adding a new build config requires touching CMakeLists — that
is a signal that something is either in the wrong place or not
parameterized. For example, warning flags hard-coded in CMakeLists for
a specific compiler without conditional logic are a seam that will
eventually require code edits when a new toolchain is added.

**CMakePresets as a contract.** This is not just convenience — it is the
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

- `CMAKE_CXX_FLAGS` applies to **everything** compiled in the build tree,
  including third-party code that Conan or `add_subdirectory` may build.
  `-Werror` on someone else's code is a classic way to get random CI
  failures after bumping a dependency that added a new deprecation warning.
- `cacheVariables` in presets **does not compose**: when inheriting,
  the last one to set a variable wins — no merging happens. Spreading
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
run with `cmake --compile-no-warning-as-error` — no edits to git-tracked
files.

- It is not an `INTERFACE_*` property, so linking `project_warnings`
  does not propagate it. Set the variable; keep the warning list in the
  INTERFACE target.
- Like other `CMAKE_*` defaults it leaks into `add_subdirectory` /
  `FetchContent` deps — set it after them or wrap them in `block()`.

### Language standard

Set `CMAKE_CXX_STANDARD`, `CMAKE_CXX_STANDARD_REQUIRED ON`, and
`CMAKE_CXX_EXTENSIONS OFF` in `CMakeLists.txt`. This is a project decision,
not a per-run decision — everyone who builds the project should get the same
language version regardless of the preset.

### `compile_commands.json` for clangd

Set [`CMAKE_EXPORT_COMPILE_COMMANDS`](https://cmake.org/cmake/help/latest/variable/CMAKE_EXPORT_COMPILE_COMMANDS.html)
to `ON` in `CMakeLists.txt` — needed always, not per-preset. clangd expects
this file; without it IDE integration does not work.

## Toolchain files: where they live and who writes them

A toolchain file is a recipe for "how to use a specific compiler for
a specific target platform". In most projects you don't need to write
one by hand — it comes ready-made. Three sources, in descending order
of frequency:

### 1. SDK / compiler vendor

The most common case. The toolchain is shipped with the SDK and lives
inside its installation:

- **Android NDK:**
  `$ANDROID_NDK/build/cmake/android.toolchain.cmake`
- **iOS** via CMake — typically `ios.toolchain.cmake` from a
  community project or Apple's own.
- Other cross-compilation SDKs ship a `<sdk>.toolchain.cmake` inside
  their installation directory.

Owner: SDK vendor. The project only specifies the path.

### 2. Package manager

Conan generates its own toolchain files when installing dependencies:

- **Conan 2:** `<build-dir>/conan_toolchain.cmake`, generated by
  `conan install`. Contains `CMAKE_PREFIX_PATH` for deps found by
  Conan, flags from the profile, build_type selection.

Owner: package manager. The project configures
the manager (profiles, manifest); it does not write the file itself.

### Combining toolchain files

CMake accepts only one `CMAKE_TOOLCHAIN_FILE`. If you need to combine
several (e.g. vendor toolchain + Conan toolchain), options include:

- **`tools.cmake.cmaketoolchain:user_toolchain`** — the recommended
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

- **`CMAKE_PROJECT_TOP_LEVEL_INCLUDES`** (CMake 3.24+) — a CMake-native
  mechanism for additional files included after the toolchain. Not
  Conan-specific.
- **Chain via `include()` in your own toolchain wrapper** — a thin
  custom wrapper that includes the needed toolchains in sequence.

In a typical setup (vendor toolchain + Conan), the canonical approach is
to set the vendor toolchain via
`tools.cmake.cmaketoolchain:user_toolchain` in the Conan profile, with
`CMAKE_TOOLCHAIN_FILE` pointing to `conan_toolchain.cmake`, which in turn
includes the vendor toolchain.

## Conan: separating profiles and who initiates what

When a project has a package manager and third-party dependencies,
there are two possible ways to build them:

1. **Via the package manager** — Conan resolves and builds
   deps before CMake even runs.
2. **Via CMake itself** — `FetchContent_MakeAvailable()`,
   `ExternalProject_Add()`, `add_subdirectory(third_party/...)`.

If Conan is already in the project — all external dependencies go through it.
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
  conan+FetchContent does not — you end up with two zlиbs in one binary.

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

**From CMakeLists this looks like a standard find_package integration**
— Conan is "invisible" to the project description itself. This is correct:
the project knows it needs `OpenSSL`, and does not know (and should not
need to know) whether it came from the system, from Conan, or was built locally.

Exceptions where FetchContent is justified:

- A header-only utility not available in Conan, where adding it there
  for a single use is overkill.
- Build-time tools (code generators, formatters) that are not linked
  into your binary. Though `tool_requires` in Conan 2 handles this too.
- The project has no package manager at all.

**Conan profiles for deps vs. your code:**

The build profile for dependencies is **not** the profile for your code.
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
**directory-scoped defaults** that are inherited by nested CMakeLists.

`set(CMAKE_CXX_STANDARD 23)` in the root CMakeLists leaks into:

- `add_subdirectory(third_party/foo)` → yes, it leaks. If `foo`
  was written for C++17 and uses something removed or broken in C++23
  — it will break.
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

**Also leaks in the same way:** `CMAKE_CXX_FLAGS`, `CMAKE_CXX_EXTENSIONS`,
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

`cxx_std_23` is a **minimum** requirement, not a forced value. Consumers
via PUBLIC get "I need a compiler with at least C++23", but the specific
standard can be raised higher.

This is cleaner but requires discipline on every target and doesn't
work perfectly for INTERFACE-only fragments.

**Pragmatic compromise:**

- `set(CMAKE_CXX_STANDARD 23)` globally as a default for your own code
  — convenient and readable.
- `block()` for cases where a dep needs something different and
  `add_subdirectory` can't be avoided.
- First priority — **don't use `add_subdirectory` for third-party**,
  so the question of leaks doesn't arise at all. Conan covers this
  for most cases.

## Anti-patterns

### `CMAKE_CXX_FLAGS` in presets with everything in it

```json
"CMAKE_CXX_FLAGS": "-Werror -Wall -Wextra ... -fsanitize=address ..."
```

- Applies globally, catches warnings from third-party code.
- Does not compose — if another preset also touches `CMAKE_CXX_FLAGS`,
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
`clang_native_release`, `gcc_dev`, `gcc_release` — sooner or later
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
- [ ] Warnings are extracted into an INTERFACE target and applied explicitly.
- [ ] Warnings-as-errors via `CMAKE_COMPILE_WARNING_AS_ERROR`, not a
      hand-written `-Werror` / `/WX`.
- [ ] `CMAKE_EXPORT_COMPILE_COMMANDS ON`.
- [ ] Dependencies via `target_link_libraries` with explicit visibility.
- [ ] Include paths via `target_include_directories`, not globally.
- [ ] LTO/sanitizers — per-target and conditional, not via a global flag.
- [ ] If `add_subdirectory` is used for in-tree source deps — wrapped
      in `block()` to protect against `CMAKE_*` leaks.

Invocation level (`CMakePresets.json`):

- [ ] `CMakeUserPresets.json` is in `.gitignore`.
- [ ] `CMAKE_CXX_FLAGS` in presets — only thin toolchain-specific
      wiring (e.g. module cache path).
- [ ] Dependency paths via env vars with documentation.
- [ ] Cross-compilation via `CMAKE_TOOLCHAIN_FILE`, not by manually
      specifying compilers.
- [ ] Composition via `inherits`, no copy-paste between presets.
- [ ] `binaryDir` is unique per preset.
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
warning flags, sanitizer settings, and project include paths — that means
project policy has leaked into build invocation. The fix is to move it
back into CMakeLists.
