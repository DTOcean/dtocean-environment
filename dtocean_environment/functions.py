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
Created on Tue Mar 24 17:31:02 2015

Functions created to compute the environmental impact of both wave energy and 
tidal energy farms.
There is an independent list of functions for wave farms and other independent
list of functions for tidal farms.

@author: Imanol TouzÃ³n. Tecnalia R&I 29-09-2015
         Jean-Francois Filipot, FEM
         Rui Duarte, FEM
"""
from __future__ import division

import numpy as np
from shapely.geometry import Point, LineString

# Positive Effect: 3 functions

def reef_eff(farm_A,submA_comp,comp_N):
    '''
    ARGS:
        farm_A: total surface area of the farm (WP2)
        submA_comp: Surface area of underwater part of a device/electrical/found (user)
        comp_N: device/electrical/found Number
    '''
    
    reefeff=submA_comp*comp_N/farm_A
    
    return reefeff
    
def reserve_eff(fish_S,farm_A):
    '''
    ARGS:
        fish_S: Fishery restriction surface (user)
        farm_A: total surface area of the farm (WP2)
    '''
    
    reseff=fish_S/farm_A

    return reseff
    
def restplace(emergA_comp,comp_N,farm_A):
    '''
    ARGS:
        emergA_comp: surface area of the emerged part of the device/electrical component (user)
        comp_N: device/electrical component Number
        farm_A: total surface area of the farm (WP2)
    '''
    
    restP=emergA_comp*comp_N/farm_A

    return restP
    
# Adverse effect: 8 functions

def coll_risk(dev_pos, dev_dim, dev_height, water_dep, cur_dir):
    '''Collision risk
    
    the function estimates the number of intersections, between
    a large number of parallel lines aligned with the mean current
    axis. The probability of collision will be: P=nb of lines with 
    at least one intersection/total nb of lines

    Args: 
        dev_pos: Coordinates of the devices
        dev_dim: Maximum horizontal size of the device
        dev_height: Height of device immersed in the water
        water_dep: Minimum water depth 
        cur_dir: direction of the current [in degrees]

    Returns:
        collision_risk: collision risk factor

    '''
    if not dev_pos:
        return 0.

    # x,y positions
    [x_pos, y_pos] = dev_pos

    # number of devices
    if len(x_pos) <= 1:
        return 0.
    else:
        ndev=len(x_pos)

    # area limits
    x_min = np.min(x_pos)
    x_max = np.max(x_pos)
    y_min = np.min(y_pos)
    y_max = np.max(y_pos)

    # initialize the nb of intersection points
    n_lines = 0
    n_intersections = 0

    #convert current direction to (0,360) degrees and to radians
    cur_dir = cur_dir % 360
    angle = np.deg2rad(cur_dir)

    # cartesian distance between the lines
    if np.sin(angle) != 0.:  # avoid division by zero (try except fails???)
        lx = np.abs(dev_dim / np.sin(angle))
    else:
        lx = x_max - x_min

    if np.cos(angle) != 0.:
        ly = np.abs(dev_dim / np.cos(angle))
    else:
        ly = y_max - y_min

    # detect the quadrant
    if cur_dir > 90. and cur_dir <= 270.:
        x_start = x_max
        x_end   = x_min
    else:
        x_start = x_min
        x_end   = x_max

    if cur_dir > 180. and cur_dir <= 360.:
        y_start = y_max
        y_end   = y_min
    else:
        y_start = y_min
        y_end   = y_max

    # along x
    il = 0
    xi = x_min

    while xi <= x_max:
        if np.tan(angle) == 0.: # division by zero
            break
        # this is where we define the equations for the parallel lines
        yi = y_start # origin of the line (ordinate)
        xf = (y_end-yi) / np.tan(angle) + xi # end of the line (absciss)
        yf = y_end
        trajectory = LineString([(xi, yi), (xf, yf)])

        # this is where we define the machines, considered as circles
        ni=0
        for id in range (0,ndev):
            device = Point(x_pos[id],y_pos[id]).buffer(dev_dim)
            # calculate nb of intersections ni
            if device.intersects(trajectory):
                ni=ni+1

        il += 1
        xi = x_min + 2. * lx * il
        n_lines += 1
        if ni > 0:
            n_intersections += 1

    # along y
    il=0
    yi = y_min

    while yi <= y_max:
        # this is where we define the equations for the parallel lines
        xi = x_start # origin of the line (ordinate)
        xf = x_end
        yf = (x_end - xi) * np.tan(angle) + yi # end of the line (absciss)
        trajectory = LineString([(xi, yi), (xf, yf)])

        # this is where we define the machines, considered as circles
        ni=0
        for id in range (0,ndev):
            device = Point(x_pos[id],y_pos[id]).buffer(dev_dim)        
            # calculate nb of intersections ni
            if device.intersects(trajectory):
                ni=ni+1

        il += 1
        yi = y_min + 2. * ly * il
        n_lines += 1
        if ni > 0:
            n_intersections += 1

    collision_rate = n_intersections / float(n_lines)

    depth_factor = dev_height / float(water_dep)

    collision_risk = depth_factor * collision_rate

    # horizontal area impact
    ''' needs some calibration
    area_dev = 0.
    for id in range (0,ndev):
        area_dev += Point(x_pos[id],y_pos[id]).buffer(dev_dim).area

    area_total = (x_max - x_min) * (y_max - y_min)
    
    area_factor = area_dev / float(area_total)

    collision_risk = min(collision_risk + area_factor, 1.)
    '''

    return collision_risk


def coll_risk_vessel(num_vessel, size_vessel, total_surf):
    '''Collision risk with vessels
    
    this function computes the factor between the number of vessels in the
    area and the total surface area 

    Args: 
        num_vessel : Number of vessels in the area
        size_vessel: Medium size of the vessels in the area
        total_surf : Total surface of the lease area

    Returns:
        collision_risk: collision risk factor

    '''

    # area occupied by a vessel
    
    area_vessel = np.pi * (0.5*size_vessel)**2

    # collision risk factor

    collision_risk = num_vessel * area_vessel / total_surf
    
    collision_risk = min(collision_risk, 1.)
    
    return collision_risk

  
def turbidity(init_turb,meas_turb):
    '''Turbidity
    
    the function compares the initial turbidity with the measured turbidity.
    If there is no change the impact is inexistent. If it increases, there is
    environmental impact.

    Args:
        init_turb: initial turbidity (user)
        meas_turb: turbidity measured during operational/installation phase of the farm with devices (user)

    Returns:
        turb: turbidity impact
    '''
    
    if meas_turb <= init_turb:
        turb = 0.
    else:
        turb = 1.

    return turb
    
def undwater_noise(init_noise, meas_noise):
    '''Underwater Noise
    
    the function compares the initial underwater noise with the measured noise.
    If there is no change the impact is inexistent. If it increases, there is
    environmental impact.

    Args:
        init_noise: initial noise (user)
        meas_noise: measured noise during operational/installation phase of the farm with devices (user)

    Returns:
        undwnoise: underwater impact
    '''
    
    if meas_noise <= init_noise:
        undwnoise = 0.
    else:
        undwnoise = 1.
    
    return undwnoise
    
def chempoll_risk(chempoll_import):
    ''' Chemical Pollution
    
    the function checks if there is the import of a chemical polutant.

    Args:
        chempoll_import: import of chemical polutant (user)

    Returns:
        chempoll_impact: chemical pollution risk during installation
    '''
    
    if chempoll_import:
        chempoll_impact = 1.
    else:
        chempoll_impact = 0.
    
    return chempoll_impact
    
def footprint(comp_A,farm_A):
    '''
    ARGS:
        comp_A: Substrata surface area covered by the elec/found components (WP3-WP4)
        farm_A: total surface area of the farm (WP2)
    '''
    
    footp= comp_A/float(farm_A)

    footp = min(footp, 1.)
    
    return footp


def electric_imp(initial_electric, measured_electric):
    '''Electric Field
    
    the function compares the initial EF with the measured EF.
    If there is no change the impact is inexistent. If it increases, there is
    environmental impact.

    Args:
        initial_electric  : initial electric field (user)
        measured_electric : measured electric field during operational/installation
                            phase of the farm with devices (user)

    Returns:
        electric: electric field impact
    '''
    
    if measured_electric <= initial_electric:
        electric = 0.
    else:
        electric = 1.
    
    return electric


def magnetic_imp(initial_magnetic,measured_magnetic):
    '''Magnectic Field
    
    the function compares the initial magnetic field with the measured magnetic field.
    If there is no change the impact is inexistent. If it increases, there is
    environmental impact.

    Args:
        initial_magnetic  : initial magnetic field (user)
        measured_magnetic : measured magnetic field during operational/installation
                            phase of the farm with devices (user)

    Returns:
        magnetic: magnetic field impact
    '''
    
    if measured_magnetic <= initial_magnetic:
        magnetic = 0.
    else:
        magnetic = 1.
    
    return magnetic

    
def temperature_mod(initial_Temp,measured_Temp):
    '''Temperature Modification
    
    the function compares the initial Temperature with the measured Temperature.
    If there is no change the impact is inexistent. If it increases, there is
    environmental impact.

    Args:
        initial_Temp: initial Temperature (user)
        measured_Temp: measured Temperature during operational/installation phase of the farm with devices (user)

    Returns:
        temperature: temperature modification impact
    '''
    
    # Threshold of temperature modification
    
    thresh_T = 5.
    
    if measured_Temp <= initial_Temp + thresh_T:
        temperature = 0.
    else:
        temperature = 1.
    
    return temperature

def energy_mod(energy):
    '''Energy Modification
    
    the function compares the value of the Energy Modification

    Args:
        energy: input from the WP2

    Returns:
        energy: energy modification impact
    '''

    return energy
