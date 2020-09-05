import dash_html_components as html
from collections import defaultdict
import functools


class FigureSet:
    def __init__(self, all_figures, category):
        self.all_figures = all_figures
        self.category = category

    def to_component(self):
        figures_in_category = self.__figures_by_category()[self.category]
        return html.Div([figure.to_div() for figure in figures_in_category])

    def __figures_by_category(self):
        grouped = defaultdict(lambda: [])
        for dash_figure in self.all_figures:
            grouped[dash_figure.category].append(dash_figure)
        return grouped
