from app.utilities import df_plot, df_filter
import i18n


class EnergyImports:

    def __init__(self, all_params, years, plot_title):
        self.all_params = all_params
        self.years = years
        self.plot_title = plot_title
        self.index_column = 'y'

    def figure(self):
        return self.plot(self.data(), self.plot_title)

    def plot(self, data, title):
        return df_plot(data, i18n.t('label.petajoules'), title)

    def data(self):
        production_by_technology_annual = self.all_params['ProductionByTechnologyAnnual']
        ene_imp_df = production_by_technology_annual[
                production_by_technology_annual.t.str.startswith('IMP')
            ].drop('r', axis=1)
        ene_imp_df = ene_imp_df.loc[~ene_imp_df['t'].str[3:6].isin(['CRP'])]
        return df_filter(ene_imp_df, 3, 6, [], self.years)
