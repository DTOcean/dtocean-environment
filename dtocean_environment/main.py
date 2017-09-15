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
Created on Mon Jul 20 11:33:58 2015

@author: Mathew Topper Tecnalia R&I
         Imanol Touzón. Tecnalia R&I
         Rui Duarte, FEM
"""

import os
import abc

import numpy as np

import pandas as pd
from polite.abc import abstractclassmethod

from .impacts import (EnergyModification,
                     Footprint,
                     CollisionRisk,
                     CollisionRiskVessel,
                     ChemicalPollution,
                     Turbidity,
                     UnderwaterNoise,
                     ElectricFields,
                     MagneticFields,
                     TemperatureModification,
                     ReefEffect,
                     ReserveEffect,
                     RestingPlace)
                      
mod_path = os.path.realpath(__file__)
mod_dir = os.path.dirname(mod_path)
                      
class Stage(object):
    
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, protected_observations=None,
                       species_observations=None,
                       constraint_observations=None):
        
        self._logigrams = self._init_logigrams(protected_observations,
                                               species_observations,
                                               constraint_observations)
        
        return
    
    @abc.abstractproperty 
    def data_dir_path(self):
        
        raise NotImplementedError
    
    @abstractclassmethod
    def get_module_name(cls):
        
        raise NotImplementedError
    
    @abstractclassmethod    
    def get_logigram_classes(cls):
        
        raise NotImplementedError
        
    def _init_logigrams(self, protected_observations=None,
                              species_observations=None,
                              constraint_observations=None):
                                  
        logigram_dict = {}
        
        for Logigram in self.get_logigram_classes():
            
            name = Logigram.get_function_name()
            
            if name not in constraint_observations:
                
                errStr = ("Constraint observation missing for function {}. "
                          "None accepted.").format(name)
                raise ValueError(errStr)
            
            logigram = Logigram(self.data_dir_path,
                                protected_observations,
                                species_observations,
                                constraint_observations[name])
                                
            logigram_dict[name] = logigram
            
        return logigram_dict
        
    def get_inputs(self):
        
        all_inputs = []
        
        for logigram in self._logigrams.itervalues():
        
            required_inputs = logigram.get_required_inputs()
            all_inputs.extend(required_inputs)
            
        return all_inputs
        
    def _can_assess(self, input_dict, logigram):
        
        input_list = [key for key, value in input_dict.iteritems()
                                                    if value is not None]
        input_set = set(input_list)
        
        function_set = set(logigram.get_required_inputs())
        
        if function_set.issubset(input_set):
            
            result = True
            
        else:
            
            result = False
            
        return result
        
    def _get_assessments(self, input_dict):
        
        confidence_dict = {}
        eis_dict = {}
        recommendations_dict = {}
        seasons_df = pd.DataFrame(columns=['january',
                                           'february',
                                           'march',
                                           'april',
                                           'may',
                                           'june',
                                           'july',
                                           'august',
                                           'september',
                                           'october',
                                           'november',
                                           'december'])
        
        for name, logigram in self._logigrams.iteritems():
            
            if self._can_assess(input_dict, logigram):
                
                assessment = logigram(input_dict)
                confidence = assessment.confidence_level
                eis = assessment.get_EIS()
                recommendations = assessment.get_recommendations()
                season = assessment.receptor_seasons

                
            else:
                
                confidence = None
                eis = None
                recommendations = None
                season = None
                
            confidence_dict[name] = confidence
            eis_dict[name] = eis
            recommendations_dict[name] = recommendations

            if season is None: continue;
                            
            if eis >= 0:
                per_season = season.max()
            else:
                per_season = season.min()
                
            per_season.name = name
            seasons_df = seasons_df.append(per_season)
                                                    
        return confidence_dict, eis_dict, recommendations_dict, seasons_df
     
    def __call__(self, input_dict):
        
        given_set = set(input_dict.keys())
        needed_set = set(self.get_inputs())
        
        if given_set != needed_set:
            
            missing_keys = list(needed_set - given_set)
            need_str = ", ".join(missing_keys)
            errStr = ("The keys of the input dictionary must contain all "
                      "required variables. Missing are: {}").format(need_str)
            raise KeyError(errStr)
        
        (confidence_dict,
         eis_dict,
         recommendations_dict,
         combined_seasons) = self._get_assessments(input_dict)

        # global environmental score

        negative_impacts = []
        positive_impacts = []

        for impact in eis_dict:
            value = eis_dict[impact]
            if value < 0:
                negative_impacts.append(value)
            else:
                positive_impacts.append(value)
        
        negative_impacts = np.array(negative_impacts, dtype=np.float)
        positive_impacts = np.array(positive_impacts, dtype=np.float)
        
        global_eis = {}
        
        if negative_impacts.size:
            global_eis["Negative Impact"] = np.nanmean(negative_impacts)
            global_eis["Max Negative Impact"] = np.nanmin(negative_impacts)
            global_eis["Min Negative Impact"] = np.nanmax(negative_impacts)
        else:
            global_eis["Negative Impact"] = np.nan
            global_eis["Max Negative Impact"] = np.nan
            global_eis["Min Negative Impact"] = np.nan

        if positive_impacts.size:
            global_eis["Positive Impact"] = np.nanmean(positive_impacts)
            global_eis["Max Positive Impact"] = np.nanmax(positive_impacts)
            global_eis["Min Positive Impact"] = np.nanmin(positive_impacts)
        else:
            global_eis["Positive Impact"] = np.nan
            global_eis["Max Positive Impact"] = np.nan
            global_eis["Min Positive Impact"] = np.nan

        return confidence_dict, eis_dict, recommendations_dict, \
            combined_seasons, global_eis


class HydroStage(Stage):
    
    @property
    def data_dir_path(self):
        
        data_path = os.path.join(mod_dir, "data", "hydrodynamics")
        
        return data_path
    
    @classmethod
    def get_module_name(cls):
        
        return "Hydrodynamics"
    
    @classmethod
    def get_logigram_classes(cls):
        
        logigram_list = [EnergyModification, CollisionRisk, Turbidity, 
                         UnderwaterNoise, ReserveEffect, ReefEffect,
                         RestingPlace]
        
        return logigram_list
        
class ElectricalStage(Stage):
    
    @property
    def data_dir_path(self):
        
        data_path = os.path.join(mod_dir, "data", "electrical subsystems")
        
        return data_path
    
    @classmethod
    def get_module_name(cls):
        
        return "Electrical Subsystems"
    
    @classmethod
    def get_logigram_classes(cls):
        
        logigram_list = [Footprint, CollisionRisk, UnderwaterNoise, 
                         ElectricFields, MagneticFields,
                         TemperatureModification,ReserveEffect,
                         ReefEffect, RestingPlace]
        
        return logigram_list
        
class MooringStage(Stage):
    
    @property
    def data_dir_path(self):
        
        data_path = os.path.join(mod_dir, "data", "moorings and foundations")
        
        return data_path
    
    @classmethod
    def get_module_name(cls):
        
        return "Moorings and Foundations"
    
    @classmethod
    def get_logigram_classes(cls):
        
        logigram_list = [Footprint, CollisionRisk, UnderwaterNoise, ReefEffect]
        
        return logigram_list
        
class InstallationStage(Stage):
    
    @property
    def data_dir_path(self):
        
        data_path = os.path.join(mod_dir, "data", "installation")
        
        return data_path
    
    @classmethod
    def get_module_name(cls):
        
        return "Installation"
    
    @classmethod
    def get_logigram_classes(cls):
        
        logigram_list = [Footprint, CollisionRiskVessel, ChemicalPollution, 
                         Turbidity, UnderwaterNoise]
        
        return logigram_list
        
class OperationMaintenanceStage(Stage):
    
    @property
    def data_dir_path(self):
        
        data_path = os.path.join(mod_dir, "data", "maintenance")
        
        return data_path
    
    @classmethod
    def get_module_name(cls):
        
        return "Operation and Maintenance"
    
    @classmethod
    def get_logigram_classes(cls):
        
        logigram_list = [Footprint, CollisionRiskVessel, ChemicalPollution, 
                         Turbidity, UnderwaterNoise]
        
        return logigram_list


if __name__=='__main__':
    
    pass