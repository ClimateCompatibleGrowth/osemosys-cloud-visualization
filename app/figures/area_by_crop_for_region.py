from app.utilities import df_plot, df_filter, df_years
import app.constants


class AreaByCropForRegion:

    def __init__(self, all_params, years, land_use, region, plot_title):
        self.all_params = all_params
        self.years = years
        self.land_use = land_use
        self.region = region
        self.plot_title = plot_title

    def figure(self):
        return self.plot(self.data(), self.plot_title)

    def plot(self, data, title):
        return df_plot(data, 'Land area (1000 sq.km.)', title)

    def data(self):
        regions = self.land_use.regions()
        mode_crop_combo = self.land_use.mode_crop_combo()
        crops_region_df = self.__calculate_crops_total_df()
        crops_region_df = crops_region_df[crops_region_df.t.str[6:9] == self.region]

        crops_region_df['m'] = crops_region_df['m'].astype(int)
        crops_region_df['crop_combo'] = crops_region_df['m'].map(mode_crop_combo)
        crops_region_df['land_use'] = crops_region_df['crop_combo'].str[0:4]
        crops_region_df.drop(['m', 'crop_combo'], axis=1, inplace=True)

        crops_region_df = crops_region_df[crops_region_df['land_use'].str.startswith('CP')]
        crops_region_df = crops_region_df.pivot_table(index='y',
                                                      columns='land_use',
                                                      values='value',
                                                      aggfunc='sum').reset_index().fillna(0)
        crops_region_df = crops_region_df.reindex(
            sorted(
                crops_region_df.columns),
            axis=1).set_index('y').reset_index().rename(
                columns=app.constants.det_col).astype('float64')
        crops_region_df = df_years(crops_region_df, self.years)
        return crops_region_df

    def __calculate_crops_total_df(self):
        total_annual_technology_activity_by_mode = self.all_params['TotalAnnualTechnologyActivityByMode']  # noqa
        crops_total_df = total_annual_technology_activity_by_mode[
            total_annual_technology_activity_by_mode.t.str.startswith('LNDAGR')
        ].drop('r', axis=1)
        return crops_total_df
