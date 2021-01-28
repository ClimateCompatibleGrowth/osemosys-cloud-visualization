from app.utilities import df_plot, df_filter, df_years
import app.constants
import pandas as pd


class WaterBalance:

    def __init__(self, all_params, years, plot_title):
        self.all_params = all_params
        self.years = years
        self.plot_title = plot_title
        self.index_column = 'y'

    def figure(self):
        return self.plot(self.data(), self.plot_title)

    def plot(self, data, title):
        return data.iplot(
                asFigure=True,
                x='y',
                kind='bar',
                barmode='relative',
                xTitle='Year',
                yTitle='Billion m3',
                color=[app.constants.color_dict[x] for x in data.columns if x != 'y'],
                title=title,
                showlegend=True,
                )

    def data(self):
        production_by_technology_annual = self.all_params['ProductionByTechnologyAnnual']
        wat_bal_df = production_by_technology_annual[
            production_by_technology_annual.f.str.startswith('WTR')
            ].drop('r', axis=1)
        wat_bal_df['f'] = wat_bal_df['f'].str[3:6]
        wat_bal_df['value'] = wat_bal_df['value'].astype('float64')
        wat_bal_df = wat_bal_df.pivot_table(index='y',
                                            columns='f',
                                            values='value',
                                            aggfunc='sum').reset_index().fillna(0)
        wat_bal_df = (wat_bal_df.reindex(sorted(wat_bal_df.columns), axis=1)
                                .set_index('y')
                                .reset_index()
                                .rename(columns=app.constants.det_col))
        wat_bal_df = df_years(wat_bal_df, self.years)
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
                                .rename(columns=app.constants.det_col))
        wat_dem_df = df_years(wat_dem_df, self.years)

        if 'Agriculture' in wat_dem_df.columns:
            wat_bal_df['Irrigation'] = wat_dem_df['Agriculture']
        elif 'Tierras agrícolas' in wat_dem_df.columns:
            wat_bal_df['Irrigation'] = wat_dem_df['Tierras agrícolas']
        else:
            wat_bal_df['Irrigation'] = 0
        # wat_bal_df['y'] = self.years
        for each in wat_bal_df.columns:
            if each in ['Evapotranspiration',
                        'Groundwater recharge',
                        'Surface water run-off',
                        'Recharge + Run-off',
                        'Groundwater',
                        'Evapotranspiración',
                        'Recarga de agua subterránea',
                        'Agua superficial',
                        'Agua subterránea']:
                wat_bal_df[each] = wat_bal_df[each].mul(-1)
        wat_bal_df = df_years(wat_bal_df, self.years)
        return wat_bal_df
