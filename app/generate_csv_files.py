import pandas as pd
import os, sys

def generate_csv_files(data_file, results_file, base_folder):

    pd.set_option('mode.chained_assignment', None)

    lines = []

    parsing = False

    data_all = []
    data_out = []
    data_inp = []
    output_table = []
    input_table = []
    storage_to = []
    storage_from = []

    with open(data_file, 'r') as f:
        for line in f:
            if line.startswith('set YEAR'):
                start_year = line.split(' ')[3]
            if line.startswith('set COMMODITY'): # Extracts list of COMMODITIES from data file. Some models use FUEL instead.
                fuel_list = line.split(' ')[3:-1]
            if line.startswith('set FUEL'): # Extracts list of FUELS from data file. Some models use COMMODITIES instead.
                fuel_list = line.split(' ')[3:-1]
            if line.startswith('set TECHNOLOGY'):
                tech_list = line.split(' ')[3:-1]
            if line.startswith('set STORAGE'):
                storage_list = line.split(' ')[3:-1]
            if line.startswith('set MODE_OF_OPERATION'):
                mode_list = line.split(' ')[3:-1]

            if line.startswith(";"):
                    parsing = False

            if parsing:
                if line.startswith('['):
                    fuel = line.split(',')[2]
                    tech = line.split(',')[1]
                elif line.startswith(start_year):
                    years = line.rstrip(':= ;\n').split(' ')[0:]
                    years = [i.strip(':=') for i in years]
                else:
                    values = line.rstrip().split(' ')[1:]
                    mode = line.split(' ')[0]

                    if param_current=='OutputActivityRatio':
                        #data_out.append(tuple([fuel,tech,mode]))
                        #data_all.append(tuple([tech,mode]))
                        for i in range(0,len(years)):
                            output_table.append(tuple([tech,fuel,mode,years[i],values[i]]))

                    if param_current=='InputActivityRatio':
                        #data_inp.append(tuple([fuel,tech,mode]))
                        #data_all.append(tuple([tech,mode]))
                        for i in range(0,len(years)):
                            input_table.append(tuple([tech,fuel,mode,years[i],values[i]]))

                    if param_current == 'TechnologyToStorage' or param_current == 'TechnologyFromStorage':
                        if not line.startswith(mode_list[0]):
                            storage = line.split(' ')[0]
                            values = line.rstrip().split(' ')[1:]
                            for i in range(0,len(mode_list)):
                                if values[i] != '0':
                                    if param_current == 'TechnologyToStorage':
                                        storage_to.append(tuple([storage,tech,mode_list[i]]))
                                        data_all.append(tuple([tech,mode_list[i]]))
                                    if param_current == 'TechnologyFromStorage':
                                        storage_from.append(tuple([storage,tech,mode_list[i]]))
                                        data_all.append(tuple([tech,mode_list[i]]))

            if line.startswith(('param OutputActivityRatio','param InputActivityRatio','param TechnologyToStorage','param TechnologyFromStorage')):
                param_current = line.split(' ')[1]
                parsing = True

    try:
        os.makedirs(os.path.join(base_folder, 'csv'))
    except FileExistsError:
        pass

    #Read CBC output file
    df = pd.read_csv(results_file, sep='\t')

    df.columns = ['temp']
    df['temp'] = df['temp'].str.lstrip(' *\n\t')
    df[['temp','value']] = df['temp'].str.split(')', expand=True)
    df = df.applymap(lambda x: x.strip() if isinstance(x,str) else x)
    df['value'] = df['value'].str.split(' ', expand=True)
    df[['parameter','id']] = df['temp'].str.split('(', expand=True)
    df['parameter'] = df['parameter'].str.split(' ', expand=True)[1]
    df = df.drop('temp', axis=1)
    df['value'] = df['value'].astype(float).round(4)

    params = df.parameter.unique()
    all_params = {}
    cols = {'NewCapacity':['r','t','y'],
            'AccumulatedNewCapacity':['r','t','y'],
            'TotalCapacityAnnual':['r','t','y'],
            'CapitalInvestment':['r','t','y'],
            'AnnualVariableOperatingCost':['r','t','y'],
            'AnnualFixedOperatingCost':['r','t','y'],
            'SalvageValue':['r','t','y'],
            'DiscountedSalvageValue':['r','t','y'],
            'TotalTechnologyAnnualActivity':['r','t','y'],
            'RateOfActivity':['r','l','t','m','y'],
            'RateOfTotalActivity':['r','t','l','y'],
            'Demand':['r','l','f','y'],
            'TotalAnnualTechnologyActivityByMode':['r','t','m','y'],
            'TotalTechnologyModelPeriodActivity':['r','t'],
            'ProductionByTechnology':['r','l','t','f','y'],
            'ProductionByTechnologyAnnual':['r','t','f','y'],
            'AnnualTechnologyEmissionByMode':['r','t','e','m','y'],
            'AnnualTechnologyEmission':['r','t','e','y'],
            'AnnualEmissions':['r','e','y'],
            'DiscountedTechnologyEmissionsPenalty':['r','t','y'],
            'RateOfProductionByTechnology':['r','l','t','f','y'],
            'RateOfUseByTechnology':['r','l','t','f','y'],
            'UseByTechnology':['r','l','t','f','y'],
            'RateOfProductionByTechnologyByMode':['r','l','t','f','m','y'],
            'RateOfUseByTechnologyByMode':['r','l','t','f','m','y'],
            'TechnologyActivityChangeByMode':['r','t','m','y'],
            'TechnologyActivityChangeByModeCostTotal':['r','t','m','y'],
            }

    for each in params:
        df_p = df[df.parameter == each]
        df_p[cols[each]] = df_p['id'].str.split(',',expand=True)
        cols[each].append('value')
        df_p = df_p[cols[each]] # Reorder dataframe to include 'value' as last column
        all_params[each] = pd.DataFrame(df_p) # Create a dataframe for each parameter
        df_p = df_p.rename(columns={'value':each})
        df_p.to_csv(os.path.join(base_folder, 'csv', str(each) + '.csv'), index=None) # Print data for each paramter to a CSV file

    year_split = []
    parsing = False

    with open(data_file, 'r') as f:
        for line in f:
            if line.startswith(";"):
                parsing = False
            if parsing:
                if line.startswith(start_year):
                    years = line.rstrip().split(' ')[0:]
                    years = [i.strip(':=') for i in years]
                elif not line.startswith(start_year):
                    time_slice = line.rstrip().split(' ')[0]
                    values = line.rstrip().split(' ')[1:]
                    for i in range(0,len(years)):
                        year_split.append(tuple([time_slice,years[i],values[i]]))
            if line.startswith('param YearSplit'):
                parsing = True

    df_yearsplit = pd.DataFrame(year_split, columns=['l','y','YearSplit'])
    df_activity = all_params['RateOfActivity'].rename(columns={'value':'RateOfActivity'})

    df_output = pd.DataFrame(output_table, columns=['t','f','m','y','OutputActivityRatio'])
    df_out_ys = pd.merge(df_output, df_yearsplit, on='y')
    df_out_ys['OutputActivityRatio'] = df_out_ys['OutputActivityRatio'].astype(float)
    df_out_ys['YearSplit'] = df_out_ys['YearSplit'].astype(float)

    df_prod = pd.merge(df_out_ys, df_activity, on=['t','m','l','y'])
    df_prod['ProductionByTechnologyAnnual'] = df_prod['OutputActivityRatio']*df_prod['YearSplit']*df_prod['RateOfActivity']
    df_prod = df_prod.drop(['OutputActivityRatio','YearSplit','RateOfActivity'], axis=1)
    df_prod = df_prod.groupby(['r','t','f','y'])['ProductionByTechnologyAnnual'].sum().reset_index()
    df_prod['ProductionByTechnologyAnnual'] = df_prod['ProductionByTechnologyAnnual'].astype(float).round(4)
    df_prod.to_csv(os.path.join(base_folder, 'csv', 'ProductionByTechnologyAnnual.csv'), index=None)
    all_params['ProductionByTechnologyAnnual'] = df_prod.rename(columns={'ProductionByTechnologyAnnual':'value'})


    df_input = pd.DataFrame(input_table, columns=['t','f','m','y','InputActivityRatio'])
    df_in_ys = pd.merge(df_input, df_yearsplit, on='y')
    df_in_ys['InputActivityRatio'] = df_in_ys['InputActivityRatio'].astype(float)
    df_in_ys['YearSplit'] = df_in_ys['YearSplit'].astype(float)

    df_use = pd.merge(df_in_ys, df_activity, on=['t','m','l','y'])
    df_use['UseByTechnologyAnnual'] = df_use['InputActivityRatio']*df_use['YearSplit']*df_use['RateOfActivity']
    df_use = df_use.drop(['InputActivityRatio','YearSplit','RateOfActivity'], axis=1)
    df_use = df_use.groupby(['r','t','f','y'])['UseByTechnologyAnnual'].sum().reset_index()
    df_use['UseByTechnologyAnnual'] = df_use['UseByTechnologyAnnual'].astype(float).round(4)
    df_use.to_csv(os.path.join(base_folder, 'csv', 'UseByTechnologyAnnual.csv'), index=None)
    all_params['UseByTechnologyAnnual'] = df_use.rename(columns={'UseByTechnologyAnnual':'value'})

if __name__ == '__main__':

    if len(sys.argv) != 3:
        msg = "Usage: python {} <datafile> <resultsfile>"
        print(msg.format(sys.argv[0]))
        sys.exit(1)
    else:
        data_file = sys.argv[1]
        results_file = sys.argv[2]
        main(data_file, results_file)
