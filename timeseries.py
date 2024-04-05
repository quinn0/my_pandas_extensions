import pandas as pd
import numpy as np
#to use in chain
import pandas_flavor as pf

@pf.register_dataframe_method
def summarize_by_time(data, date_col = "order_date", 
                      value_col = "total_price", rule = "D",
                      groups = None, agg_func = np.sum,
                      kind = 'timestamp', 
                      wide_format = True,
                      fillna = np.nan,
                      *args,**kwargs):
    """_summary_

    Args:
        data (_type_): _description_
        date_col (str, optional): _description_. Defaults to "order_date".
        value_col (str, optional): _description_. Defaults to "total_price".
        rule (str, optional): _description_. Defaults to "D".
        groups (_type_, optional): _description_. Defaults to None.
        agg_func (_type_, optional): _description_. Defaults to np.sum.
        kind (str, optional): _description_. Defaults to 'timestamp'.
        wide_format (bool, optional): _description_. Defaults to True.
        fillna (_type_, optional): _description_. Defaults to np.nan.

    Raises:
        TypeError: _description_

    Returns:
        _type_: _description_
    """
    
    ##Checks
    if type(data) is not pd.DataFrame:
        raise TypeError("'data' is not Pandas DataFrame.")
    
    
    data = data.set_index(date_col)
    
    if groups is not None:
        data = data.groupby(groups)
    if type(value_col) is not list:
        value_col = [value_col]
    if type(agg_func) is not list:
        agg_func = [agg_func]
        
    data = data.resample(rule = rule,
                         kind = kind,
                         **kwargs)
    ##handles aggregation regardless of group (eg no group Vs >= 1 group)
    func_list = agg_func * len(value_col)
    agg_dict = dict(zip(value_col, func_list))
    ##now can control specific columns in aggregation
    data = data\
        .agg(func = agg_dict, 
             *args,
             **kwargs)
    #pivot wide    
    if (wide_format) and groups is not None:
        data = data.unstack(groups)
        if(kind == "period"):
            data.index = data.index.to_period(freq = rule)
        
    data = data.fillna(value = fillna)
        
    return data