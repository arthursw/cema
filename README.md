# Wetlands - Conda Environment Manager

![Wetland](Wetland.png)

**Wetlands** is a lightweight Python library for managing **Conda** environments.

**Wetlands** can create Conda environments on demand, install dependencies, and execute arbitrary code within them. This makes it easy to build *plugin systems* or integrate external modules into an application without dependency conflicts, as each environment remains isolated.

The name ***Wetlands*** comes from the tropical *environments* where Anacondas thrive.

## ✨ Features

- **Automatic Environment Management**: Create and configure environments on demand.
- **Dependency Isolation**: Install dependencies without conflicts.
- **Embedded Execution**: Run Python functions inside isolated environments.
- **Micromamba**: Wetlands uses a self-contained `micromamba` for fast and lightweight Conda environment handling.

---

## 📦 Installation

To install **Wetlands**, simply use `pip`:

```sh
pip install wetlands
```

## 🚀 Usage Example

If the user doesn't have micromamba installed, Wetlands will download and set it up automatically.

```python

from wetlands.environment_manager import EnvironmentManager

# Initialize the environment manager
# Wetlands will use the existing Micromamba installation at the specified path (e.g., "micromamba/") if available;
# otherwise it will automatically download and install Micromamba in a self-contained manner.
environmentManager = EnvironmentManager("micromamba/")

# Create and launch an isolated Conda environment named "numpy"
env = environmentManager.create("numpy", {"pip":["numpy==2.2.4"]})
env.launch()

# Import example_module in the environment, see example_module.py below
minimal_module = env.importModule("minimal_module.py")
# example_module is a proxy to example_module.py in the environment
array = [1,2,3]
result = minimal_module.sum(array)

print(f"Sum of {array} is {result}.")

# Clean up and exit the environment
env.exit()

```

with `example_module.py` as follow:

```
def sum(x):
    import numpy as np
    return int(np.sum(x))
```

See the `examples/` folder for more detailed examples.

## 🔗 Related Projects

- [Conda](https://anaconda.org/)
- [Micromamba](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html)

## 🤖 Development

Use [uv](https://docs.astral.sh/uv/) to easily manage the project.

### Check & Format

Check for code errors with `uv run ruff check` and format the code with `uv run ruff format`.

### Tests

Test wetlands with `uv` and `ipdb`: `uv run pytest --pdb --pdbcls=IPython.terminal.debugger:TerminalPdb tests`

### Generate documentation


The Wetlands documentation is generated with [`mkdocs-material`](https://squidfunk.github.io/mkdocs-material/), [`mkdocstrings`](https://mkdocstrings.github.io/), [`mike`](https://github.com/jimporter/mike) and others.

Install the doc tools with `uv pip install  ".[docs]"`.

MkDocs includes a live preview server, so you can preview your changes as you write your documentation. The server will automatically rebuild the site upon saving. Start it with: `uv run mkdocs serve`.

[`mike`](https://github.com/jimporter/mike) is used to generate multiple versions of the docs. To create a new version, use `mike deploy [version]` (do not forget to update `.github/workflows/ci.yml`).

The doc is automatically generated by [Github Actions](https://squidfunk.github.io/mkdocs-material/publishing-your-site/#with-github-actions-material-for-mkdocs) (see `.github/workflows/ci.yml`).

The script `scripts/gen_ref_pages.py` generates the API reference automatically (see [mkdocstrings recipes](https://mkdocstrings.github.io/recipes/)).

## 📋 Todo

- Handle general [dependency specifiers](https://packaging.python.org/en/latest/specifications/dependency-specifiers/#dependency-specifiers) (handle version specifiers like '>=', '~=' etc.).

## 📜 License

This project was made at Inria in Rennes (Centre Inria de l'Université de Rennes) and is licensed under the MIT License.

The logo Wetland was made by Dan Hetteix from Noun Project (CC BY 3.0).