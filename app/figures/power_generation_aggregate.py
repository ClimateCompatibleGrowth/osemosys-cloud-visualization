import i18n
import pandas as pd
from app.utilities import df_plot, df_filter
import app.constants


class PowerGenerationAggregate:

    def __init__(self, all_params, years, plot_title):
        self.all_params = all_params
        self.years = years
        self.plot_title = plot_title
        self.index_column = 'y'

    def figure(self):
        gen_df = self.__calculate_gen_df()
        gen_agg_df = pd.DataFrame(columns=app.constants.agg_col)
        gen_agg_df.insert(0, 'y', gen_df['y'])
        gen_agg_df = gen_agg_df.fillna(0.00)

        for each in app.constants.agg_col:
            for tech_exists in app.constants.agg_col[each]:
                if tech_exists in gen_df.columns:
                    gen_agg_df[each] = gen_agg_df[each] + gen_df[tech_exists]
                    gen_agg_df[each] = gen_agg_df[each].round(2)

        gen_agg_df = gen_agg_df.loc[:, (gen_agg_df != 0).any(axis=0)]
        gen_agg_df.rename(columns={'Net electricity imports': 'Electricity exports'},
                          inplace=True)
        return gen_agg_df.iplot(asFigure=True,
                                x='y',
                                kind='bar',
                                barmode='relative',
                                xTitle=i18n.t('label.year'),
                                yTitle=i18n.t('label.petajoules'),
                                color=[app.constants.color_dict[x]
                                       for x
                                       in self.__calculate_gen_df().columns
                                       if x != 'y'],
                                title=self.plot_title,
                                showlegend=True)

    def __calculate_gen_df(self):
        production_by_technology_annual = self.all_params['ProductionByTechnologyAnnual']
        gen_df = production_by_technology_annual[
                (production_by_technology_annual.t.str.startswith('PWR') |
                    production_by_technology_annual.t.str.startswith('IMP')) &
                production_by_technology_annual.f.str.contains('ELC')
                ].drop('r', axis=1)

        gen_df = df_filter(gen_df, 3, 6, ['TRN', 'DIS'], self.years)
        gen_df['Net electricity imports'] = 0
        electricity_exports_df = self.all_params['TotalTechnologyAnnualActivity']
        ele_exp_df = electricity_exports_df[
                     electricity_exports_df.t.str.startswith('EXPELC')
                     ].drop('r', axis=1)

        if not ele_exp_df.empty:
            ele_exp_df = (df_filter(ele_exp_df, 3, 6, ['TRN', 'DIS'], self.years)
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
            # gen_df.loc[:, gen_df.columns != 'y'] = (gen_df.loc[:, gen_df.columns != 'y']
            #                                              .mul(0.28).round(2))
        return gen_df
