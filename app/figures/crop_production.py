from app.utilities import df_plot, df_filter
from app.constants import det_col


class CropProduction:

    def __init__(self, all_params, years, plot_title):
        self.all_params = all_params
        self.years = years
        self.plot_title = plot_title

    def figure(self):
        crops_prod_df = self.__calculate_crops_prod_df()
        return df_plot(crops_prod_df, 'Production (Million tonnes)', self.plot_title)

    def __calculate_crops_prod_df(self):
        production_by_technology_annual = self.all_params['ProductionByTechnologyAnnual']
        crops_prod_df = production_by_technology_annual[
                production_by_technology_annual.f.str.startswith('CRP')
            ].drop('r', axis=1)
        crops_prod_df['f'] = crops_prod_df['f'].str[3:7]
        crops_prod_df['value'] = crops_prod_df['value'].astype('float64')

        crops_prod_df = crops_prod_df.pivot_table(index='y',
                                                  columns='f',
                                                  values='value',
                                                  aggfunc='sum').reset_index().fillna(0)
        crops_prod_df = crops_prod_df.reindex(sorted(crops_prod_df.columns), axis=1).set_index(
            'y').reset_index().rename(columns=det_col)
        crops_prod_df['y'] = self.years
        return crops_prod_df
