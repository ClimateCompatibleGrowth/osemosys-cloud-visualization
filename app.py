from collections import defaultdict
from dash.dependencies import Input, Output
from plotly.offline import plot, iplot, init_notebook_mode
from zipfile import ZipFile
import IPython.core.display as di
import cufflinks
import dash
import dash_core_components as dcc
import dash_html_components as html
import os, sys
import pandas as pd
import plotly as py
import plotly.offline as pyo
import subprocess
import wget
import json
import random
import urllib
pyo.init_notebook_mode(connected=False)
cufflinks.go_offline()
cufflinks.set_config_file(world_readable=True, theme='white')

# url = 'http://osemosys-cloud.herokuapp.com/rails/active_storage/blobs/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBbXNDIiwiZXhwIjpudWxsLCJwdXIiOiJibG9iX2lkIn19--39b1f7c7ec068e24ea2346626293cc4ab41629d8/csv_160.zip?disposition=attachment'

name_color_codes = pd.read_csv(os.path.join(os.getcwd(),'name_color_codes.csv'), encoding='latin-1')
det_col = dict([(c,n) for c,n in zip(name_color_codes.code, name_color_codes.name_english)])

# List of columns for aggregated energy tables and figures
agg_col = {'Coal':['Coal'],
        'Oil': ['Diesel','HFO','JFL','Crude oil','Petroleum coke'],
        'Gas': ['Natural gas','LNG','LPG'],
        'Hydro': ['Hydro'],
        'Nuclear': ['Nuclear'],
        'Other renewables': ['Biomass','Geothermal','Solar','MSW','Wind'],
        'Net electricity imports': ['Net electricity imports']
        }

def df_plot(df,y_title,p_title):
    color_dict = dict([(n,c) for n,c in zip(name_color_codes.name_english, name_color_codes.colour)])
    return df.iplot(asFigure=True,
            x='y',
            kind='bar',
            barmode='stack',
            xTitle='Year',
            yTitle=y_title,
            color=[color_dict[x] for x in df.columns if x != 'y'],
            title=p_title,
            showlegend=True)

def download_files(url):
    random_number = random.randint(1,99999)
    zip_file_name = f'csv_{random_number}.zip'
    folder_name = f'csv_{random_number}'
    wget.download(url, zip_file_name)
    zip_path = os.path.join(os.getcwd(), zip_file_name)
    with ZipFile(zip_path, 'r') as zipObj:
        zipObj.extractall(folder_name)
    return os.path.join(os.getcwd(), f'{folder_name}/csv/')

def df_filter(df,lb,ub,t_exclude,years):
    df['t'] = df['t'].str[lb:ub]
    df['value'] = df['value'].astype('float64')
    df = df[~df['t'].isin(t_exclude)].pivot_table(index='y',
            columns='t',
            values='value',
            aggfunc='sum').reset_index().fillna(0)
    df = df.reindex(sorted(df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
    new_df = pd.DataFrame()
    new_df['y'] = years
    new_df['y'] = new_df['y'].astype(int)
    df['y'] = df['y'].astype(int)
    new_df = pd.merge(new_df,df, how='outer', on='y').fillna(0)
    return new_df

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

 

def setup_app(url):
    all_figures = {}

    results_path = download_files(url)

    all_params = {}
    df_y_min = 9999
    df_y_max = 0

    for each_file in os.listdir(results_path):
        df_param = pd.read_csv(os.path.join(results_path, each_file))
        param_name = df_param.columns[-1]
        df_param.rename(columns={param_name:'value'}, inplace=True)
        all_params[param_name] = pd.DataFrame(df_param)
        if 'y' in df_param.columns:
            if df_y_min > df_param.y.min():
                df_y_min = df_param.y.min()
            if df_y_max < df_param.y.max():
                df_y_max = df_param.y.max()

    years = pd.Series(list(range(df_y_min,df_y_max)))

    # ## Energy figures
    # This section contains figures related to specifically to the energy sector. The list of figures in this section are as follows:
    # 1. Power generation capacity (detailed)
    # 2. Power generation capacity (aggregated)
    # 3. Power generation (detailed)
    # 4. Power generation (aggregated)

    all_figures['fig1'] = fig1(all_params,years)
    all_figures['fig2'] = fig2(all_params,years)
    all_figures['fig3'] = fig3(all_params,years)
    all_figures['fig4'] = fig4(all_params,years)
    all_figures['fig5'] = fig5(all_params,years)
    all_figures['fig6'] = fig6(all_params,years)
    all_figures['fig7'] = fig7(all_params,years)

    #Energy imports
    ene_imp_df = all_params['ProductionByTechnologyAnnual'][all_params['ProductionByTechnologyAnnual'].t.str.startswith('IMP')].drop('r', axis=1)
    ene_imp_df = df_filter(ene_imp_df,3,6,[], years)
    if len(ene_imp_df.columns) > 1:
        df_plot(ene_imp_df,'Petajoules (PJ)','Energy imports')

    #Energy exports
    ene_exp_df = all_params['TotalTechnologyAnnualActivity'][all_params['TotalTechnologyAnnualActivity'].t.str.startswith('EXP')].drop('r', axis=1)
    ene_exp_df = df_filter(ene_exp_df,3,6,[],years)
    if len(ene_exp_df.columns) > 1:
        df_plot(ene_exp_df,'Petajoules (PJ)','Energy exports')

    cap_cos_df = calculate_cap_cos_df(all_params, years)
    ele_cos_df = pd.DataFrame(columns=['Total capital investment', 'Capital costs'])
    ele_cos_df.insert(0,'y',years)
    ele_cos_df['Total capital investment'] = cap_cos_df.iloc[:,1:].sum(axis=1)
    ele_cos_df['Capital costs'] = 0
    ele_cos_df = ele_cos_df.fillna(0)

    R = 0.1 # Discount rate
    n = 30 # Amortization period
    cap_exist_total = 500 # Payments on existing capacity (legacy costs)


    for i in ele_cos_df['y']:
        for j in ele_cos_df['y']:
            if i < j + n and i >= j:
                ele_cos_df.loc[ele_cos_df['y']==i,'Capital costs'] = ele_cos_df.loc[ele_cos_df['y']==i,'Capital costs'] + (((ele_cos_df.loc[ele_cos_df['y']==j,'Total capital investment'].iloc[0])*R)/(1-(1+R)**(-n)))

    ele_cos_df.drop('Total capital investment', axis=1, inplace=True)

    cap_exist_values = {}

    start_year = min(years)

    for year in years:
        if cap_exist_total - ((cap_exist_total/n)*(year - int(start_year))) > 0:
            cap_exist_values[year] = cap_exist_total - ((cap_exist_total/n)*(year - int(start_year)))
        else:
            cap_exist_values[year] = 0

    ele_cos_df['Legacy costs'] = ele_cos_df['y'].map(cap_exist_values)
    ele_cos_df['Capital costs'] += ele_cos_df['Legacy costs']
    ele_cos_df = ele_cos_df.drop('Legacy costs', axis=1)

    fix_cos_df = all_params['AnnualFixedOperatingCost'][all_params['AnnualFixedOperatingCost'].t.str.startswith('PWR')].drop('r', axis=1)
    fix_cos_df = df_filter(fix_cos_df,3,6,['TRN'],years)

    var_cos_df = all_params['AnnualVariableOperatingCost'][all_params['AnnualVariableOperatingCost'].t.str.startswith('PWR')].drop('r', axis=1)
    var_cos_df = df_filter(var_cos_df,3,6,['TRN'],years)

    dis_cos_df = all_params['AnnualVariableOperatingCost'][all_params['AnnualVariableOperatingCost'].t.str.startswith('DEMPWR')].drop('r', axis=1)
    dis_cos_df = df_filter(dis_cos_df,6,9,[],years)

    dom_val_df = all_params['AnnualVariableOperatingCost'][all_params['AnnualVariableOperatingCost'].t.str.startswith('MIN')|
                                                           all_params['AnnualVariableOperatingCost'].t.str.startswith('RNW')].drop('r', axis=1)
    dom_val_df = df_filter(dom_val_df,3,6,[],years)
    for each in dom_val_df.columns:
        if each in ['Land','Water','Geothermal','Hydro','Solar','Wind']:
            dom_val_df = dom_val_df.drop(each, axis=1)

    imp_val_df = all_params['AnnualVariableOperatingCost'][all_params['AnnualVariableOperatingCost'].t.str.startswith('IMP')].drop('r', axis=1)
    imp_val_df = df_filter(imp_val_df,3,6,[],years)

    exp_val_df = all_params['AnnualVariableOperatingCost'][all_params['AnnualVariableOperatingCost'].t.str.startswith('EXP')].drop('r', axis=1)
    exp_val_df = df_filter(exp_val_df,3,6,[],years)

    temp_col_list = []
    temp_col_list = dom_val_df.columns

    if len(imp_val_df.columns) > 1:
        temp_col_list = temp_col_list.append(imp_val_df.columns)

    if len(exp_val_df.columns) > 1:
        temp_col_list = temp_col_list.append(exp_val_df.columns)

    fue_val_df = pd.DataFrame(columns=list(set(temp_col_list)))
    fue_val_df['y'] = years
    fue_val_df = fue_val_df.reindex(sorted(fue_val_df.columns),axis=1).set_index('y').reset_index()

    fue_val_df = fue_val_df.fillna(0)

    for each in dom_val_df.columns:
        if each != 'y':
            fue_val_df[each] = dom_val_df[each]
            fue_val_df = fue_val_df.fillna(0)

    for each in imp_val_df.columns :
        if each != 'y' and len(imp_val_df.columns) > 1:
            fue_val_df[each] = fue_val_df[each] + imp_val_df[each]
            fue_val_df = fue_val_df.fillna(0)

    for each in exp_val_df.columns:
        if each != 'y' and len(ene_exp_df.columns) > 1:
            fue_val_df[each] = fue_val_df[each] + exp_val_df[each]
            fue_val_df = fue_val_df.fillna(0)


    temp_col_list = []
    dom_prd_df = calculate_dom_prd_df(all_params, years)
    temp_col_list = dom_prd_df.columns
    if len(ene_imp_df.columns) > 1:
        temp_col_list = temp_col_list.append(ene_imp_df.columns)
    if len(ene_exp_df.columns) > 1:
        temp_col_list = temp_col_list.append(ene_exp_df.columns)

    fue_prd_df = pd.DataFrame(columns=list(set(temp_col_list)))
    fue_prd_df['y'] = years
    fue_prd_df = fue_prd_df.reindex(sorted(fue_prd_df.columns),axis=1).set_index('y').reset_index()

    fue_prd_df = fue_prd_df.fillna(0)

    for each in dom_prd_df.columns:
        if each != 'y':
            fue_prd_df[each] = dom_prd_df[each]
            fue_prd_df = fue_prd_df.fillna(0)

    for each in ene_imp_df.columns:
        if each != 'y' and len(ene_imp_df.columns) > 1:
            fue_prd_df[each] = fue_prd_df[each] + ene_imp_df[each]
            fue_prd_df = fue_prd_df.fillna(0)

    for each in ene_exp_df.columns:
        if each != 'y' and len(ene_exp_df.columns) > 1:
            fue_prd_df[each] = fue_prd_df[each] - ene_exp_df[each]
            fue_prd_df = fue_prd_df.fillna(0)


    for df in [fue_val_df, fue_prd_df]:
        df['Diesel'] = df['Diesel']
        df['HFO'] = df['HFO']

    fue_cos_df = pd.DataFrame(columns=list(set(temp_col_list)))
    fue_cos_df['y'] = years

    gen_use_df = calculate_gen_use_df(all_params, years)
    fue_cos_df = (fue_val_df/fue_prd_df)*gen_use_df
    fue_cos_df = fue_cos_df.fillna(0)
    fue_cos_df = fue_cos_df.reindex(sorted(fue_cos_df.columns),axis=1).set_index('y').reset_index()
    fue_cos_df['y'] = years

    gen_df = calculate_gen_df(all_params, years)
    ele_cos_df['Electricity generation'] = gen_df.iloc[:,1:].sum(axis=1)/3.6
    ele_cos_df['Capital costs'] = ele_cos_df['Capital costs']/ele_cos_df['Electricity generation']
    ele_cos_df['Fixed costs'] = fix_cos_df.iloc[:,1:].sum(axis=1)/ele_cos_df['Electricity generation']
    ele_cos_df['Variable costs'] = var_cos_df.iloc[:,1:].sum(axis=1)/ele_cos_df['Electricity generation']
    ele_cos_df['Fuel distribution costs'] = dis_cos_df.iloc[:,1:].sum(axis=1)/ele_cos_df['Electricity generation']
    ele_cos_df['Fuel costs'] = fue_cos_df.iloc[:,1:].sum(axis=1)/ele_cos_df['Electricity generation']
    ele_cos_df.drop('Electricity generation',axis=1,inplace=True)

    all_figures['fig10'] = ele_cos_df.iplot(asFigure=True, kind='bar',barmode='stack',x='y',title='Cost of electricity generation ($/MWh)')
    return all_figures

##################################################################################################
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(children=[
    html.Div('Data-*', **{'id': 'figures-component', 'data-url': ''}),
    dcc.Location(id='url', refresh=False),
    html.H1(
        'CLEWS Dashboard',
        style={
            'textAlign':'center'
        }
    ),

    html.Div(children='An interactive tool to visualise CLEWS model results', style={
        'textAlign':'center'
    }
    ),
    html.Div(children=[], id='figures-container'),
])

def div_from_figure(figure, number):
    return html.Div(
            children=dcc.Graph(
                id=f'example-graph-{number}',
                figure=figure
                ), 
            style={'width':'50%','display':'inline-block'}
            )

@app.callback(
    Output(component_id='figures-component', component_property='data-url'),
    [Input(component_id='url', component_property='search')]
    )
def setup_url(query_string):
    return urllib.parse.unquote(query_string).split('=')[-1]

@app.callback(
    Output(component_id='figures-container', component_property='children'),
    [Input(component_id='figures-component', component_property='data-url')]
    )
def generate_figures(url):
    all_figures = setup_app(url)
    figure_divs = []
    for number, figure in all_figures.items():
        figure_divs = figure_divs + [div_from_figure(figure, number)]
    return figure_divs

if __name__ == '__main__':
    app.run_server(debug=False)
