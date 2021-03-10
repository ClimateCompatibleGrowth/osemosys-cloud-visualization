from app.utilities import df_plot, df_filter
import app.constants
import pandas as pd


class CropYield:

    def __init__(self, all_params, years, land_use, plot_title):
        self.all_params = all_params
        self.years = years
        self.land_use = land_use
        self.plot_title = plot_title
        self.index_column = 'y'

    def figure(self):
        return self.plot(self.data(), self.plot_title)

    def plot(self, data, title):
        return data.iplot(asFigure=True,
                x='y',
                mode='lines+markers',
                xTitle='Year',
                yTitle='Yield (t/ha)',
                size=10,
                color=[app.constants.color_dict[x] for x in data.columns if x != 'y'],  # noqa
                title=title,
                showlegend=True)

    def data(self):
        crops_yield_df = self.__calculate_yield_df(self.all_params, self.years, self.land_use)
        crops_yield_df.loc[:, crops_yield_df.columns != 'y'] = (crops_yield_df.loc[
            :, crops_yield_df.columns != 'y']).mul(10)
        crops_yield_df['y'] = self.years
        return crops_yield_df

    def __calculate_yield_df(self, all_params, years, land_use):
        mode_crop_combo = land_use.mode_crop_combo()
        crops = self.land_use.crop_list
        crops_total_df = all_params['TotalAnnualTechnologyActivityByMode'][all_params['TotalAnnualTechnologyActivityByMode'].t.str.startswith(  # noqa
            'LNDAGR', False)].drop('r', axis=1)
        crops_total_df['m'] = crops_total_df['m'].astype(int)
        crops_total_df['crop_combo'] = crops_total_df['m'].map(mode_crop_combo)
        #crops_total_df['land_use'] = crops_total_df['crop_combo'].str[0:4]
        crops_total_df['land_use'] = [x[0:4] 
                                      if x.startswith('CP')
                                      else x[0:3]
                                      for x in crops_total_df['crop_combo']
                                      ]
        crops_total_df.drop(['m', 'crop_combo'], axis=1, inplace=True)

        #crops_total_df = crops_total_df[crops_total_df['land_use'].str.startswith('CP', False)]
        crops_total_df = crops_total_df[crops_total_df['land_use'].isin(crops)]
        crops_total_df = crops_total_df.pivot_table(index='y',
                                                    columns='land_use',
                                                    values='value',
                                                    aggfunc='sum').reset_index().fillna(0)
        crops_total_df = crops_total_df.reindex(sorted(crops_total_df.columns), axis=1).set_index(
            'y').reset_index().rename(columns=app.constants.det_col).astype('float64')

        crops_yield_df = self.calculate_crops_prod_df(all_params, years) / crops_total_df
        return crops_yield_df

    def calculate_crops_prod_df(self, all_params, years):
        crops_prod_df = all_params['ProductionByTechnologyAnnual'][
            all_params['ProductionByTechnologyAnnual'].f.str.startswith(  # noqa
            'CRP', False) & all_params['ProductionByTechnologyAnnual'].t.str.startswith(  # noqa
            'LND', False)].drop('r', axis=1)
        crops_prod_df['f'] = crops_prod_df['f'].str[3:7]
        crops_prod_df['value'] = crops_prod_df['value'].astype('float64')

        crops_prod_df = crops_prod_df.pivot_table(index='y',
                                                  columns='f',
                                                  values='value',
                                                  aggfunc='sum').reset_index().fillna(0)
        crops_prod_df = crops_prod_df.reindex(sorted(crops_prod_df.columns), axis=1).set_index(
            'y').reset_index().rename(columns=app.constants.det_col)
        crops_prod_df['y'] = years
        return crops_prod_df
