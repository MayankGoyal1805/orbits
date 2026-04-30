# Documentation for `server/__init__.py`

Welcome to this beginner-friendly guide! We are going to explore the code in `server/__init__.py`.

## Understanding the Code Line-by-Line

If you open the `/home/mayank/repos/orbits/server/__init__.py` file, you will notice something surprising: **it is completely empty!**

### Why have an empty file?

In Python, an `__init__.py` file (pronounced "dunder init", short for double-underscore init) serves a very specific structural purpose. 

When Python looks at your computer's folders to find code to `import`, it needs a way to tell the difference between:
1. A random folder that just happens to contain some `.py` scripts.
2. A formalized **Python Package** (a collection of modules meant to work together).

By placing an `__init__.py` file (even an empty one) inside a directory, you signal to Python: *"Treat this directory as a Python Package."*

### What does this allow you to do?

Because `server/__init__.py` exists, Python allows other scripts in the project to run commands like this:

```python
from server.app import app
```

If you deleted the `__init__.py` file, older versions of Python would throw a `ModuleNotFoundError`. 

*Note: In newer versions of Python (3.3+), "Implicit Namespace Packages" allow you to import from folders without `__init__.py` files, but it is still considered a strict best practice to include them to explicitly define your packages and ensure compatibility across tools, linters, and older Python versions.*

### Can you put code in it?
Yes! You don't have to leave it empty. Any Python code written inside `__init__.py` will automatically run the very first time the package is imported. 
You will see an example of an `__init__.py` file that *does* contain code when we look at `src/orbits_env/__init__.py`!