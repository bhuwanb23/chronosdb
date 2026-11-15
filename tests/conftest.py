import tests.phase14_helpers as _h


def pytest_collection_modifyitems(items):
    for item in items:
        mod = getattr(item, "module", None)
        if mod is None:
            continue
        for name in _h.__all__:
            if name not in mod.__dict__:
                mod.__dict__[name] = getattr(_h, name)
