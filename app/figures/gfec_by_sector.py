from app.utilities import df_plot, df_filter
import i18n
import functools


class GFECBySector:

    def __init__(self, all_params, years, plot_title):
        self.all_params = all_params
        self.years = years
        self.plot_title = plot_title
        self.index_column = 'y'

    def figure(self):
        return self.plot(self.data(), self.plot_title)

    def plot(self, data, title):
        return df_plot(data, i18n.t('label.energy_pj'), title)

    @functools.lru_cache()
    def data(self):
        total_technology_annual_activity = self.all_params['ProductionByTechnologyAnnual']
        gfec_df = total_technology_annual_activity[
            total_technology_annual_activity.t.str.startswith('DEM')
            ].drop('r', axis=1)
        gfec_df = gfec_df[~gfec_df.t.str.startswith('DEMAGRSUR')]
        gfec_df = gfec_df[~gfec_df.t.str.startswith('DEMAGRGWT')]
        gfec_df = gfec_df[~gfec_df.t.str.endswith('CRU')]
        return df_filter(gfec_df, 3, 6, ['PWR', 'LVS', 'PUB', 'FOR', 'COF'], self.years)
