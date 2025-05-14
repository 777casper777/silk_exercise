from importlib import import_module
from typing import List
from app.clients.base import BaseHostFetcher
from app.config import ACTIVE_FETCHERS

def load_fetchers() -> List[BaseHostFetcher]:
    fetchers = []
    for path in ACTIVE_FETCHERS:
        module_path, class_name = path.rsplit(".", 1)
        module = import_module(module_path)
        klass = getattr(module, class_name)
        fetchers.append(klass())
    return fetchers
