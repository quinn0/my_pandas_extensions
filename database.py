import pandas as pd
import sqlalchemy as sql
from pandas_profiling import ProfileReport,\
profile_report

#COLLECT DATA
def collect_data(prof = True, con_str = "sqlite:///00_database/bike_orders_database.sqlite"):
    """
    Merges all BikeSales Data w/ Total Price

    Args:
        con_str (str, optional):
        path to SQLite file 
        Defaults to 
        "sqlite:///00_database/bike_orders_database.sqlite".

    Returns:
        Merged DataFrame
    """
    
    
    engine = sql.create_engine(con_str)
    conn = engine.connect()
    
    table_names = ['bikes', 'bikeshops', 'orderlines']

    data_dict = {}
    
    for table in table_names:
        data_dict[table] = \
        pd.read_sql(f"SELECT * FROM {table}", conn)\
        .drop("index", axis = 1)
       
    df = pd.DataFrame(data_dict["orderlines"])\
    .merge(right = pd.DataFrame(data_dict['bikes']),
           how = 'left',
           left_on="product.id",
           right_on="bike.id")\
    .merge(right = pd.DataFrame(data_dict['bikeshops']),
           how = "left",
           left_on = 'customer.id',
           right_on = "bikeshop.id")
    conn.close()
    #clean
    
    df['order.date'] = pd.to_datetime(df['order.date'])
    temp_df = df['description']\
        .str.split(pat = " - ", expand= True)

    df['terrain'] = temp_df[0]
    df['terrain2'] = temp_df[1]
    df['frame_material'] = temp_df[2]
    
    temp_df = df['location']\
    .str.split(pat = ", ", expand= True)
    
    df['city'] = temp_df[0]
    df['state'] = temp_df[1]
    df['total_price'] = df['quantity']*df['price']

    df.sort_values("total_price", ascending= False, inplace= True)

    keep_ls = ['order.id', 
    'order.line', 
    'order.date', 
    'product.id',
    'quantity', 
    'price',
    'total_price',
    'model', 
    'description',
    'bikeshop.name', 
    'city',
    'state', 
    'terrain', 
    'terrain2', 
    'frame_material']
    df  =df[keep_ls]

    df.columns = df.columns.str.replace(".", "_")
    if(prof): 
        ProfileReport(df).to_notebook_iframe() 
    
    return df
