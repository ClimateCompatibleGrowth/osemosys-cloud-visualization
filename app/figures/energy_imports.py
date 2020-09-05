from app.utilities import df_plot, df_filter


class EnergyImports:

    def __init__(self, all_params, years, plot_title):
        self.all_params = all_params
        self.years = years
        self.plot_title = plot_title

    def figure(self):
        return df_plot(self.__calculate_ene_imp_df(), 'Petajoules (PJ)', self.plot_title)

    def __calculate_ene_imp_df(self):
        production_by_technology_annual = self.all_params['ProductionByTechnologyAnnual']
        ene_imp_df = production_by_technology_annual[
                production_by_technology_annual.t.str.startswith('IMP')
            ].drop('r', axis=1)
        return df_filter(ene_imp_df, 3, 6, [], self.years)
