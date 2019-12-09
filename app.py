import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output

import pandas as pd
#import numpy as np
from IPython.display import HTML
import IPython.core.display as di
#import ipywidgets as widgets
#from ipywidgets import interact, interact_manual

#importing plotly and cufflinks in offline mode
import plotly as py
#import plotly.graph_objs as go
import cufflinks
import plotly.offline as pyo
from plotly.offline import plot, iplot, init_notebook_mode
pyo.init_notebook_mode(connected=False)
cufflinks.go_offline()
cufflinks.set_config_file(world_readable=True, theme='white')
import os, sys
import subprocess
from tkinter import filedialog
from tkinter import *
from collections import defaultdict

import wget
from zipfile import ZipFile


# In[10]:

# url = 'http://osemosys-cloud.herokuapp.com/rails/active_storage/blobs/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBbXNDIiwiZXhwIjpudWxsLCJwdXIiOiJibG9iX2lkIn19--39b1f7c7ec068e24ea2346626293cc4ab41629d8/csv_160.zip?disposition=attachment'
all_figures = {}
def setup_app(url):
    wget.download(url, 'myCsv.zip')
    zip_path = os.path.join(os.getcwd(), 'myCsv.zip')
    with ZipFile(zip_path, 'r') as zipObj:
        zipObj.extractall('myCsv')

    results_path = os.path.join(os.getcwd(), 'myCsv/csv/')
    # results_path = os.path.join(os.getcwd(), 'res/csv/')

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

    name_color_codes = pd.read_csv(os.path.join(os.getcwd(),'name_color_codes.csv'), encoding='latin-1')
    det_col = dict([(c,n) for c,n in zip(name_color_codes.code, name_color_codes.name_english)])
    color_dict = dict([(n,c) for n,c in zip(name_color_codes.name_english, name_color_codes.colour)])

    # List of columns for aggregated energy tables and figures
    agg_col = {'Coal':['Coal'],
            'Oil': ['Diesel','HFO','JFL','Crude oil','Petroleum coke'],
            'Gas': ['Natural gas','LNG','LPG'],
            'Hydro': ['Hydro'],
            'Nuclear': ['Nuclear'],
            'Other renewables': ['Biomass','Geothermal','Solar','MSW','Wind'],
            'Net electricity imports': ['Net electricity imports']
            }

    def df_filter(df,lb,ub,t_exclude):
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

    def df_plot(df,y_title,p_title):
        return df.iplot(asFigure=True,
                x='y',
                kind='bar',
                barmode='stack',
                xTitle='Year',
                yTitle=y_title,
                color=[color_dict[x] for x in df.columns if x != 'y'],
                title=p_title,
                showlegend=True)


        """ def df_filter(df,lb,ub,t_exclude):
        df['t'] = df['t'].str[lb:ub]
        df['value'] = df['value'].astype('float64')
        df = df[~df['t'].isin(t_exclude)].pivot_table(index='y',
                                              columns='t',
                                              values='value',
                                              aggfunc='sum').reset_index().fillna(0)
        df = df.reindex(sorted(df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
        df['y'] = years
        return df

    def df_plot(df,y_title,p_title):
       return df.iplot(asFigure=True,
                       x='y',
                       kind='bar',
                       barmode='stack',
                       xTitle='Year',
                       yTitle=y_title,
                       color=[color_dict[x] for x in df.columns if x != 'y'],
                       title=p_title) """


    # ## Energy figures
    # This section contains figures related to specifically to the energy sector. The list of figures in this section are as follows:
    # 1. Power generation capacity (detailed)
    # 2. Power generation capacity (aggregated)
    # 3. Power generation (detailed)
    # 4. Power generation (aggregated)

    # ### Power generation capacity

    # In[15]:


    # Power generation capacity (detailed)
    cap_df = all_params['TotalCapacityAnnual'][all_params['TotalCapacityAnnual'].t.str.startswith('PWR')].drop('r', axis=1)
    cap_df = df_filter(cap_df,3,6,['CNT','TRN','CST','CEN','SOU','NOR'])
    all_figures['fig1'] = df_plot(cap_df,'Gigawatts (GW)','Power Generation Capacity (Detail)')


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
    all_figures['fig2']= df_plot(cap_agg_df,'Gigawatts (GW)','Power Generation Capacity (Aggregate)')

    #Power generation (Detailed)
    gen_df = all_params['ProductionByTechnologyAnnual'][all_params['ProductionByTechnologyAnnual'].t.str.startswith('PWR') &
                                                       all_params['ProductionByTechnologyAnnual'].f.str.startswith('ELC001')].drop('r', axis=1)
    gen_df = df_filter(gen_df,3,6,['TRN'])
    all_figures['fig3'] = df_plot(gen_df,'Petajoules (PJ)','Power Generation (Detail)')


    # In[18]:


    # Power generation (Aggregated)
    gen_agg_df = pd.DataFrame(columns=agg_col)
    gen_agg_df.insert(0,'y',gen_df['y'])
    gen_agg_df  = gen_agg_df.fillna(0.00)

    for each in agg_col:
        for tech_exists in agg_col[each]:
            if tech_exists in gen_df.columns:
                gen_agg_df[each] = gen_agg_df[each] + gen_df[tech_exists]
                gen_agg_df[each] = gen_agg_df[each].round(2)

    all_figures['fig4'] = df_plot(gen_agg_df,'Petajoules (PJ)','Power Generation (Aggregate)')


    # In[19]:


    # Fuel use for power generation
    gen_use_df = all_params['ProductionByTechnologyAnnual'][all_params['ProductionByTechnologyAnnual'].t.str.startswith('DEMPWR')].drop('r', axis=1)
    gen_use_df = df_filter(gen_use_df,6,9,[])
    all_figures['fig5'] = df_plot(gen_use_df,'Petajoules (PJ)','Power Generation (Fuel use)')


    # In[20]:


    #Domestic fuel production
    fuels = ['OHC', 'GSL','DSL','LPG', 'JFL','HFO','NGS']

    dom_prd_df = all_params['ProductionByTechnologyAnnual'][all_params['ProductionByTechnologyAnnual'].t.str.startswith('MIN')|
                                                           all_params['ProductionByTechnologyAnnual'].t.str.startswith('RNW')].drop('r', axis=1)
    dom_prd_df = df_filter(dom_prd_df,3,6,[])

    for each in dom_prd_df.columns:
        if each in ['Land','Water','Geothermal','Hydro','Solar','Wind']:
            dom_prd_df = dom_prd_df.drop(each, axis=1)
    all_figures['fig6']  = df_plot(dom_prd_df,'Petajoules (PJ)','Domestic energy production')


    # In[21]:


    #Energy imports
    ene_imp_df = all_params['ProductionByTechnologyAnnual'][all_params['ProductionByTechnologyAnnual'].t.str.startswith('IMP')].drop('r', axis=1)
    ene_imp_df = df_filter(ene_imp_df,3,6,[])
    if len(ene_imp_df.columns) > 1:
        df_plot(ene_imp_df,'Petajoules (PJ)','Energy imports')


    # In[22]:


    #Energy exports
    ene_exp_df = all_params['TotalTechnologyAnnualActivity'][all_params['TotalTechnologyAnnualActivity'].t.str.startswith('EXP')].drop('r', axis=1)
    ene_exp_df = df_filter(ene_exp_df,3,6,[])
    if len(ene_exp_df.columns) > 1:
        df_plot(ene_exp_df,'Petajoules (PJ)','Energy exports')

    # In[23]:
    cap_cos_df = all_params['CapitalInvestment'][all_params['CapitalInvestment'].t.str.startswith('PWR')].drop('r', axis=1)
    cap_cos_df = df_filter(cap_cos_df,3,6,['TRN'])
    all_figures['fig7'] = df_plot(cap_cos_df,'Million $','Capital Investment')

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

    # In[25]:
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
    fix_cos_df = df_filter(fix_cos_df,3,6,['TRN'])

    var_cos_df = all_params['AnnualVariableOperatingCost'][all_params['AnnualVariableOperatingCost'].t.str.startswith('PWR')].drop('r', axis=1)
    var_cos_df = df_filter(var_cos_df,3,6,['TRN'])

    dis_cos_df = all_params['AnnualVariableOperatingCost'][all_params['AnnualVariableOperatingCost'].t.str.startswith('DEMPWR')].drop('r', axis=1)
    dis_cos_df = df_filter(dis_cos_df,6,9,[])

    dom_val_df = all_params['AnnualVariableOperatingCost'][all_params['AnnualVariableOperatingCost'].t.str.startswith('MIN')|
                                                           all_params['AnnualVariableOperatingCost'].t.str.startswith('RNW')].drop('r', axis=1)
    dom_val_df = df_filter(dom_val_df,3,6,[])
    for each in dom_val_df.columns:
        if each in ['Land','Water','Geothermal','Hydro','Solar','Wind']:
            dom_val_df = dom_val_df.drop(each, axis=1)

    imp_val_df = all_params['AnnualVariableOperatingCost'][all_params['AnnualVariableOperatingCost'].t.str.startswith('IMP')].drop('r', axis=1)
    imp_val_df = df_filter(imp_val_df,3,6,[])

    exp_val_df = all_params['AnnualVariableOperatingCost'][all_params['AnnualVariableOperatingCost'].t.str.startswith('EXP')].drop('r', axis=1)
    exp_val_df = df_filter(exp_val_df,3,6,[])

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
        #df['Diesel'] = df['Crude oil'].mul(0.3755) + df['Diesel']
        #df['HFO'] = df['Crude oil'].mul(0.0171) + df['HFO']
        #df.drop('Crude oil', axis=1, inplace=True)

        df['Diesel'] = df['Diesel']
        df['HFO'] = df['HFO']
        #df.drop('Crude oil', axis=1, inplace=True)

    fue_cos_df = pd.DataFrame(columns=list(set(temp_col_list)))
    fue_cos_df['y'] = years

    fue_cos_df = (fue_val_df/fue_prd_df)*gen_use_df
    fue_cos_df = fue_cos_df.fillna(0)
    fue_cos_df = fue_cos_df.reindex(sorted(fue_cos_df.columns),axis=1).set_index('y').reset_index()
    fue_cos_df['y'] = years

    ele_cos_df['Electricity generation'] = gen_df.iloc[:,1:].sum(axis=1)/3.6
    ele_cos_df['Capital costs'] = ele_cos_df['Capital costs']/ele_cos_df['Electricity generation']
    ele_cos_df['Fixed costs'] = fix_cos_df.iloc[:,1:].sum(axis=1)/ele_cos_df['Electricity generation']
    ele_cos_df['Variable costs'] = var_cos_df.iloc[:,1:].sum(axis=1)/ele_cos_df['Electricity generation']
    ele_cos_df['Fuel distribution costs'] = dis_cos_df.iloc[:,1:].sum(axis=1)/ele_cos_df['Electricity generation']
    ele_cos_df['Fuel costs'] = fue_cos_df.iloc[:,1:].sum(axis=1)/ele_cos_df['Electricity generation']
    # In[30]:
    ele_cos_df.drop('Electricity generation',axis=1,inplace=True)

    # In[31]:
    all_figures['fig10'] = ele_cos_df.iplot(asFigure=True, kind='bar',barmode='stack',x='y',title='Cost of electricity generation ($/MWh)')

setup_app(sys.argv[1])
##################################################################################################
#colors = {'background': '#111111', 'text': '#7FDBFF'}
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#app.css.config.serve_locally = True
#app.scripts.config.serve_locally = True

app.layout = html.Div(children=[
    html.Div('Data-*', **{'id': 'abc', 'data-run-id': 12}),
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
    html.Div(children=dcc.Graph(
                id='example-graph-1',
                figure=all_figures['fig1']
    ), style={'width':'50%','display':'inline-block'}),
    html.Div(children=dcc.Graph(
                id='example-graph-2',
                figure=all_figures['fig2']
    ), style={'width':'50%','display':'inline-block'}),
    html.Div(children=dcc.Graph(
                id='example-graph-3',
                figure=all_figures['fig3']
    ), style={'width':'50%','display':'inline-block'}),
    html.Div(children=dcc.Graph(
                id='example-graph-4',
                figure=all_figures['fig4']
    ), style={'width':'50%','display':'inline-block'}),
    html.Div(children=dcc.Graph(
                id='example-graph-5',
                figure=all_figures['fig5']
    ), style={'width':'50%','display':'inline-block'}),
    html.Div(children=dcc.Graph(
                id='example-graph-6',
                figure=all_figures['fig6']
    ), style={'width':'50%','display':'inline-block'}),
    html.Div(children=dcc.Graph(
                id='example-graph-10',
                figure=all_figures['fig10']
    ), style={'width':'50%','display':'inline-block'}),
])

@app.callback(
    Output(component_id='abc', component_property='data-output'),
    [Input(component_id='abc', component_property='data-run-id')]
)
def my_callback(input_value):
    print(input_value)

if __name__ == '__main__':
    app.run_server(debug=True)
