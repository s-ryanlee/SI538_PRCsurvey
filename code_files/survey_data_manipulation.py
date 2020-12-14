import pandas as pd
import seaborn as sns
import numpy as np

## FIRST SET OF MANIPULATION FUNCTIONS
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

## SECOND SET OF MANIPULATIONS FUNCTIONS
def check_relationship(data_frame, new_col, col1, col2):
    #uses logic fields to determine relationships between two columns and creates a column
    data_frame[new_col] = (data_frame[col1] == True) & (data_frame[col2] == True)
    return data_frame[new_col]
#test_df = check_relationship(joined_info, 'paper_paper', 'current_paper', 'want_paper')
#print(f"TEST: check_relationship() \n {test_df}")

def calculate_proportions_info(data_frame, col, total_n):
    #calculates proportions of filtered values and total values in a data frame
    new_data_frame = data_frame[data_frame[col] == True]
    col_n = len(new_data_frame.index)
    col_p = (col_n / total_n)
    return col_p
#test_prop = calculate_proportions_info(joined_info, 'paper_paper', total_resps)
#print(f"TEST: calculate_proportions() \n {test_prop}")

def create_proportion_dict(relationship_dict, data_frame, relationship_cols1, relationship_cols2):
    #creates dictionary of proprotions of all relationships
    relationship_proportions_dict = {}
    for value in relationship_dict.values():
        i = 0
        while i < 7:
            data_frame[value[i]] = check_relationship(data_frame, value[i], relationship_cols1[i], relationship_cols2[i])
            relationship_prop = calculate_proportions_info(data_frame, value[i], total_resps)
            relationship_proportions_dict[value[i]] = [round(relationship_prop, 3)]
            i += 1
    return relationship_proportions_dict

##FIRST SET OF MANIPULATIONS
df = pd.read_csv('comprehensive_PRCsurvey_data.csv')
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

## SECOND SET OF MANIPULATIONS

#read in all survey data
survey_resps = pd.read_csv('https://raw.githubusercontent.com/s-ryanlee/SI538_PRCsurvey/main/recorded_responses_wlists.csv')
total_resps = len(survey_resps.index)
#print(f"TEST: Total Responses = {total_resps}")

# INFORMATION RELATIONSHIPS

#read in info truth tables
current_info = pd.read_csv('https://raw.githubusercontent.com/s-ryanlee/SI538_PRCsurvey/main/current_info_dummy.csv')
current_info.rename(columns={'org': 'current_org', 'compan': 'current_compan', 'paper': 'current_paper', 'cart': 'current_cart', 'website': 'current_website', 'social_med': 'current_social_med', 'apps': 'current_apps'}, inplace=True)
want_info = pd.read_csv('https://raw.githubusercontent.com/s-ryanlee/SI538_PRCsurvey/main/want_info_dummy.csv')
want_info.rename(columns={'org': 'want_org', 'compan': 'want_compan', 'paper': 'want_paper', 'cart': 'want_cart', 'website': 'want_website', 'social_med': 'want_social_med', 'apps': 'want_apps'}, inplace=True)
#print(current_info.head())
#print(want_info.head(20))

#read in info proprtions
info_proportions = pd.read_csv('https://raw.githubusercontent.com/s-ryanlee/SI538_PRCsurvey/main/info_receipt_proportions.csv')
#print(info_proportions.head())

#join info truth tables
frames = [current_info, want_info]
joined_info = pd.concat(frames, axis=1)
#print(joined_info.head())

#check joined data
#for col in joined_info.columns:
#    print(col)

#test relationships
#how many who currently get paper also want paper
#joined_info['paper_paper'] = (joined_info['want_paper'] == True) & (joined_info['current_paper'] == True)
#print(f"TEST: current paper/want paper \n{joined_info[joined_info['paper_paper'] == True]}")
#306/540

#how many who currently get paper want website
#joined_info['paper_website'] = (joined_info['current_paper'] == True) & (joined_info['want_website'] == True)
#print(f"TEST: current paper/want website \n{joined_info[joined_info['paper_website'] == True]}")
#188/540

current_info_relationships = {
    'current_org': ['org_org', 'org_compan', 'org_paper', 'org_cart', 'org_website', 'org_social_med', 'org_apps'],
    'current_compan': ['compan_org', 'compan_compan', 'compan_paper', 'compan_cart', 'compan_website', 'compan_social_med', 'compan_apps'],
    'current_paper': ['paper_org', 'paper_compan', 'paper_paper', 'paper_cart', 'paper_website', 'paper_social_med', 'paper_apps'],
    'current_cart': ['cart_org', 'cart_compan', 'cart_paper', 'cart_cart', 'cart_website', 'cart_social_med', 'cart_apps'],
    'current_website': ['website_org', 'website_compan', 'website_paper', 'website_cart', 'website_website', 'website_social_med', 'website_apps'],
    'current_social_med': ['social_med_org', 'social_med_compan', 'social_med_paper', 'social_med_cart', 'social_med_website', 'social_med_social_med', 'social_med_apps'],
    'current_apps': ['apps_org', 'apps_compan', 'apps_paper', 'apps_cart', 'apps_website', 'apps_social_med', 'apps_apps'],
    }
want_info_relationships = {
    'want_org': ['org_org', 'compan_org', 'paper_org', 'cart_org', 'website_org', 'social_med_org', 'apps_org'],
    'want_compan': ['org_compan', 'compan_compan', 'paper_compan', 'cart_compan', 'website_compan', 'social_med_compan', 'apps_compan'],
    'want_paper': ['org_paper', 'compan_paper', 'paper_paper', 'cart_paper', 'website_paper', 'social_med_paper', 'apps_paper'],
    'want_cart': ['org_cart', 'compan_cart', 'paper_cart', 'cart_cart', 'website_cart', 'social_med_cart', 'apps_cart'],
    'want_website': ['org_website', 'compan_website', 'paper_website', 'cart_website', 'website_website', 'social_med_website', 'apps_website'],
    'want_social_med': ['org_social_med', 'compan_social_med', 'paper_social_med', 'cart_social_med', 'website_social_med', 'social_med_social_med', 'apps_social_med'],
    'want_apps': ['org_apps', 'compan_apps', 'paper_apps', 'cart_apps', 'website_apps', 'social_med_apps', 'apps_apps']
    }

current_info_cols = current_info.columns.tolist()
del current_info_cols[:2]
print(f"TEST: current_info cols to list: {current_info_cols}")
want_info_cols = want_info.columns.tolist()
del want_info_cols[:2]
print(f"TEST: want_info cols to list: {want_info_cols}")

info_relationships_df = joined_info.copy()

current_info_proportions = create_proportion_dict(current_info_relationships, info_relationships_df, current_info_cols, want_info_cols)
want_info_proportions = create_proportion_dict(want_info_relationships, info_relationships_df, current_info_cols, want_info_cols)
#print(f"TEST: Current Info Relationship Proportions: \n{current_info_proportions} \nTEST: Want Info Relationship Proportions: \n{want_info_proportions}")

info_relationships_df.to_csv('info_relationships_df.csv', index=False, encoding="utf-8")

current_info_props_df = pd.DataFrame.from_dict(current_info_proportions, orient="index")
#print(f"TEST: current info proportions dataframe: \n{current_info_props_df}")
current_info_props_df.to_csv('info_proportions_df.csv', index=False, encoding="utf-8")

want_info_props_df = pd.DataFrame.from_dict(want_info_proportions)
print(f"TEST: want info proportions dataframe: \n{want_info_props_df.head()}")

#TOP CONTAMINATIONS

#check common contaminants
#read in disposal proportions
disposal_proportions = pd.read_csv('https://raw.githubusercontent.com/s-ryanlee/SI538_PRCsurvey/main/all_disposal_proportions.csv')

#check items in recycling proprotions
#print(disposal_proportions.iloc[1])

#check contaminants in recycling proportions
contaminants = ['nonrecyclable_paper', 'specialty_glass', 'plastic_bag', 'polystyrene', 'specialty_metals', 'e_waste', 'misc']
contaminants_dict = disposal_proportions.loc[1, contaminants].to_dict()
#print(contaminants_dict)

first_contaminant = contaminants_dict.pop(max(contaminants_dict))
second_contaminant = contaminants_dict.pop(max(contaminants_dict))
third_contaminant = contaminants_dict.pop(max(contaminants_dict))
top_contaminants = {'top': first_contaminant, 'middle': second_contaminant, 'lowest': third_contaminant}

print(f'''Top 3 Contaminants are:
1. specialty metals ({round(top_contaminants['top'] * 100)}% of residents disposing in recycling)
2. specialty_glass ({round(top_contaminants['middle'] * 100)}% of residents disposing in recycling)
3. plastic bags ({round(top_contaminants['lowest'] * 100)}% of residents disposing in recycling)''')

# WISHFUL RECYCLING

#situational recycling columns: accepted_item_in_trash, accepted_item_in_recycling, not_accepted_item_in_trash, not accepted_item_in_recycling, unsure_item_in_trash, unsure_item_in_recycling, specialty_recycle_dropoff
#wishful recycling columns: not_accepted_item_in_recycling, unsure_item_in_recycling

recycling_situations = survey_resps[['responseid', 'accepted_item_in_recycling', 'not_accepted_item_in_trash', 'unsure_item_in_trash', 'not_accepted_item_in_recycling', 'unsure_item_in_recycling']]
#print(wishful_recycling)
#add ordinal scale: Extremely unlikely = 1 and Extremely likely = 5
def add_num_scale(response):
    if response == "Extremely likely":
        new_resp = 5
    elif response == "Somewhat likely":
        new_resp = 4
    elif response == "Neither likely nor unlikely":
        new_resp = 3
    elif response == "Somewhat unlikely":
        new_resp = 2
    elif response == "Extremely unlikely":
        new_resp = 1
    else:
        new_resp = 0
    return new_resp

recycling_situations['not_accepted_rc_num_scale'] = recycling_situations['not_accepted_item_in_recycling'].apply(add_num_scale)
recycling_situations['unsure_rc_num_scale'] = recycling_situations['unsure_item_in_recycling'].apply(add_num_scale)
#print(recycling_situations.head())

recycling_situations['not_accepted_trash_num_scale'] = recycling_situations['not_accepted_item_in_trash'].apply(add_num_scale)
recycling_situations['unsure_trash_num_scale'] = recycling_situations['unsure_item_in_trash'].apply(add_num_scale)

recycling_situations.to_csv('recycling_situations.csv', index=False, encoding="utf-8")

#descriptive stats
not_accepted_series = recycling_situations.loc[:, 'not_accepted_rc_num_scale']
not_accepted_mode = not_accepted_series.mode()
not_accepted_med = not_accepted_series.median()
print(f'Unaccepted Item Recycle Mode: {not_accepted_mode} \nUnaccepted Item Recycle Median: {not_accepted_med}')

unsure_series = recycling_situations.loc[:, 'unsure_rc_num_scale']
unsure_mode = unsure_series.mode()
unsure_med = unsure_series.median()
print(f'Unsure Item Recycle Mode: {unsure_mode} \nUnsure Item Recycle Median: {unsure_med}')

#plots
sns.set_theme(style="ticks", color_codes=True)
unsure_plot = sns.catplot(x='unsure_item_in_recycling', kind="count", palette="ch:.25", data=recycling_situations)

#1a. Calculate proportions of wishful recyclers
unsure_rc_counts = recycling_situations['unsure_item_in_recycling'].value_counts(dropna=False)
print(unsure_rc_counts)
unsure_rc_props = recycling_situations['unsure_item_in_recycling'].value_counts(normalize=True, dropna=False)
print(unsure_rc_props)
wishful_recycling_prop = sum(unsure_rc_props[['Extremely likely', 'Somewhat likely']])
print(f"Percentage of Wishful Recyclers: {round(wishful_recycling_prop*100, 2)}%")
unsure_rc_props.to_csv('unsure_recycling_props.csv', index=False, encoding="utf-8")


#1b. Calculate proportions of proper disposers
unsure_trash_props = recycling_situations['unsure_item_in_trash'].value_counts(normalize=True, dropna=False)
print(unsure_trash_props)
unsure_trash_prop = sum(unsure_trash_props[['Extremely likely', 'Somewhat likely']])
print(f"Percentage of Proper Disposers: {round(unsure_trash_prop*100, 2)}%")
unsure_trash_props.to_csv('unsure_trash_props.csv', index=False, encoding="utf-8")


#1c. Calculate proportion of general recyclers
general_rc_props = recycling_situations['accepted_item_in_recycling'].value_counts(normalize=True, dropna=False)
print(general_rc_props)
general_rc_prop = sum(general_rc_props[['Extremely likely', 'Somewhat likely']])
print(f"Percentage of General Recyclers: {round(general_rc_prop*100, 2)}%")
general_rc_props.to_csv('general_recycling_props.csv', index=False, encoding="utf-8")

# Data was transferred to RStudio for analysis in R