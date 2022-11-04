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
                                                                  "There are " + str(mis_val_table_ren_columns.shape[0]) +
              " columns that have missing values.")

        # Return the dataframe with missing information
        return mis_val_table_ren_columns

    def make_data_ready_for_work(
            self,
            df,
            etalon_square,
            is_auction_cor=True,
            is_floor_cor=True,
            is_square_cor=True,
            is_kitchen_square_cor=True,
            is_balcony_cor=True,
            is_metro_stepway_cor=True,
            is_repair_state=True):

        missing_df = self.missing_values_table(df)
        missing_columns = list(missing_df[missing_df['% of Total Values'] > 40].index)
        missing_columns.remove('Балкон')
        missing_columns.append('Высота потолков, м')
        missing_columns.append('Тип')
        missing_columns.append('Окна')
        df = df.drop(columns=list(missing_columns))

        df['Балкон'] = np.where(df['Балкон'].isna(), 0, 1)
        df["Площадь"] = df["Площадь, м2"].str.split('/').str[0]

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

        if is_kitchen_square_cor:
            df["Площадь кухни"] = df["Площадь, м2"].str.split('/').str[2] if len(
                df["Площадь, м2"].str.split('/')) > 2 else np.nan

        # data = data.drop(columns=['Тип', 'Метро', 'Адрес', 'Площадь, м2', 'Дом', 'Цена', 'Телефоны', 'Описание', 'Ссылка на объявление'])

        df.dropna(inplace=True)

        return df

    def calculate_floor_k(self, df: pd.DataFrame, etalon_floor_value):
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

    def calculate_balcony_k(df: pd.DataFrame, etalon_balcony: bool):
        condlist = [
            np.logical_and(df['Балкон'].astype(int) == 1, not etalon_balcony),
            np.logical_and(df['Балкон'].astype(int) == 0, etalon_balcony)
        ]
        choicelist = [
            -0.05,
            0.053
        ]
        return np.select(condlist, choicelist, default=0.0)

    def calculate_square_k(self, df: pd.DataFrame, full_square):
        condlist = [
            np.logical_and(df['Площадь'].astype(float) < 30, np.logical_and(full_square >= 30, full_square < 50)),
            np.logical_and(df['Площадь'].astype(float) < 30, full_square >= 50),
            np.logical_and(
                np.logical_and(df['Площадь'].astype(float) >= 30, df['Площадь'].astype(float) < 50),
                full_square < 30),
            np.logical_and(
                np.logical_and(df['Площадь'].astype(float) >= 30, df['Площадь'].astype(float) < 50),
                np.logical_and(full_square < 65, full_square >= 50)),
            np.logical_and(
                np.logical_and(df['Площадь'].astype(float) >= 30, df['Площадь'].astype(float) < 50),
                full_square >= 65),
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
                full_square > 90),
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
                full_square < 65),
            np.logical_and(
                np.logical_and(df['Площадь'].astype(float) >= 90, df['Площадь'].astype(float) < 120),
                np.logical_and(full_square < 90, full_square >= 65)),
            np.logical_and(
                np.logical_and(df['Площадь'].astype(float) >= 90, df['Площадь'].astype(float) < 120),
                full_square >= 120),
            np.logical_and(
                df['Площадь'].astype(float) >= 120,
                full_square < 90),
            np.logical_and(
                df['Площадь'].astype(float) >= 120,
                np.logical_and(full_square < 120, full_square >= 90)),
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
            0.03
        ]
        return np.select(condlist, choicelist, default=0.0)

    def calculateCor(
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

        auctionValue = -0.045 if is_auction_cor else 0
        full_square = df_etalon.iloc[:, 6].values[-1]
        kitchenSquad = df_etalon.iloc[:, 7].values[-1]
        hasBalcony = df_etalon.iloc[:, 8].values[-1] == 'Да'
        isMetroStepway = df_etalon.iloc[:, 9].values[-1]
        repairState = df_etalon.iloc[:, 10].values[-1]

        df = pd.read_excel(data)
        df = self.make_data_ready_for_work(
            df,
            etalon_square=full_square,
            is_auction_cor=is_auction_cor,
            is_floor_cor=is_floor_cor,
            is_square_cor=is_square_cor,
            is_kitchen_square_cor=is_kitchen_square_cor,
            is_balcony_cor=is_balcony_cor,
            is_metro_stepway_cor=is_metro_stepway_cor,
            is_repair_state=is_repair_state
        )

        df['ЭтажК'] = self.calculate_floor_k(df, etalon_floor_value) if is_floor_cor else 0
        df['ПлощадьК'] = self.calculate_square_k(df, full_square) if isSquareCor else 0
        df['БалконК'] = calculateBalconyK(df, etalon_balcony=hasBalcony)

        df['Сумма за квадратный метр для эталона'] = df['Цена/м'].astype(float) * (
                    1 + df['ЭтажК'].astype(float) + df['ПлощадьК'].astype(float) + auctionValue)

        # fCond = -7.0 if (df['Этаж'] < df['Этажность'] and df['Этаж'] > 1 and etalon_floor_value == 0) else 0.0 + \
        #         -4.0 if (df['Этаж'] < df['Этажность'] and df['Этаж'] > 1 and etalon_floor_value == 2) else 0.0 + \
        #          7.5 if (df['Этаж'] == 1 and etalon_floor_value == 1) else 0.0 + \
        #             3.2 if (df['Этаж'] == 1 and etalon_floor_value == 2) else 0.0 + \
        #             -3.1 if (df['Этаж'] == df['Этажность'] and etalon_floor_value == 0) else 0.0 + \
        #             4.2 if (df['Этаж'] == df['Этажность'] and etalon_floor_value == 1) else 0.0
        df.to_excel("output.xlsx")
