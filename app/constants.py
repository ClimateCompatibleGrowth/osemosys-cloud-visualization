import os
import pandas as pd

# List of columns for aggregated energy tables and figures
agg_col = {'Coal': ['Coal'],
           'Oil': ['Diesel', 'HFO', 'JFL', 'Crude oil', 'Petroleum coke'],
           'Gas': ['Natural gas', 'LNG', 'LPG', 'Gas'],
           'Hydro': ['Hydro'],
           'Nuclear': ['Nuclear'],
           'Other renewables': ['Biomass', 'Geothermal', 'Solar', 'MSW', 'Wind'],
           'Net electricity imports': ['Net electricity imports'],
           'Electricity exports': ['Electricity exports'],
           }

name_color_codes = pd.read_csv(
        os.path.join(os.getcwd(), 'name_color_codes.csv'),
        encoding='latin-1')

global det_col
global color_dict
det_col = None
color_dict = None

def set_cols_from_language(language):
    global det_col
    global color_dict
    if language == 'es':
        det_col = dict([(c, n) for c, n in zip(name_color_codes.code, name_color_codes.name_english)])
        color_dict = dict([(n, c) for n, c in zip(name_color_codes.name_english, name_color_codes.colour)])
    else:
        det_col = dict([(c, n) for c, n in zip(name_color_codes.code, name_color_codes.name_english)])
        color_dict = dict([(n, c) for n, c in zip(name_color_codes.name_english, name_color_codes.colour)])
    # import pdb; pdb.set_trace()
