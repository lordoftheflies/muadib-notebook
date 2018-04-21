# muadib-notebook #

## Usage ##

First, use enable notebook loading, as a side-effect of ```muadib-notebook``` import:

```python
import muadib_notebook
```

Then import notebooks as a module:

```python
import notebooks.test_notebook as given_module
```
*This means you have a notebook directory which contains an test_notebook.ipynb called notebook.*


Start webconsole

```sh
jupyter lab --config=./muadib_notebook/jupyter_notebook_config.py
```
