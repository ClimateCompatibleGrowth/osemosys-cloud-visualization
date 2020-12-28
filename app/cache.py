import os
from flask_caching import Cache


def cache_timeout():
    if 'DASH_DEBUG' in os.environ:
        return 1
    else:
        return 86400 * 365  # 1 year


def make_cache_key_for_configs(f, *args, **kwargs):
    configs = args[0]
    return '-'.join([config.input_string for config in configs])


cache = Cache()
