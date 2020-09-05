from collections import defaultdict
from app.generate_figures import GenerateFigures
from app.layout.checkboxes import Checkboxes
from app.layout.figure_set import FigureSet
import functools
import os
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
pd.set_option('mode.chained_assignment', None)


class GenerateDivs:
    def __init__(self, config):
        self.config = config
        self.ids_by_category = self.__ids_by_category()

    def generate_divs(self):
        return html.Div([
            html.Div(
                [
                    Checkboxes(self.__all_ids(), 'All').to_component(),
                    html.Div([figure.to_div() for figure in self.__all_figures()])
                ],
                className='tab-pane show active',
                id='nav-all',
                role='tabpanel',
                ),
            html.Div(
                [
                    Checkboxes(self.ids_by_category['Climate'], 'Climate').to_component(),
                    FigureSet(self.__all_figures(), 'Climate').to_component()
                ],
                className='tab-pane',
                id='nav-climate',
                role='tabpanel',
            ),
            html.Div(
                [
                    Checkboxes(self.ids_by_category['Land'], 'Land').to_component(),
                    FigureSet(self.__all_figures(), 'Land').to_component()
                ],
                className='tab-pane',
                id='nav-land',
                role='tabpanel',
            ),
            html.Div(
                [
                    Checkboxes(self.ids_by_category['Energy'], 'Energy').to_component(),
                    FigureSet(self.__all_figures(), 'Energy').to_component()
                ],
                className='tab-pane',
                id='nav-energy',
                role='tabpanel',
            ),
            html.Div(
                [
                    Checkboxes(self.ids_by_category['Water'], 'Water').to_component(),
                    FigureSet(self.__all_figures(), 'Water').to_component()
                ],
                className='tab-pane',
                id='nav-water',
                role='tabpanel',
             ),
            ], className='tab-content', id='categoryTabContent'),

    def __all_ids(self):
        return [figure.id for figure in self.__all_figures()]

    @functools.lru_cache(maxsize=128)
    def __all_figures(self):
        return GenerateFigures(self.config).all_figures()

    def __ids_by_category(self):
        grouped = defaultdict(lambda: [])
        for dash_figure in self.__all_figures():
            grouped[dash_figure.category].append(dash_figure.id)
        return grouped
