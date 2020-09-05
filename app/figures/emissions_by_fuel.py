from app.utilities import df_plot, df_filter


class EmissionsByFuel:

    def __init__(self, all_params, years, plot_title):
        self.all_params = all_params
        self.years = years
        self.plot_title = plot_title

    def figure(self):
        return df_plot(self.__calculate_emissions_fuel_df(),
                       'Million tonnes of CO2',
                       self.plot_title)

    def __calculate_emissions_fuel_df(self):
        annual_technology_emission = self.all_params['AnnualTechnologyEmission']
        emissions_df = annual_technology_emission[
            annual_technology_emission.t.str.startswith('DEM')
            ].drop('r', axis=1)
        return df_filter(emissions_df, 6, 9, [], self.years)
