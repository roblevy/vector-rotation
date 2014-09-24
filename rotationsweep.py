# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 13:33:10 2014

Sweep out the rotation between a reference country and all others,
plotting the `country_metric` at each point along the rotation.

@author: rob
"""

import rotatecountry as rc
import global_demo_model
import numpy as np
import pandas as pd

__reference_country__ = 'CAN'
__model__ = global_demo_model.GlobalDemoModel.\
    from_pickle('../../Models/model2010.gdm')
#__countries__ = ['USA', 'POL']
__countries__ = __model__.country_names

def run_experiment(nsteps = 10):
    ref_country = get_country(__reference_country__)
    print "Reference country: %s" % ref_country.name
    initial_vector = rc.reference_vector(ref_country).copy()
    t_range = np.linspace(0, 1, nsteps)
    results = []
    baseline_metric = rc.country_metric(ref_country)
    print "Baseline metric: %i" % baseline_metric
    for c in __countries__:
        if c != ref_country.name:
            other_country = get_country(c)
            u = rc.reference_vector(ref_country)
            v = rc.reference_vector(other_country)
            alpha = rc.angle_between(u, v)
            for t in t_range:
                # Do the rotation
                rc.rotate_country(ref_country, other_country, t * alpha)
                __model__.recalculate_world()
                metric = rc.country_metric(ref_country)
                # Log the results
                result = {}
                result['ref_country'] = ref_country.name
                result['other_country'] = other_country.name
                result['alpha'] = alpha
                result['t'] = t
                result['metric'] = metric
                result['baseline_metric'] = baseline_metric
                results.append(result)
                print "Other country %s. t = %.1f. Metric: %i" \
                    % (other_country.name, t, metric)
                # Rotate back
                rc.set_reference_vector(ref_country, initial_vector)
        # Leave things as we found them
        __model__.recalculate_world()
    return pd.DataFrame(results)                
        
def get_country(country_name):
    return __model__.countries[country_name]
    
results = run_experiment()
results.to_csv('rotationsweep_%s.csv' % __reference_country__, index=False)