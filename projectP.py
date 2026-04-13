import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import totaltime
import streamlit as st
from PIL import Image
st.title('Netflix Activity Analysis',text_alignment='center')
img=Image.open(r'C:\Users\there\OneDrive\Documents\VSCODEDS\netflixpy\netflix.jpg')
st.image(img)
df=pd.read_csv(r"C:\Users\there\OneDrive\Documents\ViewingActivity.csv")
df=df.loc[df['Supplemental Video Type'].isna()==True]
df['Duration']=pd.to_timedelta(df['Duration'])
df['Start Time']=pd.to_datetime(df['Start Time'])
df.drop(['Supplemental Video Type', 'Attributes','Device Type','Country','Bookmark','Latest Bookmark'],axis=1,inplace=True)
names=df['Profile Name'].unique().tolist()
df1=df.copy()
df1['day']=df1['Start Time'].dt.weekday
df1['hour']=df1['Start Time'].dt.hour
d={}
dur={}
if 'name' not in st.session_state:
    st.session_state.name=''
if 'option' not in st.session_state:
    st.session_state.option=''
for i in names:
    d[i]=df1.loc[df1['Profile Name']==i]
    dur[i]=int(d[i]['Duration'].sum().total_seconds()/3600)
col1,col2=st.columns(2)
with col1:
    name=st.selectbox('enter user name: ',options=names,placeholder='user..',index=None,key='name')
with col2:
    option=st.selectbox('enter options: ',['Time Spent','Last Watched','Most Watched','Watch Graph','Title Search'],index=None,key='option')
if option:
    
    if option=='Time Spent':
        fig,ax=plt.subplots(figsize=(10,10))
        s=ax.bar(names,dur.values())
        name_ind=names.index(name)
        s[name_ind].set_color('red')
        plt.title('Hours Spent on Netflix')
        st.pyplot(fig)
        st.write('Total Watchtime is ',d[name]['Duration'].sum().days,'days', int(d[name]['Duration'].sum().seconds/3600),'hours and',int(d[name]['Duration'].sum().seconds%3600/60),'minutes')
    elif option=='Last Watched':
        st.write('You had previously watched:',totaltime.last_watched(d[name]))
    elif option=='Most Watched':
        m,s=totaltime.most_watched(d[name])
        st.markdown(f"Most Watched Movie: <span style='color:red'>{m.index[0]}</span> was watched {m.values[0]} times",unsafe_allow_html=True)
        st.markdown(f"Most Watched Series: <span style='color:red'>{s.index[0]}</span> was watched for {s.values[0].astype('timedelta64[m]')}",unsafe_allow_html=True)
    elif option=='Watch Graph':
        dayf=totaltime.dgraphs(d[name])
        fig,ax=plt.subplots(figsize=(10,6))
        sns.heatmap(dayf,cmap='YlGnBu',ax=ax)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
        ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
        ax.set_title("Viewing Activity (Hours vs Weekdays)")
        st.pyplot(fig)
   
    elif option == 'Title Search':
        sugg = ["Select a title..."] + d[name]['Title'].unique().tolist()
        w = st.selectbox("your title", options=sugg)

        if w != "Select a title...":
            k = d[name].loc[d[name]['Title'] == w]
            if not k.empty:
                st.write(k['Title'].iloc[0])
                st.write("Last Watched at", k['Start Time'].dt.date.iloc[0], k['Start Time'].dt.time.iloc[0])
            else:
                st.write("No match found for", w)
    clear=st.button('clear X')
    if clear:
        del st.session_state.name
        del st.session_state.option
        st.rerun()