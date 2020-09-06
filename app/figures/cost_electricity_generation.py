from app.utilities import df_plot, df_filter
import pandas as pd


class CostElectrictyGeneration:

    def __init__(self, all_params, years, plot_title):
        self.all_params = all_params
        self.years = years
        self.plot_title = plot_title

    def figure(self):
        ele_cos_df = self.__calculate_ele_cos_df()
        return ele_cos_df.iplot(
                asFigure=True,
                kind='bar',
                barmode='relative',
                x='y',
                title=self.plot_title
                )

    def __calculate_ele_cos_df(self):
        ene_imp_df = self.calculate_ene_imp_df(self.all_params, self.years)
        ene_exp_df = self.calculate_ene_exp_df(self.all_params, self.years)
        cap_cos_df = self.calculate_cap_cos_df(self.all_params, self.years)
        ele_cos_df = pd.DataFrame(columns=['Total capital investment', 'Capital costs'])
        ele_cos_df.insert(0, 'y', self.years)
        ele_cos_df['Total capital investment'] = cap_cos_df.iloc[:, 1:].sum(axis=1)
        ele_cos_df['Capital costs'] = 0
        ele_cos_df = ele_cos_df.fillna(0)

        R = 0.1  # Discount rate
        n = 30  # Amortization period
        cap_exist_total = 500  # Payments on existing capacity (legacy costs)

        for i in ele_cos_df['y']:
            for j in ele_cos_df['y']:
                if i < j + n and i >= j:
                    ele_cos_df.loc[ele_cos_df['y'] == i, 'Capital costs'] = ele_cos_df.loc[ele_cos_df['y'] == i, 'Capital costs'] + (
                        ((ele_cos_df.loc[ele_cos_df['y'] == j, 'Total capital investment'].iloc[0]) * R) / (1 - (1 + R)**(-n)))

        ele_cos_df.drop('Total capital investment', axis=1, inplace=True)

        cap_exist_values = {}

        start_year = min(self.years)

        for year in self.years:
            if cap_exist_total - ((cap_exist_total / n) * (year - int(start_year))) > 0:
                cap_exist_values[year] = cap_exist_total - \
                    ((cap_exist_total / n) * (year - int(start_year)))
            else:
                cap_exist_values[year] = 0

        ele_cos_df['Legacy costs'] = ele_cos_df['y'].map(cap_exist_values)
        ele_cos_df['Capital costs'] += ele_cos_df['Legacy costs']
        ele_cos_df = ele_cos_df.drop('Legacy costs', axis=1)

        fix_cos_df = self.all_params['AnnualFixedOperatingCost'][self.all_params['AnnualFixedOperatingCost'].t.str.startswith(
            'PWR')].drop('r', axis=1)
        fix_cos_df = df_filter(fix_cos_df, 3, 6, ['TRN'], self.years)

        var_cos_df = self.all_params['AnnualVariableOperatingCost'][self.all_params['AnnualVariableOperatingCost'].t.str.startswith(
            'PWR')|
            self.all_params['AnnualVariableOperatingCost'].t.str.startswith(
            'EXPELC')
            ].drop('r', axis=1)
        var_cos_df = df_filter(var_cos_df, 3, 6, ['TRN'], self.years)

        dis_cos_df = self.all_params['AnnualVariableOperatingCost'][self.all_params['AnnualVariableOperatingCost'].t.str.startswith(
            'DEMPWR')].drop('r', axis=1)
        dis_cos_df = df_filter(dis_cos_df, 6, 9, [], self.years)

        dom_val_df = self.all_params['AnnualVariableOperatingCost'][self.all_params['AnnualVariableOperatingCost'].t.str.startswith('MIN') |
                                                               self.all_params['AnnualVariableOperatingCost'].t.str.startswith('RNW')].drop('r', axis=1)
        dom_val_df = df_filter(dom_val_df, 3, 6, [], self.years)
        for each in dom_val_df.columns:
            if each in ['Land', 'Water', 'Geothermal', 'Hydro', 'Solar', 'Wind']:
                dom_val_df = dom_val_df.drop(each, axis=1)

        imp_val_df = self.all_params['AnnualVariableOperatingCost'][self.all_params['AnnualVariableOperatingCost'].t.str.startswith(
            'IMP')].drop('r', axis=1)
        imp_val_df = df_filter(imp_val_df, 3, 6, [], self.years)

        exp_val_df = self.all_params['AnnualVariableOperatingCost'][self.all_params['AnnualVariableOperatingCost'].t.str.startswith(
            'EXP')].drop('r', axis=1)
        exp_val_df = df_filter(exp_val_df, 3, 6, [], self.years)

        temp_col_list = []
        temp_col_list = dom_val_df.columns

        if len(imp_val_df.columns) > 1:
            temp_col_list = temp_col_list.append(imp_val_df.columns)

        if len(exp_val_df.columns) > 1:
            temp_col_list = temp_col_list.append(exp_val_df.columns)

        fue_val_df = pd.DataFrame(columns=list(set(temp_col_list)))
        fue_val_df['y'] = self.years
        fue_val_df = fue_val_df.reindex(sorted(fue_val_df.columns), axis=1).set_index('y').reset_index()

        fue_val_df = fue_val_df.fillna(0)

        for each in dom_val_df.columns:
            if each != 'y':
                fue_val_df[each] = dom_val_df[each]
                fue_val_df = fue_val_df.fillna(0)

        for each in imp_val_df.columns:
            if each != 'y' and len(imp_val_df.columns) > 1:
                fue_val_df[each] = fue_val_df[each] + imp_val_df[each]
                fue_val_df = fue_val_df.fillna(0)

        for each in exp_val_df.columns:
            if each != 'y' and len(ene_exp_df.columns) > 1:
                fue_val_df[each] = fue_val_df[each] + exp_val_df[each]
                fue_val_df = fue_val_df.fillna(0)

        temp_col_list = []
        dom_prd_df = self.calculate_dom_prd_df(self.all_params, self.years)
        temp_col_list = dom_prd_df.columns
        if len(ene_imp_df.columns) > 1:
            temp_col_list = temp_col_list.append(ene_imp_df.columns)
        if len(ene_exp_df.columns) > 1:
            temp_col_list = temp_col_list.append(ene_exp_df.columns)

        fue_prd_df = pd.DataFrame(columns=list(set(temp_col_list)))
        fue_prd_df['y'] = self.years
        fue_prd_df = fue_prd_df.reindex(sorted(fue_prd_df.columns), axis=1).set_index('y').reset_index()

        fue_prd_df = fue_prd_df.fillna(0)

        for each in dom_prd_df.columns:
            if each != 'y':
                fue_prd_df[each] = dom_prd_df[each]
                fue_prd_df = fue_prd_df.fillna(0)

        for each in ene_imp_df.columns:
            if each != 'y' and len(ene_imp_df.columns) > 1:
                fue_prd_df[each] = fue_prd_df[each] + ene_imp_df[each]
                fue_prd_df = fue_prd_df.fillna(0)

        for each in ene_exp_df.columns:
            if each != 'y' and len(ene_exp_df.columns) > 1:
                fue_prd_df[each] = fue_prd_df[each] - ene_exp_df[each]
                fue_prd_df = fue_prd_df.fillna(0)

        # for df in [fue_val_df, fue_prd_df]:
        #    df['Diesel'] = df['Diesel']
        #    df['HFO'] = df['HFO']

        fue_cos_df = pd.DataFrame(columns=list(set(temp_col_list)))
        fue_cos_df['y'] = self.years

        gen_use_df = self.calculate_gen_use_df(self.all_params, self.years)
        fue_cos_df = (fue_val_df / fue_prd_df) * gen_use_df
        fue_cos_df = fue_cos_df.fillna(0)
        fue_cos_df = fue_cos_df.reindex(sorted(fue_cos_df.columns), axis=1).set_index('y').reset_index()
        fue_cos_df['y'] = self.years

        gen_df = self.calculate_gen_df(self.all_params, self.years)
        ele_cos_df['Electricity generation'] = gen_df.iloc[:, 1:].sum(axis=1)
        ele_cos_df['Capital costs'] = ele_cos_df['Capital costs'] / ele_cos_df['Electricity generation']
        ele_cos_df['Fixed costs'] = fix_cos_df.iloc[:, 1:].sum(
            axis=1) / ele_cos_df['Electricity generation']
        ele_cos_df['Variable costs'] = var_cos_df.iloc[:, 1:].sum(
            axis=1) / ele_cos_df['Electricity generation']
        ele_cos_df['Fuel distribution costs'] = dis_cos_df.iloc[:, 1:].sum(
            axis=1) / ele_cos_df['Electricity generation']
        ele_cos_df['Fuel costs'] = fue_cos_df.iloc[:, 1:].sum(
            axis=1) / ele_cos_df['Electricity generation']
        ele_cos_df.drop('Electricity generation', axis=1, inplace=True)
        return ele_cos_df

    def calculate_ene_imp_df(self, all_params, years):
        # Energy imports
        ene_imp_df = self.all_params['ProductionByTechnologyAnnual'][self.all_params['ProductionByTechnologyAnnual'].t.str.startswith(
            'IMP')].drop('r', axis=1)
        return df_filter(ene_imp_df, 3, 6, [], years)

    def calculate_ene_exp_df(self, all_params, years):
        # Energy exports
        ene_exp_df = all_params['TotalTechnologyAnnualActivity'][all_params['TotalTechnologyAnnualActivity'].t.str.startswith(
            'EXP')].drop('r', axis=1)
        return df_filter(ene_exp_df, 3, 6, [], years)

    def calculate_cap_cos_df(self, all_params, years):
        cap_cos_df = all_params['CapitalInvestment'][all_params['CapitalInvestment'].t.str.startswith(
            'PWR')].drop('r', axis=1)
        return df_filter(cap_cos_df, 3, 6, ['TRN'], years)

    def calculate_dom_prd_df(self, all_params, years):
        dom_prd_df = all_params['ProductionByTechnologyAnnual'][all_params['ProductionByTechnologyAnnual'].t.str.startswith('MIN') |
                                                                all_params['ProductionByTechnologyAnnual'].t.str.startswith('RNW')].drop('r', axis=1)
        return df_filter(dom_prd_df, 3, 6, [], years)

    def calculate_gen_use_df(self, all_params, years):
        gen_use_df = all_params['ProductionByTechnologyAnnual'][all_params['ProductionByTechnologyAnnual'].t.str.startswith(
            'DEMPWR')].drop('r', axis=1)
        gen_use_df = df_filter(gen_use_df, 6, 9, ['SUR'], years)
        return gen_use_df

    def calculate_gen_df(self, all_params, years):
        # Power generation (Detailed)
        gen_df = all_params['ProductionByTechnologyAnnual'][(all_params['ProductionByTechnologyAnnual'].t.str.startswith('PWR') |
                                                             all_params['ProductionByTechnologyAnnual'].t.str.startswith('IMP')) &
                                                            all_params['ProductionByTechnologyAnnual'].f.str.startswith('ELC')].drop('r', axis=1)
        gen_df = df_filter(gen_df, 3, 6, ['TRN'], years)
        gen_df['Net electricity imports'] = 0

        ele_exp_df = all_params['TotalTechnologyAnnualActivity'][
                     all_params['TotalTechnologyAnnualActivity'].t.str.startswith('EXPELC')
                     ].drop('r', axis=1)

        if not ele_exp_df.empty:
            ele_exp_df = (df_filter(ele_exp_df, 3, 6, ['TRN'], years)
                          .rename(columns={'Electricity': 'Electricity exports'}))
            gen_df = gen_df.merge(ele_exp_df)
            gen_df['Net electricity imports'] = (gen_df['Net electricity imports']
                                                 - gen_df['Electricity exports'])
            gen_df.drop('Electricity exports', axis=1, inplace=True)

            if 'Electricity' in gen_df.columns:
                gen_df['Net electricity imports'] = (gen_df['Net electricity imports']
                                                     - gen_df['Electricity'])
                gen_df.drop('Electricity', axis=1, inplace=True)

            gen_df.rename(columns={'Net electricity imports': 'Electricity exports'},
                          inplace=True)
            gen_df.loc[:, gen_df.columns != 'y'] = (gen_df.loc[:, gen_df.columns != 'y']
                                                          .mul(0.28).round(2))
        return gen_df
