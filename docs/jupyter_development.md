# Developing in Jupyter: Notebooks as Plug-in Transforms

## Adding Param Tags For Papermill
When corebot runs a notebook, all params will be passed to the notebook in the parameters cell; this is the cell with the tag `parameters` (strangely enough).
To set this from JupyterLabs:
1. Go to **Help -> Launch Classic Notebook**
2. Enter the classic notebook and create a cell
3. Select **View -> Cell Toolbar -> Tags** to show the tags inputs at the top of each cell.
4. Pick a cell and add the tag `parameters` to it. 
5. Save the notebook.

You are now set up to inject params! 


