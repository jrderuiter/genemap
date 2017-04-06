from .mappers import get_mappers


def map_ids(ids, mapper, from_type, to_type, drop_duplicates='both', **kwargs):
    """Maps ids using the given mapper."""

    mapper_obj = _build_mapper(
        mapper=mapper,
        from_type=from_type,
        to_type=to_type,
        drop_duplicates=drop_duplicates,
        **kwargs)

    return mapper_obj.map_ids(ids)


def _build_mapper(mapper, from_type, to_type, drop_duplicates, **kwargs):

    try:
        mapper_class = get_mappers()[mapper]
    except KeyError:
        raise ValueError('Unknown mapper {!r}. Available mappers are: {}.'
                         .format(mapper, list(get_mappers().keys())))

    return mapper_class(
        from_type=from_type,
        to_type=to_type,
        drop_duplicates=drop_duplicates,
        **kwargs)


def map_frame(df, mapper, from_type, to_type, drop_duplicates='both',
              **kwargs):
    """Maps dataframe index using the given mapper."""

    mapper_obj = _build_mapper(
        mapper=mapper,
        from_type=from_type,
        to_type=to_type,
        drop_duplicates=drop_duplicates,
        **kwargs)

    return mapper_obj.map_frame(df)
