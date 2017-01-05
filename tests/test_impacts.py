# -*- coding: utf-8 -*-
"""py.test tests on main.py

.. moduleauthor:: Mathew Topper <mathew.topper@tecnalia.com>
"""

import os

import pytest
import pandas as pd

from dtocean_environment.impacts import (EnergyModification)
#                                         CollisionRisk,
#                                         Turbidity,
#                                         UnderwaterNoise,
#                                         ChemicalPollution,
#                                         ReefEffect,
#                                         ReserveEffect,
#                                         RestingPlace)

mod_path = os.path.realpath(__file__)
mod_dir = os.path.dirname(mod_path)
data_dir = os.path.join(mod_dir, "..", "dtocean_environment", "data")
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
def receptors():

    table_path = os.path.join(test_data_dir, "species_receptors.csv")
    receptors_table = pd.read_csv(table_path, index_col=0)
    
    return receptors_table
    
# -----------TESTS ---------------
    
def test_energy_seasonal(protected, receptors):
    
    data_path = os.path.join(data_dir, "hydrodynamics")
    
    energy_logigram = EnergyModification(data_path,
                                         protected,
                                         receptors,
                                         "Loose sand")
                                         
    receptor_sensitivity_scores = {"Hard substrate benthic habitat" : 2.,
                                   "Soft substrate benthic habitat" : 3.,
                                   "Particular habitat"            : 4.}
                                         
    test = energy_logigram.get_seasonal_scores(receptor_sensitivity_scores)
            
    assert test.values.max() == 4.
    assert test.values.min() == 2.
    
def test_energy_impact_one(protected, receptors):
    
    data_path = os.path.join(data_dir, "hydrodynamics")
    
    energy_logigram = EnergyModification(data_path,
                                         protected,
                                         receptors,
                                         "Loose sand")
                                         
    input_dict = {"Energy Modification": 0.3}
    
    result = energy_logigram(input_dict)
        
    assert result.get_EIS() == -74.0
    assert result.confidence_level == 3
    
#def test_energy_impact_two(energy_logigram):
#    
#    IE=100
#    OE=95
#    constraints=["Loose Sand"]
#    species = ["ostrea edulis", "maerl"]
#    confidence, score,  _, _, _ = energy_logigram(IE,OE,constraints,species)
#        
#    assert score["Environmental Impact Score"] == -100.0
#    assert confidence == 3
#    
#def test_energy_impact_three(energy_logigram):
#    
#    IE=100
#    OE=85
#    constraints=["Loose Sand"]
#    species = ["maerl"]
#    confidence, score, ps_hist, rss_hist, _ = energy_logigram(IE,
#                                                              OE,
#                                                              constraints,
#                                                              species)
#    
#    print score
#    print ps_hist
#    print rss_hist
#    assert np.isclose(score["Environmental Impact Score"], -51.92)
#    assert confidence == 3
#    
#def test_collision_risk(collrisk_logigram):
#    
#    dev_S=10
#    comp_N=50
#    crossA_farm=500
#    constraints=["Sea Loc Entrances"]
#    species = ["black guillemot", "common eider"]
#    confidence, score,  _, _, _ = collrisk_logigram(dev_S,comp_N,crossA_farm,
#                                                 constraints,species)
#    
#    assert score["Environmental Impact Score"] == -100.0
#    assert confidence == 3
#    
#def test_turbidity(turbidity_logigram):
#    
#    init_turb=10
#    meas_turb=500
#    constraints=None
#    species = ["Ecostystem in hard substrate"]
#    confidence, score,  _, _, _ = turbidity_logigram(init_turb,meas_turb,
#                                                  constraints,species)
#        
#    assert score["Environmental Impact Score"] == -100.0
#    assert confidence == 3
#    
#def test_underwaternoise(underwaternoise_logigram):
#    
#    thresundw_sens=80
#    undwnoise_comp=0.5
#    comp_N=160
#    constraints=None
#    species = ["seals"]
#    confidence, score,  _, _, _ = underwaternoise_logigram(thresundw_sens,
#                                                        undwnoise_comp,
#                                                        comp_N,
#                                                        constraints,
#                                                        species)
#        
#    assert score["Environmental Impact Score"] == -100.0
#    assert confidence == 3
#    
#def test_chemicalpoll(chemicalpoll_logigram):
#    
#    chem_comp=15
#    chem_thres=15
#    constraints=["Irgarol 1051"]
#    species = ["Ecosystem in hard substrate"]
#    confidence, score,  _, _, _ = chemicalpoll_logigram(chem_comp,
#                                                     chem_thres,
#                                                     constraints,
#                                                     species)
#        
#    assert score["Environmental Impact Score"] == -100.0
#    assert confidence == 3
#    
#def test_reefeffect(reefeffect_logigram):
#    
#    farm_A=100
#    submA_comp=5
#    comp_N=20
#    constraints=["vertical"]
#    species = ["Benthos organisms","Ecosystem in hard substrate"]
#    confidence, score,  _, _, _ = reefeffect_logigram(farm_A,
#                                                   submA_comp,
#                                                   comp_N,
#                                                   constraints,
#                                                   species)
#        
#    assert score["Environmental Impact Score"] == 100.0
#    assert confidence == 3
#    
#def test_reserveeffect(reserveeffect_logigram):
#    
#    farm_A=100
#    fish_S=100
#    constraints=["Fishery complete prohibition"]
#    species = ["Benthos organisms"]
#    confidence, score,  _, _, _ = reserveeffect_logigram(fish_S,farm_A,
#                                                constraints,species)
#        
#    assert score["Environmental Impact Score"] == 100.0
#    assert confidence == 3
#    
#def test_restingplace_one(restingplace_logigram):
#    
#    emergA_comp=2
#    comp_N=10
#    farm_A=20
#    constraints=["No dangerous parts"]
#    species = ["Birds"]
#    
#    (confidence,
#     score,
#     pressure_history,
#     rss_history,
#     _) = restingplace_logigram(emergA_comp,
#                                comp_N,
#                                farm_A,
#                                constraints,
#                                species)
#                                
#    print score
#    print pressure_history                                                       
#    print rss_history
#        
#    assert score["Environmental Impact Score"] == 100.0
#    assert confidence == 3
#    
#def test_restingplace_two(restingplace_logigram):
#    
#    emergA_comp=2
#    comp_N=5
#    farm_A=20
#    constraints=["Moving part of device"]
#    species = ["Pinnipeds"]
#    
#    (confidence,
#     score,
#     pressure_history,
#     rss_history,
#     rrss_history) = restingplace_logigram(emergA_comp,
#                                           comp_N,
#                                           farm_A,
#                                           constraints,
#                                           species)
#                                
#    print score
#    print pressure_history                                                       
#    print rss_history
#        
#    assert score["Environmental Impact Score"] == -100.0
#    assert confidence == 3
#    assert len(rrss_history["Pinnipeds"]) == 12

