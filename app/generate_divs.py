from collections import defaultdict
import os
import pandas as pd
import dash_core_components as dcc
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
from app.figures.area_by_crop_irrigated import AreaByCropIrrigated
from app.figures.area_by_crop_rainfed import AreaByCropRainfed
from app.figures.water_demand import WaterDemand
from app.figures.water_withdrawal_by_source import WaterWithdrawalBySource
from app.figures.water_balance import WaterBalance
from app.figures.emissions_by_sector import EmissionsBySector
from app.figures.emissions_by_fuel import EmissionsByFuel
from app.figures.livestock_production import LivestockProduction
from app.figures.water_demand import WaterDemand
from app.figures.water_withdrawal_by_source import WaterWithdrawalBySource
from app.figures.water_balance import WaterBalance
from app.dash_figure import DashFigure
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
                    self.__checkboxes(self.all_ids(), 'All'),
                    html.Div(
                        self.all_divs()
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
                        self.climate_divs()
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
                        self.land_divs()
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
                        self.energy_divs()
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
                        self.water_divs()
                    ),
                ],
                className='tab-pane',
                id='nav-water',
                role='tabpanel',
             ),
            ], className='tab-content', id='categoryTabContent'),

    def climate_divs(self):
        return self.divs_by_category['Climate']

    def land_divs(self):
        return self.divs_by_category['Land']

    def energy_divs(self):
        return self.divs_by_category['Energy']

    def water_divs(self):
        return self.divs_by_category['Water']

    def all_divs(self):
        return self.flatten(list(self.divs_by_category.values()))

    def all_ids(self):
        return self.flatten(list(self.ids_by_category.values()))

    def __all_figures(self):
        land_use = LandUse(self.config)
        results_path = self.config.csv_folder_path()
        result_parser = ResultParser(results_path)

        all_params = result_parser.all_params
        years = result_parser.years

        figure_list = [
                DashFigure(
                    iplot=PowerGenerationCapacity(all_params, years),
                    category='Energy',
                    id='power-generation-capacity',
                ),
                DashFigure(
                    iplot=PowerGenerationCapacityAggregate(all_params, years),
                    category='Energy',
                    id='power-generation-capacity-aggregate',
                ),
                DashFigure(
                    iplot=PowerGenerationDetail(all_params, years),
                    category='Energy',
                    id='power-generation-detail'
                ),
                DashFigure(
                    iplot=PowerGenerationAggregate(all_params, years),
                    category='Energy',
                    id='power-generation-aggregate'
                ),
                DashFigure(
                    iplot=PowerGenerationFuelUse(all_params, years),
                    category='Energy',
                    id='power-generation-fuel-use'
                ),
                DashFigure(
                    iplot=DomesticEnergyProduction(all_params, years),
                    category='Energy',
                    id='domestic-energy-production'
                ),
                DashFigure(
                    iplot=CapitalInvestment(all_params, years),
                    category='Energy',
                    id='capital-investment'
                ),
                DashFigure(
                    iplot=EnergyImports(all_params, years),
                    category='Energy',
                    id='energy-imports'
                ),
                DashFigure(
                    iplot=EnergyExports(all_params, years),
                    category='Energy',
                    id='energy-exports'
                ),
                DashFigure(
                    iplot=CostElectrictyGeneration(all_params, years),
                    category='Energy',
                    id='cost-electricty-generation'
                ),
                DashFigure(
                    iplot=AreaByCrop(all_params, years, land_use),
                    category='Land',
                    id='area-by-crop'
                ),
                DashFigure(
                    iplot=AreaByLandCover(all_params, years, land_use),
                    category='Land',
                    id='area-by-land-cover'
                ),
                DashFigure(
                    iplot=CropProduction(all_params, years),
                    category='Land',
                    id='crop-production'
                ),
                DashFigure(
                    iplot=CropYield(all_params, years, land_use),
                    category='Land',
                    id='crop-yield'
                ),
                DashFigure(
                    iplot=WaterDemand(all_params, years),
                    category='Water',
                    id='water-demand'
                ),
                DashFigure(
                    iplot=WaterWithdrawalBySource(all_params, years),
                    category='Water',
                    id='water-withdrawal-by-source'
                ),
                DashFigure(
                    iplot=WaterBalance(all_params, years),
                    category='Water',
                    id='water-balance'
                ),
                DashFigure(
                    iplot=EmissionsBySector(all_params, years),
                    category='Climate',
                    id='emissions-by-sector'
                ),
                DashFigure(
                    iplot=EmissionsByFuel(all_params, years),
                    category='Climate',
                    id='emissions-by-fuel'
                ),
                DashFigure(
                    iplot=LivestockProduction(all_params, years),
                    category='Land',
                    id='livestock-production'
                ),
                DashFigure(
                    iplot=AreaByCropIrrigated(all_params, years, land_use),
                    category='Land',
                    id='area-by-crop-irrigated'
                ),
                DashFigure(
                    iplot=AreaByCropRainfed(all_params, years, land_use),
                    category='Land',
                    id='area-by-crop-rainfed'
                ),
            ]

        for region in land_use.regions().keys():
            figure_list.append(
                DashFigure(
                    iplot=AreaByCropForRegion(all_params, years, land_use, region),
                    category='Land',
                    id=f'area-by-crop-{region}'
                ),
            )
            figure_list.append(
                DashFigure(
                    iplot=AreaByLandCoverTypeForRegion(all_params, years, land_use, region),
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
