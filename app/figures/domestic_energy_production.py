from app.utilities import df_plot, df_filter


class DomesticEnergyProduction:

    def __init__(self, all_params, years, plot_title):
        self.all_params = all_params
        self.years = years
        self.plot_title = plot_title
        self.index_column = 'y'

    def figure(self):
        return self.plot(self.data(), self.plot_title)

    def plot(self, data, title):
        for each in data.columns:
            if each in ['Land', 'Water', 'Precipitation', 'Suelo', 'Agua', 'Precipitación']:
                data = data.drop(each, axis=1)
        return df_plot(data, 'Petajoules (PJ)', title)

    def data(self):
        production_by_technology_annual = self.all_params['ProductionByTechnologyAnnual']
        dom_prd_df = production_by_technology_annual[
                production_by_technology_annual.t.str.startswith('MIN') |
                production_by_technology_annual.t.str.startswith('RNW')
            ].drop('r', axis=1)
        return df_filter(dom_prd_df, 3, 6, [], self.years)
