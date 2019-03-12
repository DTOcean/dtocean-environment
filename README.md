[![appveyor](https://ci.appveyor.com/api/projects/status/github/DTOcean/dtocean-environment?branch=master&svg=true)](https://ci.appveyor.com/project/DTOcean/dtocean-environment)
[![codecov](https://codecov.io/gh/DTOcean/dtocean-environment/branch/master/graph/badge.svg)](https://codecov.io/gh/DTOcean/dtocean-environment)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/4cb4990e786a4470bf5531318d5bead0)](https://www.codacy.com/project/H0R5E/dtocean-environment/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=DTOcean/dtocean-environment&amp;utm_campaign=Badge_Grade_Dashboard&amp;branchId=11743625)
[![release](https://img.shields.io/github/release/DTOcean/dtocean-environment.svg)](https://github.com/DTOcean/dtocean-environment/releases/latest)

# DTOcean Environmental Module

The DTOcean Environmental Module provides functions to assess and compare the 
environmental impact of arrays designed by DTOcean. The environmental impact is 
given by two numerical values, one for positive and one for negative impacts. 
Recommendations on how to reduce negative impacts are also provided. 

See [dtocean-app](https://github.com/DTOcean/dtocean-app) or [dtocean-core](
https://github.com/DTOcean/dtocean-app) to use this package within the DTOcean
ecosystem.

* For python 2.7 only.

## Installation

Installation and development of dtocean-environment uses the [Anaconda 
Distribution](https://www.anaconda.com/distribution/) (Python 2.7)

### Conda Package

To install:

```
$ conda install -c dataonlygreater dtocean-environment
```

### Source Code

Conda can be used to install dependencies into a dedicated environment from
the source code root directory:

```
$ conda create -n _dtocean_eia python=2.7 pip
```

Activate the environment, then copy the `.condrc` file to store installation  
channels:

```
$ conda activate _dtocean_eia
$ copy .condarc %CONDA_PREFIX%
```

Install [polite](https://github.com/DTOcean/polite) into the environment. For 
example, if installing it from source:

```
$ cd \\path\\to\\polite
$ conda install --file requirements-conda-dev.txt
$ pip install -e .
```

Finally, install dtocean-environment and its dependencies using conda and pip:

```
$ cd \\path\\to\\dtocean-environment
$ conda install --file requirements-conda-dev.txt
$ pip install -e .
```

To deactivate the conda environment:

```
$ conda deactivate
```

### Tests

A test suite is provided with the source code that uses [pytest](
https://docs.pytest.org).

If not already active, activate the conda environment set up in the [Source 
Code](#source-code) section:

```
$ conda activate _dtocean_eia
```

Install packages required for testing to the environment (one time only):

```
$ conda install -y pytest
```

Run the tests:

``` 
$ py.test tests
```

### Uninstall

To uninstall the conda package:

```
$ conda remove dtocean-environment
```

To uninstall the source code and its conda environment:

```
$ conda remove --name _dtocean_eia --all
```

## Usage

### Jupyter Notebooks

Examples of using dtocean-core are given in [Jupyter Notebooks](
http://jupyter.org/) which are found in the "notebooks" folder of the
dtocean-core source code. The notebooks should be used from the installation
conda environment. To install jupyter and the matplotlib plotting library:

```
$ activate _dtocean_eia
$ conda install -y jupyter matplotlib
```

Then, to start the jupyter notebook in your default browser:

```
$ start jupyter notebook
```

Note, you only need to activate the environment once per session.

**It is important that the "test_data" directory is copied into the same 
directory where the notebooks are being executed from**. You can 
customise this directory using the config file described [here](
http://jupyter-notebook.readthedocs.io/en/latest/config.html) and setting the 
"notebook_dir" variable. 

Once the test_data directory has been placed alongside the notebook, the 
notebook can be executed in the normal way.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to
discuss what you would like to change.

See [this blog post](
https://www.dataonlygreater.com/latest/professional/2017/03/09/dtocean-development-change-management/)
for information regarding development of the DTOcean ecosystem.

Please make sure to update tests as appropriate.

## Credits

This package was initially created as part of the [EU DTOcean project](
https://www.dtoceanplus.eu/About-DTOceanPlus/History) by:

 * Mathew Topper at [TECNALIA](https://www.tecnalia.com)
 * Rui Duarte at [France Energies Marines](https://www.france-energies-marines.org/)
 * Imanol Touzon at [TECNALIA](https://www.tecnalia.com)
 * Jean-Francois Filipot at [France Energies Marines](https://www.france-energies-marines.org/)

It is now maintained by Mathew Topper at [Data Only Greater](
https://www.dataonlygreater.com/).

## License

[GPL-3.0](https://choosealicense.com/licenses/gpl-3.0/)
