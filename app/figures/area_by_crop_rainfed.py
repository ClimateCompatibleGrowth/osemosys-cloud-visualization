from app.utilities import df_plot, df_filter
import app.constants


class AreaByCropRainfed:

    def __init__(self, all_params, years, land_use, plot_title):
        self.all_params = all_params
        self.years = years
        self.land_use = land_use
        self.plot_title = plot_title
        self.index_column = 'y'

    def figure(self):
        return self.plot(self.data(), self.plot_title)

    def plot(self, data, title):
        return df_plot(data, 'Land area (1000 sq.km.)', title)

    def data(self):
        mode_crop_combo = self.land_use.mode_crop_combo()
        crops_ws_df = self.__calculate_crops_ws_df()
        crops_ws_df['m'] = crops_ws_df['m'].astype(int)
        crops_ws_df['crop_combo'] = crops_ws_df['m'].map(mode_crop_combo)
        crops_ws_df = crops_ws_df[(crops_ws_df.crop_combo.str.startswith('CP'))
                                  & (crops_ws_df.crop_combo.str[5:6] == 'R')]
        crops_ws_df['land_use'] = crops_ws_df['crop_combo'].str[0:4]
        crops_ws_df.drop(['m', 'crop_combo'], axis=1, inplace=True)
        crops_ws_df = crops_ws_df.pivot_table(index='y',
                                              columns='land_use',
                                              values='value',
                                              aggfunc='sum').reset_index().fillna(0)
        crops_ws_df = (crops_ws_df.reindex(sorted(crops_ws_df.columns), axis=1)
                                  .set_index('y')
                                  .reset_index()
                                  .rename(columns=app.constants.det_col))

        return crops_ws_df

    def __calculate_crops_ws_df(self):
        total_annual_technology_activity_by_mode = self.all_params['TotalAnnualTechnologyActivityByMode']  # noqa
        crops_ws_df = total_annual_technology_activity_by_mode[
            total_annual_technology_activity_by_mode.t.str.startswith('LNDAGR')
        ].drop('r', axis=1)
        return crops_ws_df
