from app.utilities import df_plot, df_filter


class CapitalInvestment:

    def __init__(self, all_params, years, plot_title):
        self.all_params = all_params
        self.years = years
        self.plot_title = plot_title
        self.index_column = 'y'

    def figure(self):
        return self.plot(self.data(), self.plot_title)

    def plot(self, data, title):
        return df_plot(data, 'Million $', title)

    def data(self):
        capital_investment = self.all_params['CapitalInvestment']
        cap_cos_df = capital_investment[
                capital_investment.t.str.startswith('PWR')
            ].drop('r', axis=1)
        return df_filter(cap_cos_df, 3, 6, ['TRN'], self.years)
