from datetime import datetime
from textblob import TextBlob
import pandas as pd
import json
import os

OUT_FILE = 'kick_dev.csv'
DIR_NAME = 'Kickstarter_data'

files = os.listdir(DIR_NAME)
header = True

for counter,csv in enumerate(files):

    df = pd.read_csv(os.path.join(DIR_NAME, csv))
    
    category = []
    subcategory = []
    inte = []
    days_open = []
    title_len = []
    blurb_len = []
    title_sent = []
    blurb_sent = []

    rem = []
    
    for i,r in df.iterrows():
        days_open.append( int(round( ((r['deadline'] - r['launched_at']) / (60*60*24)) )) )
        title_len.append( len(str(r['name'])) )
        blurb_len.append( len(str(r['blurb'])) )
        title_sent.append( TextBlob(str(r['name'])).polarity )
        blurb_sent.append( TextBlob(str(r['blurb'])).polarity )
    
        if r['state'] not in ['successful', 'failed']:
            rem.append(i)
          
        if r['country'] == 'US':
            inte.append(0)
        else:
            inte.append(1)
          
        cat = json.loads(r['category'])['slug'].split('/')
        category.append(cat[0])
      
    df['month'] = [datetime.fromtimestamp(ts).strftime('%b') for ts in df['launched_at']]
    df = df[['pledged', 'backers_count', 'goal', 'month']]
      
    df['international'] = inte
    df['category'] = category
    df['days_open'] = days_open
    df['title_len'] = title_len
    df['blurb_len'] = blurb_len
    df['title_sent'] = title_sent
    df['blurb_sent'] = blurb_sent
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

    with open(OUT_FILE, 'a') as f:
        df.to_csv(f, header=header, index=False)
    
    if header:
        header = False
        
    print(f'processed {counter+1}/{len(files)}')