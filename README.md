# Install the Package

It is assumed that the Anaconda Python 2.7 distribution is installed on a
Windows machine in C:\Anaconda.

Below ">" means type it into a cmd window.

## Set up environment (only once)
> conda create -n dtocean pip pytest ipython-notebook

## Activate the environment
> C:\Anaconda\Scripts\activate.bat dtocean

## Install dependencies (only once unless notified)
> conda install numpy pandas

## Install the environmental package
> cd \path\to\the\package
> winmake.bat install

# Testing the Package

There is a test suite available as an ipython notebook in the notebooks folder
of the source code.

## Start ipython notebook
> ipython notebook

## Load the notebook

Using the web interface, click "Upload" navigate to the notebooks folder and
select the "DTOcean Environmental Module Test.ipynb" file. Click "Upload" again
(now a blue button).

The notebook will appear in the list of notebooks. Click on it to start it.

On first opening the book, use the menus to select "Cell->Run All" and this
will activate the code.

Adjustments can then be made in the appropriate cells. Note that the execute a
cell "Shift+Return" is needed.
