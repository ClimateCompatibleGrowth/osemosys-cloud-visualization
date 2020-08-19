from app.utilities import df_plot, df_filter
from app.constants import det_col, color_dict
import pandas as pd


class WaterDemand:

    def __init__(self, all_params, years):
        self.all_params = all_params
        self.years = years

    def figure(self):
        print('Generating WaterDemand')
        wat_dem_df = self.__calculate_wat_dem_df()
        wat_dem_df['y'] = self.years
        return wat_dem_df.iplot(asFigure=True,
                                x='y',
                                kind='bar',
                                barmode='stack',
                                xTitle='Year',
                                yTitle='Billion m3',
                                color=[color_dict[x] for x in wat_dem_df.columns if x != 'y'],
                                title='Water Demand',
                                showlegend=True,
                                )

    def __calculate_wat_dem_df(self):
        production_by_technology_annual = self.all_params['ProductionByTechnologyAnnual']
        wat_list = ['AGRWAT', 'PUBWAT', 'PWRWAT', 'INDWAT', 'LVSWAT']
        wat_dem_df = production_by_technology_annual[
            production_by_technology_annual.f.str[0:6].isin(wat_list)
        ].drop('r', axis=1)
        wat_dem_df['f'] = wat_dem_df['f'].str[0:3]
        wat_dem_df['value'] = wat_dem_df['value'].astype('float64')
        wat_dem_df = wat_dem_df.pivot_table(index='y',
                                            columns='f',
                                            values='value',
                                            aggfunc='sum').reset_index().fillna(0)
        wat_dem_df = (wat_dem_df.reindex(sorted(wat_dem_df.columns), axis=1)
                                .set_index('y')
                                .reset_index()
                                .rename(columns=det_col))
        return wat_dem_df
