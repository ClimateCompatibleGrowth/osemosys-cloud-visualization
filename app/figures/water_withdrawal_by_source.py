from app.utilities import df_plot, df_filter


class WaterWithdrawalBySource:

    def __init__(self, all_params, years):
        self.all_params = all_params
        self.years = years

    def figure(self):
        print('Generating WaterWithdrawalBySource')
        return df_plot(self.__calculate_wat_source_df(), 'Billion m3', 'Water withdrawal by source')

    def __calculate_wat_source_df(self):
        production_by_technology_annual = self.all_params['ProductionByTechnologyAnnual']
        wat_list = ['AGRWAT', 'PUBWAT', 'PWRWAT', 'INDWAT', 'LVSWAT']
        wat_source_df = production_by_technology_annual[
            production_by_technology_annual.f.str[0:6].isin(wat_list)
        ].drop('r', axis=1)
        return df_filter(wat_source_df, 6, 9, [], self.years)
