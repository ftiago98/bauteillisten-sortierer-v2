import pandas as pd
from formatxlsx import *
from sortxlsx import *

df = pd.read_excel('D:\BauteillistenSortierer\data\Bauteilliste.xlsx')

#format xlsx for future changes
set_every_empty_field_to_zero(df)






'''
#change_columnA_with_columnB(df)
#rename_ColumnA(df)
delete_unnecessary_rows_and_columns(df)

change_LT_to_L(df)
swap_dimensions_duct(df)
swap_dimensions_duct_cone(df)

#sort the components list and delete duplicated rows
df = count_duplicates_and_delete(df)

#Save or override xlsx file
df.to_excel('D:\BauteillistenSortierer\data\Bauteilliste_edited.xlsx')
'''