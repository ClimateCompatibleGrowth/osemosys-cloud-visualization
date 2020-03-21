import os
import pandas as pd


class LandUse:
    technologies = []
    commodities = []

    def __init__(self, config):
        self.config = config
        self.__parse_file()

    def regions(self):
        # Construct dictionary of regions {region_code:region_name}.
        # Region codes are extracted from the data file
        regions_list = sorted(list(set([x[6:-3] for x in self.technologies if x.startswith('LNDAGR')])))
        regions = {}

        for each in regions_list:
            regions[each] = each

        return regions

    def mode_crop_combo(self):
        # Construct dictionary mapping modes to crop combos {mode:crop_combo}
        crop_list = sorted(list(set([x[1:5] for x in self.commodities if x.startswith('LCP')])))
        crop_order = ['HI', 'II', 'HR', 'IR', 'LR']
        crop_combo = []

        for each_crop in crop_list:
            for each_combo in crop_order:
                crop_combo.append(each_crop + each_combo)

        for each in ['BAR', 'FOR', 'GRS', 'BLT', 'WAT', 'OTH']:
            crop_combo.append(each)

        return dict([(m, c) for m, c in zip(range(1, len(crop_combo) + 1), crop_combo)])

    def crops(self):
        # Construct dictionary of crops {crop_code:crop_name}.
        # Crop codes and names are extracted from the 'name_color_codes.csv' file
        crops = {}
        for each in self.__det_col().keys():
            if each.startswith('CP'):
                crops[each] = self.__det_col()[each]

        return crops

    def water_supply(self):
        return {'I': 'Irrigated', 'R': 'Rain-fed'}

    def input_level(self):
        return {'L': 'Low', 'I': 'Intermediate', 'H': 'High'}

    def __parse_file(self):
        with open(os.path.join(os.getcwd(), 'data', 'indonesia', 'data.txt'), 'r') as f:
            for line in f:
                if line.startswith(('set TECHNOLOGY')):
                    self.technologies = line.split(' ')[3:]
                if line.startswith(('set COMMODITY', 'set FUEL')):
                    self.commodities = line.split(' ')[3:]

    def __det_col(self):
        name_color_codes = pd.read_csv(
            os.path.join(
                os.getcwd(),
                'name_color_codes.csv'),
            encoding='latin-1')
        return dict([(c, n) for c, n in zip(name_color_codes.code, name_color_codes.name_english)])
