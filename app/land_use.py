import os
import pandas as pd
import app.constants


class LandUse:
    technologies = []
    commodities = []

    def __init__(self, config):
        self.config = config
        self.__parse_file()

    def regions(self):
        # Construct dictionary of regions {region_code:region_name}.
        # Region codes are extracted from the data file
        regions_list = sorted(
                list(set([x[6:9] for x in self.technologies if x.startswith('LNDAGR')]))
            )
        regions = {}

        for each in regions_list:
            regions[each] = each

        return regions

    def mode_crop_combo(self):
        # Construct dictionary mapping modes to crop combos {mode:crop_combo}
        crop_combo_dict = dict(self.data_inp)  # noqa

        # Use custom dict below for CLEWs training workshop model (2020)
        '''
        crop_combo_dict = {1: 'CP01IR',
                           2: 'CP02IR',
                           3: 'CP01II',
                           4: 'CP02II',
                           5: 'FOR',
                           6: 'BLT',
                           7: 'WAT',
                           8: 'CP01HI',
                           9: 'NPA',
                           10: 'IPA'}
        '''
        return crop_combo_dict

    def crops(self):
        # Construct dictionary of crops {crop_code:crop_name}.
        # Crop codes and names are extracted from the 'name_color_codes.csv' file
        crops = {}
        for each in app.constants.det_col.keys():
            if each.startswith('CP'):
                crops[each] = app.constants.det_col[each]

        return crops

    def water_supply(self):
        return {'I': 'Irrigated', 'R': 'Rain-fed'}

    def input_level(self):
        return {'L': 'Low', 'I': 'Intermediate', 'H': 'High'}

    def __parse_file(self):
        parsing = False
        self.data_inp = []
        self.crop_list = []

        with open(self.config.data_file_path(), 'r') as f:
            for line in f:
                if line.startswith(";"):
                    parsing = False
                if line.startswith(('set TECHNOLOGY')):
                    self.technologies = line.split(' ')[3:]
                if line.startswith(('set COMMODITY', 'set FUEL')):
                    self.commodities = line.split(' ')[3:] 
                    for c in self.commodities:
                        if c.startswith('CRP'):
                            if c[3:].startswith('CP'):
                                self.crop_list.append(c[3:7])
                            else:
                                self.crop_list.append(c[3:6])
                if line.startswith(('set YEAR')):
                    year_list = line.split(' ')[3:-1]
                    start_year = year_list[0]

                if parsing:
                    if line.startswith('['):
                        fuel = line.split(',')[2]
                        tech = line.split(',')[1]
                    elif not line.startswith(start_year):
                        values = line.rstrip().split(' ')[1:]
                        mode = line.split(' ')[0]
                        
                        if tech.startswith('LNDAGR'):
                            if fuel.startswith('L'):
                                if fuel[1:3].startswith('CP'):
                                    crop_combo = fuel[1:7]
                                else:
                                    if fuel[1:4] in self.crop_list:
                                        crop_combo = fuel[1:6]
                                    else:
                                        crop_combo = fuel[1:4]
                                if not fuel.startswith('LND'):
                                    self.data_inp.append(tuple([int(mode), crop_combo]))

                if line.startswith(('param InputActivityRatio')):
                    parsing = True
