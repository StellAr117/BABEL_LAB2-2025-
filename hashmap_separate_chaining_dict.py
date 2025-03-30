from dataclasses import dataclass
from typing import Any, Optional, Tuple, List, Callable


@dataclass(frozen=True)
class Node:
    """不可变的链表节点，用于处理哈希冲突"""
    key: Any
    value: Any
    next: Optional['Node'] = None


class HashMapSeparateChainingDict:
    """基于不可变数据结构的哈希字典（分离链接法）"""
    def __init__(
        self,
        buckets: Tuple[Optional[Node], ...] = tuple([None] * 10),
        size: int = 0,
        keys_order: Tuple[Any, ...] = ()
    ):
        self.buckets = buckets
        self.size = size
        self.keys_order = keys_order

    def _hash(self, key) -> int:
        """简单的哈希函数，返回0-9的哈希值"""
        return hash(key) % 10

    def cons(self, key: Any, value: Any) -> 'HashMapSeparateChainingDict':
        """添加键值对，返回新字典"""
        index = self._hash(key)
        current = self.buckets[index]

        # 检查键是否已存在
        exists = False
        temp = current
        while temp:
            if temp.key == key:
                exists = True
                break
            temp = temp.next

        if exists:
            # 替换现有节点的值
            new_nodes = []
            temp = current
            while temp:
                if temp.key == key:
                    new_nodes.append(Node(key, value, temp.next))
                else:
                    new_nodes.append(Node(temp.key, temp.value, temp.next))
                temp = temp.next

            # 重建链表
            new_head = None
            for node in reversed(new_nodes):
                new_head = Node(node.key, node.value, new_head)

            new_buckets = list(self.buckets)
            new_buckets[index] = new_head
            return HashMapSeparateChainingDict(
                tuple(new_buckets), self.size, self.keys_order
            )
        else:
            # 添加新节点到链表头部
            new_buckets = list(self.buckets)
            new_buckets[index] = Node(key, value, current)
            return HashMapSeparateChainingDict(
                tuple(new_buckets), self.size + 1, self.keys_order + (key,)
            )

    def get(self, key: Any) -> Optional[Any]:
        """获取键对应的值"""
        index = self._hash(key)
        current = self.buckets[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next
        return None

    def remove(self, key: Any) -> 'HashMapSeparateChainingDict':
        """删除键值对，返回新字典"""
        index = self._hash(key)
        current = self.buckets[index]
        new_head = None
        found = False

        # 重建链表，跳过要删除的节点
        temp = current
        while temp:
            if temp.key == key:
                found = True
                temp = temp.next
                continue
            new_head = Node(temp.key, temp.value, new_head)
            temp = temp.next

        # 反转链表恢复顺序
        reversed_head = None
        while new_head:
            reversed_head = Node(new_head.key, new_head.value, reversed_head)
            new_head = new_head.next

        new_buckets = list(self.buckets)
        new_buckets[index] = reversed_head
        return HashMapSeparateChainingDict(
            tuple(new_buckets),
            self.size - 1 if found else self.size,
            tuple(k for k in self.keys_order if k != key)
        )

    def __len__(self) -> int:
        return self.size

    def __contains__(self, key: Any) -> bool:
        return self.get(key) is not None

    def to_list(self) -> List[Tuple[Any, Any]]:
        """转换为Python列表（保留插入顺序）"""
        return [(k, self.get(k)) for k in self.keys_order if k in self]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HashMapSeparateChainingDict):
            return False
        return self.to_list() == other.to_list()


# 辅助函数 -------------------------------------------------
def mempty() -> HashMapSeparateChainingDict:
    """创建空字典"""
    return HashMapSeparateChainingDict()


def cons(key: Any, value: Any, d: HashMapSeparateChainingDict) -> HashMapSeparateChainingDict:
    """添加键值对（保持原方法名）"""
    return d.cons(key, value)


def remove(d: HashMapSeparateChainingDict, key: Any) -> HashMapSeparateChainingDict:
    """删除键"""
    return d.remove(key)


def member(key: Any, d: HashMapSeparateChainingDict) -> bool:
    """检查键是否存在"""
    return key in dimport math


class Node:
    __slots__ = ('key', 'value', 'next')  # Optimize memory usage

    def __init__(self, key, value, next_node=None):
        self.key = key
        self.value = value
        self.next = next_node


class HashMapSeparateChainingDict:
    DEFAULT_CAPACITY = 16  # Default number of buckets

    def __init__(self, buckets=None, size=0):
        if buckets is not None:
            self.buckets = buckets
        else:
            self.buckets = [None] * self.DEFAULT_CAPACITY
        self.size = size  # Number of key-value pairs

    def cons(self, key, value):
        new_buckets = list(self.buckets)  # Shallow copy for immutability
        index = self._hash(key)
        current = new_buckets[index]

        prev = None
        found = False
        while current:
            if self._keys_equal(current.key, key):
                new_node = Node(key, value, current.next)
                if prev:
                    prev.next = new_node
                else:
                    new_buckets[index] = new_node
                found = True
                break
            prev, current = current, current.next

        if found:
            new_size = self.size
        else:
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
            if self._keys_equal(current.key, key):
                if prev:
                    prev.next = current.next
                else:
                    new_buckets[index] = current.next
                found = True
                break
            prev, current = current, current.next

        if found:
            return HashMapSeparateChainingDict(new_buckets, self.size - 1)
        else:
            return self

    def member(self, key):
        index = self._hash(key)
        current = self.buckets[index]
        while current:
            if self._keys_equal(current.key, key):
                return True
            current = current.next
        return False

    def _keys_equal(self, key1, key2):
        if key1 is key2:
            return True
        if (isinstance(key1, float) and
                isinstance(key2, float) and
                math.isnan(key1) and math.isnan(key2)):
            return True
        return key1 == key2

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
        if key is None:
            return 0
        if isinstance(key, float) and math.isnan(key):
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


def cons(key, value, hmap):
    return hmap.cons(key, value)


def remove(hmap, key):
    return hmap.remove(key)


def member(key, hmap):
    return hmap.member(key)


def length(hmap):
    return hmap.length()


def to_list(hmap):
    return hmap.to_list()


def from_list(lst):
    if isinstance(lst, dict):
        lst = list(lst.items())
    return HashMapSeparateChainingDict.from_list(lst)


def from_dict(d):
    return HashMapSeparateChainingDict.from_list(list(d.items()))


def concat(a, b):
    return a.concat(b)


def mempty():
    return HashMapSeparateChainingDict.mempty()


def filter(hmap, predicate):
    return hmap.filter(predicate)


def mmap(hmap, mapper):
    return hmap.mmap(mapper)


def reduce(hmap, reducer, initial):
    return hmap.reduce(reducer, initial)



def to_list(d: HashMapSeparateChainingDict) -> List[Tuple[Any, Any]]:
    """转换为Python列表"""
    return d.to_list()


def from_list(lst: List[Tuple[Any, Any]]) -> HashMapSeparateChainingDict:
    """从Python列表创建"""
    d = mempty()
    for k, v in reversed(lst):  # 倒序插入以保证顺序正确
        d = cons(k, v, d)
    return d