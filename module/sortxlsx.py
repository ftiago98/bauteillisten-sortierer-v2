import pandas as pd
from formatxlsx import *
from sortxlsx import *

df = pd.read_excel('C:\Dev\Bauteillisten-sortierer-v2\data\Bauteilliste.xlsx')

set_every_empty_field_to_zero(df)
rename_Columns(df)
delete_unnecessary_components(df)
change_LT_to_L(df)
change_asymmetrisch_to_symmetrisch(df)
arrange_dimensions(df)
df = count_duplicates_and_delete(df)
df = delete_unnecessary_rows_and_columns(df)

#Save or override xlsx file

df.to_excel('C:\Dev\Bauteillisten-sortierer-v2\data\Bauteilliste_edited.xlsx')