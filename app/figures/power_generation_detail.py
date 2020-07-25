from app.utilities import df_plot, df_filter


class PowerGenerationDetail:

    def __init__(self, all_params, years):
        self.all_params = all_params
        self.years = years

    def figure(self):
        print('Generating PowerGenerationDetail')
        return df_plot(self.__calculate_gen_df(), 'Petajoules (PJ)', 'Power Generation (Detail)')

    def __calculate_gen_df(self):
        production_by_technology_annual = self.all_params['ProductionByTechnologyAnnual']
        gen_df = production_by_technology_annual[
                (production_by_technology_annual.t.str.startswith('PWR') |
                    production_by_technology_annual.t.str.startswith('IMP')) &
                production_by_technology_annual.f.str.startswith('ELC')
                ].drop('r', axis=1)
        return df_filter(gen_df, 3, 6, ['TRN'], self.years)
