def process_to_dict(input_vec):
##reading in the data
    import pandas as pd
    from datetime import datetime
    
    collist, nullablelist,typelist,list_of_colnames = list_creation()
    
    
    for i in input_vec:    
        df = pd.read_excel(i,header=[2])
            #df.reset_index(inplace=True)
        df.drop(['DoC issue date','DoC expiry date','Additional information to facilitate the understanding of the reported average operational energy efficiency indicators','Average density of the cargo transported [m tonnes / m³]'],axis = 1,inplace=True)
        df.columns = collist



        for c in [list_of_colnames[4]]:
            df[c] = df[c].apply(pd.to_numeric, errors='coerce')

        for c in [list_of_colnames[6]]:
            df[c] = df[c].apply(pd.to_numeric, errors='coerce')

        dj = df.to_dict(orient = 'records')
        
        yield dj

def list_creation():
    
    from sqlalchemy import create_engine, Column, Integer, String, Table,MetaData, Unicode, Date, Float
    import sqlalchemy
    #input list, replace with argument

    #chunks of col
    ship_col = ['imo_number','name','type','reporting_period','technical_efficiency','port_of_registry','home_port','ice_class']
    ship_nullable = [False,False,False,False,False,False,True,True,True]
    ship_dtype = [Integer, String, String, Integer, String, String, String, String]

    #doc_col = ['issue_date','expiry_date']
    #doc_nullable = [False, False]
    #doc_dtype = [Date,Date]

    verif_col = ['verif_num','verif_name','verif_NAB','verif_address','verif_city','verif_accred_num','verif_country']
    verif_nullable = [True, False, False, False, False, False,False,False]
    verif_dtype = [String for j in range(0,8)]

    monitor_col = ['method_a','method_b','method_c','method_d']
    monitor_nullable = [True, True, True, True]
    monitor_dtype = [String for j in range(0,8)]

    totals_col = ['total_fuel_consum_ton','laden_fuel_consum_ton','total_c02_emit_ton','to_from_ms_juris_c02_emit_ton','from_ms_juris_c02_emit_ton','to_ms_juris_c02_emit_ton','port_ms_juris_c02_emit_ton','passenger_c02_emit_ton','freight_c02_emit_ton','laden_c02_emit_ton','time_at_sea_hours']
    totals_nullable = [False,True]
    totals_nullable.extend([False for i in range(0,5)])
    totals_nullable.extend([True for j in range(0,4)]) 
    totals_dtype = [Float for k in range(0,9)]

    averages_col = ['mean_fuel_consumption_kg_m','mean_fuel_consumption_transpo_mass_kg_m','mean_fuel_consumption_transpo_vol_kg_m','mean_fuel_consumption_transpo_deadweight_kg_m','mean_fuel_consumption_transpo_pax_kg_m','mean_fuel_consumption_freightwork_kg_m','mean_c02_emit_kg_knot','mean_c02_emit_transpo_mass_kg_m','mean_c02_emit_transpo_vol_kg_m','mean_c02_emit_transpo_deadweight_kg_m','mean_c02_emit_transpo_pax_kg_m','mean_c02_emit_freightwork_kg_m']
    averages_nullable = [True for k in range(0,12)]
    averages_dtype = [Float for k in range(0,12)]

    vol_distancetime_col = ['naut_m_thru_ice','hours_at_sea','hours_at_sea_thru_ice']
    vol_distancetime_nullable = [True,True,True]
    vol_distancetime_dtype = [Float,Float,Float]

    vol_energyeff_col = ['laden_mean_fuel_consumption_kg_m','laden_mean_fuel_consumption_transpo_mass_kg_m','laden_mean_fuel_consumption_transpo_vol_kg_m','laden_mean_fuel_consumption_transpo_deadweight_kg_m','laden_mean_fuel_consumption_transpo_pax_kg_m','laden_mean_fuel_consumption_freightwork_kg_m','laden_mean_c02_emit_kg_knot','laden_mean_c02_emit_transpo_mass_kg_m','laden_mean_c02_emit_transpo_vol_kg_m','laden_mean_c02_emit_transpo_deadweight_kg_m','laden_mean_c02_emit_transpo_pax_kg_m','laden_mean_c02_emit_freightwork_kg_m']
    vol_energyeff_nullable = [True for k in range(0,12)]
    vol_energyeff_dtype = [Float for l in range(0,12)]

    #vol_finalcomments_col = ['adtl_info_freetext','mean_density_cargo']
    #vol_finalcomments_nullable = [True,True]
    #vol_finalcomments_dtype = [String, String]

    list_of_colnames = [ship_col,verif_col,monitor_col,totals_col,averages_col,vol_distancetime_col,vol_energyeff_col]

    list_of_colnames_2 = [ship_nullable,verif_nullable,monitor_nullable,totals_nullable,averages_nullable,vol_distancetime_nullable,vol_energyeff_nullable]

    list_of_colnames_3 = [ship_dtype,verif_dtype,monitor_dtype,totals_dtype,averages_dtype,vol_distancetime_dtype,vol_energyeff_dtype]


    collist = []
    for t in list_of_colnames:
        collist.extend(t)

    nullable_list = []
    for t in list_of_colnames_2:
        nullable_list.extend(t)

    dtype_list = []
    for t in list_of_colnames_3:
        dtype_list.extend(t)    

        
    return collist,nullable_list,dtype_list,list_of_colnames
 