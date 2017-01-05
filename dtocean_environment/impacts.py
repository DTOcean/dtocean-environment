# -*- coding: utf-8 -*-

#    Copyright (C) 2016  Mathew Topper, Rui Duarte, Imanol Touzon,
#                        Jean-Francois Filipot
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""
Created on Wed Jul 15 11:44:29 2015

@author: Mathew Topper Tecnalia R&I
         Imanol Touzón. Tecnalia R&I
         Rui Duarte, FEM

"""

from .functions import (footprint,
                        coll_risk,
                        coll_risk_vessel,                        
                        chempoll_risk,
                        turbidity,
                        undwater_noise,
                        electric_imp,
                        magnetic_imp,
                        temperature_mod,
                        energy_mod,
                        reef_eff,
                        reserve_eff,
                        restplace)
                        
from .logigram import Logigram

class EnergyModification(Logigram):
    
    @property    
    def impact_sign(self):
        
        return -1
    
    @property    
    def pressure_scores_path(self):
        
        return "energymod_pressure.csv"
        
    @property    
    def weighting_scores_path(self):
        
        return "energymod_weighting.csv"
    
    @property
    def receptor_scores_path(self):
        
        return "energymod_receptor.csv"
    
    @classmethod
    def get_function_name(cls):
        
        return "Energy Modification"
    
    @classmethod
    def get_required_inputs(cls):
        
        return ["Energy Modification"]
        
    def __call__(self, inputs_dict):
                           
        energy_impact = energy_mod(inputs_dict["Energy Modification"])

        result = self._calculate_score(energy_impact)
                             
        return result


class Footprint(Logigram):

    @property    
    def impact_sign(self):
        
        return -1
    
    @property    
    def pressure_scores_path(self):
        
        return "footprint_pressure.csv"
        
    @property    
    def weighting_scores_path(self):
        
        return "footprint_weighting.csv"
    
    @property    
    def receptor_scores_path(self):
        
        return "footprint_receptor.csv"
    
    @classmethod
    def get_function_name(cls):
        
        return "Footprint"
    
    @classmethod
    def get_required_inputs(cls):
        
        return ["Surface Area Covered", "Total Surface Area"]

    def __call__(self, inputs_dict):
                           
        footprint_impact = footprint(inputs_dict["Surface Area Covered"],
                                     inputs_dict["Total Surface Area"])

        result = self._calculate_score(footprint_impact)     
                                                             
        return result


class CollisionRisk(Logigram):

    @property    
    def impact_sign(self):
        
        return -1

    @property    
    def pressure_scores_path(self):
        
        return "collrisk_pressure.csv"
        
    @property    
    def weighting_scores_path(self):
        
        return "collrisk_weighting.csv"
    
    @property    
    def receptor_scores_path(self):
        
        return "collrisk_receptor.csv"
    
    @classmethod
    def get_function_name(cls):
        
        return "Collision Risk"
        
    @classmethod
    def get_required_inputs(cls):
        
        return ["Coordinates of the Devices",
                "Size of the Devices",
                "Immersed Height of the Devices",
                "Water Depth",
                "Current Direction"]

    def __call__(self, inputs_dict):
                           
        collision_impact = coll_risk(
                                inputs_dict["Coordinates of the Devices"],
                                inputs_dict["Size of the Devices"],
                                inputs_dict["Immersed Height of the Devices"],
                                inputs_dict["Water Depth"],
                                inputs_dict["Current Direction"])

        result = self._calculate_score(collision_impact)     
                                                             
        return result


class CollisionRiskVessel(Logigram):

    @property    
    def impact_sign(self):
        
        return -1

    @property    
    def pressure_scores_path(self):
        
        return "collriskvessel_pressure.csv"
        
    @property    
    def weighting_scores_path(self):
        
        return "collriskvessel_weighting.csv"
    
    @property    
    def receptor_scores_path(self):
        
        return "collriskvessel_receptor.csv"
    
    @classmethod
    def get_function_name(cls):
        
        return "Collision Risk Vessel"
        
    @classmethod
    def get_required_inputs(cls):
        
        return ["Number of Vessels",
                "Size of Vessels",
                "Total Surface Area"]

    def __call__(self, inputs_dict):
                           
        collision_impact = coll_risk_vessel(
                                inputs_dict["Number of Vessels"],
                                inputs_dict["Size of Vessels"],
                                inputs_dict["Total Surface Area"])

        result = self._calculate_score(collision_impact)     
                                                             
        return result


class ChemicalPollution(Logigram):
        
    @property    
    def impact_sign(self):
        
        return -1

    @property    
    def pressure_scores_path(self):
        
        return "chemicalpollution_pressure.csv"
        
    @property    
    def weighting_scores_path(self):
        
        return "chemicalpollution_weighting.csv"
    
    @property    
    def receptor_scores_path(self):
        
        return "chemicalpollution_receptor.csv"
    
    @classmethod
    def get_function_name(cls):
        
        return "Chemical Pollution"
        
    @classmethod
    def get_required_inputs(cls):
        
        return ["Import of Chemical Polutant"]

    def __call__(self, inputs_dict):

        chempollution_impact = chempoll_risk(inputs_dict["Import of Chemical Polutant"])

        result = self._calculate_score(chempollution_impact)     
                                                             
        return result
        
class Turbidity(Logigram):

    @property    
    def impact_sign(self):
        
        return -1
        
    @property    
    def pressure_scores_path(self):
        
        return "turbidity_pressure.csv"
        
    @property    
    def weighting_scores_path(self):
        
        return "turbidity_weighting.csv"
    
    @property    
    def receptor_scores_path(self):
        
        return "turbidity_receptor.csv"
    
    @classmethod
    def get_function_name(cls):
        
        return "Turbidity"
        
    @classmethod
    def get_required_inputs(cls):
        
        return ["Initial Turbidity",
                "Measured Turbidity"]

    def __call__(self, inputs_dict):
                           
        turbidity_impact = turbidity(
                                inputs_dict["Initial Turbidity"],
                                inputs_dict["Measured Turbidity"])

        result = self._calculate_score(turbidity_impact)
                               
        return result
        
class UnderwaterNoise(Logigram):

    @property    
    def impact_sign(self):
        
        return -1

    @property    
    def pressure_scores_path(self):
        
        return "underwaternoise_pressure.csv"
        
    @property    
    def weighting_scores_path(self):
        
        return "underwaternoise_weighting.csv"
    
    @property    
    def receptor_scores_path(self):
        
        return "underwaternoise_receptor.csv"
    
    @classmethod
    def get_function_name(cls):
        
        return "Underwater Noise"
        
    @classmethod
    def get_required_inputs(cls):
        
        return ["Initial Noise dB re 1muPa",
                "Measured Noise dB re 1muPa"]

    def __call__(self, inputs_dict):
                           
        underwaternoise_impact = undwater_noise(
                                    inputs_dict["Initial Noise dB re 1muPa"],
                                    inputs_dict["Measured Noise dB re 1muPa"])

        result = self._calculate_score(underwaternoise_impact)     
                                                             
        return result
        
class ElectricFields(Logigram):

    @property    
    def impact_sign(self):
        
        return -1

    @property    
    def pressure_scores_path(self):
        
        return "electricfields_pressure.csv"
        
    @property    
    def weighting_scores_path(self):
        
        return "electricfields_weighting.csv"
    
    @property    
    def receptor_scores_path(self):
        
        return "electricfields_receptor.csv"
    
    @classmethod
    def get_function_name(cls):
        
        return "Electric Fields"
        
    @classmethod
    def get_required_inputs(cls):
        
        return ["Initial Electric Field",
                "Measured Electric Field"]

    def __call__(self, inputs_dict):
                           
        electricfield_impact = electric_imp(
                                inputs_dict["Initial Electric Field"],
                                inputs_dict["Measured Electric Field"])

        result = self._calculate_score(electricfield_impact)     
                                                             
        return result


class MagneticFields(Logigram):

    @property    
    def impact_sign(self):
        
        return -1

    @property    
    def pressure_scores_path(self):
        
        return "magneticfields_pressure.csv"
        
    @property    
    def weighting_scores_path(self):
        
        return "magneticfields_weighting.csv"
    
    @property    
    def receptor_scores_path(self):
        
        return "magneticfields_receptor.csv"
    
    @classmethod
    def get_function_name(cls):
        
        return "Magnetic Fields"
        
    @classmethod
    def get_required_inputs(cls):
        
        return ["Initial Magnetic Field",
                "Measured Magnetic Field"]

    def __call__(self, inputs_dict):
                           
        magneticfield_impact = magnetic_imp(
                                inputs_dict["Initial Magnetic Field"],
                                inputs_dict["Measured Magnetic Field"])

        result = self._calculate_score(magneticfield_impact)     
                                                             
        return result


class TemperatureModification(Logigram):
    
    @property    
    def impact_sign(self):
        
        return -1
        
    @property    
    def pressure_scores_path(self):
        
        return "temperaturemodification_pressure.csv"
        
    @property    
    def weighting_scores_path(self):
        
        return "temperaturemodification_weighting.csv"
    
    @property    
    def receptor_scores_path(self):
        
        return "temperaturemodification_receptor.csv"
    
    @classmethod
    def get_function_name(cls):
        
        return "Temperature Modification"
        
    @classmethod
    def get_required_inputs(cls):
        
        return ["Initial Temperature",
                "Measured Temperature"]

    def __call__(self, inputs_dict):
                           
        temperaturemodificaton_impact = temperature_mod(
                                inputs_dict["Initial Temperature"],
                                inputs_dict["Measured Temperature"])

        result = self._calculate_score(temperaturemodificaton_impact)     
                                                             
        return result
        
class ReserveEffect(Logigram):

    @property    
    def impact_sign(self):
        
        return 1
    
    @property    
    def pressure_scores_path(self):
        
        return "reserveeffect_pressure.csv"
        
    @property    
    def weighting_scores_path(self):
        
        return "reserveeffect_weighting.csv"
    
    @property    
    def receptor_scores_path(self):
        
        return "reserveeffect_receptor.csv"
    
    @classmethod
    def get_function_name(cls):
        
        return "Reserve Effect"
        
    @classmethod
    def get_required_inputs(cls):
        
        return ["Fishery Restriction Surface",
                "Total Surface Area"]

    def __call__(self, inputs_dict):
                           
        reserveeffect_impact = reserve_eff(
                                inputs_dict["Fishery Restriction Surface"],
                                inputs_dict["Total Surface Area"])

        result = self._calculate_score(reserveeffect_impact)     
                                                             
        return result
        
class ReefEffect(Logigram):

    @property    
    def impact_sign(self):
        
        return 1

    @property    
    def pressure_scores_path(self):
        
        return "reefeffect_pressure.csv"
        
    @property    
    def weighting_scores_path(self):
        
        return "reefeffect_weighting.csv"
    
    @property    
    def receptor_scores_path(self):
        
        return "reefeffect_receptor.csv"
    
    @classmethod
    def get_function_name(cls):
        
        return "Reef Effect"
        
    @classmethod
    def get_required_inputs(cls):
        
        return ["Total Surface Area",
                "Surface Area of Underwater Part",
                "Number of Objects"]

    def __call__(self, inputs_dict):
                           
        reefeffect_impact = reef_eff(
                                inputs_dict["Total Surface Area"],
                                inputs_dict["Surface Area of Underwater Part"],
                                inputs_dict["Number of Objects"])

        result = self._calculate_score(reefeffect_impact)     
                                                             
        return result
        
class RestingPlace(Logigram):

    @property    
    def impact_sign(self):
        
        return 1

    @property    
    def pressure_scores_path(self):
        
        return "restingplace_pressure.csv"
        
    @property    
    def weighting_scores_path(self):
        
        return "restingplace_weighting.csv"
    
    @property    
    def receptor_scores_path(self):
        
        return "restingplace_receptor.csv"
    
    @classmethod
    def get_function_name(cls):
        
        return "Resting Place"
        
    @classmethod
    def get_required_inputs(cls):
        
        return ["Object Emerged Surface",
                "Number of Objects",
                "Total Surface Area"]

    def __call__(self, inputs_dict):
                           
        restingplace_impact = restplace(
                                inputs_dict["Object Emerged Surface"],
                                inputs_dict["Number of Objects"],
                                inputs_dict["Total Surface Area"])

        result = self._calculate_score(restingplace_impact)     
                                                             
        return result
