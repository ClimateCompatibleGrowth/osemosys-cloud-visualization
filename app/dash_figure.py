import dash_core_components as dcc
import dash_html_components as html


class DashFigure:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def to_div(self):
        return html.Div(dcc.Graph(figure=self.dataframe), className='figure')
