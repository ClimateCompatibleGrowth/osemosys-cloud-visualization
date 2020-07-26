from collections import defaultdict
import os
import pandas as pd
import dash_html_components as html
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
from app.figures.area_by_crop_for_region import AreaByCropForRegion
from app.figures.area_by_land_cover_type_for_region import AreaByLandCoverTypeForRegion
from app.dash_figure import DashFigure
pd.set_option('mode.chained_assignment', None)


class GenerateDivs:
    def __init__(self, config):
        self.config = config
        self.all_divs = self.__figures_grouped_by_category()
        self.all_ids = self.__ids_by_category()

    def generate_divs(self):
        return html.Div([
            html.Div(
                    self.climate_divs(),
                    className='tab-pane',
                    id='nav-climate',
                    role='tabpanel',
                ),
            html.Div(
                    self.land_divs(),
                    className='tab-pane',
                    id='nav-land',
                    role='tabpanel',
                    ),
            html.Div(
                    self.energy_divs(),
                    className='tab-pane show active',
                    id='nav-energy',
                    role='tabpanel',
                    ),
            html.Div(
                    self.water_divs(),
                    className='tab-pane',
                    id='nav-water',
                    role='tabpanel',
                    ),
            ], className='tab-content', id='categoryTabContent'),

    def climate_divs(self):
        return self.all_divs['Climate']

    def land_divs(self):
        return self.all_divs['Land']

    def energy_divs(self):
        return self.all_divs['Energy']

    def water_divs(self):
        return self.all_divs['Water']

    def __all_figures(self):
        land_use = LandUse(self.config)
        results_path = self.config.csv_folder_path()
        result_parser = ResultParser(results_path)

        all_params = result_parser.all_params
        years = result_parser.years

        figure_list = [
                DashFigure(
                    iplot=PowerGenerationCapacity(all_params, years).figure(),
                    category='Energy',
                    id='power-generation-capacity',
                ),
                DashFigure(
                    iplot=PowerGenerationCapacityAggregate(all_params, years).figure(),
                    category='Energy',
                    id='power-generation-capacity-aggregate',
                ),
                DashFigure(
                    iplot=PowerGenerationDetail(all_params, years).figure(),
                    category='Energy',
                    id='power-generation-detail'
                ),
                DashFigure(
                    iplot=PowerGenerationAggregate(all_params, years).figure(),
                    category='Energy',
                    id='power-generation-aggregate'
                ),
                DashFigure(
                    iplot=PowerGenerationFuelUse(all_params, years).figure(),
                    category='Energy',
                    id='power-generation-fuel-use'
                ),
                DashFigure(
                    iplot=DomesticEnergyProduction(all_params, years).figure(),
                    category='Energy',
                    id='domestic-energy-production'
                ),
                DashFigure(
                    iplot=CapitalInvestment(all_params, years).figure(),
                    category='Energy',
                    id='capital-investment'
                ),
                DashFigure(
                    iplot=EnergyImports(all_params, years).figure(),
                    category='Energy',
                    id='energy-imports'
                ),
                DashFigure(
                    iplot=EnergyExports(all_params, years).figure(),
                    category='Energy',
                    id='energy-exports'
                ),
                DashFigure(
                    iplot=CostElectrictyGeneration(all_params, years).figure(),
                    category='Energy',
                    id='cost-electricty-generation'
                ),
                DashFigure(
                    iplot=AreaByCrop(all_params, years, land_use).figure(),
                    category='Land',
                    id='area-by-crop'
                ),
                DashFigure(
                    iplot=AreaByLandCover(all_params, years, land_use).figure(),
                    category='Land',
                    id='area-by-land-cover'
                ),
                DashFigure(
                    iplot=CropProduction(all_params, years).figure(),
                    category='Land',
                    id='crop-production'
                ),
                DashFigure(
                    iplot=CropYield(all_params, years, land_use).figure(),
                    category='Land',
                    id='crop-yield'
                ),
            ]

        for region in land_use.regions().keys():
            figure_list.append(
                DashFigure(
                    iplot=AreaByCropForRegion(all_params, years, land_use, region).figure(),
                    category='Land',
                    id=f'area-by-crop-{region}'
                ),
            )
            figure_list.append(
                DashFigure(
                    iplot=AreaByLandCoverTypeForRegion(all_params, years, land_use, region).figure(),
                    category='Land',
                    id=f'area-by-land-{region}'
                ),
            )

        return figure_list

    def __figures_grouped_by_category(self):
        grouped = defaultdict(lambda: [])
        for dash_figure in self.__all_figures():
            grouped[dash_figure.category].append(dash_figure.to_div())
        return grouped

    def __ids_by_category(self):
        grouped = defaultdict(lambda: [])
        for dash_figure in self.__all_figures():
            grouped[dash_figure.category].append(dash_figure.id)
        return grouped
