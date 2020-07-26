import dash_core_components as dcc
import dash_html_components as html
import random


class DashFigure:
    def __init__(self, iplot):
        self.iplot = iplot

    def to_div(self, id=''):
        random_number = random.randint(1, 99999)
        if id is '':
            id = random_number
        return html.Div(dcc.Graph(figure=self.iplot), className=f'figure figure-{id}')
