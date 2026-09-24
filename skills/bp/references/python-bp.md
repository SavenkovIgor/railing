# Python Best Practices

`Scripts` - python files that could be started directly from CLI
`Modules` - python files that are imported by other python files, but cant be started directly

## Style

- Follow PEP 8 style guidelines
- Use 4 spaces for indentation
- Sort imports with VSCode's "Organize imports" command

## Type hints

- Preserve existing local variable type hints
- Require type hints for all functions (arguments and return values)
- If you have a family of related functions, you should consider joining them into a class
- Use built-in types for type hints (`list`, `dict`, `tuple` instead of `List`, `Dict`, `Tuple` from `typing`) — since Python 3.9 built-ins support generics natively, so `typing` imports are redundant and add noise

## Language core & Libraries

- Use Python 3 syntax and features
- Prefer standard library modules over third-party dependencies unless strictly necessary
- Use `pathlib` module for path operations instead of `os.path` or string paths
- Use the logging module instead of print statements for complex scripts

## Code organization

- Add comments only for complex or non-obvious code; docstrings should be concise (one line max, or none if the function name and type hints are self-explanatory)
- Prefer explicit type | none semantic over exceptions for control flow (e.g., return None instead of raising an exception for expected cases). Exceptions should be reserved for truly exceptional cases, not for things that happen frequently

## Strings

- Prefer f-strings for string formatting
- When constructing Path with string literals, use compact notation: `'a/b/c'` instead of `'a' / 'b' / 'c'`

## Script structure & requirements

Scripts should be organized using the following pattern (exclude comments):

For simple cases where no arguments are needed:

```python
#!/usr/bin/env python3
import sys

def main(args: list[str]) -> int:
    # Main function code
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
```

This structure allows for better testability, making return codes explicit and usable in CLI.
It also provides a clear entry point for the script, and allows for easier integration with other tools and scripts.

If you need to parse arguments, you can use an extension of this pattern:

```python
#!/usr/bin/env python3
import sys
import argparse

def main(args: argparse.Namespace) -> int:
    # Main function code
    return 0

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    # Parser configuration should be done here, so that separation between
    # argument syntax declaration and main logic is clear
    args = arg_parser.parse_args()
    sys.exit(main(args))
```

Also ensure the script has executable permissions (`chmod +x`) at git repo level
(Verify with `git ls-tree HEAD <path>` - should show `100755`)

## Modules structure & requirements

- In modules if a main function exists, it is reserved for unit tests
