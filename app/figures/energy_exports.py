from app.utilities import df_plot, df_filter


class EnergyExports:

    def __init__(self, all_params, years, plot_title):
        self.all_params = all_params
        self.years = years
        self.plot_title = plot_title

    def figure(self):
        return df_plot(self.__calculate_ene_exp_df(), 'Petajoules (PJ)', self.plot_title)

    def __calculate_ene_exp_df(self):
        total_capacity_annual_params = self.all_params['TotalTechnologyAnnualActivity']
        ene_exp_df = total_capacity_annual_params[
                total_capacity_annual_params.t.str.startswith('EXP')
            ].drop('r', axis=1)
        return df_filter(ene_exp_df, 3, 6, [], self.years)
