from app.utilities import df_plot, df_filter


class GFECByFuel:

    def __init__(self, all_params, years):
        self.all_params = all_params
        self.years = years

    def figure(self):
        print('Generating GFECByFuel')
        return df_plot(self.__calculate_gfec_df(),
                       'Energy (PJ)',
                       'Gross final energy consumption - by fuel')

    def __calculate_gfec_df(self):
        total_technology_annual_activity = self.all_params['TotalTechnologyAnnualActivity']
        gfec_fuel_df = total_technology_annual_activity[
            total_technology_annual_activity.t.str.startswith('DEM')
            ].drop('r', axis=1)
        gfec_fuel_df = gfec_fuel_df[~gfec_fuel_df.t.str.startswith('DEMPWR')]
        return df_filter(gfec_fuel_df, 6, 9, ['SUR', 'WND', 'HYD', 'SOL', 'GEO', 'GWT', 'CRU'],
                         self.years)
