# -*- coding: utf-8 -*-
"""py.test tests on main.py

.. moduleauthor:: Mathew Topper <mathew.topper@tecnalia.com>
"""

import os

import pytest
import pandas as pd

import numpy as np

from dtocean_environment.main import HydroStage

mod_path = os.path.realpath(__file__)
mod_dir = os.path.dirname(mod_path)
test_data_dir = os.path.join(mod_dir, "..", "test_data")

@pytest.fixture
def protected():
    
    # Input Dictionary
    protected_dict = {"species name": ["mysticete",
                                       "dolphinds",
                                       "large odontocete",
                                       "odontocete",
                                       "particular habitat",
                                       "fish"],
                      "observed": [False, False, False, False,False, False]}
                      
    protected_table = pd.DataFrame(protected_dict)
    protected_table = protected_table.set_index("species name")
    
    return protected_table
    
@pytest.fixture
def weighting():

    weighting_dict = {"Energy Modification": "Loose sand",
                      "Collision Risk": None,
                      "Turbidity": None,
                      "Underwater Noise": None,
                      "Reserve Effect": None,
                      "Reef Effect": None,
                      "Resting Place": None}
    
    return weighting_dict

@pytest.fixture    
def receptors():
    
    table_path = os.path.join(test_data_dir, "species_receptors.csv")
    receptors_table = pd.read_csv(table_path, index_col=0)
    
    return receptors_table

def test_HydroStage(protected, weighting, receptors):
    
    test_hydro = HydroStage(protected,
                            receptors,
                            weighting)

    # Read devices positions for the test
    
    f = open(os.path.join(test_data_dir,"positions.txt"), 'r')
    data = np.genfromtxt(f)
    x=np.zeros(50)
    y=np.zeros(50)

    for ii in range(0, 50):
        datatmp=data[ii]
        x[ii]=datatmp[0]
        y[ii]=datatmp[1]
                            
    input_dict = {"Energy Modification"             : 0.3,
                  "Coordinates of the Devices"      : [x,y],
                  "Size of the Devices"             : 30.,
                  "Immersed Height of the Devices"  : 10.,
                  "Water Depth"                     : 15.,
                  "Current Direction"               : 45.,
                  "Initial Turbidity"               : 50.,
                  "Measured Turbidity"              : 70.,
                  "Initial Noise dB re 1muPa"       : 60.,
                  "Measured Noise dB re 1muPa"      : 150.,
                  "Fishery Restriction Surface"     : 1000.,
                  "Total Surface Area"              : 94501467.,
                  "Number of Objects"               : 50,
                  "Object Emerged Surface"          : 20.,
                  "Surface Area of Underwater Part" : 60.
                  }

    (confidence_dict, 
     eis_dict, 
     recommendation_dict,
     seasons,
     global_eis) = test_hydro(input_dict)
    
    assert 'Resting Place' in eis_dict.keys()
    assert len(seasons.columns) == 12
    assert "Energy Modification" in seasons.index

