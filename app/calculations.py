from app.utilities import df_plot, df_filter, det_col


def calculate_crops_total_df(all_params, years):
    crops_total_df = all_params['TotalAnnualTechnologyActivityByMode'][all_params['TotalAnnualTechnologyActivityByMode'].t.str.startswith(
        'LNDAGR')].drop('r', axis=1)
    return crops_total_df


def calculate_land_total_df(all_params, years):
    land_total_df = all_params['TotalAnnualTechnologyActivityByMode'][all_params['TotalAnnualTechnologyActivityByMode'].t.str.startswith(
        'LNDAGR')].drop('r', axis=1)
    return land_total_df
