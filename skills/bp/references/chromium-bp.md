# Chromium C++ guidelines

## Code style

- Prefer Chromium's existing patterns, components and style
- Follow Google/Chromium C++ style guide consistently

## Best practices

- Add at least `DCHECK` at the beginning of each method for each pointer member access, to catch use-after-free bugs early in development and testing
- Avoid callbacks bound with `base::Unretained(this)`. Prefer the `WeakPtr` pattern - add `base::WeakPtrFactory<ClassName> weak_factory_{this};` to the class and bind callbacks using `weak_factory_.GetWeakPtr()`
- If SEQUENCE_CHECKER is used, apply it consistently to all methods of a class
- Methods returning a view into internal state (`std::string_view`, `base::span`, `const T&`) must be ref-qualified: `std::string_view name() const& { return name_; }` plus `std::string name() && { return std::move(name_); }`. On a temporary (`MakeFoo().name()`, `for (char c : MakeFoo().name())`) the `&&` overload returns an owning value instead of a view that dangles at the end of the full expression. Use `= delete` on the `&&` overload instead if moving out is not meaningful

## KeyedService derived classes

- Avoid storing `KeyedService` derived classes in `std::unique_ptr` because they manage their own lifetime via the keyed service factory mechanism. Use `raw_ptr` instead
- Explicitly drop `raw_ptr` pointers to other services in the `Shutdown()` method, not the destructor, to prevent dangling pointers during service teardown
