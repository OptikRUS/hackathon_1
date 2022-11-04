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
            isAuctionCor=True,
            isFloorCor=True,
            isSquareCor=True,
            isKichenSquareCor=True,
            isBalconyCor=True,
            isMetroStepwayCor=True,
            isRepairState=True):

        missing_df = self.missing_values_table(df)
        missing_columns = list(missing_df[missing_df['% of Total Values'] > 40].index)
        # missing_columns.remove('Название ЖК')
        missing_columns.append('Высота потолков, м')
        df = df.drop(columns=list(missing_columns))

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

        df["Площадь"] = df["Площадь, м2"].str.split('/').str[0]

        df["Цена/м"] = df['Цена'].str.extract('([0-9]+)')[0].astype(float) / df['Площадь'].astype(float)

        if isKichenSquareCor:
            df["Площадь кухни"] = df["Площадь, м2"].str.split('/').str[2] if len(
                df["Площадь, м2"].str.split('/')) > 2 else None

        # data = data.drop(columns=['Тип', 'Метро', 'Адрес', 'Площадь, м2', 'Дом', 'Цена', 'Телефоны', 'Описание', 'Ссылка на объявление'])

        df.dropna(inplace=True)

        return df

    def calculate_floor_k(self, df: pd.DataFrame, etalonFloorValue):
        condlist = [
            np.logical_and(np.logical_and(df['Этаж'].astype(int) > 1, df['Этаж'].astype(int) < df['Этажность'].astype(int)),
                           etalonFloorValue == 0),
            np.logical_and(np.logical_and(df['Этаж'].astype(int) > 1, df['Этаж'].astype(int) < df['Этажность'].astype(int)),
                           etalonFloorValue == 2),
            np.logical_and(df['Этаж'] == 1, etalonFloorValue == 1),
            np.logical_and(df['Этаж'] == 1, etalonFloorValue == 2),
            np.logical_and(df['Этаж'] == df['Этажность'], etalonFloorValue == 0),
            np.logical_and(df['Этаж'] == df['Этажность'], etalonFloorValue == 1),
        ]
        choicelist = [
            -0.07,
            -0.04,
            0.075,
            0.032,
            -0.031,
            0.042
        ]
        return np.select(condlist, choicelist, default=0.0)

    def calculate_square_k(self, df: pd.DataFrame, fullSquad):
        condlist = [
            np.logical_and((df['Площадь'].astype(float) - fullSquad) < 30, (df['Площадь'].astype(float) - fullSquad) > 20),
            np.logical_and((df['Площадь'].astype(float) - fullSquad) <= 20, (df['Площадь'].astype(float) - fullSquad) > 10),
            np.logical_and((df['Площадь'].astype(float) - fullSquad) <= 10,
                           (df['Площадь'].astype(float) - fullSquad) > -10),
            np.logical_and((df['Площадь'].astype(float) - fullSquad) <= -10,
                           (df['Площадь'].astype(float) - fullSquad) > -20),
            np.logical_and((df['Площадь'].astype(float) - fullSquad) <= -20,
                           (df['Площадь'].astype(float) - fullSquad) > -30),
        ]
        choicelist = [
            -0.07,
            -0.04,
            0.0,
            0.04,
            0.07
        ]
        return np.select(condlist, choicelist, default=0.0)

    def calculateCor(
            self,
            data: str,
            isAuctionCor=True,
            isFloorCor=True,
            isSquareCor=True,
            isKichenSquareCor=False,
            isBalconyCor=True,
            isMetroStepwayCor=True,
            isRepairState=False
    ):
        etalonXls = pd.ExcelFile(self.etalon)
        dfEtalon = pd.read_excel(etalonXls, "Данные по объекту")
        # dfEtalon = dfEtalon.dropna()
        floor = dfEtalon.iloc[:, 5].values[-1]
        fullFloor = dfEtalon.iloc[:, 3].values[-1]
        etalonFloorValue = 0

        if floor == fullFloor:
            etalonFloorValue = 2
        elif floor > 1 and floor < fullFloor:
            etalonFloorValue = 1

        auctionValue = -0.045 if isAuctionCor else 0
        fullSquad = dfEtalon.iloc[:, 6].values[-1]
        kitchenSquad = dfEtalon.iloc[:, 7].values[-1]
        hasBalcony = dfEtalon.iloc[:, 8].values[-1] == 'Да'
        isMetroStepway = dfEtalon.iloc[:, 9].values[-1]
        repairState = dfEtalon.iloc[:, 10].values[-1]

        df = pd.read_excel(data)
        df = self.make_data_ready_for_work(
            df.head(),
            isAuctionCor=isAuctionCor,
            isFloorCor=isFloorCor,
            isSquareCor=isSquareCor,
            isKichenSquareCor=isKichenSquareCor,
            isBalconyCor=isBalconyCor,
            isMetroStepwayCor=isMetroStepwayCor,
            isRepairState=isRepairState
        )

        df['ЭтажК'] = self.calculate_floor_k(df, etalonFloorValue) if isFloorCor else 0
        df['ПлощадьК'] = self.calculate_square_k(df, fullSquad) if isSquareCor else 0

        df['Сумма за квадратный метр для эталона'] = df['Цена/м'].astype(float) * (1 + df['ЭтажК'].astype(float)
                                                                                   + df['ПлощадьК'].astype(float)
                                                                                   + auctionValue)

        # fCond = -7.0 if (df['Этаж'] < df['Этажность'] and df['Этаж'] > 1 and etalonFloorValue == 0) else 0.0 + \
        #         -4.0 if (df['Этаж'] < df['Этажность'] and df['Этаж'] > 1 and etalonFloorValue == 2) else 0.0 + \
        #          7.5 if (df['Этаж'] == 1 and etalonFloorValue == 1) else 0.0 + \
        #             3.2 if (df['Этаж'] == 1 and etalonFloorValue == 2) else 0.0 + \
        #             -3.1 if (df['Этаж'] == df['Этажность'] and etalonFloorValue == 0) else 0.0 + \
        #             4.2 if (df['Этаж'] == df['Этажность'] and etalonFloorValue == 1) else 0.0
        df.to_excel("output.xlsx")
