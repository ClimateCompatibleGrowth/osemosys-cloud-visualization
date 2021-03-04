from app.utilities import df_plot, df_filter


class AgricultureImports:

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
        agr_imp_df = total_annual_technology_activity[
                total_annual_technology_activity.t.str.startswith('IMP')
            ].drop('r', axis=1)
        agr_imp_df = df_filter(agr_imp_df, 3, 6, [], self.years)
        for each in agr_imp_df.columns:
            if each not in crops:
                if each not in ['y']:
                    agr_imp_df.drop(each,
                                    axis=1,
                                    inplace=True)
        return agr_imp_df
