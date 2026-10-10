---
applyTo: "**/*.py"
---

# Python Code and API Design Guidelines

## Core Principles

**Primary Goal:** Make APIs easy to use correctly and hard to use incorrectly

```python
# BAD: Easy to use incorrectly
class Buffer:
    def __init__(self, size):
        self._data = [0] * size
        self._size = size

    def get_data(self):  # Exposes internal list directly
        return self._data

    def get_size(self):  # Unnecessary getter prefix
        return self._size

    def set_item(self, index, value):  # No bounds checking
        self._data[index] = value

# GOOD: Hard to use incorrectly, follows Python conventions
class Buffer:
    def __init__(self, size: int):
        self._data = [0] * size

    def __getitem__(self, index: int) -> int:
        if not 0 <= index < len(self._data):
            raise IndexError(f"Buffer index {index} out of range [0, {len(self._data)})")
        return self._data[index]

    def __setitem__(self, index: int, value: int) -> None:
        if not 0 <= index < len(self._data):
            raise IndexError(f"Buffer index {index} out of range [0, {len(self._data)})")
        self._data[index] = value

    def __len__(self) -> int:
        return len(self._data)

    @property
    def raw_data(self) -> list[int]:  # Explicit when raw access needed
        return self._data.copy()
```

### Principle of Least Astonishment

- **Review all function names, class names, and API endpoints** - try to guess developer expectations and validate those names against them
- **Ensure error messages provide clear guidance** for developers using your APIs
- Use Pythonic operators and patterns (dunder methods, properties, context managers)
- Follow PEP 8 and standard library patterns for naming conventions
- Make custom classes behave like built-in types

```python
# BAD: Unexpected behavior and poor error messages
class Vector3:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def multiply(self, other):  # Expected __mul__ instead
        return Vector3(self.x * other.x, self.y * other.y, self.z * other.z)

    def get(self, index):  # Throws generic exception
        if index > 2:
            raise Exception("Error")
        return [self.x, self.y, self.z][index]

# GOOD: Intuitive interface with clear error messages
class Vector3:
    def __init__(self, x: float, y: float, z: float):
        self.x, self.y, self.z = x, y, z

    def __mul__(self, other: "Vector3") -> "Vector3":  # Expected operator
        return Vector3(self.x * other.x, self.y * other.y, self.z * other.z)

    def __getitem__(self, index: int) -> float:  # Standard sequence access
        if not 0 <= index <= 2:
            raise IndexError(f"Vector3 index must be 0, 1, or 2, got: {index}")
        return [self.x, self.y, self.z][index]

    def __eq__(self, other: object) -> bool:  # Behaves like built-in types
        if not isinstance(other, Vector3):
            return NotImplemented
        return (self.x, self.y, self.z) == (other.x, other.y, other.z)

    def __repr__(self) -> str:
        return f"Vector3({self.x}, {self.y}, {self.z})"
```

## Design Standards

### Error Handling and Return Types

In Python, prefer using exceptions for error conditions as they are part of the language design.
Use `Optional[T]` when a function may legitimately return `None`.
Use custom exception types to provide specific error information.
Consider using `Union` types or `dataclasses` for complex return types.

```python
from typing import Optional, Union
from dataclasses import dataclass

# For functions that may return nothing legitimately
def find_user(user_id: int) -> Optional[User]:
    """Returns user or None if not found."""
    return database.get_user(user_id)

# For operations that can fail with specific errors
class DatabaseError(Exception):
    pass

class UserNotFoundError(DatabaseError):
    def __init__(self, user_id: int):
        super().__init__(f"User with ID {user_id} not found")
        self.user_id = user_id

def get_user(user_id: int) -> User:
    """Returns user or raises UserNotFoundError."""
    user = database.get_user(user_id)
    if user is None:
        raise UserNotFoundError(user_id)
    return user

# For complex results
@dataclass
class ProcessResult:
    success: bool
    message: str
    data: Optional[dict] = None
```

### Naming Conventions

#### Function Names

- Use `snake_case` for functions and variables (PEP 8)
- Should be descriptive and concise
- Well-known abbreviations should be lowercase like `set_html` not `set_HTML`
- For properties use `@property` decorator, avoid `get` prefixes for getters
- Avoid repeating the class name in method names

```python
# BAD: Non-descriptive and inconsistent naming
class Document:
    def proc(self):           # What does this process? Unnecessary abbreviation
        pass

    def setHTML(self, content):  # Wrong case convention
        pass

    def get_size(self):       # Unnecessary getter prefix
        pass

    def change_title(self):   # Inconsistent with property pattern
        pass

    def open_document(self):  # Redundant class name in method name
        pass

# GOOD: Descriptive and consistent naming
class Document:
    def process_content(self):
        pass

    def set_html(self, content: str):
        pass

    @property
    def size(self) -> int:  # Property instead of getter
        return len(self._content)

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        self._title = value

    def open(self):  # No class name prefix
        pass
```

#### Function Arguments

- Use type hints for all parameters
- Should be in the order of most common usage
- For similar functions, the order of arguments should be consistent
- Avoid more than 4-5 arguments in a function
- Use keyword-only arguments for clarity when needed
- Use `dataclasses` or `TypedDict` for complex parameter groups

```python
from dataclasses import dataclass
from typing import TypedDict

# BAD: Too many arguments and confusing order
def create_window(resizable: bool, x: int, y: int, title: str,
                 width: int, height: int, visible: bool):
    pass

# GOOD: Using dataclass for configuration
@dataclass
class WindowConfig:
    title: str
    x: int = 0
    y: int = 0
    width: int = 800
    height: int = 600
    resizable: bool = True
    visible: bool = True

def create_window(config: WindowConfig):
    pass

# GOOD: For simple, well-known cases with keyword-only args
def set_size(*, width: int, height: int):
    """Use keyword-only to prevent confusion about order."""
    pass

# GOOD: Using TypedDict for flexible configurations
class WindowOptions(TypedDict, total=False):
    resizable: bool
    visible: bool
    theme: str

def create_window(title: str, width: int, height: int,
                 *, x: int = 0, y: int = 0, **options: WindowOptions):
    pass
```

#### Variable and Path Naming

- Always prefer to use `pathlib.Path` for any path handling
- For variables containing paths, use `_dir` suffix for directories and `_file` or `_path` suffix for full paths
- Use `_filename` for just the file name without the path

```python
from pathlib import Path

# BAD: Unclear path naming
data = "/home/user/documents"
info = "config.json"
location = "/tmp/cache/"

# GOOD: Clear path naming with pathlib
documents_dir = Path("/home/user/documents")
config_file = Path("/home/user/config.json")
config_filename = "config.json"
cache_dir = Path("/tmp/cache")
```

#### Argument Order and Consistency

- Most important/common arguments should come first
- Similar functions should have consistent argument order
- Use keyword-only arguments when order might be confusing

```python
# BAD: Inconsistent argument order across similar functions
def copy_file(source: str, destination: str, overwrite: bool):
    pass

def move_file(overwrite: bool, destination: str, source: str):
    pass

# GOOD: Consistent argument order, defaults for less common options
def copy_file(source: Path, destination: Path, *, overwrite: bool = False):
    pass

def move_file(source: Path, destination: Path, *, overwrite: bool = False):
    pass
```

### API Completeness

- APIs usually should contain all CRUD operations (Create, Read, Update, Delete)
  for main entities
- Use context managers for resource management
- Ensure destructive operations are protected or clearly marked
- Support both synchronous and asynchronous patterns when appropriate

```python
from typing import Optional, Iterator
from contextlib import contextmanager

# BAD: Incomplete API with unclear destructive operations
class UserManager:
    def add(self, user: User):     # Create only
        pass

    def get(self, user_id: int):   # Read only
        pass

    def remove(self, user_id: int):  # Destructive operation not protected
        pass

# GOOD: Complete CRUD API with protected destructive operations
from enum import Enum

class DeleteResult(Enum):
    SUCCESS = "success"
    NOT_FOUND = "not_found"
    PERMISSION_DENIED = "permission_denied"

class UserManager:
    # Create
    def add_user(self, user: User) -> bool:
        pass

    # Read
    def user(self, user_id: int) -> Optional[User]:
        pass

    def users(self) -> list[User]:
        pass

    def find_users(self, **criteria) -> Iterator[User]:
        pass

    # Update
    def update_user(self, user_id: int, user: User) -> bool:
        pass

    # Delete
    def delete_user(self, user_id: int) -> DeleteResult:
        pass

    def delete_all_users(self, *, confirmation_token: str) -> int:
        """Returns number of deleted users. Requires confirmation token."""
        if confirmation_token != "CONFIRM_DELETE_ALL":
            raise ValueError("Invalid confirmation token")
        return self._delete_all()

    # Context manager for batch operations
    @contextmanager
    def batch_operation(self):
        """Context manager for efficient batch operations."""
        try:
            self._begin_batch()
            yield self
        finally:
            self._commit_batch()
```

## Implementation Guidelines

### Development Process

- Use type hints consistently
- Follow PEP 8 style guidelines
- Test with developer expectations in mind
- Verify all names are descriptive and unambiguous
- Check consistency with existing project APIs
- Use `@property` for computed values and simple getters
- Implement appropriate dunder methods (`__str__`, `__repr__`, `__eq__`, etc.)

```python
# BAD: Inconsistent API patterns within the same class
class FileManager:
    def open_file(self, path: str) -> bool:          # Returns bool
        pass

    def create_file(self, path: str) -> 'File':      # Returns object
        pass

    def delete_file(self, path: str) -> None:        # Returns None
        pass

    def move_file(self, from_path: str, to_path: str) -> int:  # Returns int
        pass

# GOOD: Consistent error handling and return patterns
from enum import Enum
from pathlib import Path

class FileResult(Enum):
    SUCCESS = "success"
    NOT_FOUND = "not_found"
    PERMISSION_DENIED = "permission_denied"
    ALREADY_EXISTS = "already_exists"

class FileHandler:
    def create(self, path: Path) -> FileResult:
        pass

    def open(self, path: Path) -> FileResult:
        pass

    def move(self, from_path: Path, to_path: Path) -> FileResult:
        pass

    def remove(self, path: Path) -> FileResult:
        pass

    # Alternative: Use exceptions consistently
    # def open_file(self, path: Path) -> File:  # raises FileError
    # def create_file(self, path: Path) -> File:  # raises FileError

    @property
    def current_file(self) -> Optional[Path]:
        return self._current_file
```

### Testing Requirements

- Validate that common programming tasks are straightforward
- Use `pytest` for testing with clear test names
- Test both success and failure cases

```python
# BAD: Complex setup for simple operations
class ConfigManager:
    def __init__(self):
        self._initialized = False

    def initialize(self, config_dir: str, app_name: str):
        # Complex initialization required before use
        self._initialized = True

    def set_config_value(self, section: str, key: str, value: str) -> bool:
        if not self._initialized:
            return False
        # ...

    def get_config_value(self, section: str, key: str) -> str:
        if not self._initialized:
            return ""
        # ...

# Usage: Complex and error-prone
config = ConfigManager()
config.initialize("/etc/myapp", "MyApp")
config.set_config_value("ui", "theme", "dark")

# GOOD: Simple interface for common operations
from typing import ClassVar

class ConfigManager:
    _instance: ClassVar[Optional['ConfigManager']] = None

    def __init__(self, config_dir: Path = Path("/etc/myapp")):
        self._config_dir = config_dir
        self._load_config()

    @classmethod
    def instance(cls) -> 'ConfigManager':
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @property
    def theme(self) -> str:
        return self.get_value("ui.theme", "light")

    @theme.setter
    def theme(self, value: str):
        self.set_value("ui.theme", value)

    def set_value(self, key: str, value: str) -> None:
        # Simple dot notation for nested keys
        pass

    def get_value(self, key: str, default: str = "") -> str:
        pass

# Usage: Simple and intuitive
ConfigManager.instance().theme = "dark"
```

## Quality Checklist

### Before releasing any API

- [ ] All names follow PEP 8 conventions and are descriptive
- [ ] Type hints are provided for all public functions and methods
- [ ] Error messages provide clear guidance to developers
- [ ] Common programming tasks are straightforward
- [ ] Destructive operations are protected or clearly marked
- [ ] Successful usage is the obvious path
- [ ] Consistency with existing project APIs
- [ ] Function signatures follow Python conventions
- [ ] CRUD operations available for main entities (where applicable)
- [ ] Appropriate dunder methods implemented (`__str__`, `__repr__`, `__eq__`, etc.)
- [ ] Properties used instead of getter/setter methods where appropriate
- [ ] Context managers implemented for resource management when needed

### Python-Specific Checklist

- [ ] Uses `pathlib.Path` for file system operations
- [ ] Implements `__enter__` and `__exit__` for context managers when appropriate
- [ ] Uses `@property` and `@setter` decorators instead of getter/setter methods
- [ ] Follows duck typing principles when appropriate
- [ ] Uses type hints from `typing` module consistently
- [ ] Implements appropriate comparison operators (`__eq__`, `__lt__`, etc.) when needed
- [ ] Uses `dataclasses` or `NamedTuple` for data containers
- [ ] Follows PEP 8 naming conventions strictly

### Remember

> "If developers are smart, motivated, have experience with Python, are willing
   to read documentation, and want to succeed - yet they still fail to use
   your API correctly, it's the API's fault, not theirs."

### Goal

Create APIs where developers accidentally do the right thing by default,
requiring minimal thought or memorization to achieve their programming goals,
while following Python's philosophy of being explicit, readable, and "Pythonic".
