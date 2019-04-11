from datetime import datetime
import pandas as pd
import json
import os

dir_name = 'Kickstarter_data'
files = os.listdir(dir_name)
header = True

for counter,csv in enumerate(files):

    df = pd.read_csv(os.path.join(dir_name, csv))
    
    category = []
    subcategory = []
    inte = []
    days_open = []
    title_len = []
    blurb_len = []

    rem = []
    
    for i,r in df.iterrows():
        days_open.append( int(round( ((r['deadline'] - r['launched_at']) / (60*60*24)) )) )
        title_len.append( len(str(r['name'])) )
        blurb_len.append( len(str(r['blurb'])) )
    
        if r['state'] not in ['successful', 'failed']:
            rem.append(i)
          
        if r['country'] == 'US':
            inte.append(0)
        else:
            inte.append(1)
          
        cat = json.loads(r['category'])['slug'].split('/')
        category.append(cat[0])
        try:
            subcategory.append(cat[1])
        except:
              subcategory.append(' ')
              rem.append(i)
      
    df = df[['pledged', 'backers_count', 'deadline', 'goal', 'launched_at', 'state']]
      
    df['international'] = inte
    df['category'] = category
    df['subcategory'] = subcategory
    df['days_open'] = days_open
    df['title_len'] = title_len
    df['blurb_len'] = blurb_len
    df['month'] = [datetime.fromtimestamp(ts).strftime('%b') for ts in df['launched_at']]
    
    df = pd.get_dummies(df, prefix=['cat'], columns=['category'], drop_first=True)
    df = pd.get_dummies(df, prefix=['mo'], columns=['month'], drop_first=True)
    
    df['cat_design_crafts'] = df['cat_design'] + df['cat_crafts']
    df['cat_film_vid_photo'] = df['cat_film & video'] = df['cat_photography']
    df['cat_publishing_journal_comics'] = df['cat_publishing'] + df['cat_journalism'] + df['cat_comics']
    df['cat_theater_dance'] = df['cat_theater'] + df['cat_dance']
    
    # array(['film & video', 'music', 'games', 'crafts', 'art', 'publishing',
       # 'food', 'technology', 'fashion', 'comics', 'design', 'theater',
       # 'photography', 'journalism', 'dance'], dtype=object)  15
       
    df = df.drop(list(set(rem)))

    with open('kick.csv', 'a') as f:
        df.to_csv(f, header=header, index=False)
    
    if header:
        header = False
        
    print(f'processed {counter+1}/{len(files)}')

    # array(['film & video', 'music', 'games', 'crafts', 'art', 'publishing',
       # 'food', 'technology', 'fashion', 'comics', 'design', 'theater',
       # 'photography', 'journalism', 'dance'], dtype=object)  15
    

    
# cat_comics .0423998 ###
# cat_crafts .0287635 ###
# cat_dance .0132242 ###
# cat_design  .040822  # + crafts
# cat_fashion .0576517 
# cat_film__~o .1378101 + photography
# cat_food .0782552 
# cat_games  .0678505  
# cat_journa~m  .0249356 ###
# cat_music  .1366281 
# cat_photog~y  .0363814  ###
# cat_publis~g   .0997262  + journalism + comics
# cat_techno~y   .104427 
# cat_theater .0319571 # + dance

# cat_art 0.0991676


# cat_fashion .0576517 
# cat_food .0782552 
# cat_games  .0678505  
# cat_music 
# cat_techno~y   
# cat_design_crafts
# cat_publis~g_journal_comics
# cat_film__photography
# cat_theater_dance
# cat_art 0.0991676 (EXCLUDED)