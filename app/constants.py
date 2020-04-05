import os
import pandas as pd

# List of columns for aggregated energy tables and figures
agg_col = {'Coal': ['Coal'],
           'Oil': ['Diesel', 'HFO', 'JFL', 'Crude oil', 'Petroleum coke'],
           'Gas': ['Natural gas', 'LNG', 'LPG'],
           'Hydro': ['Hydro'],
           'Nuclear': ['Nuclear'],
           'Other renewables': ['Biomass', 'Geothermal', 'Solar', 'MSW', 'Wind'],
           'Net electricity imports': ['Net electricity imports']
           }

name_color_codes = pd.read_csv(
        os.path.join(os.getcwd(), 'name_color_codes.csv'),
        encoding='latin-1')
det_col = dict([(c, n) for c, n in zip(name_color_codes.code, name_color_codes.name_english)])
