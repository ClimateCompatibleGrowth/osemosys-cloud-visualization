import os
import sys
import pandas as pd
import app.constants
pd.set_option('mode.chained_assignment', None)


def df_plot(df, y_title, p_title):
    return df.iplot(asFigure=True,
                    x='y',
                    kind='bar',
                    barmode='relative',
                    xTitle='Year',
                    yTitle=y_title,
                    color=[app.constants.color_dict[x] for x in df.columns if x != 'y'],
                    title=p_title,
                    showlegend=True)


def df_filter(df, lb, ub, t_exclude, years):
    df['t'] = df['t'].str[lb:ub]
    df['value'] = df['value'].astype('float64')
    df = df[~df['t'].isin(t_exclude)].pivot_table(index='y',
                                                  columns='t',
                                                  values='value',
                                                  aggfunc='sum').reset_index().fillna(0)
    df = df.reindex(sorted(df.columns), axis=1).set_index('y').reset_index().rename(columns=app.constants.det_col)  # noqa
    df = df_years(df, years)
    return df


def df_years(df, years):
    new_df = pd.DataFrame()
    new_df['y'] = years
    new_df['y'] = new_df['y'].astype(int)
    df['y'] = df['y'].astype(int)
    new_df = pd.merge(new_df, df, how='outer', on='y').fillna(0)
    return new_df
