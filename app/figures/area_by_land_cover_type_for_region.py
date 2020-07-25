from app.utilities import df_plot, df_filter
from app.constants import det_col


class AreaByLandCoverTypeForRegion:

    def __init__(self, all_params, years, land_use, region):
        self.all_params = all_params
        self.years = years
        self.land_use = land_use
        self.region = region

    def figure(self):
        print('Generating AreaByLandCoverTypeForRegion')

        regions = self.land_use.regions()
        mode_crop_combo = self.land_use.mode_crop_combo()
        crops = self.land_use.crops()
        land_cluster_df = self.calculate_land_total_df(self.all_params, self.years)
        land_cluster_df = land_cluster_df[land_cluster_df.t.str[6:9] == self.region]

        land_cluster_df['m'] = land_cluster_df['m'].astype(int)
        land_cluster_df['crop_combo'] = land_cluster_df['m'].map(mode_crop_combo)
        land_cluster_df['land_use'] = land_cluster_df['crop_combo'].str[0:4]
        land_cluster_df.drop(['m', 'crop_combo'], axis=1, inplace=True)

        land_cluster_df['value'] = land_cluster_df['value'].astype('float64')
        land_cluster_df = land_cluster_df.pivot_table(index='y',
                                                      columns='land_use',
                                                      values='value',
                                                      aggfunc='sum').reset_index().fillna(0)
        land_cluster_df['AGR'] = 0

        for crop in crops:
            if crop in land_cluster_df.columns:
                land_cluster_df['AGR'] += land_cluster_df[crop]
                land_cluster_df.drop(crop, axis=1, inplace=True)

        land_cluster_df = land_cluster_df.reindex(
            sorted(
                land_cluster_df.columns),
            axis=1).set_index('y').reset_index().rename(
                columns=det_col)
        return df_plot(land_cluster_df, 'Land area (1000 sq.km.)',
                'Area by land cover type (' + regions[self.region] + ' region)')

    def calculate_land_total_df(self, all_params, years):
        land_total_df = all_params['TotalAnnualTechnologyActivityByMode'][all_params['TotalAnnualTechnologyActivityByMode'].t.str.startswith(
            'LNDAGR')].drop('r', axis=1)
        return land_total_df
