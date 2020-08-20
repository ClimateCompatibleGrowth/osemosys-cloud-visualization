from app.utilities import df_plot, df_filter
from app.constants import det_col, name_color_codes, color_dict
import pandas as pd


class CropYield:

    def __init__(self, all_params, years, land_use):
        self.all_params = all_params
        self.years = years
        self.land_use = land_use

    def figure(self):
        print('Generating CropYield')
        crops_yield_df = self.calculate_yield_df(self.all_params, self.years, self.land_use)
        crops_yield_df.loc[:, crops_yield_df.columns != 'y'] = (crops_yield_df.loc[
            :, crops_yield_df.columns != 'y'])
        crops_yield_df['y'] = self.years
        return crops_yield_df.iplot(asFigure=True,
                                    x='y',
                                    mode='lines+markers',
                                    xTitle='Year',
                                    yTitle='Yield (t/ha)',
                                    size=10,
                                    color=[color_dict[x] for x in crops_yield_df.columns if x != 'y'],  # noqa
                                    title='Yield (tonnes/hectare)',
                                    showlegend=True)

    def calculate_yield_df(self, all_params, years, land_use):
        mode_crop_combo = land_use.mode_crop_combo()
        crops_total_df = all_params['TotalAnnualTechnologyActivityByMode'][all_params['TotalAnnualTechnologyActivityByMode'].t.str.startswith(  # noqa
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

        crops_yield_df = self.calculate_crops_prod_df(all_params, years) / crops_total_df
        return crops_yield_df

    def calculate_crops_prod_df(self, all_params, years):
        crops_prod_df = all_params['ProductionByTechnologyAnnual'][all_params['ProductionByTechnologyAnnual'].f.str.startswith(  # noqa
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
