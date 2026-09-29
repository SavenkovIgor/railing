# Chromium C++ guidelines

## Code style

- Prefer Chromium's existing patterns, components and style
- Follow Google/Chromium C++ style guide consistently

## Best practices

- Add at least `DCHECK` at the beginning of each method for each pointer member access, to catch use-after-free bugs early in development and testing
- Avoid callbacks bound with `base::Unretained(this)`. Prefer the `WeakPtr` pattern - add `base::WeakPtrFactory<ClassName> weak_factory_{this};` to the class and bind callbacks using `weak_factory_.GetWeakPtr()`
- If SEQUENCE_CHECKER is used, apply it consistently to all methods of a class

## KeyedService derived classes

- Avoid storing `KeyedService` derived classes in `std::unique_ptr` because they manage their own lifetime via the keyed service factory mechanism. Use `raw_ptr` instead
- Explicitly drop `raw_ptr` pointers to other services in the `Shutdown()` method, not the destructor, to prevent dangling pointers during service teardown
