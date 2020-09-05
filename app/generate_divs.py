from collections import defaultdict
from app.generate_figures import GenerateFigures
from app.layout.checkboxes import Checkboxes
import os
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
pd.set_option('mode.chained_assignment', None)


class GenerateDivs:
    def __init__(self, config):
        self.config = config
        self.divs_by_category = self.__figures_grouped_by_category()
        self.ids_by_category = self.__ids_by_category()

    def generate_divs(self):
        return html.Div([
            html.Div(
                [
                    Checkboxes(self.__all_ids(), 'All').to_component(),
                    html.Div(self.__all_divs()),
                ],
                className='tab-pane show active',
                id='nav-all',
                role='tabpanel',
                ),
            html.Div(
                [
                    Checkboxes(self.ids_by_category['Climate'], 'Climate').to_component(),
                    html.Div(self.__climate_divs()),
                ],
                className='tab-pane',
                id='nav-climate',
                role='tabpanel',
            ),
            html.Div(
                [
                    Checkboxes(self.ids_by_category['Land'], 'Land').to_component(),
                    html.Div(self.__land_divs()),
                ],
                className='tab-pane',
                id='nav-land',
                role='tabpanel',
            ),
            html.Div(
                [
                    Checkboxes(self.ids_by_category['Energy'], 'Energy').to_component(),
                    html.Div(self.__energy_divs()),
                ],
                className='tab-pane',
                id='nav-energy',
                role='tabpanel',
            ),
            html.Div(
                [
                    Checkboxes(self.ids_by_category['Water'], 'Water').to_component(),
                    html.Div(self.__water_divs()),
                ],
                className='tab-pane',
                id='nav-water',
                role='tabpanel',
             ),
            ], className='tab-content', id='categoryTabContent'),

    def __climate_divs(self):
        return self.divs_by_category['Climate']

    def __land_divs(self):
        return self.divs_by_category['Land']

    def __energy_divs(self):
        return self.divs_by_category['Energy']

    def __water_divs(self):
        return self.divs_by_category['Water']

    def __all_divs(self):
        return self.flatten(list(self.divs_by_category.values()))

    def __all_ids(self):
        return self.flatten(list(self.ids_by_category.values()))

    def __all_figures(self):
        return GenerateFigures(self.config).all_figures()

    def __figures_grouped_by_category(self):
        grouped = defaultdict(lambda: [])
        for dash_figure in self.__all_figures():
            grouped[dash_figure.category].append(dash_figure.to_div())
        return grouped

    def __ids_by_category(self):
        grouped = defaultdict(lambda: [])
        for dash_figure in self.__all_figures():
            grouped[dash_figure.category].append(dash_figure.id)
        return grouped

    def flatten(self, list_of_lists):
        return [item for sublist in list_of_lists for item in sublist]
