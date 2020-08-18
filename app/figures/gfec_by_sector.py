from app.utilities import df_plot, df_filter


class GFECBySector:

    def __init__(self, all_params, years):
        self.all_params = all_params
        self.years = years

    def figure(self):
        print('Generating GFECBySector')
        return df_plot(self.__calculate_gfec_df(),
                       'Energy (PJ)',
                       'Gross final energy consumption - by sector')

    def __calculate_gfec_df(self):
        total_technology_annual_activity = self.all_params['TotalTechnologyAnnualActivity']
        gfec_df = total_technology_annual_activity[
            total_technology_annual_activity.t.str.startswith('DEM')
            ].drop('r', axis=1)
        gfec_df = gfec_df[~gfec_df.t.str.startswith('DEMAGRSUR')]
        gfec_df = gfec_df[~gfec_df.t.str.endswith('CRU')]
        return df_filter(gfec_df, 3, 6, ['PWR', 'LVS'], self.years)
