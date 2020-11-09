import pandas as pd
df = pd.read_csv('comprehensive_PRCsurvey_data.csv')

def extract_time(date_time):
    if len(date_time) == 19:
        dt_list = date_time.split(' ')
        time = dt_list.pop(-1)
    else:
        time = date_time
    return time
print(f"test: extract_time \n {extract_time('2020-10-05 20:15:00')}")

def extract_date(date_time):
    if len(date_time) == 19:
        dt_list = date_time.split(' ')
        date = dt_list.pop(0)
    else:
        date = date_time
    return date
print(f"test: extract_date \n {extract_date('2020-10-05 20:15:00')}")

def change_comma(response):
    if response != 'NA' and ', ' in response:
        resp_wout_comma = response.replace(', ', '/')
    else:
        resp_wout_comma = response
    return resp_wout_comma
print(f"test: change_comma \n {change_comma('Mailed pamphlets, flyers, or newsletters,The Capital Area Recycling And Trash website,The City of Lansing social media pages,The Recycle Coach and/or Lansing Connect app')}")

def extract_multi_resp(response):
    if ',' in response:
        new_resp = response.split(',')
    else:
        new_resp = response
    return new_resp

#rename columns
df.rename(columns={'Duration (in seconds)': 'duration_in_secs',
       'Q1': 'current_info_receipt', 'Q2': 'how_do_you_want_info',
       'Q3#1_1': 'recyclable_paper_disposal', 'Q3#1_2': 'nonrecyclable_paper_disposal',
       'Q3#1_3':  'cardboard_boxboard_disposal', 'Q3#1_4':  'recyclable_glass_disposal',
       'Q3#1_5':  'specialty_glass_disposal', 'Q3#1_6':  'recyclable_plastics_disposal',
       'Q3#1_7': 'plastic_bag_disposal', 'Q3#1_8': 'bulky_plastic_disposal',
       'Q3#1_9': 'polystyrene_foam_disposal', 'Q3#1_10': 'recyclable_metals_disposal',
       'Q3#1_11':  'specialty_metals_disposal', 'Q3#1_12':  'e_waste_disposal', 
       'Q3#1_13':  'misc_items_disposal', 'Q4_1':  'accepted_item_in_trash', 
       'Q4_2': 'accepted_item_in_recycling', 'Q4_3': 'not_accepted_item_in_trash', 
       'Q4_4': 'not_accepted_item_in_recycling', 'Q4_5': 'unsure_item_in_trash', 
       'Q4_6': 'unsure_item_in_recycling', 'Q4_7':  'specialty_recycle_dropoff',
       'Q5':  'what_happens_unwashed', 'Q9': 'what_happens_bagged',
       'Q6':  'what_happens_unsure'}, inplace=True)

#convert all columns to lowercase
df.columns = [x.lower() for x in df.columns]

#extract date/time and create new column
df['starttime'] = df['startdate'].apply(extract_time)
df['startdate'] = df['startdate'].apply(extract_date)
df['endtime'] = df['enddate'].apply(extract_time)
df['enddate'] = df['enddate'].apply(extract_date)

#rearrange columns
cols = df.columns.tolist()
cols.insert(1, cols[-2])
cols.insert(3, cols[-1])
del cols[-2:]
#print(f"test: rearrange columns \n {cols}")
df = df[cols]


#filter responses on survey circulation dates
circulation_dates = ['2020-10-19', '2020-10-20', '2020-10-21', '2020-10-22', '2020-10-23', '2020-10-24', '2020-10-25',
'2020-10-26', '2020-10-27', '2020-10-28', '2020-10-29']
circ_filt = (df['startdate'].isin(circulation_dates))
rec_resps = df.loc[circ_filt]
print(f"test: filter on release date \n {rec_resps.iloc[0:5]}")

#test .csv file write
#rec_resps.to_csv('recorded_responses.csv',index=False, encoding="utf-8")

#Fill NaN
rec_resps.fillna('NA', inplace=True)
#print(f"test nan: {rec_resps}")

#test check columns
#print(rec_resps.columns)

#replace commas in multi-response questions
rec_resps['current_info_receipt'] = rec_resps['current_info_receipt'].apply(change_comma)
rec_resps['how_do_you_want_info'] = rec_resps['how_do_you_want_info'].apply(change_comma)
rec_resps['what_happens_unsure'] = rec_resps['what_happens_unsure'].apply(change_comma)
#print(f"test: change commas \n {rec_resps['what_happens_unsure']}")

#extract multiple responses
rec_resps = rec_resps.applymap(extract_multi_resp)
#print(f"test extract multi-response: {rec_resps.iloc[5]}")

#check type
#print(type(rec_resps.loc[5, 'current_info_receipt']))
#print(f"test: check type \n {rec_resps['current_info_receipt'].dtypes}")

#test .csv file write
rec_resps.to_csv('recorded_responses_wlists.csv',index=False, encoding="utf-8")