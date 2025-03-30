# GROUP-NAME - lab NUMBER - variant NUMBER

A Python implementation of an immutable hashmap using separate
chaining for collision resolution.
Designed with functional programming patterns,
this structure returns a new instance on every modification,
preserving the original data.

## Project structure

- `hashmap_separate_chaining_dict.py`

-- Implementation of immutable hashmap using separate chaining.
  Core features: `cons`, `remove`, `member`, `filter`, `mmap`, `reduce`.  
  Immutable semantics (returns new instances on modification).  

- `hashmap_separate_chaining_dict_test.py`

-- Unit and property-based tests (PBT).
  Validates: insertion/removal, equality checks, monoid laws,
  filtering/mapping operations.  
  Uses Hypothesis for generative testing.  

## Features

- **Core Operations**  
   - `cons(key, value)`: Insert a key-value pair (returns new instance).  
   - `remove(key)`: Delete a key-value pair (returns new instance).  
   - `member(key)`: Check if a key exists.  
   - `length()`: Get the number of entries.  

- **Functional Utilities**  
   - `filter(predicate)`: Retain entries matching a predicate.  
   - `mmap(mapper)`: Apply a mapper function to all entries.  
   - `reduce(reducer, initial)`: Fold entries into an accumulated value.  

- **Conversions**  
   - `to_list()`: Convert to a list of `(key, value)` tuples.  
   - `from_list()`: Create from a list/dictionary.  
   - `concat(other)`: Merge two hashmaps (last write wins on conflicts).  

- **Immutability**  
  All operations return new instances, ensuring thread safety and
   predictable state transitions.

## Contributors

| Contributor       | Contact                | Contributions                 |
| ----------------- | ---------------------- | ----------------------------- |
| He Jian           | <hj66216084@gmail.com> | Core implementation & testing |
| Aleksandr Penskoi | <penskoi@example.com>  | Project template design       |

## Changelog

### 2025-3-26

- Complete `hashmap_separate_chaining_dict_test` implementation  

### 2025-3-28

- Complete `hashmap_separate_chaining_dict` implementation
- Initial project scaffolding  
- Basic README structure  

### 2025-3-30

- finish all part

## Design notes

Comparison: Mutable vs. Immutable HashMaps

| **Aspect**          | **Immutable**               | **Mutable**              |
|---------------------|-----------------------------|--------------------------|
| **State Changes**   | New instances on modify     | In-place state updates   |
| **Thread Safety**   | ✅ Thread-safe              | ❌ Needs sync           |
| **Memory Efficiency** | Shared buckets (optimized)| Full copies (higher cost)|
| **Use Cases**       | Functional/versioned data   | High-speed updates       |
| **Example**         | Data history tracking       | Real-time caching        |
