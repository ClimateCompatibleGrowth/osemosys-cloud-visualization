import os
import pandas as pd


class ResultParser:
    all_params = {}
    _df_y_min = 9999
    _df_y_max = 0

    def __init__(self, results_path):
        self.results_path = results_path
        self.__parse_results()
        self.years = pd.Series(list(range(self._df_y_min, self._df_y_max)))

    def __parse_results(self):
        for each_file in os.listdir(self.results_path):
            df_param = pd.read_csv(os.path.join(self.results_path, each_file))
            param_name = df_param.columns[-1]
            df_param.rename(columns={param_name: 'value'}, inplace=True)
            self.all_params[param_name] = pd.DataFrame(df_param)
            if 'y' in df_param.columns:
                if self._df_y_min > df_param.y.min():
                    self._df_y_min = df_param.y.min()
                if self._df_y_max < df_param.y.max():
                    self._df_y_max = df_param.y.max()
