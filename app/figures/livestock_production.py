from app.utilities import df_plot, df_filter
import app.constants


class LivestockProduction:

    def __init__(self, all_params, years, plot_title):
        self.all_params = all_params
        self.years = years
        self.plot_title = plot_title
        self.index_column = 'y'

    def figure(self):
        return self.plot(self.data(), self.plot_title)

    def plot(self, data, title):
        return df_plot(data, 'Heads of livestock (Millions)', title)

    def data(self):
        production_by_technology_annual = self.all_params['ProductionByTechnologyAnnual']
        lvs_prod_df = production_by_technology_annual[
            production_by_technology_annual.f.str.startswith('LVS')
            ].drop('r', axis=1)
        lvs_prod_df = lvs_prod_df.loc[~lvs_prod_df['f'].str[3:6].isin(['BEF',
                                                                       'MUT',
                                                                       'MLK',
                                                                       'HID',
                                                                       'CSH',
                                                                       'WOL',
                                                                       'SHE',
                                                                       'TLU',
                                                                       'WAT',
                                                                       'SUS',
                                                                       'UNS',
                                                                       'RST'])]

        lvs_prod_df['f'] = lvs_prod_df['f'].str[3:6]
        lvs_prod_df['value'] = lvs_prod_df['value'].astype('float64')
        lvs_prod_df = lvs_prod_df.pivot_table(index='y',
                                              columns='f',
                                              values='value',
                                              aggfunc='sum').reset_index().fillna(0)
        lvs_prod_df = (lvs_prod_df.reindex(sorted(lvs_prod_df.columns), axis=1)
                                  .set_index('y')
                                  .reset_index()
                                  .rename(columns=app.constants.det_col))
        lvs_prod_df['y'] = self.years
        return lvs_prod_df
