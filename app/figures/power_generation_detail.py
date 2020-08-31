from app.utilities import df_plot, df_filter
from app.constants import color_dict
import pandas as pd


class PowerGenerationDetail:

    def __init__(self, all_params, years):
        self.all_params = all_params
        self.years = years

    def figure(self):
        print('Generating PowerGenerationDetail')
        return self.__calculate_gen_df().iplot(asFigure=True,
                                               x='y',
                                               kind='bar',
                                               barmode='relative',
                                               xTitle='Year',
                                               yTitle='Terawatt-hours (TWh)',
                                               color=[color_dict[x]
                                                      for x
                                                      in self.__calculate_gen_df().columns
                                                      if x != 'y'],
                                               title='Power Generation (Detail)',
                                               showlegend=True)

    def __calculate_gen_df(self):
        production_by_technology_annual = self.all_params['ProductionByTechnologyAnnual']
        gen_df = production_by_technology_annual[
                (production_by_technology_annual.t.str.startswith('PWR') |
                    production_by_technology_annual.t.str.startswith('IMP')) &
                production_by_technology_annual.f.str.startswith('ELC')
                ].drop('r', axis=1)

        gen_df = df_filter(gen_df, 3, 6, ['TRN'], self.years)
        gen_df['Net electricity imports'] = 0
        electricity_exports_df = self.all_params['TotalTechnologyAnnualActivity']
        ele_exp_df = electricity_exports_df[
                     electricity_exports_df.t.str.startswith('EXPELC')
                     ].drop('r', axis=1)

        if not ele_exp_df.empty:
            ele_exp_df = (df_filter(ele_exp_df, 3, 6, ['TRN'], self.years)
                          .rename(columns={'Electricity': 'Electricity exports'}))
            gen_df = gen_df.merge(ele_exp_df)
            gen_df['Net electricity imports'] = (gen_df['Net electricity imports']
                                                 - gen_df['Electricity exports'])
            gen_df.drop('Electricity exports', axis=1, inplace=True)

            if 'Electricity' in gen_df.columns:
                gen_df['Net electricity imports'] = (gen_df['Net electricity imports']
                                                     - gen_df['Electricity'])
                gen_df.drop('Electricity', axis=1, inplace=True)

            gen_df.rename(columns={'Net electricity imports': 'Electricity exports'},
                          inplace=True)
            gen_df.loc[:, gen_df.columns != 'y'] = (gen_df.loc[:, gen_df.columns != 'y']
                                                          .mul(0.28).round(2))

        return gen_df
