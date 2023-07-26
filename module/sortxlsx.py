import pandas as pd
from formatxlsx import *
from sortxlsx import *

df = pd.read_excel('C:\Dev\Bauteillisten-sortierer-v2\data\Bauteilliste.xlsx')

set_every_empty_field_to_zero(df)
rename_Columns(df)
delete_unnecessary_components(df)
change_LT_to_L(df)
arrange_dimensions(df)
df = count_duplicates_and_delete(df)

#Save or override xlsx file
df.to_excel('C:\Dev\Bauteillisten-sortierer-v2\data\Bauteilliste_edited.xlsx')

'''
#change_columnA_with_columnB(df)
#rename_ColumnA(df)
delete_unnecessary_rows_and_columns(df)

change_LT_to_L(df)
swap_dimensions_duct(df)
swap_dimensions_duct_cone(df)

#sort the components list and delete duplicated rows
df = count_duplicates_and_delete(df)


'''