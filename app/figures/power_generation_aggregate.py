import pandas as pd
from app.utilities import df_plot, df_filter
from app.constants import agg_col


class PowerGenerationAggregate:

    def __init__(self, all_params, years):
        self.all_params = all_params
        self.years = years

    def figure(self):
        gen_df = self.__calculate_gen_df()
        gen_agg_df = pd.DataFrame(columns=agg_col)
        gen_agg_df.insert(0, 'y', gen_df['y'])
        gen_agg_df = gen_agg_df.fillna(0.00)

        for each in agg_col:
            for tech_exists in agg_col[each]:
                if tech_exists in gen_df.columns:
                    gen_agg_df[each] = gen_agg_df[each] + gen_df[tech_exists]
                    gen_agg_df[each] = gen_agg_df[each].round(2)
        return df_plot(gen_agg_df, 'Petajoules (PJ)', 'Power Generation (Aggregate)')

    def __calculate_gen_df(self):
        production_by_technology_annual = self.all_params['ProductionByTechnologyAnnual']
        gen_df = production_by_technology_annual[
                (production_by_technology_annual.t.str.startswith('PWR') |
                    production_by_technology_annual.t.str.startswith('IMP')) &
                production_by_technology_annual.f.str.startswith('ELC')
                ].drop('r', axis=1)
        return df_filter(gen_df, 3, 6, ['TRN'], self.years)
