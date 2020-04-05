from app.old_figures import *
import os
import pandas as pd
from app.config import Config
from app.land_use import LandUse
from app.result_parser import ResultParser
from app.figures.power_generation_capacity import PowerGenerationCapacity
from app.figures.power_generation_capacity_aggregate import PowerGenerationCapacityAggregate
from app.figures.power_generation_detail import PowerGenerationDetail
from app.figures.power_generation_aggregate import PowerGenerationAggregate
from app.figures.power_generation_fuel_use import PowerGenerationFuelUse
from app.figures.domestic_energy_production import DomesticEnergyProduction
from app.figures.capital_investment import CapitalInvestment
from app.figures.energy_imports import EnergyImports
from app.figures.energy_exports import EnergyExports
from app.figures.cost_electricity_generation import CostElectrictyGeneration
from app.figures.area_by_crop import AreaByCrop
from app.figures.area_by_land_cover import AreaByLandCover
from app.figures.crop_production import CropProduction
from app.figures.crop_yield import CropYield
pd.set_option('mode.chained_assignment', None)


def generate_figures(url):
    config = Config(url)
    land_use = LandUse(config)
    results_path = config.csv_folder_path()
    result_parser = ResultParser(results_path)

    all_params = result_parser.all_params
    years = result_parser.years

    figure_list = [
            PowerGenerationCapacity(all_params, years).figure(),
            PowerGenerationCapacityAggregate(all_params, years).figure(),
            PowerGenerationDetail(all_params, years).figure(),
            PowerGenerationAggregate(all_params, years).figure(),
            PowerGenerationFuelUse(all_params, years).figure(),
            DomesticEnergyProduction(all_params, years).figure(),
            CapitalInvestment(all_params, years).figure(),
            EnergyImports(all_params, years).figure(),
            EnergyExports(all_params, years).figure(),
            CostElectrictyGeneration(all_params, years).figure(),
            AreaByCrop(all_params, years, land_use).figure(),
            AreaByLandCover(all_params, years, land_use).figure(),
            CropProduction(all_params, years).figure(),
            CropYield(all_params, years, land_use).figure(),
        ]

    for region in land_use.regions().keys():
        figure_list.append(fig11b(all_params, years, land_use, region))
        figure_list.append(fig12b(all_params, years, land_use, region))
        # figure_list.append(fig11c(all_params,years,region))

    return figure_list
