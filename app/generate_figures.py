from input import input_path
from figures import fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig10
import os
import pandas as pd

def generate_figures(url):
    results_path = input_path(url)

    all_params = {}
    df_y_min = 9999
    df_y_max = 0

    for each_file in os.listdir(results_path):
        df_param = pd.read_csv(os.path.join(results_path, each_file))
        param_name = df_param.columns[-1]
        df_param.rename(columns={param_name:'value'}, inplace=True)
        all_params[param_name] = pd.DataFrame(df_param)
        if 'y' in df_param.columns:
            if df_y_min > df_param.y.min():
                df_y_min = df_param.y.min()
            if df_y_max < df_param.y.max():
                df_y_max = df_param.y.max()

    years = pd.Series(list(range(df_y_min,df_y_max)))

    return [
        fig1(all_params,years),
        fig2(all_params,years),
        fig3(all_params,years),
        fig4(all_params,years),
        fig5(all_params,years),
        fig6(all_params,years),
        fig7(all_params,years),
        fig8(all_params,years),
        fig9(all_params,years),
        fig10(all_params,years),
    ]
