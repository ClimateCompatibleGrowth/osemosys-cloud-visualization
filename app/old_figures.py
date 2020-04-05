import os
from app.calculations import *
from app.utilities import df_plot, det_col, df_years
import pandas as pd
from app.land_use import LandUse
from app.constants import agg_col
pd.set_option('mode.chained_assignment', None)


def fig11b(all_params, years, land_use, each_region):
    regions = land_use.regions()
    mode_crop_combo = land_use.mode_crop_combo()
    crops_region_df = calculate_crops_total_df(all_params, years)
    crops_region_df = crops_region_df[crops_region_df.t.str[6:9] == each_region]

    crops_region_df['m'] = crops_region_df['m'].astype(int)
    crops_region_df['crop_combo'] = crops_region_df['m'].map(mode_crop_combo)
    crops_region_df['land_use'] = crops_region_df['crop_combo'].str[0:4]
    crops_region_df.drop(['m', 'crop_combo'], axis=1, inplace=True)

    crops_region_df = crops_region_df[crops_region_df['land_use'].str.startswith('CP')]
    crops_region_df = crops_region_df.pivot_table(index='y',
                                                  columns='land_use',
                                                  values='value',
                                                  aggfunc='sum').reset_index().fillna(0)
    crops_region_df = crops_region_df.reindex(
        sorted(
            crops_region_df.columns),
        axis=1).set_index('y').reset_index().rename(
            columns=det_col).astype('float64')
    crops_region_df = df_years(crops_region_df, years)
    return df_plot(crops_region_df, 'Land area (1000 sq.km.)',
                   'Area by crop (' + regions[each_region] + ' region)')


def fig12b(all_params, years, land_use, each_region):
    regions = land_use.regions()
    mode_crop_combo = land_use.mode_crop_combo()
    crops = land_use.crops()
    land_cluster_df = calculate_land_total_df(all_params, years)
    land_cluster_df = land_cluster_df[land_cluster_df.t.str[6:9] == each_region]

    land_cluster_df['m'] = land_cluster_df['m'].astype(int)
    land_cluster_df['crop_combo'] = land_cluster_df['m'].map(mode_crop_combo)
    land_cluster_df['land_use'] = land_cluster_df['crop_combo'].str[0:4]
    land_cluster_df.drop(['m', 'crop_combo'], axis=1, inplace=True)

    land_cluster_df['value'] = land_cluster_df['value'].astype('float64')
    land_cluster_df = land_cluster_df.pivot_table(index='y',
                                                  columns='land_use',
                                                  values='value',
                                                  aggfunc='sum').reset_index().fillna(0)
    land_cluster_df['AGR'] = 0

    for crop in crops:
        if crop in land_cluster_df.columns:
            land_cluster_df['AGR'] += land_cluster_df[crop]
            land_cluster_df.drop(crop, axis=1, inplace=True)

    land_cluster_df = land_cluster_df.reindex(
        sorted(
            land_cluster_df.columns),
        axis=1).set_index('y').reset_index().rename(
            columns=det_col)
    return df_plot(land_cluster_df, 'Land area (1000 sq.km.)',
                   'Area by land cover type (' + regions[each_region] + ' region)')

# def fig11c(all_params,years,each_ws):
#     crops_ws_df = calculate_crops_total_df(all_params,years)
#     crops_ws_df['m'] = crops_ws_df['m'].astype(int)
#     crops_ws_df['crop_combo'] = crops_ws_df['m'].map(mode_crop_combo)
#     crops_ws_df = crops_ws_df[(crops_ws_df.crop_combo.str.startswith('CP')) & (crops_ws_df.crop_combo.str[5:6] == each_ws)]
#     crops_ws_df['land_use'] = crops_ws_df['crop_combo'].str[0:4]
#     crops_ws_df.drop(['m','crop_combo'], axis=1, inplace=True)

#     crops_ws_df = crops_ws_df.pivot_table(index='y',
#                                           columns='land_use',
#                                           values='value',
#                                           aggfunc='sum').reset_index().fillna(0)
#     crops_ws_df = crops_ws_df.reindex(sorted(crops_ws_df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
# return df_plot(crops_ws_df,'Land area (1000 sq.km.)','Area by crop (' +
# water_supply[each_ws] + ')')
