from app.utilities import df_plot, df_filter


class PowerGenerationFuelUse:

    def __init__(self, all_params, years, plot_title):
        self.all_params = all_params
        self.years = years
        self.plot_title = plot_title

    def figure(self):
        return df_plot(
                    self.__calculate_gen_use_df(),
                    'Petajoules (PJ)',
                    self.plot_title
                )

    def __calculate_gen_use_df(self):
        production_by_technology_annual = self.all_params['ProductionByTechnologyAnnual']
        gen_use_df = production_by_technology_annual[
                production_by_technology_annual.t.str.startswith('DEMPWR')
            ].drop('r', axis=1)
        gen_use_df = df_filter(gen_use_df, 6, 9, ['SUR'], self.years)
        return gen_use_df
