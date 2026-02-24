import pytest

from useless_classes import NullObject


@pytest.fixture
def null() -> NullObject:
    return NullObject()


class TestNullObjectInstantiation:
    def test_can_be_instantiated(self):
        obj = NullObject()
        assert obj is not None

    def test_two_instances_are_equal(self):
        a = NullObject()
        b = NullObject()
        assert a == b


class TestNullObjectCall:
    def test_calling_returns_self(self, null: NullObject):
        result = null()
        assert result is null

    def test_calling_with_positional_args_returns_self(self, null: NullObject):
        result = null(1, 2, 3)
        assert result is null

    def test_calling_with_keyword_args_returns_self(self, null: NullObject):
        result = null(a=1, b="hello")
        assert result is null

    def test_calling_with_mixed_args_returns_self(self, null: NullObject):
        result = null(42, key="value")
        assert result is null

    def test_chained_calls_return_self(self, null: NullObject):
        result = null()()()
        assert result is null


class TestNullObjectGetAttr:
    def test_getattr_returns_self(self, null: NullObject):
        result = null.anything
        assert result is null

    def test_getattr_arbitrary_name_returns_self(self, null: NullObject):
        assert null.foo is null
        assert null.bar is null
        assert null.some_method is null

    def test_getattr_chained_returns_self(self, null: NullObject):
        result = null.a.b.c
        assert result is null

    def test_getattr_then_call_returns_self(self, null: NullObject):
        result = null.some_method()
        assert result is null

    def test_deeply_chained_attr_and_calls_return_self(self, null: NullObject):
        result = null.a.b().c.d(1, 2).e
        assert result is null


class TestNullObjectSetAttr:
    def test_setattr_does_nothing(self, null: NullObject):
        null.foo = 42
        # Attribute access still returns self, not 42
        assert null.foo is null

    def test_setattr_does_not_raise(self, null: NullObject):
        try:
            null.anything = "some value"
        except Exception as e:
            pytest.fail(f"Setting an attribute raised an exception: {e}")

    def test_setattr_multiple_times_does_nothing(self, null: NullObject):
        null.x = 1
        null.x = 2
        null.x = 3
        assert null.x is null


class TestNullObjectBool:
    def test_bool_is_false(self, null: NullObject):
        assert bool(null) is False

    def test_is_falsy_in_if_statement(self, null: NullObject):
        if null:
            pytest.fail("NullObject should be falsy")

    def test_is_falsy_with_not(self, null: NullObject):
        assert not null

    def test_is_falsy_in_or_expression(self, null: NullObject):
        result = null or "fallback"
        assert result == "fallback"

    def test_is_falsy_in_and_expression(self, null: NullObject):
        result = null and "never reached"
        assert result is null


class TestNullObjectStr:
    def test_str_returns_none_string(self, null: NullObject):
        assert str(null) == "None"

    def test_str_matches_str_of_none(self, null: NullObject):
        assert str(null) == str(None)

    def test_fstring_uses_str(self, null: NullObject):
        assert f"{null}" == "None"


class TestNullObjectRepr:
    def test_repr_returns_nullclass(self, null: NullObject):
        assert repr(null) == "NullClass"


class TestNullObjectEquality:
    def test_null_equals_null(self, null: NullObject):
        other = NullObject()
        assert null == other

    def test_null_equals_itself(self, null: NullObject):
        assert null == null

    def test_null_not_equal_to_none(self, null: NullObject):
        assert null != None  # noqa: E711

    def test_null_not_equal_to_zero(self, null: NullObject):
        assert null != 0

    def test_null_not_equal_to_false(self, null: NullObject):
        assert null != False  # noqa: E712

    def test_null_not_equal_to_empty_string(self, null: NullObject):
        assert null != ""

    def test_null_not_equal_to_arbitrary_object(self, null: NullObject):
        assert null != object()

    def test_null_not_equal_to_integer(self, null: NullObject):
        assert null != 42

    def test_null_not_equal_to_dict(self, null: NullObject):
        assert null != {}
