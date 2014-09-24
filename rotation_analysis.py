# -*- coding: utf-8 -*-
"""
Created on Fri Sep 19 17:51:08 2014

@author: rob
"""

import pandas as pd
import rotatecountry
import matplotlib.pyplot as plt
from matplotlib import cm

results = pd.read_csv('rotation_results.csv')

#%%
print('Which countries would benefit from consuming like the most people?')
print results[results.delta < 0].groupby('base_country').delta \
    .count().order(ascending=False).head(20)
#base_country
#TUR             38
#LTU             37
#RUS             36
#MLT             32
#SVK             29
#HUN             29
#IND             26
#SVN             25
#ROU             24
#CAN             23
#MEX             22
#CZE             22
#PRT             20
#POL             20
#BGR             18
#DEU             17
#ITA             17
#BRA             16
#EST             16
#FRA             15
    
#%%
print ('Which is the most popular country to consume like?')
print results[results.delta < 0].groupby('country').delta \
    .count().order(ascending=False).head(20)
#USA        37
#JPN        36
#DNK        35
#NLD        29
#GBR        28
#FIN        27
#LVA        26
#SWE        26
#LUX        26
#BEL        25
#CYP        25
#AUS        23
#KOR        22
#AUT        20
#ESP        18
#IRL        17
#EST        16
#FRA        15
#GRC        15
#ITA        13

#%%
print "Which country scores the most number ones?"
results = results.set_index(['base_country', 'country'])
results['delta_rank'] = results.delta.groupby(level='base_country') \
    .transform(pd.Series.rank)
print results.delta_rank[results.delta_rank == 1] \
    .groupby(level='country').count().order(ascending=False)
#country
#DNK        14
#JPN        10
#USA         6
#LVA         6
#NLD         1
#CYP         1
#CHN         1
#AUS         1
#%%
# Plot improves vs improved by
improves_count = results.delta[results.delta < 0] \
    .groupby(level='country').count()
improves_count.name = 'improves'
improved_by_count = results.delta[results.delta < 0] \
    .groupby(level='base_country').count()
improved_by_count.name = 'improved_by'
country_summary = \
    pd.concat([improves_count, improved_by_count], axis=1).fillna(0)
fig, ax = plt.subplots()
cmap = cm.get_cmap('Spectral')
country_summary.plot('improves', 'improved_by', kind='scatter',
    ax=ax, c=range(len(country_summary)),
    colormap=cmap, s=120, alpha=0.8,
    linewidth=0)
for k, v in country_summary.iterrows():
    ax.annotate(k, v,
                xytext=(10,-5), textcoords='offset points',
                family='sans-serif', fontsize=14, color='darkslategrey')