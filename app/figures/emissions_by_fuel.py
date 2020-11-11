from app.utilities import df_plot, df_filter
import app.constants


class EmissionsByFuel:

    def __init__(self, all_params, years, plot_title):
        self.all_params = all_params
        self.years = years
        self.plot_title = plot_title

    def figure(self):
        return self.__calculate_emissions_fuel_df().iplot(asFigure=True,
                                               x='y',
                                               kind='bar',
                                               barmode='relative',
                                               xTitle='Year',
                                               # yTitle='Terawatt-hours (TWh)',
                                               yTitle='Million tonnes of CO2',
                                               color=[app.constants.color_dict[x]
                                                      for x
                                                      in self.__calculate_emissions_fuel_df().columns
                                                      if x != 'y'],
                                               title=self.plot_title,
                                               showlegend=True)

                       

    def __calculate_emissions_fuel_df(self):
        annual_technology_emission = self.all_params['AnnualTechnologyEmission']
        emissions_df = annual_technology_emission[
            annual_technology_emission.t.str.startswith('DEM') |
            annual_technology_emission.t.str.startswith('MIN')            
            ].drop('r', axis=1)
        return df_filter(emissions_df, 6, 9, [], self.years)
