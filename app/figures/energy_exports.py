from app.utilities import df_plot, df_filter
import i18n


class EnergyExports:

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
        total_capacity_annual_params = self.all_params['TotalTechnologyAnnualActivity']
        ene_exp_df = total_capacity_annual_params[
                total_capacity_annual_params.t.str.startswith('EXP')
            ].drop('r', axis=1)
        ene_exp_df = ene_exp_df.loc[~ene_exp_df['t'].str[3:6].isin(['CRP'])]
        return df_filter(ene_exp_df, 3, 6, [], self.years)
