---
name: C++ Coding Style
applyTo: "**/*.{cpp,hpp,cppm,ipp,h,cc}"
---

# C++ coding style

## Core Principles

```cpp
// BAD: Easy to use incorrectly
class Buffer {
    // Based on data type impossible to distinguish between 1 char and char array
    char* data;
    size_t size;
public:
    Buffer(size_t size) : data(new char[size]), size(size) {}
    char* getData() { return data; }  // Raw pointer exposed
    size_t getSize() { return size; }  // c++ standard has clear reserved names for size operations
    // No destructor - memory leak! And zero/three/five rule violation
};

// GOOD: Hard to use incorrectly. Internal structure is protected and hidden
class Buffer {
    // Proper data type explicitly indicates it is a buffer of characters
    vector<char> data;
public:
    Buffer(size_t size) : data(size) {}

    // Fast access - precondition: index < size(), no bounds check
    char& operator[](size_t index) {
        assert(index < data.size());
        return data[index];
    }

    const char& operator[](size_t index) const {
        assert(index < data.size());
        return data[index];
    }

    // Safe access - returns nullopt on out-of-range (char is trivially copyable, copy is fine)
    std::optional<char> at(size_t index) const {
        if (index >= data.size())
            return std::nullopt;
        return data[index];
    }

    size_t size() const { return data.size(); }  // Naming consistent with standard library
    char* rawData() { return data.data(); }  // Explicit name when raw access needed
};
```

### Principle of Least Astonishment

- Use expected operators and patterns for each programming language

```cpp
// BAD: Unexpected behavior and poor error messages
class Vector3 {
    float x, y, z;
public:
    Vector3 multiply(const Vector3& other) {  // Expected operator* instead
        return Vector3{x * other.x, y * other.y, z * other.z};
    }

    // using int for index allows negative indices and almost always wrong
    // in contemporary C++ code
    float get(int index) {
        // Throws too generic exception
        if (index < 0 || index > 2) throw runtime_error("Error");
        // UB access to y and z components
        return (&x)[index];
    }
};

// GOOD: Intuitive interface with clear error messages
class Vector3 {
    float x, y, z;
public:
    // Use operator* for multiplication because it is expected by developers
    // and supports natural syntax
    Vector3 operator*(const Vector3& other) const {
        return Vector3{x * other.x, y * other.y, z * other.z};
    }

    // Standard array-like access
    // size_t limits the index to >= 0 so we don't need to check
    // for negative indices - it is guaranteed by the type system
    float operator[](size_t index) const {
        switch (index) {
            case 0: return x;
            case 1: return y;
            case 2: return z;
            // Precondition: index must be 0, 1, or 2
            default: std::unreachable();  // Clear indication of invalid index, no exceptions needed
        }
    }

    // Behaves like built-in types
    bool operator==(const Vector3& other) const = default;
};
```

## Design Standards

### Naming Conventions

#### Function Names

- Write a well-known abbreviation in camelCase like `setHtml`, not capitalized like `setHTML`
- Reserve the `get` prefix for explicit owning copies of non-trivial members (e.g., `getTitle()`), as defined in Member Accessor Naming

```cpp
// BAD: Non-descriptive and inconsistent naming
class Document {
    void proc();           // What does this process? Unnecessary abbreviation
    void setHTML(string);  // Inconsistent capitalization
    int getSize();         // Getter with get prefix, wrong return type and inconsistent with std lib
    void changeTitle();    // Inconsistent with setter pattern
    void openDocument();   // Redundant class name in method name
};

// GOOD: Descriptive and consistent naming
class Document {
    void processContent();                // Clear, not shortened name
    void setHtml(string_view content);  // Consistent with camelCase and abbreviation rules
    size_t size() const;                    // Consistent with standard library naming conventions and dont have get prefix
    void setTitle(string_view title);  // Valid marker for setter
    void open();                          // No class name prefix to avoid redundancy like `Document::openDocument`
};
```

#### Function Arguments

- Group arguments with type aliases or structs
- Prefer `std::string_view` over `const std::string&` for read-only string arguments - it accepts `std::string`, string literals, and substrings without allocation

```cpp
// BAD: Too many arguments and confusing order
void createWindow(bool resizable, int x, int y, string title, int width, int height, bool visible) {
    // Which size parameter is which?
}

// GOOD: Logical order, grouped parameters and default values
struct WindowConfig {
    string title;
    int x, y;
    int width, height;
    bool resizable = true;
    bool visible = true;
};

void createWindow(const WindowConfig& config) {
    // Clear and extensible
}

// GOOD: For simple, well-known cases of arguments
void setSize(int width, int height) {
    // This is intuitive and expected
}
```

```cpp
// BAD: Inconsistent argument order across similar functions
void copyFile(string_view source, string_view destination, bool overwrite);
void moveFile(bool overwrite, string_view destination, string_view source);

// GOOD: Consistent argument order
void copyFile(string_view source, string_view destination, bool overwrite = false);
void moveFile(string_view source, string_view destination, bool overwrite = false);
```

#### Member Accessor Naming

Standard naming pattern for class member accessors
The general idea is to provide a cheap way to access the member value without
forcing an allocation or copy, while still allowing for an explicit owning copy when needed.

Lets assume that:

View - is a zero-cost, read-only handle that does not own the data:

- plain copy of a trivially-copyable small type (`sizeof(T) <= sizeof(void*)`) - cheaper than a reference
- `std::string_view`, `std::span<T>` - non-owning slice of a sequence
- `const T&` - reference to a complex object

The View examples are priority-ordered from preferable API to less preferable.
The exact result depends on the type of the member and the expected usage patterns.
So, it should look like this:

- `int` -> plain copy
- `std::string` -> `std::string_view`
- `std::vector<T>` -> `std::span<T>`
- `complex objects` -> `const T&`

Rules for always-present member (`T` always exists):

| Method            | Semantics                                           |
|-------------------|-----------------------------------------------------|
| `obj() -> view`   | Zero-cost read access; returns a view of the member |
| `getObj() -> T`   | Explicit owning copy - signals allocation cost      |
| `setObj(view)`    | Sets or replaces the value                          |
| `isFoo() -> bool` | `true` if the value satisfies property *Foo*        |

Rules for optional member (`std::optional<T>`, may be absent):

| Method                             | Semantics                                                    |
|------------------------------------|--------------------------------------------------------------|
| `hasObj() -> bool`                 | `true` if the value is present                               |
| `obj() -> const std::optional<T>&` | View of the optional; caller decides how to handle absence   |
| `getObj() -> T`                    | Explicit owning copy - signals allocation cost               |
| `setObj(view)`                     | Sets or replaces the value                                   |
| `takeObj() -> T`                   | Moves out ownership; after the call `hasObj() == false`      |
| `isFoo() -> bool`                  | `true` if present **and** the value satisfies property *Foo* |

```cpp
class Document {
    std::string title_;                  // always exists
    std::optional<Metadata> metadata_;   // may be absent

public:
    // --- title (always present) ---

    // Cheap access - returns string_view (no allocation)
    string_view title() const { return title_; }

    // Owning copy of a non-trivial type - signals allocation cost
    std::string getTitle() const { return title_; }

    // Setter
    void setTitle(string_view t) { title_ = t; }

    // Property check
    bool isCapitalized() const { return !title_.empty() && std::isupper(title_[0]); }

    // --- metadata (optional) ---

    // Existence check - meaningful only for optional fields
    bool hasMetadata() const { return metadata_.has_value(); }

    // Cheap access - returns optional ref so caller decides how to handle absence
    const std::optional<Metadata>& metadata() const { return metadata_; }

    // Owning copy of a non-trivial type
    Metadata getMetadata() const {
        assert(metadata_.has_value());  // Precondition: metadata must be present
        return metadata_.value();
    }

    // Setter
    void setMetadata(const Metadata& m) { metadata_ = m; }

    // Move out - caller takes ownership, field becomes empty
    Metadata takeMetadata() {
        assert(metadata_.has_value());  // Precondition: metadata must be present
        return std::exchange(metadata_, std::nullopt).value();
    }

    // Property check - implies existence for optional fields
    bool isReadOnly() const { return hasMetadata() && metadata_->readOnly; }
};
```

#### Variable and Path Naming

- If variable content is not obvious, use `path` suffix

```cpp
// BAD: Unclear path naming, bad type usage
string data = "/home/user/documents";
string info = "config.json";
string location = "/tmp/cache/";

// GOOD: Clear path naming
std::filesystem::path documentsDir = "/home/user/documents";
std::filesystem::path configFile = "/home/user/config.json";
std::filesystem::path configFilename = "config.json";
std::filesystem::path cachePath = "/tmp/cache/";
```

### API Completeness

```cpp
// BAD: Incomplete API with unclear destructive operations
class UserManager {
    void add(const User& user);     // Create only
    User get(int id);               // Read only
    void remove(int id);            // Destructive operation not protected
};

// GOOD: Complete CRUD API with protected destructive operations
// Better than using int directly, but still not strongly typed
using user_id = int;

// Ideal case looks like this, but apply according to project conventions
template <typename Tag, typename T>
class StrongType {
public:
    using underlying_type = T;

    constexpr explicit StrongType(T value) : value_(value) {}

    constexpr T value() const { return value_; }

    friend constexpr bool operator==(const StrongType&, const StrongType&) = default;

private:
    T value_;
};

struct UserIdTag;
using UserId = StrongType<UserIdTag, int>;

class UserManager {
    // Create
    bool addUser(const User& user);

    // Read
    User user(UserId id) const;
    vector<User> allUsers() const;

    // Update
    bool updateUser(UserId id, const User& user);

    // Delete
    enum class DeleteResult { Success, NotFound };
    std::expected<void, DeleteResult> deleteUser(UserId id);

    // Bulk operations
    void deleteAllUsers(string_view confirmationToken);
};
```

## Implementation Guidelines

### Development Process

```cpp
// BAD: Inconsistent API patterns within the same class
class FileManager {
    // Naming duplication between class and methods
    // Non-specific argument types
    bool openFile(string path);          // Returns bool
    File* createFile(string path);       // Returns pointer
    void deleteFile(string path);        // Returns void
    int moveFile(string fromPath, string toPath); // Returns int (error code).
};

// GOOD: Consistent error handling and return patterns
class FileHandler {
  public:
    enum class Result { Success, NotFound, PermissionDenied, AlreadyExists };

    Result create(const std::filesystem::path& path);
    Result open(const std::filesystem::path& path);
    Result move(const std::filesystem::path& from, const std::filesystem::path& to);
    Result remove(const std::filesystem::path& path);

    Handler* fileHandler();

  private:
    InternalHandler mFileHandler; // Internal handler for file operations
};
```

### Error Handling

It is better to avoid exceptions in APIs, especially in C++.
First because they break the flow of the program and make it harder to reason about.
Second, because it is too easy to ignore them until it is too late.
Instead, if possible use `std::expected` or `std::optional` if the
function legally return nothing.
If `std::expected` is not available, use `std::variant<T, ErrorType>`.

```cpp
// BAD: Unhelpful error messages and unclear failure modes
class Database {
    bool connect(string connectionString) {
        // Returns false with no indication of what went wrong
        return false;
    }

    void executeQuery(string sql) {
        // Can fail silently or throw generic exception
        throw runtime_error("Query failed");
    }
};

// GOOD: Clear error messages with actionable guidance
class Database {
    enum class ConnectionResult {
        Success,
        InvalidConnectionString,
        NetworkError,
        AuthenticationFailed
    };

    ConnectionResult connect(string_view connectionString) {
        // Clear indication of what went wrong
        if (connectionString.empty()) {
            return ConnectionResult::InvalidConnectionString;
        }
        // ... other checks
        return ConnectionResult::Success;
    }

    struct SuccessQueryResult {
        vector<Row> data;
    };

    std::expected<SuccessQueryResult, string> executeQuery(string_view sql) {
        if (sql.empty()) {
            return std::unexpected{"SQL query cannot be empty. Provide a valid SQL statement."};
        }
        // ... execute query
        return SuccessQueryResult{true, data};
    }
};
```

### Common Tasks

```cpp
// BAD: Complex setup for simple operations
class ConfigManager {
    void initialize(string_view configDir, string_view appName) {
        // Complex initialization required before use
    }
    bool setConfigValue(string_view section, string_view key, string_view value) {
        if (!isInitialized) return false;
        // ...
    }
    string getConfigValue(string_view section, string_view key) {
        if (!isInitialized) return "";
        // ...
    }
};

// Usage: Complex and error-prone
ConfigManager config;
config.initialize("/etc/myapp", "MyApp");
config.setConfigValue("ui", "theme", "dark");

// GOOD: Simple interface for common operations
class ConfigManager {
public:
    ConfigManager(string_view configDir = "/etc/myapp", string_view appName = "MyApp") {}

    void setTheme(string_view theme) { /* ... */ }
    string theme() const { /* ... */ }

    // Explicitly fix sections in the API
    void setSectionValue(string_view key, string_view value) { /* ... */ }
    string sectionValue(string_view key) const { /* ... */ }
};

// Usage: Simple and intuitive
auto config = ConfigManager();
config.setTheme("dark");
```

## Compile-time constants

Let the compiler deduce the element type and size when the deduced type is the one you need:

```cpp
// BAD: size is counted by hand and can drift from the elements
constexpr std::array<int, 3> values = {1, 2, 3};

// GOOD: type and size are deduced
constexpr auto values = std::array{1, 2, 3};
```

When the needed type differs from the deduced one (e.g. `uint8_t` from integer literals), keep the explicit `std::array<T, N>`: casting every element to enable deduction defeats the purpose of brevity.

## Language usage

### Structured bindings

Name the parts of a pair or a tuple with a structured binding instead of `.first` and `.second`:

```cpp
// BAD: the reader has to remember what first and second hold
for (const auto& item : prices) std::println("{}: {}", item.first, item.second);

// GOOD
for (const auto& [product, price] : prices) std::println("{}: {}", product, price);
```

### Absent enum values

Express "not set" as `std::optional<Enum>`, not as an `Undefined` or `Unknown` enumerator. Keep `Unknown` only when it is a real value of the domain, such as a value received from an external system or stored in a database.

Why: an enumerator that means "not set" passes for a valid value, so every function that takes the enum has to check for it.

```cpp
// BAD: every switch over Color has to handle a value that is not a color
enum class Color { Undefined, Red, Green };
Color color = Color::Undefined;

// GOOD: absence is visible in the type
enum class Color { Red, Green };
std::optional<Color> color;
```

### Time

- Measure intervals and timeouts with `std::chrono::steady_clock`; use `system_clock` for dates and wall-clock time. Why: `system_clock` jumps when the system time is changed, so an interval measured with it can come out negative.
- Combine only time points of the same clock. Converting one clock to another through `time_since_epoch()` mixes different epochs.
- Convert a duration to a coarser unit with `std::chrono::floor`, `ceil`, or `round`, so the rounding is explicit; `duration_cast` truncates silently.
- Keep durations typed, and call `.count()` only at a boundary: logging, serialization, a C API.

```cpp
// BAD: 1999 ms silently becomes 1 s; the unit is lost in an int
auto seconds = std::chrono::duration_cast<std::chrono::seconds>(elapsed);
void wait(int timeoutMs);

// GOOD
auto seconds = std::chrono::round<std::chrono::seconds>(elapsed);
void wait(std::chrono::milliseconds timeout);
```

### Const correctness

- Mark `const` every method that does not change the object, and every variable that is not reassigned. Leave a local non-`const` when it is moved from later: `std::move` of a `const` object copies it.
- Fix a missing `const` where it is missing instead of hiding it with `mutable` or `const_cast`. `mutable` stays for members that are not part of the observable state, such as a mutex or a cache.

```cpp
// BAD
size_t itemCount() { return items_.size(); }
auto total = sum(items);  // never reassigned

// GOOD
size_t itemCount() const { return items_.size(); }
const auto total = sum(items);
```

### Namespaces

- Put all internal helpers of a `.cpp` file into one anonymous namespace at the top, after the includes, so the reader finds them in one place.
- Write a nested namespace as `namespace a::b {`, not as `namespace a { namespace b {`.

### Unused values

Mark a variable or a parameter that is unused in some builds with `[[maybe_unused]]`, not with `(void)x;`. Drop the name of a parameter that is never used.

```cpp
// BAD
const bool removed = ids.erase(id) == 1;
(void)removed;
assert(removed);

// GOOD: the declaration says the variable is unused in release builds
[[maybe_unused]] const bool removed = ids.erase(id) == 1;
assert(removed);
```
