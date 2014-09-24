# -*- coding: utf-8 -*-
"""
Created on Wed Sep 17 16:36:03 2014
a.k.a. Who should we consume like?

@author: rob
"""
import numpy as np
import global_demo_model
from vectorrotation import *

model = global_demo_model.GlobalDemoModel.\
    from_pickle('../../Models/model2010.gdm')

__debugmode__ = False
__theta__ = np.deg2rad(1) # 1 degree in radians

if __debugmode__:
    __country_names__ = ['AUS', 'BRA', 'FRA']
else:
    __country_names__ = model.country_names
    
def country_metric(country):
    """
    Return a metric used to evaluate changes to `country`
    """
    intermediate_usage = country.Z().sum() # Column sum
    value_added = country.x - intermediate_usage
    return value_added.sum()

def reference_vector(country):
    """
    Return the vector to be used in the rotation experiment
    """
    try:
        vec = country.f
    except AttributeError:
        vec = model.countries[country].f
    return vec

def set_reference_vector(country, v):
    ref_vector = reference_vector(country)
    for k in ref_vector.keys():
        ref_vector[k] = v[k]
    
def min_angle(countries, base_country):
    """
    Find the smallest angle, in radians, of the vector 
    given by `reference_vector()`
    between each element of countries and base_country.
    
    Parameters
    ----------
    countries: dict
        A dictionary of Country objects, keyed on country name
    base_country: Country
        A Country object extracted from a GlobalDemoModel
        
    Returns
    -------
    float
        Angle in radians
    """
    angles = pd.DataFrame([[c,
        angle_between(reference_vector(countries[c]), 
                      reference_vector(base_country))]
                      for c in countries if c != base_country])
    angles.columns = ['country', 'angle']
    return angles.angle.min()
    
def rotate_country(from_country, to_country, angle):
    """
    Rotate the reference vector of `from_country` towards
    that of `to_country` by `angle` radians
    """
    u = reference_vector(from_country)
    v = reference_vector(to_country)
    w = vector_rotate(u, v, angle)
    for k in u.keys():
        u[k] = w[k]

def rotation_experiment(model, base_country):
    print "Running experiment for %s" % base_country
    if min_angle(model.countries, base_country) < __theta__:
        theta = min_angle(model.countries, base_country)
        print "Warning: minimum angle from %s " \
            "is less than __theta__" % base_country
        print "Using theta = %.1f" % theta
    else:
        theta = __theta__
    try:
        base_country = model.countries[base_country]
    except:
        pass
    baseline_metric = country_metric(base_country)
    baseline_vector = reference_vector(base_country).copy()
    print "Baseline metric: %i" % baseline_metric
    results = []
    for cname in __country_names__:
        if cname != base_country.name:
            other_country = model.countries[cname]
            # Rotate towards other_country by angle theta
            rotate_country(base_country, other_country, theta)
            model.recalculate_world()
            metric = country_metric(base_country)
            print "Country: %s, metric: %i" % (cname, metric)
            results.append({'base_country':base_country.name,
                            'country':cname,
                            'x_total':base_country.x.sum(),
                            'f_total':base_country.f.sum(),
                            'z_total':base_country.Z().sum().sum(),
                            'metric':metric})
            # Now rotate back to the starting point.
            # No need to recalculate world here.
            set_reference_vector(base_country, baseline_vector)
    # Leave things as we found them
    model.recalculate_world()        
    results = pd.DataFrame(results)
    results['delta'] = baseline_metric - results.metric
    return results

def run_experiment():
    results = [rotation_experiment(model, c) for c in __country_names__]
    results = pd.concat(results)
    results.to_csv('rotation_results.csv', index=False)