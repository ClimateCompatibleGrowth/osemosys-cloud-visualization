from app.utilities import df_plot, df_filter


class DomesticEnergyProduction:

    def __init__(self, all_params, years, plot_title):
        self.all_params = all_params
        self.years = years
        self.plot_title = plot_title

    def figure(self):
        dom_prd_df = self.__calculate_dom_prd_df()
        for each in dom_prd_df.columns:
            if each in ['Land', 'Water', 'Precipitation', 'Suelo', 'Agua', 'Precipitación']:
                dom_prd_df = dom_prd_df.drop(each, axis=1)
        return df_plot(dom_prd_df, 'Petajoules (PJ)', self.plot_title)

    def __calculate_dom_prd_df(self):
        production_by_technology_annual = self.all_params['ProductionByTechnologyAnnual']
        dom_prd_df = production_by_technology_annual[
                production_by_technology_annual.t.str.startswith('MIN') |
                production_by_technology_annual.t.str.startswith('RNW')
            ].drop('r', axis=1)
        return df_filter(dom_prd_df, 3, 6, [], self.years)
