from utilities import df_plot, df_filter

def calculate_cap_df(all_params, years):
    cap_df = all_params['TotalCapacityAnnual'][all_params['TotalCapacityAnnual'].t.str.startswith('PWR')].drop('r', axis=1)
    return df_filter(cap_df,3,6,['CNT','TRN','CST','CEN','SOU','NOR'],years)

def calculate_gen_df(all_params, years):
    #Power generation (Detailed)
    gen_df = all_params['ProductionByTechnologyAnnual'][all_params['ProductionByTechnologyAnnual'].t.str.startswith('PWR') &
                                                       all_params['ProductionByTechnologyAnnual'].f.str.startswith('ELC001')].drop('r', axis=1)
    gen_df = df_filter(gen_df,3,6,['TRN'],years)
    return gen_df

def calculate_gen_use_df(all_params, years):
    gen_use_df = all_params['ProductionByTechnologyAnnual'][all_params['ProductionByTechnologyAnnual'].t.str.startswith('DEMPWR')].drop('r', axis=1)
    gen_use_df = df_filter(gen_use_df,6,9,[], years)
    return gen_use_df

def calculate_dom_prd_df(all_params, years):
    dom_prd_df = all_params['ProductionByTechnologyAnnual'][all_params['ProductionByTechnologyAnnual'].t.str.startswith('MIN')|
                                                           all_params['ProductionByTechnologyAnnual'].t.str.startswith('RNW')].drop('r', axis=1)
    return df_filter(dom_prd_df,3,6,[], years)

def calculate_cap_cos_df(all_params, years):
    cap_cos_df = all_params['CapitalInvestment'][all_params['CapitalInvestment'].t.str.startswith('PWR')].drop('r', axis=1)
    return df_filter(cap_cos_df,3,6,['TRN'],years)

def calculate_ene_imp_df(all_params, years):
    #Energy imports
    ene_imp_df = all_params['ProductionByTechnologyAnnual'][all_params['ProductionByTechnologyAnnual'].t.str.startswith('IMP')].drop('r', axis=1)
    return df_filter(ene_imp_df,3,6,[], years)

def calculate_ene_exp_df(all_params, years):
    #Energy exports
    ene_exp_df = all_params['TotalTechnologyAnnualActivity'][all_params['TotalTechnologyAnnualActivity'].t.str.startswith('EXP')].drop('r', axis=1)
    return df_filter(ene_exp_df,3,6,[],years)
