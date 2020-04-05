from app.utilities import df_plot, df_filter, det_col


def calculate_crops_total_df(all_params, years):
    crops_total_df = all_params['TotalAnnualTechnologyActivityByMode'][all_params['TotalAnnualTechnologyActivityByMode'].t.str.startswith(
        'LNDAGR')].drop('r', axis=1)
    return crops_total_df


def calculate_land_total_df(all_params, years):
    land_total_df = all_params['TotalAnnualTechnologyActivityByMode'][all_params['TotalAnnualTechnologyActivityByMode'].t.str.startswith(
        'LNDAGR')].drop('r', axis=1)
    return land_total_df


def calculate_crops_prod_df(all_params, years):
    crops_prod_df = all_params['ProductionByTechnologyAnnual'][all_params['ProductionByTechnologyAnnual'].f.str.startswith(
        'CRP')].drop('r', axis=1)
    crops_prod_df['f'] = crops_prod_df['f'].str[3:7]
    crops_prod_df['value'] = crops_prod_df['value'].astype('float64')

    crops_prod_df = crops_prod_df.pivot_table(index='y',
                                              columns='f',
                                              values='value',
                                              aggfunc='sum').reset_index().fillna(0)
    crops_prod_df = crops_prod_df.reindex(sorted(crops_prod_df.columns), axis=1).set_index(
        'y').reset_index().rename(columns=det_col)
    crops_prod_df['y'] = years
    return crops_prod_df


def calculate_yield_df(all_params, years, land_use):
    mode_crop_combo = land_use.mode_crop_combo()
    crops_total_df = all_params['TotalAnnualTechnologyActivityByMode'][all_params['TotalAnnualTechnologyActivityByMode'].t.str.startswith(
        'LNDAGR')].drop('r', axis=1)
    crops_total_df['m'] = crops_total_df['m'].astype(int)
    crops_total_df['crop_combo'] = crops_total_df['m'].map(mode_crop_combo)
    crops_total_df['land_use'] = crops_total_df['crop_combo'].str[0:4]
    crops_total_df.drop(['m', 'crop_combo'], axis=1, inplace=True)

    crops_total_df = crops_total_df[crops_total_df['land_use'].str.startswith('CP')]
    crops_total_df = crops_total_df.pivot_table(index='y',
                                                columns='land_use',
                                                values='value',
                                                aggfunc='sum').reset_index().fillna(0)
    crops_total_df = crops_total_df.reindex(sorted(crops_total_df.columns), axis=1).set_index(
        'y').reset_index().rename(columns=det_col).astype('float64')

    crops_yield_df = calculate_crops_prod_df(all_params, years) / crops_total_df
    return crops_yield_df
