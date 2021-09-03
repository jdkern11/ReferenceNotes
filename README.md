# Reference Notes
Creates templates for reference notes by loading meta data from a Zotero
database.

## Install
Download the repository and then 
edit referencenotes/utils/constants.py with the path to your zotero.sqlite file.
For example
```Python
PATH = "/Users/josephkern/Zotero/zotero.sqlite"

# fieldID constants
TITLE = 1
DATE = 6
PUBLISHER = 37
DOI = 58

...
```

The only dependency is pandas, so you can either use  
`poetry install`  
in the the folder with pyproject.toml, or some other environment manager like
anaconda. If you don't use poetry, you'll have to run  
`pip install .`  
in folder with pyproject.toml.

## Examples  
- [Example 1](references/SolNet/XuOnSplittingTraining.md)
- [Example 2](references/SolNet/ProbstHyperparametersandTuning.md)

## FAQ
### How do I change templates?
You can write your own templates in constants.py. Just write an array of lines
or tell me what you want and I can modify the code.

### Why did you spend four hours writing this?
I thought it would be more fun than actually reading the papers...
