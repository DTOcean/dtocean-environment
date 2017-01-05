# -*- coding: utf-8 -*-
"""py.test tests on main.py

.. moduleauthor:: Mathew Topper <mathew.topper@tecnalia.com>
"""
import numpy as np

from dtocean_environment.functions import (reef_eff,
                                           reserve_eff,
                                           restplace,
                                           energy_mod,
                                           coll_risk,
                                           turbidity,
                                           undwater_noise,
                                           footprint,
                                           chempoll_risk,
                                           electric_imp,
                                           temperature_mod)

#Tests positive impact assessment functions

def test_reef_eff():
    
    '''Test res_effect_elect'''

    out = reef_eff(100,1,50)
    
    assert out == 0.5
    assert isinstance(out, float)

def test_reserve_eff():
    
    '''Test res_effect_found'''

    out = reserve_eff(70,100)
    
    assert out == 0.7
    assert isinstance(out, float)
    
def test_restplace():
    
    '''Test restplace_dev'''

    out = restplace(1,50,100)
    
    assert out == 0.5
    assert isinstance(out, float)
    
# Tests for adverse impact assessment functions

def test_energy_mod():
    
    '''Test energy_mod'''

    out = energy_mod(0.3)

    assert out == 0.3
    assert isinstance(out, float)
    
def test_coll_risM():
    
    '''Test coll_riskM'''

    x = [100, 200, 300]
    y = [300,  50, 100]

    out = coll_risk([x,y],30,50,100,50)
    
    assert np.isclose(out, 0.1666, rtol=1e-03)
    assert isinstance(out, float)
    
def test_turbidity():
    
    '''Test turbid'''

    out = turbidity(10,40)
    
    assert out == 1.
    assert isinstance(out, float)
    
def test_undwater_noise():

    out = undwater_noise(100,50)
    
    assert out==0.
    assert isinstance(out, float)

def test_chempoll_risk():
    
    '''Test chem_poll_I'''

    out = chempoll_risk('True')
    
    assert out == 1.
    assert isinstance(out, float)
    
def test_footprint():
    
    '''Test footprint()'''
    
    out = footprint(40,100)
    
    assert out==0.4
    assert isinstance(out,float)

def test_electric_imp():
    
    '''Test electric_imp'''

    out = electric_imp(60,100)
    
    assert out == 1.0
    assert isinstance(out, float)

def test_temperature_mod():
    
    '''Test temperature_mod'''

    out = temperature_mod(40,200)
    
    assert out == 1.0
    assert isinstance(out, float)

