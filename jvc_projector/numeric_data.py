from enum import Enum, EnumMeta

class NumericDataMeta(EnumMeta):
    @staticmethod
    def _name_from_int(value):
        i = int(value)
        if i < 0:
            return 'n%d' % -i
        return 'p%d' % i

    @staticmethod
    def _value_from_int(value):
        i = int(value)
        if i < 0:
            return b'%04X' % (i % 65536)
        return b'%04X' % i

    def __new__(metacls, cls, bases, clsdict, **kwds):
        enum_dict = super(__class__, metacls).__prepare__(cls, bases, **kwds)
        min = clsdict.pop('_min', 0)
        max = clsdict.pop('_max', -1)
        for name, value in clsdict.items():
            enum_dict[name] = value
        for i in range(min, max + 1):
            enum_dict[__class__._name_from_int(i)] = __class__._value_from_int(i)
        return super(__class__, metacls).__new__(metacls, cls, bases, enum_dict, **kwds)

    def __getitem__(self, name):
        return super().__getitem__(__class__._name_from_int(name))

class NumericData(Enum, metaclass=NumericDataMeta):
    @property
    def name(self):
        if self._name_.startswith('n'):
            return '-' + self._name_[1:]
        return self._name_[1:]

