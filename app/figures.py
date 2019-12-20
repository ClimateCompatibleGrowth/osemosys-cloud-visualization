import pandas as pd
from utilities import df_plot
from calculations import calculate_cap_df, calculate_gen_df, calculate_gen_use_df, calculate_cap_cos_df, calculate_ene_imp_df, calculate_ene_exp_df, calculate_dom_prd_df

# List of columns for aggregated energy tables and figures
agg_col = {'Coal':['Coal'],
        'Oil': ['Diesel','HFO','JFL','Crude oil','Petroleum coke'],
        'Gas': ['Natural gas','LNG','LPG'],
        'Hydro': ['Hydro'],
        'Nuclear': ['Nuclear'],
        'Other renewables': ['Biomass','Geothermal','Solar','MSW','Wind'],
        'Net electricity imports': ['Net electricity imports']
        }

def fig1(all_params,years):
    # ### Power generation capacity
    # Power generation capacity (detailed)
    cap_df = calculate_cap_df(all_params, years)
    return df_plot(cap_df,'Gigawatts (GW)','Power Generation Capacity (Detail)')

def fig2(all_params, years):
    cap_df = calculate_cap_df(all_params, years)
    # Power generation capacity (Aggregated)
    cap_agg_df = pd.DataFrame(columns=agg_col)
    cap_agg_df.insert(0,'y',cap_df['y'])
    cap_agg_df  = cap_agg_df.fillna(0.00)

    for each in agg_col:
        for tech_exists in agg_col[each]:
            if tech_exists in cap_df.columns:
                cap_agg_df[each] = cap_agg_df[each] + cap_df[tech_exists]
                cap_agg_df[each] = cap_agg_df[each].round(2)

    cap_agg_df = cap_agg_df.loc[:,(cap_agg_df != 0).any(axis=0)]
    return df_plot(cap_agg_df,'Gigawatts (GW)','Power Generation Capacity (Aggregate)')

def fig3(all_params, years):
    gen_df = calculate_gen_df(all_params, years)
    return df_plot(gen_df,'Petajoules (PJ)','Power Generation (Detail)')

def fig4(all_params, years):
    gen_df = calculate_gen_df(all_params, years)
    # Power generation (Aggregated)
    gen_agg_df = pd.DataFrame(columns=agg_col)
    gen_agg_df.insert(0,'y',gen_df['y'])
    gen_agg_df  = gen_agg_df.fillna(0.00)

    for each in agg_col:
        for tech_exists in agg_col[each]:
            if tech_exists in gen_df.columns:
                gen_agg_df[each] = gen_agg_df[each] + gen_df[tech_exists]
                gen_agg_df[each] = gen_agg_df[each].round(2)
    return df_plot(gen_agg_df,'Petajoules (PJ)','Power Generation (Aggregate)')

def fig5(all_params, years):
    gen_use_df = calculate_gen_use_df(all_params, years)
    # Fuel use for power generation
    return df_plot(gen_use_df,'Petajoules (PJ)','Power Generation (Fuel use)')

def fig6(all_params, years):
    #Domestic fuel production

    dom_prd_df = calculate_dom_prd_df(all_params, years)
    for each in dom_prd_df.columns:
        if each in ['Land','Water','Geothermal','Hydro','Solar','Wind']:
            dom_prd_df = dom_prd_df.drop(each, axis=1)
    return df_plot(dom_prd_df,'Petajoules (PJ)','Domestic energy production')

def fig7(all_params, years):
    cap_cos_df = calculate_cap_cos_df(all_params, years)
    return df_plot(cap_cos_df,'Million $','Capital Investment')

def fig8(all_params, years):
    ene_imp_df = calculate_ene_imp_df(all_params, years)
    return df_plot(ene_imp_df,'Petajoules (PJ)','Energy imports')

def fig9(all_params, years):
    ene_exp_df = calculate_ene_exp_df(all_params, years)
    return df_plot(ene_exp_df,'Petajoules (PJ)','Energy exports')

