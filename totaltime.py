import pandas as pd

def last_watched(d):
    lw=d['Title'].head(1).values[0]
    return lw
def most_watched(d):
    tvseries=d.loc[d['Title'].str.contains('Episode')]
    movie=d.loc[d['Title'].str.contains('Episode')==False]
    movie_most_watched=movie['Title'].value_counts().head(1)
    tvseries['Title']=tvseries['Title'].str.split(':').str[0]
    tvseries_most_watched=tvseries.groupby('Title')['Duration'].sum().sort_values(ascending=False).head(1)
    return movie_most_watched,tvseries_most_watched


def dgraphs(d):
    days={0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}
    d['day']=d['day'].map(days)
    d['day']=pd.Categorical(d['day'],categories=['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],ordered=True)
    f=d['day'].value_counts().sort_index()
    time={0:'12 am'}
    for i in range(1,24):
        if i < 13:
            time[i]=f'{i} am'
        else:
            time[i]=f'{i-12} pm'
    d['hour']=d['hour'].map(time)
    d['hour']=pd.Categorical(d['hour'],categories=[time.values()],ordered=True)
    h=d['hour'].value_counts().sort_index()
    dayf=pd.pivot_table(data=d,index='day',columns='hour',values='Title',aggfunc='count')
    return dayf

def search(w,d):
    word=d.loc[d['Title'].str.lower().str.contains(w.lower()),['Duration','Start Time','Title']].head(1)
    return word