from typing import Sequence
from numbers import Number

import numpy as np
import pandas as pd


def try_(lazy_func, default=None, exception=Exception):
    try:
        return lazy_func()
    except exception:
        return default


def _as_str(value):
    if isinstance(value, (Number, str)):
        return str(value)
    if isinstance(value, pd.DataFrame):
        return 'df'
    name = str(getattr(value, 'name', '') or '')
    if name in ('Open', 'High', 'Low', 'Close', 'Volume',
                'Open2', 'High2', 'Low2', 'Close2', 'Volume2',
                'Open3', 'High3', 'Low3', 'Close3', 'Volume3',
                'Flg1', 'Flg2', 'Flg3', 'Flg4', 'Flg5'):
        return name[:1]
    if callable(value):
        name = value.__name__.replace('<lambda>', 'λ')
    if len(name) > 10:
        name = name[:9] + '…'
    return name


def _as_list(value):
    if isinstance(value, Sequence) and not isinstance(value, str):
        return list(value)
    return [value]


def _data_period(df):
    """Return data index period as pd.Timedelta"""
    values = df.index[-100:].to_series()
    return values.diff().median()


class _Array(np.ndarray):
    """
    ndarray extended to supply .name and other arbitrary properties
    in ._opts dict.
    """
    def __new__(cls, array, *, name=None, write=False, **kwargs):
        obj = np.asarray(array).view(cls)
        obj.name = name or array.name
        obj._opts = kwargs
        if not write:
            obj.setflags(write=False)
        return obj

    def __array_finalize__(self, obj):
        if obj is not None:
            self.name = getattr(obj, 'name', '')
            self._opts = getattr(obj, '_opts', {})

    def __bool__(self):
        try:
            return bool(self[-1])
        except IndexError:
            return super().__bool__()

    def __float__(self):
        try:
            return float(self[-1])
        except IndexError:
            return super().__float__()

    def to_series(self):
        return pd.Series(self, index=self._opts['data'].index, name=self.name)


class _Indicator(_Array):
    pass


class _Data:
    """
    A data array accessor. Provides access to OHLCV "columns"
    as a standard `pd.DataFrame` would, except it's not a DataFrame
    and the returned "series" are _not_ `pd.Series` but `np.ndarray`
    for performance reasons.
    """
    def __init__(self, df):
        self.__i = len(df)
        self.__pip = None
        self.__cache = {}

        self.__arrays = {col: _Array(arr, data=self)
                         for col, arr in df.items()}
        # Leave index as Series because pd.Timestamp nicer API to work with
        self.__arrays['__index'] = df.index.copy()

    def __getitem__(self, item):
        return self.__get_array(item)

    def __getattr__(self, item):
        try:
            return self.__get_array(item)
        except KeyError:
            raise AttributeError("Column '{}' not in data".format(item)) from None

    def _set_length(self, i):
        self.__i = i
        self.__cache.clear()

    def __len__(self):
        return self.__i

    @property
    def pip(self):
        if self.__pip is None:
            self.__pip = 10**-np.median([len(s.partition('.')[-1])
                                         for s in self.__arrays['Close'].astype(str)])
        return self.__pip

    def __get_array(self, key):
        arr = self.__cache.get(key)
        if arr is None:
            arr = self.__cache[key] = self.__arrays[key][:self.__i]
        return arr

    @property
    def Open(self):
        return self.__get_array('Open')

    @property
    def High(self):
        return self.__get_array('High')

    @property
    def Low(self):
        return self.__get_array('Low')

    @property
    def Close(self):
        return self.__get_array('Close')

    @property
    def Volume(self):
        return self.__get_array('Volume')

    def Open2(self):
        return self.__get_array('Open2')

    @property
    def High2(self):
        return self.__get_array('High2')

    @property
    def Low2(self):
        return self.__get_array('Low2')

    @property
    def Close2(self):
        return self.__get_array('Close2')

    @property
    def Volume2(self):
        return self.__get_array('Volume2')

    def Open3(self):
        return self.__get_array('Open3')

    @property
    def High3(self):
        return self.__get_array('High3')

    @property
    def Low3(self):
        return self.__get_array('Low3')

    @property
    def Close3(self):
        return self.__get_array('Close3')

    @property
    def Volume3(self):
        return self.__get_array('Volume3')

    @property
    def Flg1(self):
        return self.__get_array('Flg1')

    @property
    def Flg2(self):
        return self.__get_array('Flg2')

    @property
    def Flg3(self):
        return self.__get_array('Flg3')

    @property
    def Flg4(self):
        return self.__get_array('Flg4')

    @property
    def Flg5(self):
        return self.__get_array('Flg5')

    @property
    def index(self):
        return self.__get_array('__index')

    # Make pickling in Backtest.optimize() work with our catch-all __getattr__
    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, state):
        self.__dict__ = state
