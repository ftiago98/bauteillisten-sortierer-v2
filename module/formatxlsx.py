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
    rename Column
'''
def rename_Columns(df):
    df.columns.values[10] = 'Breite'
    df.columns.values[11] = 'Höhe'
    df.columns.values[12] = 'Breite reduziert'
    df.columns.values[13] = 'Höhe reduziert'
    df.columns.values[16] = 'Gesamtlänge'
    df.columns.values[17] = 'Winkel'
    df.columns.values[30] = 'Isolation m²'
    df.columns.values[46] = 'Art der Isolation'
    df.columns.values[47] = 'Dämmdicke'
    df.columns.values[49] = 'Medium'
    
'''
    delete unnecessary components
'''
def delete_unnecessary_components(df):
    #set filter
    filt_no_IfcGlobalId = df[(df['IfcGlobalId'] == 0)].index
    #delete rows
    df.drop(filt_no_IfcGlobalId, inplace = True)
'''
    change 'LT' to 'Gesamtlänge'
'''
def change_LT_to_L(df):
    # Components with ID LT are renamed to L
    df.replace({'LT': 'L'}, inplace=True)
    # Components with name Luftleitungsteil are renamed to Luftleitung
    df.replace({'Luftleitungsteil': 'Luftleitung'}, inplace=True)

'''
    Rename 'Übergang Asymmetrisch' to 'Übergang Symmetrisch'
'''
def change_asymmetrisch_to_symmetrisch(df):
    df.replace({'UA': 'US'}, inplace=True)
    df.replace({'Übergang asymmetrisch': 'Übergang symmetrisch'}, inplace=True)


'''
    compares all dimensions of a component
    sets the largest dimension as width and height
'''
def arrange_dimensions(df):
    #set filter
    components_luftleitung = df.loc[(df['KZ'] == 'Gesamtlänge') | (df['KZ'] == 'BS')]

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
        width_two = components_konus.loc[index, 'Breite reduziert']
        height_two = components_konus.loc[index, 'Höhe reduziert']

        surface_one = width_one * height_one
        surface_two = width_two * height_two

        if width_one < height_one:
            tem_width = df.at[index, 'Breite']
            df.at[index, 'Breite'] = df.at[index, 'Höhe']
            df.at[index, 'Höhe'] = tem_width
        
        if width_two < height_two:
            tem_width = df.at[index, 'Breite reduziert']
            df.at[index, 'Breite reduziert'] = df.at[index, 'Höhe reduziert']
            df.at[index, 'Höhe reduziert'] = tem_width

        if surface_one < surface_two:

            df.at[index, 'Breite'] = width_two
            df.at[index, 'Höhe'] = height_two
            df.at[index, 'Breite reduziert'] = width_one
            df.at[index, 'Höhe reduziert'] = height_one

    #Hosenstücke, abzweigstücke, kreuzstück müssen noch hinzugefügt werden!

'''
    Uses filter to get all duplicates from the index row
    Add's up all important metrics
    delets all duplicate rows and updates the first with the new metrics
    renewes the index for every row (to ressolve KeyError Exception)
'''
def count_duplicates_and_delete(df):
    df = df.reset_index(drop=True)
    for index, row in df.iterrows():
        if len(df.axes[0]) > index:
            duplicatedRows = df.loc[(df['KZ'] == df.at[index, 'KZ']) & 
                                    (df['Breite'] == df.at[index, 'Breite']) & 
                                    (df['Höhe'] == df.at[index, 'Höhe']) & 
                                    (df['Winkel'] == df.at[index, 'Winkel']) & 
                                    (df['Höhe reduziert'] == df.at[index, 'Höhe reduziert']) & 
                                    (df['D1'] == df.at[index, 'D1']) & 
                                    (df['D2'] == df.at[index, 'D2']) & 
                                    (df['D3'] == df.at[index, 'D3']) & 
                                    (df['Art der Isolation'] == df.at[index, 'Art der Isolation']) & 
                                    (df['Dämmdicke'] == df.at[index, 'Dämmdicke']) & 
                                    (df['Medium'] == df.at[index, 'Medium'])]

            #length and pieces
            df.at[index, 'Gesamtlänge'] = duplicatedRows['Gesamtlänge'].sum()
            df.at[index, 'Anz'] = len(duplicatedRows)

            '''
            count isolation:
                -IsoOf = square
                -OfIsoRund = round
                -OfIsoBauteil = components
            '''
            df.at[index, 'Isolation m²'] = duplicatedRows['Isolation m²'].sum() + duplicatedRows['OfIsoRund'].sum() + duplicatedRows['OfIsoBauteil'].sum()

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

    df.drop(['Nr', 'OfIsoRund', 'TsNr', 'LvPos', 'PosNr', 'KennZahl', 
             'Art', 'AG', 'G', 'M', 'X', 'Y', 'Ra1Vt', 'Ra2Vt', 
             'Ra3Vt', 'OF', 'GW', 'Bem', 'Bem1', 'RF', 'Abmessung', 
             'Ma', 'MS', 'St', 'Bem2', 'Ma', 'Ra1Rl', 'Ra2Rl', 'Ra3Rl', 
             'OfRoh', 'AbrArt', 'ListTyp', 'ContainsIso', 'ContainsFrames', 
             'HatEinzelteilzeichnung', 'Du', 'Lu', 'OfRund','MaterialListeOf','Dmax', 
             'MaterialListeAG', 'IsZehnderUPV', 'IsHovalUPV', 'OfIsoBauteil','OfOval', 
             'OfL90', 'IfcGlobalId', 'Manufacturer', 'ArticleNumber', 'StandardNumber',
             'L1','L2','L3','L4','L5', 'R', 'N', 'E', 'F', 'KZ'], inplace=True, axis=1)
    return df