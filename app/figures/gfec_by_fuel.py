from app.utilities import df_plot, df_filter


class GFECByFuel:

    def __init__(self, all_params, years, plot_title):
        self.all_params = all_params
        self.years = years
        self.plot_title = plot_title

    def figure(self):
        return df_plot(self.__calculate_gfec_df(),
                       'Energy (PJ)',
                       self.plot_title)

    def __calculate_gfec_df(self):
        total_technology_annual_activity = self.all_params['ProductionByTechnologyAnnual']
        gfec_fuel_df = total_technology_annual_activity[
            total_technology_annual_activity.t.str.startswith('DEM')
            ].drop('r', axis=1)
        #gfec_fuel_df = gfec_fuel_df[~gfec_fuel_df.t.str.startswith('DEMPWR')]
        return df_filter(gfec_fuel_df, 6, 9, [
                                              #'SUR',
                                              'WND',
                                              'HYD',
                                              'SOL',
                                              'GEO',
                                              #'GWT',
                                              'CRU',
                                              'TLU',
                                              'FLU',
                                              'IRR',
                                              'RAI'],
                         self.years)
