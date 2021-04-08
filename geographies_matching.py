def reset_index_rename(df):
    df_columns = df.columns
    df_columns = df_columns.insert(0,'id')
    df = df.reset_index()
    df.columns=df_columns
    return df

def compute_matching_matrix(df_a, df_b, id_a=None, id_b=None, reverse=False):
    #if no column id name is defined, we assume it is the index,
    #we reset the index and rename it
    if not id_a:
        df_a = reset_index_rename(df_a)
        id_a = 'id'
    if not id_b:
        df_b = reset_index_rename(df_b)
        id_b = 'id'
    df_a = df_a[[id_a,'geometry']]
    df_a[id_a] = df_a[id_a].astype(str)
    df_b = df_b[[id_b,'geometry']]
    df_b[id_b] = df_b[id_b].astype(str)
    #if the two id columns have the same name, we rename them accounting for the overlay transformation
    if id_a==id_b:
        id_a = id_a + '_1'
        id_b = id_b + '_2'

    #if reverse==True, we group by the id of df_b otherwise we group y id of df_a
    if not reverse:
        id_from = id_b
        id_to = id_a
    else:
        id_from = id_a
        id_to = id_b
    tmp_overlay = gpd.overlay(df_a, df_b)
    tmp_overlay['area']= tmp_overlay.area
    tmp_overlay = tmp_overlay.merge(tmp_overlay.groupby(id_to).sum().rename(columns={'area':'total_area'}).reset_index(), on=id_to)
    tmp_overlay['ratio'] = tmp_overlay['area']/tmp_overlay['total_area']
    matching_ratio_matrix = tmp_overlay.pivot(index=id_to, columns=id_from, values='ratio')
    #id_to is the target geography: it will be the index of the matching table
    return matching_ratio_matrix
