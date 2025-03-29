class Node:
    __slots__ = ('key', 'value', 'next')  # Optimize memory usage

    def __init__(self, key, value, next_node=None):
        self.key = key
        self.value = value
        self.next = next_node


class HashMapSeparateChainingDict:
    DEFAULT_CAPACITY = 16  # Default number of buckets

    def __init__(self, buckets=None, size=0):
        # Initialize buckets with shallow copy
        if buckets is not None:
            self.buckets = buckets
        else:
            self.buckets = [None] * self.DEFAULT_CAPACITY
        self.size = size  # Number of key-value pairs

    def cons(self, key, value):
        new_buckets = list(self.buckets)  # Shallow copy for immutability
        index = self._hash(key)
        current = new_buckets[index]

        # Traverse the linked list to check for existing key
        prev = None
        found = False
        while current:
            if current.key == key:
                # Replace existing node
                new_node = Node(key, value, current.next)
                if prev:  # Middle node replacement
                    prev.next = new_node
                else:     # Head node replacement
                    new_buckets[index] = new_node
                found = True
                break
            prev, current = current, current.next

        # Handle insertion result
        if found:
            new_size = self.size  # No size change for replacement
        else:
            # Insert new node at head
            new_node = Node(key, value, new_buckets[index])
            new_buckets[index] = new_node
            new_size = self.size + 1

        return HashMapSeparateChainingDict(new_buckets, new_size)

    def remove(self, key):
        new_buckets = list(self.buckets)
        index = self._hash(key)
        current = new_buckets[index]

        prev = None
        found = False
        while current:
            if current.key == key:
                # Remove current node
                if prev:
                    prev.next = current.next  # Middle node removal
                else:
                    new_buckets[index] = current.next  # Head node removal
                found = True
                break
            prev, current = current, current.next

        if found:
            return HashMapSeparateChainingDict(new_buckets, self.size - 1)
        else:
            return self  # Key not found, return original

    def member(self, key):
        index = self._hash(key)
        current = self.buckets[index]
        while current:
            if current.key == key:
                return True
            current = current.next
        return False

    def length(self):
        return self.size

    def to_list(self):
        items = []
        # Traverse all buckets
        for bucket in self.buckets:
            current = bucket
            # Traverse linked list
            while current:
                items.append((current.key, current.value))
                current = current.next
        return items

    @classmethod
    def from_list(cls, lst):
        d = cls()  # Create empty dict
        for k, v in lst:
            d = d.cons(k, v)  # Insert sequentially
        return d

    def concat(self, other):
        merged = self
        # Insert all entries from other dict
        for k, v in other.to_list():
            merged = merged.cons(k, v)
        return merged

    def filter(self, predicate):
        filtered = []
        for k, v in self.to_list():
            if predicate(k, v):
                filtered.append((k, v))
        return self.from_list(filtered)

    def mmap(self, mapper):
        mapped = []
        for k, v in self.to_list():
            new_k, new_v = mapper(k, v)
            mapped.append((new_k, new_v))
        return self.from_list(mapped)

    def reduce(self, reducer, initial):
        acc = initial
        for k, v in self.to_list():
            acc = reducer(k, v, acc)
        return acc

    def _hash(self, key):
        # Handle None key
        if key is None:
            return 0
        return hash(key) % len(self.buckets)

    # ----------- Magic Methods -----------
    def __eq__(self, other):
        # Compare sorted entries (order-insensitive)
        self_sorted = sorted(self.to_list(), key=lambda x: str(x[0]))
        other_sorted = sorted(other.to_list(), key=lambda x: str(x[0]))
        return self_sorted == other_sorted

    def __str__(self):
        items = []
        # Sort for predictable output order
        for k, v in sorted(self.to_list(), key=lambda x: str(x[0])):
            items.append(f"{repr(k)}: {repr(v)}")
        return "{" + ", ".join(items) + "}"

    def __iter__(self):
        return iter([k for k, _ in self.to_list()])

    @classmethod
    def mempty(cls):
        return cls()
