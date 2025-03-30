import itertools
from hypothesis import given, strategies as st
from hashmap_separate_chaining_dict import (
    HashMapSeparateChainingDict,
    concat,
    cons,
    from_list,
    from_dict,
    length,
    member,
    remove,
    to_list,
    mempty,
    filter,
    mmap,
    reduce
)


class TestHashMapSeparateChainingDict:
    def test_api(self):
        empty = HashMapSeparateChainingDict()
        l1 = cons(None, "c", cons(2, "b", cons("a", 1, empty)))
        l2 = cons("a", 1, cons(None, "c", cons(2, "b", empty)))

        assert str(empty) == "{}"
        assert str(l1) in [
            "{'a': 1, 2: 'b', None: 'c'}",
            "{'a': 1, None: 'c', 2: 'b'}",
            "{2: 'b', 'a': 1, None: 'c'}",
            "{2: 'b', None: 'c', 'a': 1}",
            "{None: 'c', 2: 'b', 'a': 1}",
            "{None: 'c', 'a': 1, 2: 'b'}"
        ]
        assert empty != l1
        assert empty != l2
        assert l1 == l2

        assert length(empty) == 0
        assert length(l1) == 3
        assert length(l2) == 3

        assert str(remove(l1, None)) in ["{2: 'b', 'a': 1}",
                                         "{'a': 1, 2: 'b'}"]
        assert str(remove(l1, "a")) in ["{2: 'b', None: 'c'}",
                                        "{None: 'c', 2: 'b'}"]

        assert not member(None, empty)
        assert member(None, l1)
        assert member("a", l1)
        assert member(2, l1)
        assert not member(3, l1)

        assert to_list(l1) in map(list, itertools.permutations(
            [("a", 1), (2, "b"), (None, "c")]
        ))
        assert l1 == from_list([("a", 1), (2, "b"), (None, "c")])
        assert l1 == from_list([(2, "B"), ("a", 1), (2, "b"), (None, "c")])
        assert concat(l1, l2) == from_list(
            [(2, "B"), ("a", 1), (2, "b"), (None, "c")]
        )

        buf = []
        for e in l1:
            buf.append(e)
        assert buf in map(list, itertools.permutations(["a", 2, None]))

        lst = (list(map(lambda e: e[0], to_list(l1))) +
               list(map(lambda e: e[0], to_list(l2))))
        for e in l1:
            lst.remove(e)
        for e in l2:
            lst.remove(e)
        assert lst == []

    def test_filter(self):
        data = from_list([(1, 1), (2, "a"), ("b", 3), ("4", 4), (5, None)])

        # Test filtering by integer keys
        filtered_int_keys = filter(data, lambda k, v: isinstance(k, int))
        result_keys = to_list(filtered_int_keys)
        expected_keys = [(1, 1), (2, "a"), (5, None)]
        assert sorted(result_keys, key=str) == sorted(expected_keys, key=str)

        # Test filtering by integer values
        filtered_int_values = filter(data, lambda k, v: isinstance(v, int))
        result_values = to_list(filtered_int_values)
        expected_values = [(1, 1), ("4", 4), ("b", 3)]
        assert sorted(result_values, key=str) == sorted(
            expected_values, key=str)

    def test_mmap(self):
        original = from_list({1: 1, 2: 2, 3: 3})
        mapped = mmap(original, lambda k, v: (str(k), str(v)))
        expected = {"1": "1", "2": "2", "3": "3"}
        assert sorted(to_list(mapped)) == sorted(expected.items())

    def test_reduce(self):
        empty_dict = mempty()
        data = from_list({"a": 2, "b": 3})
        assert reduce(empty_dict, lambda k, v, acc: acc + 1, 0) == 0
        assert reduce(data, lambda k, v, acc: acc + 1, 0) == 2
        assert reduce(data, lambda k, v, acc: acc + v, 0) == 5

    def test_empty(self):
        empty = mempty()
        data = from_list([(1, "one"), (2, "two")])
        assert concat(empty, data) == data
        assert concat(data, empty) == data
        assert length(empty) == 0


class TestHashMapPBT:
    _keys = st.one_of(st.integers(), st.text(), st.floats(), st.none())
    _values = st.one_of(st.integers(), st.text(), st.floats(), st.none())
    _dict_strategy = st.dictionaries(_keys, _values)

    @given(
        a=_dict_strategy,
        b=_dict_strategy,
        c=_dict_strategy
    )
    def test_monoid_associativity(self, a, b, c):
        dict_a = from_dict(a)
        dict_b = from_dict(b)
        dict_c = from_dict(c)
        left = concat(concat(dict_a, dict_b), dict_c)
        right = concat(dict_a, concat(dict_b, dict_c))
        assert left == right

    @given(_dict_strategy)
    def test_monoid_identity(self, d):
        hdict = from_dict(d)
        empty = mempty()
        assert concat(empty, hdict) == hdict
        assert concat(hdict, empty) == hdict

    @given(
        initial=st.dictionaries(_keys, _values),
        updates=st.dictionaries(_keys, _values)
    )
    def test_insert_override_property(self, initial, updates):
        hdict = from_dict(initial)
        updated = hdict
        for k, v in updates.items():
            updated = updated.cons(k, v)
        expected = from_dict({**initial, **updates})
        assert updated == expected

    @given(
        base=st.dictionaries(_keys, _values),
        to_remove=st.lists(_keys)
    )
    def test_remove_property(self, base, to_remove):
        hdict = from_dict(base)
        current = hdict
        for key in to_remove:
            current = current.remove(key)
        for key in to_remove:
            assert not current.member(key)
        remaining_keys = set(base.keys()) - set(to_remove)
        for key in remaining_keys:
            assert current.member(key)
