from app.utilities import df_plot, df_filter


class PowerGenerationCapacity:

    def __init__(self, all_params, years, plot_title):
        self.all_params = all_params
        self.years = years
        self.plot_title = plot_title
        self.index_column = 'y'

    def figure(self):
        return self.plot(self.data(), self.plot_title)

    def plot(self, data, title):
        return df_plot(data, 'Gigawatts (GW)', title)

    def data(self):
        total_capacity_annual_params = self.all_params['TotalCapacityAnnual']
        cap_df = total_capacity_annual_params[total_capacity_annual_params.t.str.startswith('PWR')]\
            .drop('r', axis=1)
        return df_filter(cap_df, 3, 6, ['CNT', 'TRN', 'CST', 'CEN', 'SOU', 'NOR'], self.years)
