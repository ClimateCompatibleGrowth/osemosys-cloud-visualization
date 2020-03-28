from app.utilities import df_plot, df_filter


class PowerGenerationCapacity:

    def __init__(self, all_params, years):
        self.all_params = all_params
        self.years = years

    def figure(self):
        return df_plot(self.__cap_df(), 'Gigawatts (GW)', 'Power Generation Capacity (Detail)')

    def __cap_df(self):
        total_capacity_annual_params = self.all_params['TotalCapacityAnnual']
        cap_df = total_capacity_annual_params[total_capacity_annual_params.t.str.startswith('PWR')]\
            .drop('r', axis=1)
        return df_filter(cap_df, 3, 6, ['CNT', 'TRN', 'CST', 'CEN', 'SOU', 'NOR'], self.years)
