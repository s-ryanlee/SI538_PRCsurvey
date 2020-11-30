import pandas as pd
df = pd.read_csv('comprehensive_PRCsurvey_data.csv')

def extract_time(date_time):
    if len(date_time) == 19:
        dt_list = date_time.split(' ')
        time = dt_list.pop(-1)
    else:
        time = date_time
    return time
#print(f"test: extract_time \n {extract_time('2020-10-05 20:15:00')}")

def extract_date(date_time):
    if len(date_time) == 19:
        dt_list = date_time.split(' ')
        date = dt_list.pop(0)
    else:
        date = date_time
    return date
#print(f"test: extract_date \n {extract_date('2020-10-05 20:15:00')}")

def change_comma(response):
    if response != 'NA' and ', ' in response:
        resp_wout_comma = response.replace(', ', '/')
    else:
        resp_wout_comma = response
    return resp_wout_comma
#print(f"test: change_comma \n {change_comma('Mailed pamphlets, flyers, or newsletters,The Capital Area Recycling And Trash website,The City of Lansing social media pages,The Recycle Coach and/or Lansing Connect app')}")

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
#print(f"test: filter on release date \n {rec_resps.iloc[0:5]}")

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
#rec_resps = rec_resps.applymap(extract_multi_resp)
#print(f"test extract multi-response: {rec_resps.iloc[5]}")

#check type
#print(type(rec_resps.loc[5, 'current_info_receipt']))
#print(f"test: check type \n {rec_resps['current_info_receipt'].dtypes}")

#test .csv file write
rec_resps.to_csv('recorded_responses_wlists.csv',index=False, encoding="utf-8")

#create dummy dataframes
org = "A school/commercial business/and/or my place of work"
compan = "Friends/family/and/or neighbors"
paper = "Mailed pamphlets/flyers/or newsletters"
cart = "Information on my recycling cart"
website1 = "The Capital Area Recycling And Trash website"
website2 = "The Capital Area Recycling and Trash website"
social_med = "The City of Lansing social media pages"
apps = "The Recycle Coach and/or Lansing Connect app"
q1_resps = [org, compan, paper, cart, website1, social_med, apps]
q2_resps = [org, compan, paper, cart, website2, social_med, apps]
#q12_resps = []
#for response in q1n2_resps:
#    new_response = change_comma(response)
#    print(response)
#    q12_resps.append(response)
#print(q12_resps)

trash = "Trash Cart"
recycle = "Recycling Cart"
dropoff = "Take to Drop-off Recycling Center"
other = "Other (such as can and bottle return or compost)"
q3_resps = [trash, recycle, dropoff, other]

resp_cols = rec_resps.columns.tolist()
#print(resp_cols)
dummy_cols = resp_cols[12:27]
#print(dummy_cols)

info_cols = ['org', 'compan', 'paper', 'cart', 'website', 'social_med', 'apps']
dispose_cols = ['trash', 'recycle', 'dropoff', 'other']

#i = 0
#while i < 27:
#    dummy_dict = {'responseid': rec_resps['responseid'], 'dummy': rec_resps[dummy_cols[i]]}
#    if "info" in dummy_cols[i]:
#        a = 0
#        for col in info_cols:
#            print(type(dummy_dict))
#            dummy_dict[col]: rec_resps[f"{dummy_cols[i]}"].str.contains(q12_resps[a], regex=False)
#            a += 1
#            i = pd.DataFrame(dummy_dict)
#            i.to_csv(f'dummy_{col}.csv',index=False, encoding="utf-8")
#    elif "disposal" in dummy_cols[i]:
#        b = 0
#        for col in dispose_cols:
#            dummy_dict[col]: rec_resps[f"{dummy_cols[i]}"].str.contains(q3_resps[b], regex=False)
#            b += 1
#            i = pd.DataFrame(dummy_dict)
#            i.to_csv(f'dummy_{col}.csv',index=False, encoding="utf-8")
#    i += 1
#    print(i)

#current info dummy
current_info_dummy = rec_resps[['responseid', 'current_info_receipt']]
i = 0
for col in info_cols:
    current_info_dummy[col] = current_info_dummy['current_info_receipt'].str.contains(q1_resps[i], regex=False)
    i +=1
current_info_dummy.to_csv('current_info_dummy.csv',index=False, encoding="utf-8")

#want info dummy
want_info_dummy = rec_resps[['responseid', 'how_do_you_want_info']]
i = 0
for col in info_cols:
    want_info_dummy[col] = want_info_dummy['how_do_you_want_info'].str.contains(q2_resps[i], regex=False)
    i +=1
want_info_dummy.to_csv('want_info_dummy.csv',index=False, encoding="utf-8")

#disposal dummies
recyclable_paper_dummy = rec_resps[['responseid', "recyclable_paper_disposal"]]
i = 0
for col in dispose_cols:
    recyclable_paper_dummy[col] = recyclable_paper_dummy['recyclable_paper_disposal'].str.contains(q3_resps[i], regex=False)
    i +=1
recyclable_paper_dummy.to_csv('recyclable_paper_dummy.csv',index=False, encoding="utf-8")

nonrecyclable_paper_dummy = rec_resps[['responseid', "nonrecyclable_paper_disposal"]]
i = 0
for col in dispose_cols:
    nonrecyclable_paper_dummy[col] = nonrecyclable_paper_dummy['nonrecyclable_paper_disposal'].str.contains(q3_resps[i], regex=False)
    i +=1
nonrecyclable_paper_dummy.to_csv('nonrecyclable_paper_dummy.csv',index=False, encoding="utf-8")

cardboard_boxboard_dummy = rec_resps[['responseid', "cardboard_boxboard_disposal" ]]
i = 0
for col in dispose_cols:
    cardboard_boxboard_dummy[col] = cardboard_boxboard_dummy["cardboard_boxboard_disposal" ].str.contains(q3_resps[i], regex=False)
    i +=1
cardboard_boxboard_dummy.to_csv('cardboard_boxboard_dummy.csv',index=False, encoding="utf-8")

recyclable_glass_dummy = rec_resps[['responseid',"recyclable_glass_disposal"]]
i = 0
for col in dispose_cols:
    recyclable_glass_dummy[col] = recyclable_glass_dummy["recyclable_glass_disposal"].str.contains(q3_resps[i], regex=False)
    i +=1
recyclable_glass_dummy.to_csv('recyclable_glass_dummy.csv',index=False, encoding="utf-8")

specialty_glass_dummy = rec_resps[['responseid',"specialty_glass_disposal"]]
i = 0
for col in dispose_cols:
    specialty_glass_dummy[col] = specialty_glass_dummy["specialty_glass_disposal"].str.contains(q3_resps[i], regex=False)
    i +=1
specialty_glass_dummy.to_csv('specialty_glass_dummy.csv',index=False, encoding="utf-8")

recyclable_plastics_dummy = rec_resps[['responseid',"recyclable_plastics_disposal"]]
i = 0
for col in dispose_cols:
    recyclable_plastics_dummy[col] = recyclable_plastics_dummy["recyclable_plastics_disposal"].str.contains(q3_resps[i], regex=False)
    i +=1
recyclable_plastics_dummy.to_csv('recyclable_plastics_dummy.csv',index=False, encoding="utf-8")

plastic_bag_dummy = rec_resps[['responseid',"plastic_bag_disposal"]]
i = 0
for col in dispose_cols:
    plastic_bag_dummy[col] = plastic_bag_dummy["plastic_bag_disposal"].str.contains(q3_resps[i], regex=False)
    i +=1
plastic_bag_dummy.to_csv('plastic_bag_dummy.csv',index=False, encoding="utf-8")

bulky_plastic_dummy = rec_resps[['responseid',"bulky_plastic_disposal"]]
i = 0
for col in dispose_cols:
    bulky_plastic_dummy[col] = bulky_plastic_dummy["bulky_plastic_disposal"].str.contains(q3_resps[i], regex=False)
    i +=1
bulky_plastic_dummy.to_csv('bulky_plastic_dummy.csv',index=False, encoding="utf-8")

polystyrene_dummy = rec_resps[['responseid',"polystyrene_foam_disposal"]]
i = 0
for col in dispose_cols:
    polystyrene_dummy[col] = polystyrene_dummy["polystyrene_foam_disposal"].str.contains(q3_resps[i], regex=False)
    i +=1
polystyrene_dummy.to_csv('polystyrene_dummy.csv',index=False, encoding="utf-8")

recyclable_metals_disposal_dummy = rec_resps[['responseid',"recyclable_metals_disposal"]]
i = 0
for col in dispose_cols:
    recyclable_metals_disposal_dummy[col] = recyclable_metals_disposal_dummy["recyclable_metals_disposal"].str.contains(q3_resps[i], regex=False)
    i +=1
recyclable_metals_disposal_dummy.to_csv('recyclable_metals_disposal_dummy.csv',index=False, encoding="utf-8")

specialty_metals_disposal_dummy = rec_resps[['responseid',"specialty_metals_disposal"]]
i = 0
for col in dispose_cols:
    specialty_metals_disposal_dummy[col] = specialty_metals_disposal_dummy["specialty_metals_disposal"].str.contains(q3_resps[i], regex=False)
    i +=1
specialty_metals_disposal_dummy.to_csv('specialty_metals_disposal_dummy.csv',index=False, encoding="utf-8")

e_waste_dummy = rec_resps[['responseid',"e_waste_disposal"]]
i = 0
for col in dispose_cols:
    e_waste_dummy[col] = e_waste_dummy["e_waste_disposal"].str.contains(q3_resps[i], regex=False)
    i +=1
e_waste_dummy.to_csv('e_waste_dummy.csv',index=False, encoding="utf-8")

misc_items_dummy = rec_resps[['responseid',"misc_items_disposal"]]
i = 0
for col in dispose_cols:
    misc_items_dummy[col] = misc_items_dummy["misc_items_disposal"].str.contains(q3_resps[i], regex=False)
    i +=1
misc_items_dummy.to_csv('misc_items_dummy.csv',index=False, encoding="utf-8")
