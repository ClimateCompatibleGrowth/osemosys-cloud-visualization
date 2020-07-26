import dash_core_components as dcc
import dash_html_components as html


class DashFigure:
    def __init__(self, iplot):
        self.iplot = iplot

    def to_div(self):
        return html.Div(dcc.Graph(figure=self.iplot), className='figure')
