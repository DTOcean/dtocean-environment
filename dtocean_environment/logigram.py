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

Mats notes:

* Descriptions of the purpose of each method is useful.
* Classes start with a capital letter.
* Each line should be less than 80 chars
* Whitespace improves readability
* list initialisation is not necessary but numpy arrays do need it. Numpy
  arrays are faster.
"""

import os
import abc
from collections import OrderedDict

import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
from polite.abc import abstractclassmethod


class Score(object):
    
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, data_path):
        
        self._table = self._init_table(data_path)
        
        return
        
    @abc.abstractproperty    
    def index_column(self):
        
        raise NotImplementedError
        
    def _init_table(self, data_path):
        
        table = pd.read_csv(data_path)
        table = table.set_index(self.index_column)
                       
        return table
        
    def is_empty(self):
        
        return self._table.empty
        
    def get_index(self):
        
        return self._table.index
        
    def get_column(self, column, idx=None):
        
        result = self._table[column]
        
        if idx is not None: result = result.loc[idx];
            
        return result
        
    def get_score(self, idx=None):
        
        result = self.get_column("score", idx)
        
        return result

    def get_genericexplanation(self, idx=None):
        
        result = self.get_column("generic explanation score", idx)
        
        return result

    def get_generalrecommendation(self, idx=None):
        
        result = self.get_column("general recommendation", idx)
        
        return result

    def get_detailedrecommendation(self, idx=None):
        
        result = self.get_column("detailed recommendation", idx)
        
        return result


class PressureScore(Score):
    
    @property
    def index_column(self):
        
        return "function result"
        
        
class WeightingScore(Score):
    
    @property
    def index_column(self):
        
        return "weighting parameter"
        
        
class ReceptorScore(Score):
    
    @property
    def index_column(self):
        
        return "Subclass or group"
        
    def get_impact_score(self, idx, impact):
        
        idx_scores = self._table.loc[idx]
        
        result = None
        
        for row in idx_scores.iterrows():
            
            if impact < row[1]["upper bound"]:

                result = row[1]["score"]
                break
            
        if result == None:
            
            errStr = ("No score was found for receptor {} corresponding to "
                      "function result {}").format(idx, impact)
            raise ValueError(errStr)
                
        return result

        
class Assessment(object):
    
    def __init__(self, pressure_score,
                       adjusted_pressure_score,
                       constraint,
                       environmental_impact_score,
                       pressure_recommendations,
                       species_list=None,
                       score_list=None,
                       eis_list=None,
                       season_table=None):
                
        self.score_history = None
        self.receptor_history = None
        self.receptor_seasons = None
        
        self.confidence_level = 1
        self.score_history = self._init_score_history(
                                                pressure_score,
                                                adjusted_pressure_score,
                                                constraint,
                                                environmental_impact_score,
                                                pressure_recommendations)
                                                
        if (species_list is None or 
                score_list is None or
                    eis_list is None): return;
                        
        self.confidence_level = 2
        self.receptor_history = self._init_receptor_history(species_list,
                                                            score_list,
                                                            eis_list)
                                                            
        if season_table is None: return;
        
        self.confidence_level = 3
        self.receptor_seasons = season_table
        
        return
        
    def _init_score_history(self, pressure_score,
                                  adjusted_pressure_score,
                                  constraint,
                                  environmental_impact_score,
                                  pressure_recommendations):
              
        # Record the scoring steps
        score_history = OrderedDict()                                  
    
        score_history["Pressure Score"] = pressure_score
        
        if adjusted_pressure_score is not None:
            
            score_history["Adjusted Pressure Score"] = adjusted_pressure_score
            score_history["Constraint"] = constraint
            
        score_history["Environmental Impact Score"] = \
                                                    environmental_impact_score
                                                    
        score_history["Pressure Recommendations"] = pressure_recommendations
        
        return score_history
        
    def _init_receptor_history(self, species_list,
                                     score_list,
                                     eis_list):

        receptor_score_dict = {}
                                                            
        receptor_score_dict["Species"] = species_list
        receptor_score_dict["Receptor Sensitivity Score"] = score_list
        receptor_score_dict["Environmental Impact Score"] = eis_list
            
        receptor_score_history = pd.DataFrame(receptor_score_dict)
        receptor_score_history = receptor_score_history.set_index("Species")
        
        return receptor_score_history
        
    def get_EIS(self):
        
        return self.score_history["Environmental Impact Score"]
                                                                    

    def get_recommendations(self):
        
        return self.score_history["Pressure Recommendations"]


class Logigram(object):
    
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, data_dir_path,
                       protected_observations=None,
                       receptor_observations=None,
                       weighting_parameter=None):
        
        self._pressure_score = None
        self._weighting_score = None
        self._receptor_score = None
        self._protected_table = None
        self._receptor_table = None
        self._weighting_parameter = None
        
        self._pressure_score = self._init_pressure_score(data_dir_path)
        self._weighting_score = self._init_weighting_score(data_dir_path)
        self._receptor_score = self._init_receptor_score(data_dir_path)
        self._protected_table = protected_observations       
        self._receptor_table = self._init_receptor_table(receptor_observations)
        self._weighting_parameter = weighting_parameter
        
        return

    @abc.abstractproperty    
    def pressure_scores_path(self):
        
        raise NotImplementedError
     
    @abc.abstractproperty 
    def weighting_scores_path(self):
        
        raise NotImplementedError
        
    @abc.abstractproperty
    def receptor_scores_path(self):
        
        raise NotImplementedError
    
    @abstractclassmethod
    def get_function_name(cls):
        
        raise NotImplementedError
    
    @abstractclassmethod
    def get_required_inputs(cls):
        
        raise NotImplementedError
        
    def _init_pressure_score(self, dir_path):
        
        pressure_score_path = os.path.join(dir_path, self.pressure_scores_path)
        pressure_score = PressureScore(pressure_score_path)
                       
        return pressure_score
        
    def _init_weighting_score(self, dir_path):
        
        weighting_score_path = os.path.join(dir_path,
                                            self.weighting_scores_path)
        weighting_score = WeightingScore(weighting_score_path)
                       
        return weighting_score
        
    def _init_receptor_score(self, dir_path):
        
        receptor_score_path = os.path.join(dir_path, self.receptor_scores_path)
        receptor_score = ReceptorScore(receptor_score_path)
                       
        return receptor_score
        
    def _init_receptor_table(self, receptor_observations):
        
        if receptor_observations is None: return None;
        if self._receptor_score.is_empty(): return None;
        
        # Check that the observations are sufficient and filter if over
        # specified            
        given_set = set(receptor_observations.index)
        needed_set = set(self._receptor_score.get_index())
                    
        if given_set <= needed_set:
            
            missing_keys = list(needed_set - given_set)
           
            need_str = " ,".join(missing_keys)
            errStr = ("Observation data for all receptors of {} must be "
                      "given. Missing are: {}").format(
                                                    self.get_function_name(),
                                                    need_str)
    
            raise KeyError(errStr)
            
        receptor_table = receptor_observations.loc[needed_set]
        
        return receptor_table

    def get_pressure_score(self, impact):
        
        '''Linear interpolation of the impact given by the corresponding
        environmental function between the scores stored in local tables'''
        
        impact_levels = self._pressure_score.get_index()
        impact_scores = self._pressure_score.get_score()

        f1_int = interp1d(impact_levels, impact_scores)
        f_score = f1_int(impact)

        return float(f_score)
    
    def get_adjusted_pressure_score(self, pressure_score):
        
        '''Procedure that checks if the 'constraints' is contained within
        the constraint table. If 'yes' the weighted score is returned.'''
        
        constraint = self._weighting_parameter
            
        if constraint in self._weighting_score.get_index():
            
            constraint_score = self._weighting_score.get_score(constraint)
            adjusted_pressure_score = pressure_score * constraint_score
            
            return adjusted_pressure_score, constraint
            
        else:
            
            return None
        
    def get_receptor_sensitivity_scores(self, pressure_score, impact):
        
        '''Procedure which extracts receptor scores from the 'active' tables
        and multiplies by the weighted score giving it back.'''
        
        if self._receptor_table is None: return None;
            
        receptor_sensitivity_scores = {}
                
        for receptor in self._receptor_score.get_index():

            if not self._receptor_table.loc[receptor, "observed"]:
                receptor_score = 0
            else:
                receptor_score = self._receptor_score.get_score(receptor)
            
            # Modification for receptor scores modified by impact value.
            if isinstance(receptor_score, pd.Series):
                
                receptor_score = self._receptor_score.get_impact_score(
                                                                    receptor,
                                                                    impact)
            
            combined_score = pressure_score * receptor_score
            receptor_sensitivity_scores[receptor] = combined_score
                        
        return receptor_sensitivity_scores


    def get_recommendations(self, impact):
        
        '''Recomendations corresponding to the nearest pressure score
        '''

        impact_levels = self._pressure_score.get_index()
        
        
        rec1 = self._pressure_score.get_genericexplanation()
        rec2 = self._pressure_score.get_generalrecommendation()
        rec3 = self._pressure_score.get_detailedrecommendation()

        # nearest pressure score
        idx = impact_levels[np.argmin(np.abs(impact_levels.values - 0.2*impact))]

        rec_dict = {}
        
        rec_dict["Generic Explanation"] = rec1[idx]
        rec_dict["General Recommendation"] = rec2[idx]
        rec_dict["Detailed Recommendation"] = rec3[idx]

        return rec_dict


    def normalise_score(self, score):
        
        '''Normalise the environmental impact score
           [-10,-90] for a negative impact
           [10,50] for a positive impact
        '''
        
        if self.impact_sign < 0:
            mapped_score = - 3.2 * score - 10.
        else:
            mapped_score = 1.6 * score + 10.
            
        return mapped_score

        
    def get_environmental_impact_score(self, score):
        
        '''Test for protected species'''
        
        if any(self._protected_table["observed"]) and self.impact_sign < 0:
                                
            environmental_impact_score = -100.
            
        else:
            
            environmental_impact_score = score
        
        return environmental_impact_score
        
    def get_seasonal_scores(self, receptor_normal_scores):
        
        if self._receptor_table is None: return None;
        
        if (set(receptor_normal_scores.keys()) !=
                                        set(self._receptor_table.index)):
                                            
            missing = (set(self._receptor_table.index) -
                                    set(receptor_normal_scores.keys()))
                                            
            missing_str = " ,".join(list(missing))
            errStr = ("The keys of receptor_sensitivity_scores must "
                      "match the receptor scores table index. "
                      "Missing is: {}").format(missing_str)
            raise KeyError(errStr)

        # Test if any subclasses have seasonal records
        seasonal_receptors = self._receptor_table.copy()
        seasonal_receptors = seasonal_receptors.drop("observed", 1)
        
        if seasonal_receptors.isnull().values.all(): return None;
            
        # Fix the column names and order
        column_order = [('observed january', 'january'),
                        ('observed february', 'february'),
                        ('observed march', 'march'),
                        ('observed april', 'april'),
                        ('observed may', 'may'),
                        ('observed june', 'june'),
                        ('observed july', 'july'),
                        ('observed august', 'august'),
                        ('observed september', 'september'),
                        ('observed october', 'october'),
                        ('observed november', 'november'),
                        ('observed december', 'december')
                        ]
        new_columns = OrderedDict(column_order)
                       
        seasonal_receptors = seasonal_receptors.rename(columns=new_columns)
        seasonal_receptors = seasonal_receptors.reindex(new_columns.values(),
                                                        axis=1)
        sensitivity_series = pd.Series(receptor_normal_scores)
        
        seasonal_scores = seasonal_receptors.fillna(1)
        seasonal_scores = seasonal_scores.multiply(sensitivity_series,
                                                   axis="index")
                                                   
        return seasonal_scores
        
    def _calculate_score(self, impact):
                                   
        # Find the pressure score and set the sign of the function
        pressure_score = self.get_pressure_score(impact)

        pressure_recommendations = self.get_recommendations(pressure_score)
        
        # Check for constraint to adjust
        if self._weighting_parameter is None:
            
            adjusted_pressure_score = pressure_score
            constraint = None
            
        else:
            
            # Constraints update the signed pressure score.
            (adjusted_pressure_score,
             constraint) = self.get_adjusted_pressure_score(pressure_score)
            
        # Try for an RSS score
        receptor_sensitivity_scores = self.get_receptor_sensitivity_scores(
                                                    adjusted_pressure_score,
                                                    impact)

        # Bifurcation. Finish if there is no receptor information.
        if receptor_sensitivity_scores is None:
            
            receptor_sensitivity_score = adjusted_pressure_score * 5.
            normalised_score = self.normalise_score(receptor_sensitivity_score)
            environmental_impact_score = self.get_environmental_impact_score(
                                                            normalised_score)
                                                                        
            result = Assessment(pressure_score,
                                adjusted_pressure_score,
                                constraint,
                                environmental_impact_score,
                                pressure_recommendations)
                    
            return result
        
        # Calculate per receptor scores.                                                                                                               
        species_list = []
        score_list = []
        eis_list = []
        normal_score_dict = {}
            
        for species, score in receptor_sensitivity_scores.iteritems():
            
            species_list.append(species)
            score_list.append(score)

            normalised_score = self.normalise_score(score)
            eis = self.get_environmental_impact_score(normalised_score)
            eis_list.append(eis)
            
            normal_score_dict[species] = normalised_score
            
        seasonal_score = self.get_seasonal_scores(normal_score_dict)
        
        if self.impact_sign > 0:
            
            environmental_impact_score = max(eis_list)
            
        else:
            
            environmental_impact_score = min(eis_list)
            
            
        result = Assessment(pressure_score,
                            adjusted_pressure_score,
                            constraint,
                            environmental_impact_score,
                            pressure_recommendations,
                            species_list,
                            score_list,
                            eis_list,
                            seasonal_score)
                
        return result
    
    @abc.abstractmethod
    def __call__(self):
        
        raise NotImplementedError

        
