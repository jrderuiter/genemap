import pandas as pd

from . import util

_registry = {}


def register_mapper(name, mapper):
    _registry[name] = mapper


def get_mappers():
    return dict(_registry)


class Mapper(object):
    def __init__(self):
        pass

    @classmethod
    def configure_args(cls, parser):
        pass

    @classmethod
    def parse_args(cls, args):
        return {}

    @classmethod
    def from_args(cls, args):
        return cls(**cls.parse_args(args))

    def map_ids(self, ids, from_type, to_type):
        # Fetch mapping.
        mapping = self.get_map(
            from_type, to_type, drop_duplicates='both', drop_na=False)
        mapping = mapping.set_index(mapping.columns[0])[mapping.columns[1]]

        # Lookup ids.
        mapped = mapping.ix[ids]

        # Convert to list.
        mapped = list(mapped.where((pd.notnull(mapped)), None))

        return mapped

    def map_dataframe(self, df, from_type, to_type):
        # Fetch mapping.
        mapping = self.get_map(
            from_type, to_type, drop_duplicates='both', drop_na=False)
        mapping = mapping.set_index(mapping.columns[0])[mapping.columns[1]]

        # Subset mapping for input frame and drop missing entries.
        mapping = mapping.ix[df.index]
        mapping.dropna(inplace=True)

        # Apply mapping to frame.
        mapped = df.ix[mapping.index].copy()
        mapped.index = mapping

        return mapped

    def get_map(self, from_type, to_type, drop_duplicates='both',
                drop_na=True):
        mapping = self._fetch_map(from_type, to_type)

        if drop_na:
            mapping = mapping.dropna()

        mapping = util.drop_duplicates(mapping, how=drop_duplicates)

        return mapping

    def _fetch_map(self, from_type, to_type):
        raise NotImplementedError()
