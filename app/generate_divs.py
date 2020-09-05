from collections import defaultdict
from app.generate_figures import GenerateFigures
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
                    self.__checkboxes(self.__all_ids(), 'All'),
                    html.Div(
                        self.__all_divs()
                    ),
                ],
                className='tab-pane show active',
                id='nav-all',
                role='tabpanel',
                ),
            html.Div(
                [
                    self.__checkboxes(self.ids_by_category['Climate'], 'Climate'),
                    html.Div(
                        self.__climate_divs()
                    ),
                ],
                className='tab-pane',
                id='nav-climate',
                role='tabpanel',
            ),
            html.Div(
                [
                    self.__checkboxes(self.ids_by_category['Land'], 'Land'),
                    html.Div(
                        self.__land_divs()
                    ),
                ],
                className='tab-pane',
                id='nav-land',
                role='tabpanel',
            ),
            html.Div(
                [
                    self.__checkboxes(self.ids_by_category['Energy'], 'Energy'),
                    html.Div(
                        self.__energy_divs()
                    ),
                ],
                className='tab-pane',
                id='nav-energy',
                role='tabpanel',
            ),
            html.Div(
                [
                    self.__checkboxes(self.ids_by_category['Water'], 'Water'),
                    html.Div(
                        self.__water_divs()
                    ),
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

    def __checkboxes(self, ids, category):
        return dcc.Checklist(
            options=[
                {'label': id.replace('-', ' ').title(), 'value': id} for id in ids
            ],
            value=ids,
            id={'type': 'checkboxes', 'index': category},
            persistence=True,
            className='form-check checkbox-container',
            inputClassName='form-check-input custom-checkbox',
            labelClassName='form-check-label'
        )

    def __ids_by_category(self):
        grouped = defaultdict(lambda: [])
        for dash_figure in self.__all_figures():
            grouped[dash_figure.category].append(dash_figure.id)
        return grouped

    def flatten(self, list_of_lists):
        return [item for sublist in list_of_lists for item in sublist]
