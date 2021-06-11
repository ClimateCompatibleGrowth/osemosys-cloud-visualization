from app.utilities import df_plot, df_filter
import app.constants
import i18n


class EmissionsByFuel:

    def __init__(self, all_params, years, plot_title):
        self.all_params = all_params
        self.years = years
        self.plot_title = plot_title
        self.index_column = 'y'

    def figure(self):
        return self.plot(self.data(), self.plot_title)

    def plot(self, data, title):
        return data.iplot(
                asFigure=True,
                x='y',
                kind='bar',
                barmode='relative',
                xTitle=i18n.t('label.year'),
                yTitle=i18n.t('label.million_tonnes_co2'),
                color=[app.constants.color_dict[x] for x in data.columns if x != 'y'],
                title=title,
                showlegend=True
                )

    def data(self):
        annual_technology_emission = self.all_params['AnnualTechnologyEmission']
        emissions_df = annual_technology_emission[
            annual_technology_emission.t.str.startswith('DEM') |
            annual_technology_emission.t.str.startswith('MIN') |
            annual_technology_emission.t.str.startswith('LND')
            ].drop('r', axis=1)
        emissions_df = emissions_df.loc[~emissions_df['e'].str[:3].isin(['DUM'])]
        emissions_df.t.replace('MINGAS', 'MINPWRGAS', inplace=True)
        emissions_df.t.replace('MINCOA', 'MINPWRCOA', inplace=True)
        
        emissions_df.t.replace('LNDMAIHR', 'LNDAGRLND', inplace=True)
        emissions_df.t.replace('LNDRICHR', 'LNDAGRLND', inplace=True)
        emissions_df.t.replace('LNDMAIHI', 'LNDAGRLND', inplace=True)
        emissions_df.t.replace('LNDRICHI', 'LNDAGRLND', inplace=True)
        emissions_df.t.replace('LNDFOR', 'LNDFORLND', inplace=True)
        return df_filter(emissions_df, 6, 9, [], self.years)
