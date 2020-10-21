from app.utilities import df_plot, df_filter
from app.constants import det_col, color_dict
import pandas as pd


class PowerGenerationTimeslice:

    def __init__(self, all_params, years, plot_title):
        self.all_params = all_params
        self.years = years
        self.plot_title = plot_title

    def figure(self):
        return self.__calculate_gen_ts_df().iplot(asFigure=True,
                                               x='l',
                                               kind='bar',
                                               barmode='relative',
                                               xTitle='Timeslice',
                                               # yTitle='Terawatt-hours (TWh)',
                                               yTitle='Petajoules (PJ)',
                                               color=[color_dict[x]
                                                      for x
                                                      in self.__calculate_gen_df().columns
                                                      if x != 'l'],
                                               title=self.plot_title,
                                               showlegend=True)

    def __calculate_gen_ts_df(self):
        production_by_technology = self.all_params['ProductionByTechnology']
        gen_ts_df = production_by_technology[
                                            (production_by_technology.t.str.startswith('PWR') |
                                             production_by_technology.t.str.startswith('IMP')) &
                                             production_by_technology.f.str.startswith('ELC')
                                            ].drop('r', axis=1)

        gen_ts_df['t'] = gen_ts_df['t'].str[3:6]
        gen_ts_df['value'] = gen_ts_df['value'].astype('float64')
        gen_ts_df = gen_ts_df[~gen_ts_df['t'].isin(['TRN'])].pivot_table(index='l', 
                                                          columns='t',
                                                          values='value',
                                                          aggfunc='mean').reset_index().fillna(0)
        gen_ts_df = gen_ts_df.reindex(sorted(gen_ts_df.columns), axis=1).set_index('l').reset_index().rename(columns=det_col)

        return gen_ts_df
