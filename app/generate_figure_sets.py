import functools
import i18n
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
                    id='gfec_by_sector',
                    name=i18n.t('figure.gfec_by_sector'),
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
                    id='gfec_by_fuel',
                    name=i18n.t('figure.gfec_by_fuel'),
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
                    id='power_generation_capacity_detail',
                    name=i18n.t('figure.power_generation_capacity_detail'),
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
                    id='power_generation_detail',
                    name=i18n.t('figure.power_generation_detail'),
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
                    id='power_generation_timeslice',
                    name=i18n.t('figure.power_generation_timeslice'),
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
                    id='power_generation_fuel_use',
                    name=i18n.t('figure.power_generation_fuel_use'),
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
                    id='domestic_energy_production',
                    name=i18n.t('figure.domestic_energy_production'),
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
                    id='capital_investment',
                    name=i18n.t('figure.capital_investment'),
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
                    id='energy_imports',
                    name=i18n.t('figure.energy_imports'),
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
                    id='energy_exports',
                    name=i18n.t('figure.energy_exports'),
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
                    id='cost_of_electricity_generation',
                    name=i18n.t('figure.cost_of_electricity_generation'),
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
                    id='area_by_crop',
                    name=i18n.t('figure.area_by_crop'),
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
                    id='area_by_land',
                    name=i18n.t('figure.area_by_land'),
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
                    id='crop_production',
                    name=i18n.t('figure.crop_production'),
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
                    id='yield',
                    name=i18n.t('figure.yield'),
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
                    id='water_demand',
                    name=i18n.t('figure.water_demand'),
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
                    id='water_withdrawal_by_source',
                    name=i18n.t('figure.water_withdrawal_by_source'),
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
                    id='water_balance',
                    name=i18n.t('figure.water_balance'),
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
                    id='emissions_by_sector',
                    name=i18n.t('figure.emissions_by_sector'),
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
                    id='emissions_by_fuel',
                    name=i18n.t('figure.emissions_by_fuel'),
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
                    id='livestock_production',
                    name=i18n.t('figure.livestock_production'),
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
                    id='area_by_crop_irrigated',
                    name=i18n.t('figure.area_by_crop_irrigated'),
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
                    id='area_by_crop_rainfed',
                    name=i18n.t('figure.area_by_crop_rainfed'),
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
                    id=f'area_by_crop_region_i18n_{region}',
                    name=i18n.t('figure.area_by_crop_region', region=region),
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
                    id=f'area_by_land_cover_type_region_i18n_{region}',
                    name=i18n.t('figure.area_by_land_cover_type_region', region=region),
                ),
            )

        return figure_list
