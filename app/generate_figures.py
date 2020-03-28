from app.figures import *
import os
import pandas as pd
from app.config import Config
from app.land_use import LandUse
from app.result_parser import ResultParser
pd.set_option('mode.chained_assignment', None)


def generate_figures(url):
    config = Config(url)
    land_use = LandUse(config)
    results_path = config.csv_folder_path()
    result_parser = ResultParser(results_path)

    all_params = result_parser.all_params
    years = result_parser.years

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
