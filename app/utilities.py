import os
import sys
import pandas as pd
pd.set_option('mode.chained_assignment', None)
name_color_codes = pd.read_csv(
    os.path.join(
        os.getcwd(),
        'name_color_codes.csv'),
    encoding='latin-1')
det_col = dict([(c, n) for c, n in zip(name_color_codes.code, name_color_codes.name_english)])


def landuse():
    technologies = []
    commodities = []
    with open(os.path.join(os.getcwd(), 'data', 'indonesia', 'data.txt'), 'r') as f:
        for line in f:
            if line.startswith(('set TECHNOLOGY')):
                technologies = line.split(' ')[3:]
            if line.startswith(('set COMMODITY', 'set FUEL')):
                commodities = line.split(' ')[3:]

    # Construct dictionary mapping modes to crop combos {mode:crop_combo}
    crop_list = sorted(list(set([x[1:5] for x in commodities if x.startswith('LCP')])))
    crop_order = ['HI', 'II', 'HR', 'IR', 'LR']
    crop_combo = []

    for each_crop in crop_list:
        for each_combo in crop_order:
            crop_combo.append(each_crop + each_combo)

    for each in ['BAR', 'FOR', 'GRS', 'BLT', 'WAT', 'OTH']:
        crop_combo.append(each)

    mode_crop_combo = dict([(m, c) for m, c in zip(range(1, len(crop_combo) + 1), crop_combo)])

    # Construct dictionary of regions {region_code:region_name}.
    # Region codes are extracted from the data file
    regions_list = sorted(list(set([x[6:-3] for x in technologies if x.startswith('LNDAGR')])))
    regions = {}

    for each in regions_list:
        regions[each] = each

    # Construct dictionary of crops {crop_code:crop_name}.
    # Crop codes and names are extracted from the 'name_color_codes.csv' file
    crops = {}
    for each in det_col.keys():
        if each.startswith('CP'):
            crops[each] = det_col[each]

    # Dictionaries  of water supply and input level combinations
    water_supply = {'I': 'Irrigated',
                    'R': 'Rain-fed'}

    input_level = {'L': 'Low',
                   'I': 'Intermediate',
                   'H': 'High'}

    return regions, mode_crop_combo, crops, water_supply, input_level


def df_plot(df, y_title, p_title):
    color_dict = dict([(n, c)
                       for n, c in zip(name_color_codes.name_english, name_color_codes.colour)])
    return df.iplot(asFigure=True,
                    x='y',
                    kind='bar',
                    barmode='stack',
                    xTitle='Year',
                    yTitle=y_title,
                    color=[color_dict[x] for x in df.columns if x != 'y'],
                    title=p_title,
                    showlegend=True)


def df_years(df, years):
    new_df = pd.DataFrame()
    new_df['y'] = years
    new_df['y'] = new_df['y'].astype(int)
    df['y'] = df['y'].astype(int)
    new_df = pd.merge(new_df, df, how='outer', on='y').fillna(0)
    return new_df


def df_filter(df, lb, ub, t_exclude, years):
    df['t'] = df['t'].str[lb:ub]
    df['value'] = df['value'].astype('float64')
    df = df[~df['t'].isin(t_exclude)].pivot_table(index='y',
                                                  columns='t',
                                                  values='value',
                                                  aggfunc='sum').reset_index().fillna(0)
    df = df.reindex(sorted(df.columns), axis=1).set_index('y').reset_index().rename(columns=det_col)
    new_df = df_years(df, years)
    return new_df
