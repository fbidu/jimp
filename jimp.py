"""
Provides custom importer for JSON files as module.

## Usage

Assuming a `data.json` file with contents:

```json
{
    "name": "John Doe",
    "age": 42,
}
```

You can import it as:

```python
import jimp
import data

print(data.name)
print(data.age)
```
"""
import json
import os
import sys
from importlib.abc import Loader, MetaPathFinder
from importlib.util import spec_from_loader


class JimpLoader(Loader):
    # pylint: disable=abstract-method
    """
    Loads a JSON file as a module
    """

    def __init__(self, path):
        self.path = path
        self.spec = spec_from_loader(self.path, self)
        self.module = None
        self.data = {}

    def create_module(self, spec):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        except Exception as e:
            raise ImportError("Could not load json file") from e

    def exec_module(self, module):
        """
        Loads the json data into the module
        """
        module.__dict__.update(self.data)
        return module

    def __repr__(self) -> str:
        return f"JSON File @ {self.path}"


class JimpFinder(MetaPathFinder):
    """
    Finds a JSON file in the current python paths and loads it as a module
    """

    # pylint: disable=unused-argument,no-self-use

    def find_spec(self, fullname, path, target=None):
        """
        Searches for the JSON file and returns a spec for it.
        """
        module_name = fullname.split(".")[-1]
        paths = path if path else [os.getcwd()]
        for path_ in paths:
            file_path = os.path.join(path_, module_name + ".json")
            if os.path.exists(file_path):
                return spec_from_loader(fullname, JimpLoader(file_path))
        return None


sys.meta_path.append(JimpFinder())
