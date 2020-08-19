from app.utilities import df_plot, df_filter
from app.constants import det_col


class AreaByCropIrrigated:

    def __init__(self, all_params, years, land_use):
        self.all_params = all_params
        self.years = years
        self.land_use = land_use

    def figure(self):
        print('Generating AreaByCropIrrigated')
        mode_crop_combo = self.land_use.mode_crop_combo()
        crops_ws_df = self.__calculate_crops_ws_df()
        crops_ws_df['m'] = crops_ws_df['m'].astype(int)
        crops_ws_df['crop_combo'] = crops_ws_df['m'].map(mode_crop_combo)
        crops_ws_df = crops_ws_df[(crops_ws_df.crop_combo.str.startswith('CP'))
                                  & (crops_ws_df.crop_combo.str[5:6] == 'I')]
        crops_ws_df['land_use'] = crops_ws_df['crop_combo'].str[0:4]
        crops_ws_df.drop(['m', 'crop_combo'], axis=1, inplace=True)
        crops_ws_df = crops_ws_df.pivot_table(index='y',
                                              columns='land_use',
                                              values='value',
                                              aggfunc='sum').reset_index().fillna(0)
        crops_ws_df = (crops_ws_df.reindex(sorted(crops_ws_df.columns), axis=1)
                                  .set_index('y')
                                  .reset_index()
                                  .rename(columns=det_col))
        return df_plot(crops_ws_df, 'Land area (1000 sq.km.)', 'Area by crop (Irrigated)')

    def __calculate_crops_ws_df(self):
        total_annual_technology_activity_by_mode = self.all_params['TotalAnnualTechnologyActivityByMode']  # noqa
        crops_ws_df = total_annual_technology_activity_by_mode[
            total_annual_technology_activity_by_mode.t.str.startswith('LNDAGR')
        ].drop('r', axis=1)
        return crops_ws_df
