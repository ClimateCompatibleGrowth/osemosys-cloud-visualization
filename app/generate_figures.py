from figures import *
import os
import pandas as pd
from config import Config
from land_use import LandUse
pd.set_option('mode.chained_assignment', None)


def generate_figures(url):
    config = Config(url)
    land_use = LandUse(config)
    results_path = config.csv_folder_path()

    all_params = {}
    df_y_min = 9999
    df_y_max = 0

    for each_file in os.listdir(results_path):
        df_param = pd.read_csv(os.path.join(results_path, each_file))
        param_name = df_param.columns[-1]
        df_param.rename(columns={param_name: 'value'}, inplace=True)
        all_params[param_name] = pd.DataFrame(df_param)
        if 'y' in df_param.columns:
            if df_y_min > df_param.y.min():
                df_y_min = df_param.y.min()
            if df_y_max < df_param.y.max():
                df_y_max = df_param.y.max()

    years = pd.Series(list(range(df_y_min, df_y_max)))

    figure_list = [
            fig1(all_params, years),
            fig2(all_params, years),
            fig3(all_params, years),
            fig4(all_params, years),
            fig5(all_params, years),
            fig6(all_params, years),
            fig7(all_params, years),
            fig8(all_params, years),
            fig9(all_params, years),
            fig10(all_params, years),
            fig11a(all_params, years, land_use),
            fig12a(all_params, years, land_use),
            fig13(all_params, years),
            fig14(all_params, years, land_use),
        ]

    for region in land_use.regions().keys():
        figure_list.append(fig11b(all_params, years, land_use, region))
        figure_list.append(fig12b(all_params, years, land_use, region))
        # figure_list.append(fig11c(all_params,years,region))

    return figure_list
