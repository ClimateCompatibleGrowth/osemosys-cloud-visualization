from app.utilities import df_plot, df_filter


class AgricultureExports:

    def __init__(self, all_params, years, land_use, plot_title):
        self.all_params = all_params
        self.years = years
        self.land_use = land_use
        self.plot_title = plot_title
        self.index_column = 'y'

    def figure(self):
        return self.plot(self.data(), self.plot_title)

    def plot(self, data, title):
        return df_plot(data, 'Million tonnes (Mt)', title)

    def data(self):
        crops = self.land_use.crop_list
        total_annual_technology_activity = self.all_params['TotalTechnologyAnnualActivity']
        agr_exp_df = total_annual_technology_activity[
                total_annual_technology_activity.t.str.startswith('EXP')
            ].drop('r', axis=1)
        agr_exp_df = agr_exp_df.loc[agr_exp_df.t.str[3:].isin(crops)]
        agr_exp_df = df_filter(agr_exp_df, 6, 9, [], self.years)
        return agr_exp_df
