from app.utilities import df_plot, df_filter
import app.constants


class AreaByCrop:

    def __init__(self, all_params, years, land_use, plot_title):
        self.all_params = all_params
        self.years = years
        self.land_use = land_use
        self.plot_title = plot_title

    def figure(self):
        mode_crop_combo = self.land_use.mode_crop_combo()
        crops_total_df = self.__calculate_crops_total_df()
        crops_total_df['m'] = crops_total_df['m'].astype(int)
        crops_total_df['crop_combo'] = crops_total_df['m'].map(mode_crop_combo)
        crops_total_df['land_use'] = crops_total_df['crop_combo'].str[0:4]
        crops_total_df.drop(['m', 'crop_combo'], axis=1, inplace=True)

        crops_total_df = crops_total_df[crops_total_df['land_use'].str.startswith('CP')]
        crops_total_df = crops_total_df.pivot_table(index='y',
                                                    columns='land_use',
                                                    values='value',
                                                    aggfunc='sum').reset_index().fillna(0)
        crops_total_df = crops_total_df.reindex(
            sorted(
                crops_total_df.columns),
            axis=1).set_index('y').reset_index().rename(
                columns=app.constants.det_col).astype('float64')

        return df_plot(crops_total_df, 'Land area (1000 sq.km.)', self.plot_title)

    def __calculate_crops_total_df(self):
        total_annual_technology_activity_by_mode = self.all_params['TotalAnnualTechnologyActivityByMode']  # noqa
        crops_total_df = total_annual_technology_activity_by_mode[
            total_annual_technology_activity_by_mode.t.str.startswith('LNDAGR')
        ].drop('r', axis=1)
        return crops_total_df
