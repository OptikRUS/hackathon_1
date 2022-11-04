import pandas as pd
import numpy as np


class PoolEstimate:
    def __init__(self, etalon):
        self.etalon = etalon

    def missing_values_table(self, df):
        # Total missing values
        mis_val = df.isnull().sum()

        # Percentage of missing values
        mis_val_percent = 100 * df.isnull().sum() / len(df)

        # Make a table with the results
        mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)

        # Rename the columns
        mis_val_table_ren_columns = mis_val_table.rename(
            columns={0: 'Missing Values', 1: '% of Total Values'}
        )

        # Sort the table by percentage of missing descending
        mis_val_table_ren_columns = mis_val_table_ren_columns[
            mis_val_table_ren_columns.iloc[:, 1] != 0].sort_values(
            '% of Total Values', ascending=False).round(1)

        # Print some summary information
        print("Your selected dataframe has " + str(df.shape[1]) + " columns.\n"
                                                                  "There are " + str(
            mis_val_table_ren_columns.shape[0]) +
              " columns that have missing values.")

        # Return the dataframe with missing information
        return mis_val_table_ren_columns


    def make_data_ready_for_work(
            self,
            df,
            etalon_square,
            is_floor_cor=True,
            is_square_cor=True,
            is_kitchen_square_cor=True,
            is_balcony_cor=True,
            is_metro_stepway_cor=True,
            is_repair_state=True):
        """Подготовить данные с циана для корректировки, удаление неподходящих аналогов"""
        missing_df = self.missing_values_table(df)
        missing_columns = list(missing_df[missing_df['% of Total Values'] > 40].index)
        if is_balcony_cor:
            missing_columns.remove('Балкон')
        missing_columns.append('Высота потолков, м')
        missing_columns.append('Тип')
        missing_columns.append('Окна')
        df = df.drop(columns=list(missing_columns))

        if is_balcony_cor:
            df['Балкон'] = np.where(df['Балкон'].isna(), 0, 1)
        df["Площадь"] = df["Площадь, м2"].str.split('/').str[0]

        """Удаление неподходящих аналогов по квадратуре"""
        cond_list = [
            np.logical_and(df['Площадь'].astype(float) > 65, etalon_square < 30),
            np.logical_and(df['Площадь'].astype(float) > 90, etalon_square <= 50),
            np.logical_and(df['Площадь'].astype(float) > 120, etalon_square <= 65),
            np.logical_and(df['Площадь'].astype(float) < 30, etalon_square > 65),
            np.logical_and(df['Площадь'].astype(float) <= 50, etalon_square > 90),
            np.logical_and(df['Площадь'].astype(float) <= 65, etalon_square > 120),
        ]
        choice_list = [
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            np.nan
        ]

        df["Площадь"] = np.select(cond_list, choice_list, default=df['Площадь'])

        if is_kitchen_square_cor:
            df["Площадь кухни"] = df["Площадь, м2"].str.split('/').str[2] if len(
                df["Площадь, м2"].str.split('/')) > 2 else np.nan

        df.dropna(inplace=True)

        # data["Количество комнат"] = data["Количество комнат"].str.extract('(\d+)')
        df["Этажность"] = df["Дом"].str.extract('(\/(?!\/)([0-9]+))')[1]
        df["Этаж"] = df["Дом"].str.extract('([0-9]+)')[0]

        df["Материал"] = df["Дом"].str.extract('([ЁёА-я]+)')

        df["Год"] = df["Название ЖК"].str.extract('(\d{4})')

        replacements = {
            'Материал': {
                'Моно': 0,
                'Кирп': 1,
                'Панел|Бло': 2,
            }
        }

        df.replace(replacements, inplace=True, regex=True)

        df["Цена/м"] = df['Цена'].str.extract('([0-9]+)')[0].astype(float) / df['Площадь'].astype(float)

        return df

    def calculate_floor_k(self, df: pd.DataFrame, etalon_floor_value):
        """Рассчитать коэффициент этажности"""
        cond_list = [
            np.logical_and(
                np.logical_and(df['Этаж'].astype(int) > 1, df['Этаж'].astype(int) < df['Этажность'].astype(int)),
                etalon_floor_value == 0),
            np.logical_and(
                np.logical_and(df['Этаж'].astype(int) > 1, df['Этаж'].astype(int) < df['Этажность'].astype(int)),
                etalon_floor_value == 2),
            np.logical_and(df['Этаж'] == 1, etalon_floor_value == 1),
            np.logical_and(df['Этаж'] == 1, etalon_floor_value == 2),
            np.logical_and(df['Этаж'] == df['Этажность'], etalon_floor_value == 0),
            np.logical_and(df['Этаж'] == df['Этажность'], etalon_floor_value == 1),
        ]
        choice_list = [
            -0.07,
            -0.04,
            0.075,
            0.032,
            -0.031,
            0.042
        ]
        return np.select(cond_list, choice_list, default=0.0)

    def calculate_balcony_k(self, df: pd.DataFrame, etalon_balcony: bool):
        """Рассчитать коэффициент по наличию балкона"""
        condlist = [
            np.logical_and(df['Балкон'].astype(int) == 1, not etalon_balcony),
            np.logical_and(df['Балкон'].astype(int) == 0, etalon_balcony)
        ]
        choicelist = [
            -0.05,
            0.053
        ]
        return np.select(condlist, choicelist, default=0.0)

    def calculate_kitchen_k(self, df: pd.DataFrame, etalon_kitchen_square):
        cond_list = [
            np.logical_and(
                np.logical_and(df['Площадь кухни'].astype(float) >= 7, df['Площадь кухни'].astype(float) < 10),
                etalon_kitchen_square < 7),
            np.logical_and(
                np.logical_and(df['Площадь кухни'].astype(float) >= 7, df['Площадь кухни'].astype(float) < 10),
                etalon_kitchen_square >= 10),
            np.logical_and(
                df['Площадь кухни'].astype(float) < 7,
                np.logical_and(etalon_kitchen_square >= 7, etalon_kitchen_square < 10)),
            np.logical_and(
                df['Площадь кухни'].astype(float) < 7,
                etalon_kitchen_square >= 10),
            np.logical_and(
                df['Площадь кухни'].astype(float) >= 10,
                etalon_kitchen_square < 7),
            np.logical_and(
                df['Площадь кухни'].astype(float) >= 10,
                np.logical_and(etalon_kitchen_square >= 7, etalon_kitchen_square < 10)),
        ]
        choice_list = [
            -0.029,
            0.058,
            0.03,
            0.09,
            -0.083,
            -0.55
        ]
        return np.select(cond_list, choice_list, default=0.0)

    def calculate_square_k(self, df: pd.DataFrame, full_square):
        condlist = [
            np.logical_and(df['Площадь'].astype(float) < 30, np.logical_and(full_square >= 30, full_square < 50)),
            np.logical_and(
                df['Площадь'].astype(float) < 30,
                np.logical_and(full_square >= 50, full_square < 65)),
            np.logical_and(
                np.logical_and(df['Площадь'].astype(float) >= 30, df['Площадь'].astype(float) < 50),
                full_square < 30),
            np.logical_and(
                np.logical_and(df['Площадь'].astype(float) >= 30, df['Площадь'].astype(float) < 50),
                np.logical_and(full_square < 65, full_square >= 50)),
            np.logical_and(
                np.logical_and(df['Площадь'].astype(float) >= 30, df['Площадь'].astype(float) < 50),
                np.logical_and(full_square >= 65, full_square < 90)),
            np.logical_and(
                np.logical_and(df['Площадь'].astype(float) >= 50, df['Площадь'].astype(float) < 65),
                full_square < 30),
            np.logical_and(
                np.logical_and(df['Площадь'].astype(float) >= 50, df['Площадь'].astype(float) < 65),
                np.logical_and(full_square < 50, full_square >= 30)),
            np.logical_and(
                np.logical_and(df['Площадь'].astype(float) >= 50, df['Площадь'].astype(float) < 65),
                np.logical_and(full_square < 90, full_square >= 65)),
            np.logical_and(
                np.logical_and(df['Площадь'].astype(float) >= 50, df['Площадь'].astype(float) < 65),
                np.logical_and(full_square >= 90, full_square < 120)),
            np.logical_and(
                np.logical_and(df['Площадь'].astype(float) >= 65, df['Площадь'].astype(float) < 90),
                np.logical_and(full_square < 50, full_square >= 30)),
            np.logical_and(
                np.logical_and(df['Площадь'].astype(float) >= 65, df['Площадь'].astype(float) < 90),
                np.logical_and(full_square < 65, full_square >= 50)),
            np.logical_and(
                np.logical_and(df['Площадь'].astype(float) >= 65, df['Площадь'].astype(float) < 90),
                np.logical_and(full_square < 120, full_square >= 90)),
            np.logical_and(
                np.logical_and(df['Площадь'].astype(float) >= 65, df['Площадь'].astype(float) < 90),
                full_square >= 120),
            np.logical_and(
                np.logical_and(df['Площадь'].astype(float) >= 90, df['Площадь'].astype(float) < 120),
                np.logical_and(full_square < 65, full_square >= 50)),
            np.logical_and(
                np.logical_and(df['Площадь'].astype(float) >= 90, df['Площадь'].astype(float) < 120),
                np.logical_and(full_square < 90, full_square >= 65)),
            np.logical_and(
                np.logical_and(df['Площадь'].astype(float) >= 90, df['Площадь'].astype(float) < 120),
                full_square >= 120),
            np.logical_and(
                df['Площадь'].astype(float) >= 120,
                np.logical_and(full_square < 90, full_square >= 65)),
            np.logical_and(
                df['Площадь'].astype(float) >= 120,
                np.logical_and(full_square < 120, full_square >= 90)),
            np.logical_and(
                df['Площадь'].astype(float) < 30,
                np.logical_and(full_square < 90, full_square >= 65)),
            np.logical_and(
                df['Площадь'].astype(float) < 30,
                np.logical_and(full_square < 120, full_square >= 90)),
            np.logical_and(
                df['Площадь'].astype(float) < 30,
                full_square >= 120),
            np.logical_and(
                np.logical_and(df['Площадь'].astype(float) >= 30, df['Площадь'].astype(float) < 50),
                np.logical_and(full_square < 120, full_square >= 90)),
            np.logical_and(
                np.logical_and(df['Площадь'].astype(float) >= 30, df['Площадь'].astype(float) < 50),
                full_square > 120),
            np.logical_and(
                np.logical_and(df['Площадь'].astype(float) >= 50, df['Площадь'].astype(float) < 65),
                full_square >= 120),
            np.logical_and(
                np.logical_and(df['Площадь'].astype(float) >= 65, df['Площадь'].astype(float) < 90),
                full_square < 30),
            np.logical_and(
                np.logical_and(df['Площадь'].astype(float) >= 90, df['Площадь'].astype(float) < 120),
                full_square < 30),
            np.logical_and(
                np.logical_and(df['Площадь'].astype(float) >= 90, df['Площадь'].astype(float) < 120),
                np.logical_and(full_square >= 30, full_square < 50)),
            np.logical_and(
                df['Площадь'].astype(float) >= 120,
                full_square < 30),
            np.logical_and(
                df['Площадь'].astype(float) >= 120,
                np.logical_and(full_square < 50, full_square >= 30)),
            np.logical_and(
                df['Площадь'].astype(float) >= 120,
                np.logical_and(full_square < 65, full_square >= 50)),
        ]
        choicelist = [
            -0.06,
            -0.12,
            0.06,
            -0.07,
            -0.12,
            0.07,
            0.14,
            -0.06,
            -0.11,
            0.14,
            0.06,
            -0.06,
            -0.08,
            0.13,
            0.06,
            -0.03,
            0.09,
            0.03,
            -0.17,
            -0.22,
            -0.24,
            -0.17,
            -0.19,
            -0.13,
            0.21,
            0.28,
            0.21,
            0.31,
            0.24,
            0.16
        ]
        return np.select(condlist, choicelist, default=0.0)

    def calculate_cor(
            self,
            data: str,
            is_auction_cor=True,
            is_floor_cor=True,
            is_square_cor=True,
            is_kitchen_square_cor=True,
            is_balcony_cor=True,
            is_metro_stepway_cor=True,
            is_repair_state=True
    ):
        etalon_xls = pd.ExcelFile(self.etalon)
        df_etalon = pd.read_excel(etalon_xls, 0)
        # df_etalon = df_etalon.dropna()
        floor = df_etalon.iloc[:, 5].values[-1]
        full_floor = df_etalon.iloc[:, 3].values[-1]
        etalon_floor_value = 0

        if floor == full_floor:
            etalon_floor_value = 2
        elif 1 < floor < full_floor:
            etalon_floor_value = 1

        auction_value = -0.045 if is_auction_cor else 0
        full_square = df_etalon.iloc[:, 6].values[-1]
        kitchen_squad = df_etalon.iloc[:, 7].values[-1]
        has_balcony = df_etalon.iloc[:, 8].values[-1] == 'Да'
        is_metro_stepway = df_etalon.iloc[:, 9].values[-1]
        repair_state = df_etalon.iloc[:, 10].values[-1]

        df = pd.read_excel(data)
        df = self.make_data_ready_for_work(
            df,
            etalon_square=full_square,
            is_floor_cor=is_floor_cor,
            is_square_cor=is_square_cor,
            is_kitchen_square_cor=is_kitchen_square_cor,
            is_balcony_cor=is_balcony_cor,
            is_metro_stepway_cor=is_metro_stepway_cor,
            is_repair_state=is_repair_state
        )

        if is_floor_cor:
            df['ЭтажК'] = self.calculate_floor_k(df, etalon_floor_value)
        if is_square_cor:
            df['ПлощадьК'] = self.calculate_square_k(df, full_square)
        if is_balcony_cor:
            df['БалконК'] = self.calculate_balcony_k(df, etalon_balcony=has_balcony)
        if is_kitchen_square_cor:
            df['КухняК'] = self.calculate_kitchen_k(df, etalon_kitchen_square=kitchen_squad)

        df['Сумма за квадратный метр для эталона'] = df['Цена/м'].astype(float) * (
                1 + (df['ЭтажК'].astype(float) if is_floor_cor else 0)
                + (df['ПлощадьК'].astype(float) if is_square_cor else 0)
                + (df['БалконК'].astype(float) if is_balcony_cor else 0)
                + (df['КухняК'].astype(float) if is_kitchen_square_cor else 0)
                + auction_value)

        df.to_excel("output.xlsx")
