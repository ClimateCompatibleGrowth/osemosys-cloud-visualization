from app.utilities import df_plot, df_filter


class DomesticEnergyProduction:

    def __init__(self, all_params, years):
        self.all_params = all_params
        self.years = years

    def figure(self):
        print('Generating DomesticEnergyProduction')
        dom_prd_df = self.__calculate_dom_prd_df()
        for each in dom_prd_df.columns:
            if each in ['Land', 'Water', 'Precipitation']:
                dom_prd_df = dom_prd_df.drop(each, axis=1)
        return df_plot(dom_prd_df, 'Petajoules (PJ)', 'Domestic energy production')

    def __calculate_dom_prd_df(self):
        production_by_technology_annual = self.all_params['ProductionByTechnologyAnnual']
        dom_prd_df = production_by_technology_annual[
                production_by_technology_annual.t.str.startswith('MIN') |
                production_by_technology_annual.t.str.startswith('RNW')
            ].drop('r', axis=1)
        return df_filter(dom_prd_df, 3, 6, [], self.years)
