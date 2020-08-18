from app.utilities import df_plot, df_filter
from app.constants import det_col


class LivestockProduction:

    def __init__(self, all_params, years):
        self.all_params = all_params
        self.years = years

    def figure(self):
        print('Generating CropProduction')
        return df_plot(self.__calculate_lvs_prod_df(),
                       'Production (Million tonnes)',
                       'Livestock production')

    def __calculate_lvs_prod_df(self):
        production_by_technology_annual = self.all_params['ProductionByTechnologyAnnual']
        lvs_prod_df = production_by_technology_annual[
            production_by_technology_annual.f.str.startswith('LVS')
            ].drop('r', axis=1)
        lvs_prod_df = lvs_prod_df.loc[lvs_prod_df['f'].str.contains('PRD')]
        lvs_prod_df['value'] = lvs_prod_df['value'].astype('float64')
        lvs_prod_df = lvs_prod_df.pivot_table(index='y',
                                              columns='f',
                                              values='value',
                                              aggfunc='sum').reset_index().fillna(0)
        lvs_prod_df = (lvs_prod_df.reindex(sorted(lvs_prod_df.columns), axis=1)
                                  .set_index('y')
                                  .reset_index()
                                  .rename(columns=det_col))
        lvs_prod_df['y'] = self.years
        return lvs_prod_df
