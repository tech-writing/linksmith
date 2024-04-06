from functools import cmp_to_key
from operator import attrgetter, itemgetter


def multikeysort(items, *columns, attrs=True) -> list:
    """
    Perform a multiple column sort on a list of dictionaries or objects.
    Args:
        items (list): List of dictionaries or objects to be sorted.
        *columns: Columns to sort by, optionally preceded by a '-' for descending order.
        attrs (bool): True if items are objects, False if items are dictionaries.

    Returns:
        list: Sorted list of items.

    Source: https://stackoverflow.com/a/77401782. Thanks, @pymen.
    """
    getter = attrgetter if attrs else itemgetter

    def get_comparers():
        comparers = []

        for col in columns:
            col = col.strip()
            if col.startswith("-"):  # If descending, strip '-' and create a comparer with reverse order
                key = getter(col[1:])
                order = -1
            else:  # If ascending, use the column directly
                key = getter(col)
                order = 1

            comparers.append((key, order))
        return comparers

    def custom_compare(left, right):
        """Custom comparison function to handle multiple keys"""
        for fn, reverse in get_comparers():
            # Minor enhancement when to-be-compared attribute values are `None`.
            if fn(left) is not None and fn(right) is not None:
                result = (fn(left) > fn(right)) - (fn(left) < fn(right))
                if result != 0:
                    return result * reverse
        return 0

    return sorted(items, key=cmp_to_key(custom_compare))
