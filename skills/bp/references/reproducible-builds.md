# Reproducible builds best practices

## Definitions

Source of truth — everything in the repo from which the build is uniquely reproduced: scripts, lock files, CI, pinned toolchain
Generated artifact — IDE settings, generated project files. Useful, but not required for the build
Local config - IDE settings, local config files, and other environment state that could affect the build locally but should not affect the main build path on other machines. Should never be committed
Snowflake — a build that works only on one machine due to undocumented environment state

## Best practices

- Keep everything that affects build output in the repo — otherwise the build can't be reproduced from a clean clone.
- Don't commit generated files — commit the generator, not its output; artifacts may be stored for convenience, but must not be the only path to a working build.
- Pin toolchain and dependency versions — otherwise different machines produce different code and different binaries.
- Don't rely on the IDE for build steps — the editor is optional for the build; all steps must work without it.
- For long-lived or multi-person projects, use a hermetic environment (Nix, Docker, pinned container) — scripts declare reproducibility, a hermetic environment enforces it.
