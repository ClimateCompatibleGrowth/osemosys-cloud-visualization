import os
from app.calculations import *
from app.utilities import df_plot, det_col, df_years
import pandas as pd
from app.land_use import LandUse
from app.constants import agg_col
pd.set_option('mode.chained_assignment', None)


def fig6(all_params, years):
    # Domestic fuel production

    dom_prd_df = calculate_dom_prd_df(all_params, years)
    for each in dom_prd_df.columns:
        if each in ['Land', 'Water', 'Precipitation']:
            dom_prd_df = dom_prd_df.drop(each, axis=1)
    return df_plot(dom_prd_df, 'Petajoules (PJ)', 'Domestic energy production')


def fig7(all_params, years):
    cap_cos_df = calculate_cap_cos_df(all_params, years)
    return df_plot(cap_cos_df, 'Million $', 'Capital Investment')


def fig8(all_params, years):
    ene_imp_df = calculate_ene_imp_df(all_params, years)
    return df_plot(ene_imp_df, 'Petajoules (PJ)', 'Energy imports')


def fig9(all_params, years):
    ene_exp_df = calculate_ene_exp_df(all_params, years)
    return df_plot(ene_exp_df, 'Petajoules (PJ)', 'Energy exports')


def fig10(all_params, years):
    ele_cos_df = calculate_ele_cos_df(all_params, years)

    return ele_cos_df.iplot(asFigure=True, kind='bar', barmode='stack',
                            x='y', title='Cost of electricity generation ($/MWh)')


def fig11a(all_params, years, land_use):
    mode_crop_combo = land_use.mode_crop_combo()
    crops_total_df = calculate_crops_total_df(all_params, years)
    crops_total_df['m'] = crops_total_df['m'].astype(int)
    crops_total_df['crop_combo'] = crops_total_df['m'].map(mode_crop_combo)
    crops_total_df['land_use'] = crops_total_df['crop_combo'].str[0:4]
    crops_total_df.drop(['m', 'crop_combo'], axis=1, inplace=True)

    crops_total_df = crops_total_df[crops_total_df['land_use'].str.startswith('CP')]
    crops_total_df = crops_total_df.pivot_table(index='y',
                                                columns='land_use',
                                                values='value',
                                                aggfunc='sum').reset_index().fillna(0)
    crops_total_df = crops_total_df.reindex(
        sorted(
            crops_total_df.columns),
        axis=1).set_index('y').reset_index().rename(
            columns=det_col).astype('float64')
    return df_plot(crops_total_df, 'Land area (1000 sq.km.)', 'Area by crop')


def fig12a(all_params, years, land_use):
    mode_crop_combo = land_use.mode_crop_combo()
    crops = land_use.crops()
    land_total_df = calculate_land_total_df(all_params, years)
    land_total_df['m'] = land_total_df['m'].astype(int)
    land_total_df['crop_combo'] = land_total_df['m'].map(mode_crop_combo)
    land_total_df['land_use'] = land_total_df['crop_combo'].str[0:4]
    land_total_df.drop(['m', 'crop_combo'], axis=1, inplace=True)

    land_total_df = land_total_df.pivot_table(index='y',
                                              columns='land_use',
                                              values='value',
                                              aggfunc='sum').reset_index().fillna(0)
    land_total_df['AGR'] = 0

    for crop in crops:
        if crop in land_total_df.columns:
            land_total_df['AGR'] += land_total_df[crop]
            land_total_df.drop(crop, axis=1, inplace=True)
    land_total_df = land_total_df.reindex(
        sorted(
            land_total_df.columns),
        axis=1).set_index('y').reset_index().rename(
            columns=det_col).astype('float64')
    return df_plot(land_total_df, 'Land area (1000 sq.km.)', 'Area by land cover type')


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


def fig13(all_params, years):
    crops_prod_df = calculate_crops_prod_df(all_params, years)
    return df_plot(crops_prod_df, 'Production (Million tonnes)', 'Crop production')


def fig14(all_params, years, land_use):
    crops_yield_df = calculate_yield_df(all_params, years, land_use)
    crops_yield_df['y'] = years
    crops_yield_df = crops_yield_df.mul(10)
    name_color_codes = pd.read_csv(
        os.path.join(
            os.getcwd(),
            'name_color_codes.csv'),
        encoding='latin-1')
    color_dict = dict([(n, c)
                       for n, c in zip(name_color_codes.name_english, name_color_codes.colour)])
    return crops_yield_df.iplot(asFigure=True,
                                x='y',
                                mode='lines+markers',
                                xTitle='Year',
                                yTitle='Yield (t/ha)',
                                size=10,
                                color=[color_dict[x] for x in crops_yield_df.columns if x != 'y'],
                                title='Yield (tonnes/hectare)',
                                showlegend=True)
