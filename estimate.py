from io import BytesIO

import pandas as pd
import numpy as np


class PoolEstimate:
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
            exclude_list=None,
            etalon_square=None,
            kitchen_square_cor=None,
            balcony_cor=None,
            repair_state=None):
        """Подготовить данные с циана для корректировки, удаление неподходящих аналогов"""
        if exclude_list is None:
            exclude_list = []
        missing_df = self.missing_values_table(df)
        missing_columns = list(missing_df[missing_df['% of Total Values'] > 40].index)
        if balcony_cor:
            missing_columns.remove('Балкон')
        if repair_state:
            missing_columns.remove('Ремонт')
        missing_columns.append('Высота потолков, м')
        missing_columns.append('Тип')
        # missing_columns.append('Название ЖК')
        missing_columns.append('Окна')
        missing_columns.append('Количество комнат')
        missing_columns.append('Описание')
        df = df.drop(columns=list(missing_columns))

        df = df[~df.ID.isin(exclude_list)]

        if balcony_cor:
            df['Балкон'] = np.where(df['Балкон'].isna(), 0, 1)

        square_table_name = 'Площадь квартиры, кв.м'
        df[square_table_name] = df["Площадь, м2"].str.split('/').str[0]

        """Удаление неподходящих аналогов по квадратуре"""
        if etalon_square:
            cond_list = [
                np.logical_and(df[square_table_name].astype(float) > 65, etalon_square < 30),
                np.logical_and(df[square_table_name].astype(float) > 90, etalon_square <= 50),
                np.logical_and(df[square_table_name].astype(float) > 120, etalon_square <= 65),
                np.logical_and(df[square_table_name].astype(float) < 30, etalon_square > 65),
                np.logical_and(df[square_table_name].astype(float) <= 50, etalon_square > 90),
                np.logical_and(df[square_table_name].astype(float) <= 65, etalon_square > 120),
            ]
            choice_list = [
                np.nan,
                np.nan,
                np.nan,
                np.nan,
                np.nan,
                np.nan
            ]

            df[square_table_name] = np.select(cond_list, choice_list, default=df[square_table_name])

        kitchen_square_column_name = 'Площадь кухни, кв.м'
        if kitchen_square_cor:
            df[kitchen_square_column_name] = df["Площадь, м2"].str.split('/').str[2] if len(
                df["Площадь, м2"].str.split('/')) > 2 else np.nan

        if repair_state:
            replacements = {
                'Ремонт': {
                    'Без': 0,
                    'Косметический': 1,
                    'Евро|Диза': 2,
                }
            }

            df.replace(replacements, inplace=True, regex=True)
            df['Ремонт'] = np.where(df['Ремонт'].isna(), 0, df['Ремонт'])
        df.dropna(inplace=True)
        df = df.head()
        df['Этажность дома'] = df["Дом"].str.extract('(\/(?!\/)([0-9]+))')[1]
        df["Этаж расположения"] = df["Дом"].str.extract('([0-9]+)')[0]

        df["Материал"] = df["Дом"].str.extract('([ЁёА-я]+)')

        replacements = {
            'Материал': {
                'Моно': 0,
                'Кирп': 1,
                'Панел|Бло': 2,
            }
        }

        df.replace(replacements, inplace=True, regex=True)

        df["Цена/м"] = df['Цена'].str.extract('([0-9]+)')[0].astype(float) / df[square_table_name].astype(
            float)

        return df

    def make_pull_data_ready_for_work(
            self,
            df,
            etalon_room_count,
            etalon_segment,
            etalon_material,
            etalon_max_floor
    ):
        df['Балкон'] = np.where(df['Балкон'].str.contains('Нет', case=False), 0, 1)

        replacements = {
            'Ремонт': {
                'без|Без': 0,
                'муниц|Муниц': 1,
                'совр|Совр': 2,
            }
        }

        df.replace(replacements, inplace=True, regex=True)
        df['Ремонт'] = np.where(df['Ремонт'].isna(), 0, df['Ремонт'])

        replacements = {
            'Материал стен': {
                'Монолит|монолит': 0,
                'Кирп|кирп': 1,
                'Панел|панел': 2,
            }
        }

        df.replace(replacements, inplace=True, regex=True)

        df['Количество комнат'] = np.where(df['Количество комнат'] == etalon_room_count, df['Количество комнат'],
                                           np.nan)
        df['Сегмент'] = np.where(df['Сегмент'] == etalon_segment, df['Сегмент'], np.nan)
        df['Этажность дома'] = np.where(df['Этажность дома'] == etalon_max_floor, df['Этажность дома'], np.nan)
        df['Материал стен'] = np.where(df['Материал стен'] == etalon_material, df['Материал стен'], np.nan)

        df.dropna(inplace=True)
        return df

    def calculate_floor_k(self, df: pd.DataFrame, etalon_floor_value):
        """Рассчитать коэффициент этажности"""
        max_floor_column_name = 'Этажность дома'
        floor_column_name = 'Этаж расположения'
        cond_list = [
            np.logical_and(
                np.logical_and(df[floor_column_name].astype(int) > 1,
                               df[floor_column_name].astype(int) < df[max_floor_column_name].astype(int)),
                etalon_floor_value == 0),
            np.logical_and(
                np.logical_and(df[floor_column_name].astype(int) > 1,
                               df[floor_column_name].astype(int) < df[max_floor_column_name].astype(int)),
                etalon_floor_value == 2),
            np.logical_and(df[floor_column_name] == 1, etalon_floor_value == 1),
            np.logical_and(df[floor_column_name] == 1, etalon_floor_value == 2),
            np.logical_and(df[floor_column_name] == df[max_floor_column_name], etalon_floor_value == 0),
            np.logical_and(df[floor_column_name] == df[max_floor_column_name], etalon_floor_value == 1),
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


    def calculate_balcony_k(self, df: pd.DataFrame, etalon_balcony: int):
        """Рассчитать коэффициент по наличию балкона"""
        condlist = [
            np.logical_and(df['Балкон'].astype(int) == 1, etalon_balcony == 0),
            np.logical_and(df['Балкон'].astype(int) == 0, etalon_balcony == 1)
        ]
        choicelist = [
            -0.05,
            0.053
        ]
        return np.select(condlist, choicelist, default=0.0)

    def calculate_kitchen_k(self, df: pd.DataFrame, etalon_kitchen_square):
        kitchen_square_column_name = 'Площадь кухни, кв.м'
        cond_list = [
            np.logical_and(
                np.logical_and(df[kitchen_square_column_name].astype(float) >= 7,
                               df[kitchen_square_column_name].astype(float) < 10),
                etalon_kitchen_square < 7),
            np.logical_and(
                np.logical_and(df[kitchen_square_column_name].astype(float) >= 7,
                               df[kitchen_square_column_name].astype(float) < 10),
                etalon_kitchen_square >= 10),
            np.logical_and(
                df[kitchen_square_column_name].astype(float) < 7,
                np.logical_and(etalon_kitchen_square >= 7, etalon_kitchen_square < 10)),
            np.logical_and(
                df[kitchen_square_column_name].astype(float) < 7,
                etalon_kitchen_square >= 10),
            np.logical_and(
                df[kitchen_square_column_name].astype(float) >= 10,
                etalon_kitchen_square < 7),
            np.logical_and(
                df[kitchen_square_column_name].astype(float) >= 10,
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

    def calculate_repair_state_k(self, df: pd.DataFrame, etalon_repair_state):
        cond_list = [
            np.logical_and(df['Ремонт'].astype(int) == 0, etalon_repair_state == 1),
            np.logical_and(df['Ремонт'].astype(int) == 0, etalon_repair_state == 2),
            np.logical_and(df['Ремонт'].astype(int) == 1, etalon_repair_state == 0),
            np.logical_and(df['Ремонт'].astype(int) == 1, etalon_repair_state == 2),
            np.logical_and(df['Ремонт'].astype(int) == 2, etalon_repair_state == 0),
            np.logical_and(df['Ремонт'].astype(int) == 2, etalon_repair_state == 1),
        ]
        choice_list = [
            13400,
            20100,
            -13400,
            6700,
            -20100,
            -6700
        ]
        return np.select(cond_list, choice_list, default=0.0)

    def calculate_square_k(self, df: pd.DataFrame, full_square):
        table_name = 'Площадь квартиры, кв.м'
        condlist = [
            np.logical_and(df[table_name].astype(float) < 30, np.logical_and(full_square >= 30, full_square < 50)),
            np.logical_and(
                df[table_name].astype(float) < 30,
                np.logical_and(full_square >= 50, full_square < 65)),
            np.logical_and(
                np.logical_and(df[table_name].astype(float) >= 30, df[table_name].astype(float) < 50),
                full_square < 30),
            np.logical_and(
                np.logical_and(df[table_name].astype(float) >= 30, df[table_name].astype(float) < 50),
                np.logical_and(full_square < 65, full_square >= 50)),
            np.logical_and(
                np.logical_and(df[table_name].astype(float) >= 30, df[table_name].astype(float) < 50),
                np.logical_and(full_square >= 65, full_square < 90)),
            np.logical_and(
                np.logical_and(df[table_name].astype(float) >= 50, df[table_name].astype(float) < 65),
                full_square < 30),
            np.logical_and(
                np.logical_and(df[table_name].astype(float) >= 50, df[table_name].astype(float) < 65),
                np.logical_and(full_square < 50, full_square >= 30)),
            np.logical_and(
                np.logical_and(df[table_name].astype(float) >= 50, df[table_name].astype(float) < 65),
                np.logical_and(full_square < 90, full_square >= 65)),
            np.logical_and(
                np.logical_and(df[table_name].astype(float) >= 50, df[table_name].astype(float) < 65),
                np.logical_and(full_square >= 90, full_square < 120)),
            np.logical_and(
                np.logical_and(df[table_name].astype(float) >= 65, df[table_name].astype(float) < 90),
                np.logical_and(full_square < 50, full_square >= 30)),
            np.logical_and(
                np.logical_and(df[table_name].astype(float) >= 65, df[table_name].astype(float) < 90),
                np.logical_and(full_square < 65, full_square >= 50)),
            np.logical_and(
                np.logical_and(df[table_name].astype(float) >= 65, df[table_name].astype(float) < 90),
                np.logical_and(full_square < 120, full_square >= 90)),
            np.logical_and(
                np.logical_and(df[table_name].astype(float) >= 65, df[table_name].astype(float) < 90),
                full_square >= 120),
            np.logical_and(
                np.logical_and(df[table_name].astype(float) >= 90, df[table_name].astype(float) < 120),
                np.logical_and(full_square < 65, full_square >= 50)),
            np.logical_and(
                np.logical_and(df[table_name].astype(float) >= 90, df[table_name].astype(float) < 120),
                np.logical_and(full_square < 90, full_square >= 65)),
            np.logical_and(
                np.logical_and(df[table_name].astype(float) >= 90, df[table_name].astype(float) < 120),
                full_square >= 120),
            np.logical_and(
                df[table_name].astype(float) >= 120,
                np.logical_and(full_square < 90, full_square >= 65)),
            np.logical_and(
                df[table_name].astype(float) >= 120,
                np.logical_and(full_square < 120, full_square >= 90)),
            np.logical_and(
                df[table_name].astype(float) < 30,
                np.logical_and(full_square < 90, full_square >= 65)),
            np.logical_and(
                df[table_name].astype(float) < 30,
                np.logical_and(full_square < 120, full_square >= 90)),
            np.logical_and(
                df[table_name].astype(float) < 30,
                full_square >= 120),
            np.logical_and(
                np.logical_and(df[table_name].astype(float) >= 30, df[table_name].astype(float) < 50),
                np.logical_and(full_square < 120, full_square >= 90)),
            np.logical_and(
                np.logical_and(df[table_name].astype(float) >= 30, df[table_name].astype(float) < 50),
                full_square > 120),
            np.logical_and(
                np.logical_and(df[table_name].astype(float) >= 50, df[table_name].astype(float) < 65),
                full_square >= 120),
            np.logical_and(
                np.logical_and(df[table_name].astype(float) >= 65, df[table_name].astype(float) < 90),
                full_square < 30),
            np.logical_and(
                np.logical_and(df[table_name].astype(float) >= 90, df[table_name].astype(float) < 120),
                full_square < 30),
            np.logical_and(
                np.logical_and(df[table_name].astype(float) >= 90, df[table_name].astype(float) < 120),
                np.logical_and(full_square >= 30, full_square < 50)),
            np.logical_and(
                df[table_name].astype(float) >= 120,
                full_square < 30),
            np.logical_and(
                df[table_name].astype(float) >= 120,
                np.logical_and(full_square < 50, full_square >= 30)),
            np.logical_and(
                df[table_name].astype(float) >= 120,
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

    """
        max_floor - Этажность
    """

    def calculate_cor(
            self,
            data: BytesIO,
            exclude_list=None,
            address="",
            room_count=0,
            material="",
            segment="",
            max_floor=0,
            auction_cor=None,
            floor_cor=None,
            square_cor=None,
            kitchen_square_cor=None,
            balcony_cor=False,
            metro_stepway_cor=None,
            repair_state=None
    ):
        if exclude_list is None:
            exclude_list = []
        etalon_floor_value = 0

        if floor_cor:
            if floor_cor == max_floor:
                etalon_floor_value = 2
            elif 1 < floor_cor < max_floor:
                etalon_floor_value = 1

        has_balcony = 0

        if balcony_cor:
            has_balcony = 1

        auction_value = -0.045 if auction_cor else 0

        if repair_state:
            repair_state = 1 if repair_state.lower() == 'муниципальный ремонт' else (
                0 if repair_state.lower() == 'без отделки' else 2)

        df = pd.read_excel(data)
        df = self.make_data_ready_for_work(
            df,
            exclude_list=exclude_list,
            etalon_square=square_cor,
            kitchen_square_cor=kitchen_square_cor,
            balcony_cor=has_balcony,
            repair_state=repair_state
        )

        if floor_cor:
            df['ЭтажК'] = self.calculate_floor_k(df, etalon_floor_value)
        if square_cor:
            df['ПлощадьК'] = self.calculate_square_k(df, square_cor)
        if balcony_cor:
            df['БалконК'] = self.calculate_balcony_k(df, etalon_balcony=has_balcony)
        if kitchen_square_cor:
            df['КухняК'] = self.calculate_kitchen_k(df, etalon_kitchen_square=kitchen_square_cor)
        if repair_state:
            df['РемонтК'] = self.calculate_repair_state_k(df, repair_state)

        df['Итого сумма, кв метр'] = (df['Цена/м'].astype(float)) * (
                1 + (df['ЭтажК'].astype(float) if floor_cor else 0)
                + (df['ПлощадьК'].astype(float) if square_cor else 0)
                + (df['БалконК'].astype(float) if balcony_cor else 0)
                + (df['КухняК'].astype(float) if kitchen_square_cor else 0)
                + auction_value) + (df['РемонтК'] if repair_state else 0)

        etalon_price = df['Итого сумма, кв метр'].mean()

        # df_etalon["Цена, кв метр"] = etalon_price

        dict_etalon = {"row_1": [address,
                                 room_count,
                                 segment,
                                 max_floor,
                                 material,
                                 floor_cor,
                                 square_cor,
                                 kitchen_square_cor,
                                 balcony_cor,
                                 metro_stepway_cor,
                                 repair_state,
                                 etalon_price]}
        df_etalon = pd.DataFrame.from_dict(dict_etalon, orient='index')

        columns = [
            'Местоположение',
            'Количество комнат',
            'Сегмент(Новостройка, современное жилье, старый жилой фонд)',
            'Этажность дома',
            "Материал стен(Кипич, панель, монолит)",
            "Этаж расположения",
            "Площадь квартиры, кв.м",
            "Площадь кухни, кв.м",
            "Наличие балкона / лоджии",
            "Удаленность от станции метро, мин.пешком",
            "Состояние(без отделки, муниципальный ремонт, с современная отделка)",
            "Цена за кв метр"
        ]
        df_etalon.columns = columns
        writer = pd.ExcelWriter('output.xlsx', engine='openpyxl')
        df_etalon.to_excel(writer, sheet_name='Эталон')
        df.to_excel(writer, sheet_name='Аналоги')
        writer.close()

        etalon_json = df_etalon.to_json(orient="records")
        # result_df = pd.ExcelFile('output.xlsx', engine='openpyxl')

        return [etalon_json, df.to_json(orient="records")]

    """
    pull - загруженный пользователем файл для расчета  
    etalon_price - цена за квадратный метр эталона на основе рассчета предыдущей функции  
    """
    def calculate_pull(
            self,
            pull: BytesIO,
            etalon_json,
            auction_cor=True,
            floor_cor=True,
            square_cor=True,
            kitchen_square_cor=True,
            balcony_cor=True,
            metro_stepway_cor=False,
            repair_state=True
    ):
        df_etalon = pd.read_json(etalon_json, orient='records')

        etalon_floor = df_etalon.iloc[:, 5][0]
        etalon_room_count = df_etalon.iloc[:, 1][0]
        etalon_segment = df_etalon.iloc[:, 2][0]
        etalon_max_floor = df_etalon.iloc[:, 3][0]
        etalon_material = df_etalon.iloc[:, 4][0]
        etalon_price = df_etalon.iloc[:, 11][0]
        etalon_square = df_etalon.iloc[:, 6][0]
        etalon_kitchen_square = df_etalon.iloc[:, 7][0]
        etalon_has_balkony = df_etalon.iloc[:, 8][0]
        etalon_metro_stepway = df_etalon.iloc[:, 9][0]
        etalon_repair_state = df_etalon.iloc[:, 10][0]

        if floor_cor:
            if etalon_floor == etalon_max_floor:
                etalon_floor = 2
            elif 1 < etalon_floor < etalon_max_floor:
                etalon_floor = 1

        auction_value = -0.045 if auction_cor else 0

        pull_df = pd.read_excel(pull)

        pull_df.rename(columns={
            pull_df.columns[2]: "Сегмент",
            pull_df.columns[10]: "Ремонт",
            pull_df.columns[8]: "Балкон",
            pull_df.columns[4]: "Материал стен"
        }, inplace=True)

        pull_df = self.make_pull_data_ready_for_work(
            pull_df,
            etalon_room_count=etalon_room_count,
            etalon_segment=etalon_segment,
            etalon_material=etalon_material,
            etalon_max_floor=etalon_max_floor
        )

        if floor_cor:
            pull_df['ЭтажК'] = self.calculate_floor_k(pull_df, etalon_floor)
        if square_cor:
            pull_df['ПлощадьК'] = self.calculate_square_k(pull_df, etalon_square)
        if balcony_cor:
            pull_df['БалконК'] = self.calculate_balcony_k(pull_df, etalon_balcony=etalon_has_balkony)
        if kitchen_square_cor:
            pull_df['КухняК'] = self.calculate_kitchen_k(pull_df, etalon_kitchen_square=etalon_kitchen_square)
        if repair_state:
            pull_df['РемонтК'] = self.calculate_repair_state_k(pull_df, etalon_repair_state)

        pull_df['Итого сумма, кв метр'] = etalon_price * (
                1 + (pull_df['ЭтажК'].astype(float) if floor_cor else 0)
                + (pull_df['ПлощадьК'].astype(float) if square_cor else 0)
                + (pull_df['БалконК'].astype(float) if balcony_cor else 0)
                + (pull_df['КухняК'].astype(float) if kitchen_square_cor else 0)
                + auction_value) + (pull_df['РемонтК'] if repair_state else 0)

        replacements = {
            'Ремонт': {
                0: 'Без ремонта',
                1: 'Муниципальный ремонт',
                2: 'Современный ремонт',
            }
        }

        pull_df.replace(replacements, inplace=True, regex=True)

        pull_df.dropna(inplace=True)

        replacements = {
            'Материал стен': {
                0: 'Монолит',
                1: 'Кирпич',
                2: 'Панельный',
            }
        }

        pull_df.replace(replacements, inplace=True, regex=True)

        writer = pd.ExcelWriter('output_pull.xlsx', engine='openpyxl')
        df_etalon.to_excel(writer, sheet_name='Эталон')
        pull_df.to_excel(writer, sheet_name='Пул')
        writer.close()

        return [df_etalon.to_json(orient="records"), pull_df.to_json(orient="records")]

