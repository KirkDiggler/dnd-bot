from enum import Enum

class OptionType(Enum):
    CHOICE = "choice"
    REFERENCE = "reference"
    MULTIPLE = "multiple"

class Option:
    def __init__(self, type: OptionType):
        __slots__ = '_type'

        self._type = type

    @property
    def type(self):
        return self._type

# TODO: add type form choice type enum for equipment, proficiency etc
class Choice(Option):
    def __init__(self, **kwargs):
        allowed_attributes = ['choose', 'option_list']
        __slots__ = '_choose', '_option_list', '_chosen'

        super().__init__(type=OptionType.CHOICE)

        for key in kwargs:
            if key in allowed_attributes:
                setattr(self, f"_{key}", kwargs[key])

        self._chosen = 0

    @property
    def choose(self):
        return self._choose

    @property
    def type(self):
        return self._type

    @property
    def option_list(self):
        return self._option_list

    def select(self, key: str):
        if self._chosen >= self._choose:
            raise Exception(f"Cannot select more than {self._choose} options.")

        return self._option_list.select(key)

class OptionList:
    def __init__(self, select_from):
        self._current_idx = 0
        __slots__ = '_select_from'

        # select_from is a list of either ReferenceOption or Choice, both support select 
        self._select_from = select_from

    def __iter__(self):
        return self

    def __next__(self):
        if self._current_idx >= len(self):
            raise StopIteration

        self._current_idx += 1
        return self._select_from[self._current_idx - 1]

    def __len__(self):
        return len(self._select_from)

    def __getitem__(self, key):
        return self._select_from[key]

    @property
    def type(self):
        return self._type

    @property
    def select_from(self):
        return self._select_from

    def select(self, key: str):
        for option in self._select_from:
            if option.type == OptionType.CHOICE:
                selected = option.select(key)
                if selected is not None:
                    return selected
            elif option.key == key:
                return option.select()

        # We return none because a choice could be a dead end but we will have to traverse it to know
        return None

class MultipleReferenceOptions(Option):
    def __init__(self, items):
        __slots__ = '_items', '_selected'

        super().__init__(type=OptionType.MULTIPLE)
        self._items = items
        self._selected = False

    @property
    def key(self):
        return self._items[0].key

    @property
    def items(self):
        return self._items
 
    def select(self):
        self._selected = True
        return self._items

class ReferenceOption(Option):
    def __init__(self, item):
        __slots__ = '_item', '_selected'

        super().__init__(type=OptionType.REFERENCE)
        self._item = item
        self._selected = False

    @property
    def key(self):
        return self._item.key

    @property
    def item(self):
        return self._item

    def select(self):
        self._selected = True
        return self._item
        