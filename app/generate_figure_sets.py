import functools
from app.land_use import LandUse
from app.result_parser import ResultParser
from app.dash_figure_set import DashFigureSet
from app.figures.gfec_by_sector import GFECBySector
from app.figures.gfec_by_fuel import GFECByFuel
from app.figures.power_generation_capacity import PowerGenerationCapacity
from app.figures.power_generation_detail import PowerGenerationDetail
from app.figures.power_generation_timeslice import PowerGenerationTimeslice
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
from app.figures.livestock_production import LivestockProduction
from app.figures.water_demand import WaterDemand
from app.figures.water_withdrawal_by_source import WaterWithdrawalBySource
from app.figures.water_balance import WaterBalance
from app.figures.emissions_by_sector import EmissionsBySector
from app.figures.emissions_by_fuel import EmissionsByFuel


class GenerateFigureSets:
    def __init__(self, configs):
        self.configs = configs

    def iplot_input_from(self, config):
        result_parser = ResultParser(config.csv_folder_path())
        return {
                    'config': config,
                    'land_use': LandUse(config),
                    'all_params': result_parser.all_params,
                    'years': result_parser.years,
               }

    @functools.lru_cache(maxsize=128)
    def __iplot_inputs(self):
        return [self.iplot_input_from(config) for config in self.configs]

    def all_figure_sets(self):
        figure_list = [
                DashFigureSet(
                    figures=[
                        GFECBySector(
                            iplot_input['all_params'],
                            iplot_input['years'],
                            iplot_input['config'].title()
                        ) for iplot_input in self.__iplot_inputs()
                    ],
                    category='Energy',
                    id='gfec-by-sector',
                    name='Gross final energy consumption - by sector',
                ),
                DashFigureSet(
                    figures=[
                        GFECByFuel(
                            iplot_input['all_params'],
                            iplot_input['years'],
                            iplot_input['config'].title()
                        ) for iplot_input in self.__iplot_inputs()
                    ],
                    category='Energy',
                    id='gfec-by-fuel',
                    name='Gross final energy consumption - by fuel',
                ),
                DashFigureSet(
                    figures=[
                        PowerGenerationCapacity(
                            iplot_input['all_params'],
                            iplot_input['years'],
                            iplot_input['config'].title()
                        ) for iplot_input in self.__iplot_inputs()
                    ],
                    category='Energy',
                    id='power-generation-capacity',
                    name='Power Generation Capacity (Detail)',
                ),
                DashFigureSet(
                    figures=[
                        PowerGenerationDetail(
                            iplot_input['all_params'],
                            iplot_input['years'],
                            iplot_input['config'].title()
                        ) for iplot_input in self.__iplot_inputs()
                    ],
                    category='Energy',
                    id='power-generation-detail',
                    name='Power Generation (Detail)',
                ),
                DashFigureSet(
                    figures=[
                        PowerGenerationTimeslice(
                            iplot_input['all_params'],
                            iplot_input['years'],
                            iplot_input['config'].title()
                        ) for iplot_input in self.__iplot_inputs()
                    ],
                    category='Energy',
                    id='power-generation-timeslice',
                    name='Power Generation (Timeslice)',
                ),
                DashFigureSet(
                    figures=[
                        PowerGenerationFuelUse(
                            iplot_input['all_params'],
                            iplot_input['years'],
                            iplot_input['config'].title()
                        ) for iplot_input in self.__iplot_inputs()
                    ],
                    category='Energy',
                    id='power-generation-fuel-use',
                    name='Power Generation (Fuel Use)',
                ),
                DashFigureSet(
                    figures=[
                        DomesticEnergyProduction(
                            iplot_input['all_params'],
                            iplot_input['years'],
                            iplot_input['config'].title()
                        ) for iplot_input in self.__iplot_inputs()
                    ],
                    category='Energy',
                    id='domestic-energy-production',
                    name='Domestic Energy Production',
                ),
                DashFigureSet(
                    figures=[
                        CapitalInvestment(
                            iplot_input['all_params'],
                            iplot_input['years'],
                            iplot_input['config'].title()
                        ) for iplot_input in self.__iplot_inputs()
                    ],
                    category='Energy',
                    id='capital-investment',
                    name='Capital Investment',
                ),
                DashFigureSet(
                    figures=[
                        EnergyImports(
                            iplot_input['all_params'],
                            iplot_input['years'],
                            iplot_input['config'].title()
                        ) for iplot_input in self.__iplot_inputs()
                    ],
                    category='Energy',
                    id='energy-imports',
                    name='Energy Imports',
                ),
                DashFigureSet(
                    figures=[
                        EnergyExports(
                            iplot_input['all_params'],
                            iplot_input['years'],
                            iplot_input['config'].title()
                        ) for iplot_input in self.__iplot_inputs()
                    ],
                    category='Energy',
                    id='energy-exports',
                    name='Energy Exports',
                ),
                DashFigureSet(
                    figures=[
                        CostElectrictyGeneration(
                            iplot_input['all_params'],
                            iplot_input['years'],
                            iplot_input['config'].title()
                        ) for iplot_input in self.__iplot_inputs()
                    ],
                    category='Energy',
                    id='cost-electricty-generation',
                    name='Cost Of Electricity Generation',
                ),
                DashFigureSet(
                    figures=[
                        AreaByCrop(
                            iplot_input['all_params'],
                            iplot_input['years'],
                            iplot_input['land_use'],
                            iplot_input['config'].title()
                        ) for iplot_input in self.__iplot_inputs()
                    ],
                    category='Land',
                    id='area-by-crop',
                    name='Area By Crop',
                ),
                DashFigureSet(
                    figures=[
                        AreaByLandCover(
                            iplot_input['all_params'],
                            iplot_input['years'],
                            iplot_input['land_use'],
                            iplot_input['config'].title()
                        ) for iplot_input in self.__iplot_inputs()
                    ],
                    category='Land',
                    id='area-by-land-cover',
                    name='Area By Land Cover Type',
                ),
                DashFigureSet(
                    figures=[
                        CropProduction(
                            iplot_input['all_params'],
                            iplot_input['years'],
                            iplot_input['config'].title()
                        ) for iplot_input in self.__iplot_inputs()
                    ],
                    category='Land',
                    id='crop-production',
                    name='Crop Production',
                ),
                DashFigureSet(
                    figures=[
                        CropYield(
                            iplot_input['all_params'],
                            iplot_input['years'],
                            iplot_input['land_use'],
                            iplot_input['config'].title()
                        ) for iplot_input in self.__iplot_inputs()
                    ],
                    category='Land',
                    id='crop-yield',
                    name='Yield',
                ),
                DashFigureSet(
                    figures=[
                        WaterDemand(
                            iplot_input['all_params'],
                            iplot_input['years'],
                            iplot_input['config'].title()
                        ) for iplot_input in self.__iplot_inputs()
                    ],
                    category='Water',
                    id='water-demand',
                    name='Water Demand',
                ),
                DashFigureSet(
                    figures=[
                        WaterWithdrawalBySource(
                            iplot_input['all_params'],
                            iplot_input['years'],
                            iplot_input['config'].title()
                        ) for iplot_input in self.__iplot_inputs()
                    ],
                    category='Water',
                    id='water-withdrawal-by-source',
                    name='Water Withdrawal By Source',
                ),
                DashFigureSet(
                    figures=[
                        WaterBalance(
                            iplot_input['all_params'],
                            iplot_input['years'],
                            iplot_input['config'].title()
                        ) for iplot_input in self.__iplot_inputs()
                    ],
                    category='Water',
                    id='water-balance',
                    name='Water Balance',
                ),
                DashFigureSet(
                    figures=[
                        EmissionsBySector(
                            iplot_input['all_params'],
                            iplot_input['years'],
                            iplot_input['config'].title()
                        ) for iplot_input in self.__iplot_inputs()
                    ],
                    category='Climate',
                    id='emissions-by-sector',
                    name='CO2 Emissions By Sector',
                ),
                DashFigureSet(
                    figures=[
                        EmissionsByFuel(
                            iplot_input['all_params'],
                            iplot_input['years'],
                            iplot_input['config'].title()
                        ) for iplot_input in self.__iplot_inputs()
                    ],
                    category='Climate',
                    id='emissions-by-fuel',
                    name='CO2 Emissions By Source',
                ),
                DashFigureSet(
                    figures=[
                        LivestockProduction(
                            iplot_input['all_params'],
                            iplot_input['years'],
                            iplot_input['config'].title()
                        ) for iplot_input in self.__iplot_inputs()
                    ],
                    category='Land',
                    id='livestock-production',
                    name='Livestock Production',
                ),
                DashFigureSet(
                    figures=[
                        AreaByCropIrrigated(
                            iplot_input['all_params'],
                            iplot_input['years'],
                            iplot_input['land_use'],
                            iplot_input['config'].title()
                        ) for iplot_input in self.__iplot_inputs()
                    ],
                    category='Land',
                    id='area-by-crop-irrigated',
                    name='Area By Crop (Irrigated)',
                ),
                DashFigureSet(
                    figures=[
                        AreaByCropRainfed(
                            iplot_input['all_params'],
                            iplot_input['years'],
                            iplot_input['land_use'],
                            iplot_input['config'].title()
                        ) for iplot_input in self.__iplot_inputs()
                    ],
                    category='Land',
                    id='area-by-crop-rainfed',
                    name='Area By Crop (Rainfed)',
                ),
            ]

        # Abstract away?
        first_land_use = self.__iplot_inputs()[0]['land_use']
        for region in first_land_use.regions().keys():
            figure_list.append(
                DashFigureSet(
                    figures=[
                        AreaByCropForRegion(
                            iplot_input['all_params'],
                            iplot_input['years'],
                            iplot_input['land_use'],
                            region,
                            iplot_input['config'].title()
                        ) for iplot_input in self.__iplot_inputs()
                    ],
                    category='Land',
                    id=f'area-by-crop-{region}',
                    name=f'Area by crop ({region})',
                ),
            )
            figure_list.append(
                DashFigureSet(
                    figures=[
                        AreaByLandCoverTypeForRegion(
                            iplot_input['all_params'],
                            iplot_input['years'],
                            iplot_input['land_use'],
                            region,
                            iplot_input['config'].title()
                        ) for iplot_input in self.__iplot_inputs()
                    ],
                    category='Land',
                    id=f'area-by-land-{region}',
                    name=f'Area by land cover type ({region})',
                ),
            )

        return figure_list
