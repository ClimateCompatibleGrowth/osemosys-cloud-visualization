from app.land_use import LandUse
from app.result_parser import ResultParser
from app.dash_figure_set import DashFigureSet
from app.figures.gfec_by_sector import GFECBySector
from app.figures.gfec_by_fuel import GFECByFuel
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
from app.figures.livestock_production import LivestockProduction
from app.figures.water_demand import WaterDemand
from app.figures.water_withdrawal_by_source import WaterWithdrawalBySource
from app.figures.water_balance import WaterBalance
from app.figures.emissions_by_sector import EmissionsBySector
from app.figures.emissions_by_fuel import EmissionsByFuel


class GenerateFigures:
    def __init__(self, config):
        self.config = config

    def all_figure_sets(self):
        land_use = LandUse(self.config)
        results_path = self.config.csv_folder_path()
        result_parser = ResultParser(results_path)

        all_params = result_parser.all_params
        years = result_parser.years

        figure_list = [
                DashFigureSet(
                    iplots=[GFECBySector(all_params, years, self.config.title())],
                    category='Energy',
                    id='gfec-by-sector',
                    name='Gross final energy consumption - by sector',
                ),
                DashFigureSet(
                    iplots=[GFECByFuel(all_params, years, self.config.title())],
                    category='Energy',
                    id='gfec-by-fuel',
                    name='Gross final energy consumption - by fuel',
                ),
                DashFigureSet(
                    iplots=[PowerGenerationCapacity(all_params, years, self.config.title())],
                    category='Energy',
                    id='power-generation-capacity',
                    name='Power Generation Capacity (Detail)',
                ),
                DashFigureSet(
                    iplots=[PowerGenerationCapacityAggregate(
                        all_params, years, self.config.title()
                    )],
                    category='Energy',
                    id='power-generation-capacity-aggregate',
                    name='Power Generation Capacity (Aggregate)',
                ),
                DashFigureSet(
                    iplots=[PowerGenerationDetail(all_params, years, self.config.title())],
                    category='Energy',
                    id='power-generation-detail',
                    name='Power Generation (Detail',
                ),
                DashFigureSet(
                    iplots=[PowerGenerationAggregate(all_params, years, self.config.title())],
                    category='Energy',
                    id='power-generation-aggregate',
                    name='Power Generation (Aggregate)',
                ),
                DashFigureSet(
                    iplots=[PowerGenerationFuelUse(all_params, years, self.config.title())],
                    category='Energy',
                    id='power-generation-fuel-use',
                    name='Power Generation (Fuel Use)',
                ),
                DashFigureSet(
                    iplots=[DomesticEnergyProduction(all_params, years, self.config.title())],
                    category='Energy',
                    id='domestic-energy-production',
                    name='Domestic Energy Production',
                ),
                DashFigureSet(
                    iplots=[CapitalInvestment(all_params, years, self.config.title())],
                    category='Energy',
                    id='capital-investment',
                    name='Capital Investment',
                ),
                DashFigureSet(
                    iplots=[EnergyImports(all_params, years, self.config.title())],
                    category='Energy',
                    id='energy-imports',
                    name='Energy Imports',
                ),
                DashFigureSet(
                    iplots=[EnergyExports(all_params, years, self.config.title())],
                    category='Energy',
                    id='energy-exports',
                    name='Energy Exports',
                ),
                DashFigureSet(
                    iplots=[CostElectrictyGeneration(all_params, years, self.config.title())],
                    category='Energy',
                    id='cost-electricty-generation',
                    name='Cost Of Electricity Generation',
                ),
                DashFigureSet(
                    iplots=[AreaByCrop(all_params, years, land_use, self.config.title())],
                    category='Land',
                    id='area-by-crop',
                    name='Area By Crop',
                ),
                DashFigureSet(
                    iplots=[AreaByLandCover(all_params, years, land_use, self.config.title())],
                    category='Land',
                    id='area-by-land-cover',
                    name='Area By Land Cover Type',
                ),
                DashFigureSet(
                    iplots=[CropProduction(all_params, years, self.config.title())],
                    category='Land',
                    id='crop-production',
                    name='Crop Production',
                ),
                DashFigureSet(
                    iplots=[CropYield(all_params, years, land_use, self.config.title())],
                    category='Land',
                    id='crop-yield',
                    name='Yield',
                ),
                DashFigureSet(
                    iplots=[WaterDemand(all_params, years, self.config.title())],
                    category='Water',
                    id='water-demand',
                    name='Water Demand',
                ),
                DashFigureSet(
                    iplots=[WaterWithdrawalBySource(all_params, years, self.config.title())],
                    category='Water',
                    id='water-withdrawal-by-source',
                    name='Warer Withdrawal By Source',
                ),
                DashFigureSet(
                    iplots=[WaterBalance(all_params, years, self.config.title())],
                    category='Water',
                    id='water-balance',
                    name='Water Balance',
                ),
                DashFigureSet(
                    iplots=[EmissionsBySector(all_params, years, self.config.title())],
                    category='Climate',
                    id='emissions-by-sector',
                    name='CO2 Emissions By Sector',
                ),
                DashFigureSet(
                    iplots=[EmissionsByFuel(all_params, years, self.config.title())],
                    category='Climate',
                    id='emissions-by-fuel',
                    name='CO2 Emissions By Fuel',
                ),
                DashFigureSet(
                    iplots=[LivestockProduction(all_params, years, self.config.title())],
                    category='Land',
                    id='livestock-production',
                    name='Livestock Production',
                ),
                DashFigureSet(
                    iplots=[AreaByCropIrrigated(all_params, years, land_use, self.config.title())],
                    category='Land',
                    id='area-by-crop-irrigated',
                    name='Area By Crop (Irrigated)',
                ),
                DashFigureSet(
                    iplots=[AreaByCropRainfed(all_params, years, land_use, self.config.title())],
                    category='Land',
                    id='area-by-crop-rainfed',
                    name='Area By Crop (Rainfed)',
                ),
            ]

        for region in land_use.regions().keys():
            figure_list.append(
                DashFigureSet(
                    iplots=[AreaByCropForRegion(
                        all_params, years, land_use, region, self.config.title()
                    )],
                    category='Land',
                    id=f'area-by-crop-{region}',
                    name=f'Area by crop ({region})',
                ),
            )
            figure_list.append(
                DashFigureSet(
                    iplots=[AreaByLandCoverTypeForRegion(
                        all_params, years, land_use, region, self.config.title()
                    )],
                    category='Land',
                    id=f'area-by-land-{region}',
                    name=f'Area by land cover type ({region})',
                ),
            )

        return figure_list
