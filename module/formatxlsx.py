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
    rename Column:
        - A (Column K / Index 10) to 'Breite'
        - B (Column L / Index 11) to 'Höhe'


'''
def rename_Columns(df):
    df.columns.values[10] = 'Breite'
    df.columns.values[11] = 'Höhe'


'''
    delete unnecessary components
'''
def delete_unnecessary_components(df):
    #set filter
    filt_no_IfcGlobalId = df[(df['IfcGlobalId'] == 0)].index
    #delete rows
    df.drop(filt_no_IfcGlobalId, inplace = True)

'''
    change 'LT' to 'L'
'''
def change_LT_to_L(df):
    # Components with ID LT are renamed to L
    df.replace({'LT': 'L'}, inplace=True)
    # Components with name Luftleitungsteil are renamed to Luftleitung
    df.replace({'Luftleitungsteil': 'Luftleitung'}, inplace=True)

'''
    compares all dimensions of a component
    sets the largest dimension as width and height
'''
def arrange_dimensions(df):
    #set filter
    components_luftleitung = df.loc[(df['KZ'] == 'L') | (df['KZ'] == 'BS')]

    #get index
    components_liste = components_luftleitung.index.tolist()
    
    for index in components_liste:
        width = components_luftleitung.loc[index, 'Breite']
        height = components_luftleitung.loc[index, 'Höhe']

        if width < height:
            tem_width = df.at[index, 'Breite']
            df.at[index, 'Breite'] = df.at[index, 'Höhe']
            df.at[index, 'Höhe'] = tem_width
    
    components_konus = df.loc[(df['KZ'] == 'UA') | (df['KZ'] == 'US')]
    
    #get index
    components_liste = components_konus.index.tolist()
    
    for index in components_liste:
        width_one = components_konus.loc[index, 'Breite']
        height_one = components_konus.loc[index, 'Höhe']
        width_two = components_konus.loc[index, 'C']
        height_two = components_konus.loc[index, 'D']

        surface_one = width_one * height_one
        surface_two = width_two * height_two

        if width_one < height_one:
            tem_width = df.at[index, 'Breite']
            df.at[index, 'Breite'] = df.at[index, 'Höhe']
            df.at[index, 'Höhe'] = tem_width
        
        if width_two < height_two:
            tem_width = df.at[index, 'C']
            df.at[index, 'C'] = df.at[index, 'D']
            df.at[index, 'D'] = tem_width

        if surface_one < surface_two:

            df.at[index, 'Breite'] = width_two
            df.at[index, 'Höhe'] = height_two
            df.at[index, 'C'] = width_one
            df.at[index, 'D'] = height_one

    #Hosenstücke, abzweigstücke, kreuzstück müssen noch hinzugefügt werden!

'''
    Uses filter to get all duplicates from the index row
    Add's up all important metrics
    delets all duplicate rows and updates the first with the new metrics
    renewes the index for every row (to ressolve KeyError Exception)
'''
def count_duplicates_and_delete(df):
    for index, row in df.iterrows():
        if len(df) > index:
            duplicatedRows = df.loc[(df['KZ'] == df.at[index, 'KZ']) & 
                                    (df['Breite'] == df.at[index, 'Breite']) & 
                                    (df['Höhe'] == df.at[index, 'Höhe']) & 
                                    (df['W'] == df.at[index, 'W']) & 
                                    (df['D'] == df.at[index, 'D']) & 
                                    (df['D1'] == df.at[index, 'D1']) & 
                                    (df['D2'] == df.at[index, 'D2']) & 
                                    (df['D3'] == df.at[index, 'D3']) & 
                                    (df['IsoArt'] == df.at[index, 'IsoArt']) & 
                                    (df['IsoZ'] == df.at[index, 'IsoZ']) & 
                                    (df['LtgTyp'] == df.at[index, 'LtgTyp'])]

            #length and pieces
            df.at[index, 'L'] = duplicatedRows['L'].sum()
            df.at[index, 'Anz'] = len(duplicatedRows)

            #isolation
            df.at[index, 'IsoOf'] = duplicatedRows['IsoOf'].sum() + duplicatedRows['OfRoh'].sum() + duplicatedRows['OfIsoBauteil'].sum()

            #get index of duplicates and delete them
            duplicatedRows_index = duplicatedRows.index.tolist()
            duplicatedRows_index.pop(0)

            df = df.drop(duplicatedRows_index)
            df = df.reset_index(drop=True)
    return df

'''
    delete all unnecessary column and rows in the file
    1. Empty field
    2. Generated Object without GuID
'''
def delete_unnecessary_rows_and_columns(df):

    '''
    unnecessary column:
        - Nr
        - TsNr
        - LvPos
        - PosNr
        - KennZahl
        - Art
        - AG
        - G
        - M
        - X
        - Y
        - Ra1Vt
        - Ra2Vt
        - Ra3Vt
        - OF
        - GW
        - Bem
        - Bem1
        - RF
        - Abmessung
        - Ma
        - MS
        - St
        - Bem2
        - Ra1Rl
        - Ra2Rl
        - Ra3Rl
        - OfRoh
        - AbrArt
        - ListTyp
        - ContainsIso
        - ContainsFrames
        - HatEinzelteilzeichnung
        - Du
        - Lu
        - OfRund
        - MaterialListeOf
        - Dmax
        - MaterialListeAG
        - IsZehnderUPV
        - IsHovalUPV
        - OfIsoBauteil
        - OfOval
        - OfL90
        - IfcGlobalId
        - Manufacturer
        - ArticleNumber
        - StandardNumber
    '''
    return None