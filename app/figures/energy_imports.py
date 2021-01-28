from app.utilities import df_plot, df_filter


class EnergyImports:

    def __init__(self, all_params, years, plot_title):
        self.all_params = all_params
        self.years = years
        self.plot_title = plot_title
        self.index_column = 'y'

    def figure(self):
        return self.plot(self.data(), self.plot_title)

    def plot(self, data, title):
        return df_plot(data, 'Petajoules (PJ)', title)

    def data(self):
        production_by_technology_annual = self.all_params['ProductionByTechnologyAnnual']
        ene_imp_df = production_by_technology_annual[
                production_by_technology_annual.t.str.startswith('IMP')
            ].drop('r', axis=1)
        return df_filter(ene_imp_df, 3, 6, [], self.years)
