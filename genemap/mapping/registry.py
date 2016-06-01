import functools

# Private list of mappers.
_mappers = {}
_mapper_options = {}


def mapper(name, option_func=None):
    def decorator(func):
        # Wrap mapper function.
        @functools.wraps(func)
        def wrapper(from_type, to_type, **kwargs):
            return func(from_type, to_type, **kwargs)

        # Add wrapped function to mappers.
        _mappers[name] = wrapper

        if option_func is None:
            _mapper_options[name] = lambda x: x
        else:
            _mapper_options[name] = option_func

        return wrapper
    return decorator


def get_mapper(name):
    try:
        return _mappers[name]
    except KeyError:
        raise ValueError('Invalid mapper, available mappers are: {}'
                         .format(', '.join(available_mappers())))


def get_mapper_options(name):
    try:
        return _mapper_options.get(name)
    except KeyError:
        raise ValueError('Invalid mapper, available mappers are: {}'
                         .format(', '.join(available_mappers())))


def available_mappers():
    for name in _mappers.keys():
        yield name
