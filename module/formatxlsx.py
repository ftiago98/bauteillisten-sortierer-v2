import pandas as pd  
import numpy as np

'''
    Empty fields (Nan) generated errors
    Resolution -> fill all empty fields with the value 0
'''
def set_every_empty_field_to_zero(df):
    #replaces all empty fields with the value 0
    df.fillna(0, inplace = True)

'''
    Column K = height
    Kolumn L = width
    function swaps both columns to get bxh
'''
def change_columnA_with_columnB(df):
    #get all Column in the xlsx
    column_list = list(df)

    #swap both column
    column_list[10], column_list[11] = column_list[11], column_list[10]
    df.columns = column_list

'''
    rename Column A (Index 11) to H (height)
'''
def rename_ColumnA(df):
    df.columns.values[11] = 'H'

'''
    delete all unnecessary column and rows in the file
    1. Empty field
    2. Generated Object without GuID
'''
def delete_unnecessary_rows_and_columns(df):
    #Define filter
    filt_no_IfcGlobalId = df[(df['IfcGlobalId'] == '0')].index

    #delete rows
    df.drop(filt_no_IfcGlobalId, inplace = True)

'''
    Duct transitions are usually generated on random lenghts.
    So that these components do not generate unnecessary lines, they are rounded to 500mm, 750mm and 1000m.
'''
def format_etagen_and_konus(df):
    #set filter
    components = df.loc[(df['KZ'] == 'UA')]
    
    #get index from every etage / konus
    components_liste = components.index.tolist()
    
    #format every length
    for index in components_liste:
        length = components.loc[index, 'L']
        
        if length < 500.0:
            df.at[index, 'L'] = 500.0
        elif length < 750.0:
            df.at[index, 'L'] = 750.0
        elif length < 1000.0:
            df.at[index, 'L'] = 1000.0
        else:
            df.at[index, 'L'] = 1500.0

'''
    change 'LT' to 'L' 
'''
def change_LT_to_L(df):
    # Components with ID LT are renamed to component L
    df.replace({'LT': 'L'}, inplace=True)
    # Components with name Luftleitungsteil are renamed to Luftleitung
    df.replace({'Luftleitungsteil': 'Luftleitung'}, inplace=True)

'''
    Bei Kanälen sollte das grössere Mass in die Spalte 'Breite' eingetragen werden
    Dadurch können doppelte Zeilen verhindert werden
'''
def swap_dimensions_duct(df):
    #set filter
    components = df.loc[(df['KZ'] == 'L')]

    #get index
    components_liste = components.index.tolist()
    
    for index in components_liste:
        width = components.loc[index, 'Breite']
        height = components.loc[index, 'Höhe']

        if width < height:
            tem_width = df.at[index, 'Breite']
            df.at[index, 'Breite'] = df.at[index, 'Höhe']
            df.at[index, 'Höhe'] = tem_width

'''
    Bei Konus/Übergang müssen die grösste Abmessung in 'Breite' und 'Höhe' eingetragen werden
    Um die grössere Seite herauszufinden werden die Flächen verglichen
    Dadurch können doppelte Zeilen verhindert werden
'''
def swap_dimensions_duct_cone(df):
    components = df.loc[(df['KZ'] == 'UA')]
    
    #get index
    components_liste = components.index.tolist()
    
    for index in components_liste:
        width_one = components.loc[index, 'Breite']
        height_one = components.loc[index, 'Höhe']
        width_two = components.loc[index, 'C']
        height_two = components.loc[index, 'D']

        surface_one = width_one * height_one
        surface_two = width_two * height_two

        if surface_one < surface_two:

            df.at[index, 'Breite'] = width_two
            df.at[index, 'Höhe'] = height_two

            df.at[index, 'C'] = width_one
            df.at[index, 'D'] = height_one

'''
    Uses filter to get all duplicates from the index row
    Add's up all important metrics
    delets all duplicate rows and updates the first with the new metrics
    renewes the index for every row (to ressolve KeyError Exception)
'''
def count_duplicates_and_delete(df):
    for index, row in df.iterrows():
        if len(df) > index:
            duplicatedRows = df.loc[(df['KZ'] == df.at[index, 'KZ']) & (df['Breite'] == df.at[index, 'Breite']) & (df['Höhe'] == df.at[index, 'Höhe']) & (df['W'] == df.at[index, 'W']) & (df['D'] == df.at[index, 'D']) & (df['D1'] == df.at[index, 'D1']) & (df['D2'] == df.at[index, 'D2']) & (df['D3'] == df.at[index, 'D3']) & (df['IsoArt'] == df.at[index, 'IsoArt']) & (df['IsoZ'] == df.at[index, 'IsoZ']) & (df['LtgTyp'] == df.at[index, 'LtgTyp'])]

            #length and pieces
            df.at[index, 'L'] = duplicatedRows['L'].sum()
            df.at[index, 'Anz'] = len(duplicatedRows)

            #isolation
            df.at[index, 'IsoOf'] = duplicatedRows['IsoOf'].sum() + duplicatedRows['OfRoh'].sum()

            #get index of duplicates and delete them
            duplicatedRows_index = duplicatedRows.index.tolist()
            df = df.drop(duplicatedRows_index)
            df = df.reset_index(drop=True)
    return df