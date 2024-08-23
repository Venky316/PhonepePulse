import streamlit as st
import psycopg2
import urllib.request
from PIL import Image
import pandas as pd
import numpy as np
import plotly.express as px


urllib.request.urlretrieve('https://play-lh.googleusercontent.com/6iyA2zVz5PyyMjK5SIxdUhrb7oh9cYVXJ93q6DZkmx07Er1o90PXYeo6mzL4VC2Gj9s','getimage.png')
img = Image.open('getimage.png')
st.set_page_config(page_title='An Analysis of Phonepe Pulse Data',layout='wide',initial_sidebar_state='auto')
st.image(image=img,width=100)
st.title(':red[Phonepe Pulse Data Visualization]')
st.caption(body='This app intends to extract the data about the transactions & users of Phonepe app and create an analysis of how digital payments has evolved since years.:thumbsup:')

client = psycopg2.connect(host='localhost',database='postgres',user='postgres',password='Venky@24121993')
cur = client.cursor()
cur.execute('select * from aggdata')
row = cur.fetchall()
getpd = pd.DataFrame(row,columns=['Stat_Type','Year','Category','State_FileRef','Transaction_Type','Transaction_Count','Transaction_Amount','Registered_Users','Brand','Brand_Count','Brand_Percentage'])
gettranspd = getpd[getpd['Stat_Type'].str.contains('Transactions')]
getaggtransquartpd = gettranspd[gettranspd['State_FileRef'].str.contains('Nil')]
getaggtransstatpd = gettranspd[gettranspd['State_FileRef'].str.contains('Nil')==False]
getuserspd = getpd[getpd['Stat_Type'].str.contains('Users')]
getaggusersquartpd = getuserspd[getuserspd['State_FileRef'].str.contains('Nil')]
getaggusersstattpd = getuserspd[getuserspd['State_FileRef'].str.contains('Nil')==False]

cur.execute('select * from topdata')
row = cur.fetchall()
getpd = pd.DataFrame(row,columns=['Stat_Type','Year','Category','State_FileRef','State_Name','State_Users','District_Name','District_Users','Pincode','Pincode_Users','State_Count','State_Amount','District_Count','District_Amount','Pincode_Count','Pincode_Amount'])
gettoptranspd = getpd[getpd['Stat_Type'].str.contains('Transactions')]
gettoptransquartpd = gettoptranspd[gettoptranspd['State_FileRef'].str.contains('Nil')]
gettoptransstatpd = gettoptranspd[gettoptranspd['State_FileRef'].str.contains('Nil')==False]
gettopuserspd = getpd[getpd['Stat_Type'].str.contains('Users')]
gettopusersquartpd = gettopuserspd[gettopuserspd['State_FileRef'].str.contains('Nil')]
gettopusersstatpd = gettopuserspd[gettopuserspd['State_FileRef'].str.contains('Nil')==False]
getyearlist = ['2018','2019','2020','2021','2022','2023']
getquarterlist = ['Q1','Q2','Q3','Q4']
getstatelist = getaggtransstatpd['State_FileRef'].unique().tolist()
getcumsum = int(getaggtransquartpd['Transaction_Amount'].sum())
getcumcount = int(getaggtransquartpd['Transaction_Count'].sum())
getcumusers = int(getaggusersquartpd['Brand_Count'].sum())

cur.execute('select * from statlatlon')
row = cur.fetchall()
statelatlongdf = pd.DataFrame(row,columns=['State_Name','lon','lat'])

cur.execute('select * from distlatlon')
row = cur.fetchall()
districtlatlongdf = pd.DataFrame(row,columns=['District_Name','State_Name','lon','lat'])

cur.execute('select * from pincodelatlon')
row = cur.fetchall()
pincodelatlongdf = pd.DataFrame(row,columns=['Pincode','State_Name','District_Name','City','lon','lat'])

def crorefunc(getval):
    getcroreval = (getval // 10000000)
    return(getcroreval)

#Overall Aggregate Stats
st.header(':blue[Digital Transactions Stats]')
st.write('Transaction Value (since 2018) : ',crorefunc(getcumsum),' Crs')
st.write('No. of Transactions (since 2018) : ',crorefunc(getcumcount),' Crs')
st.write('No. of Users Registered (since 2018) : ',crorefunc(getcumusers),' Crs')

getlist = list()
for i in getyearlist:
    getdf = getaggtransquartpd[getaggtransquartpd['Year'].str.contains(i)]
    getsum = crorefunc(int(getdf['Transaction_Amount'].sum()))
    getlist.append([i,getsum])
getover1df = pd.DataFrame(getlist,columns=['Year','Amount (In Crores)'])
st.write('')

getlist = list()
for i in getyearlist:
    getdf = getaggtransquartpd[getaggtransquartpd['Year'].str.contains(i)]
    getsum = crorefunc(int(getdf['Transaction_Count'].sum()))
    getlist.append([i,getsum])
getover2df = pd.DataFrame(getlist,columns=['Year','Transactions (In Crores)'])

getlist = list()
for i in getyearlist:
    getdf = getaggusersquartpd[getaggusersquartpd['Year'].str.contains(i)]
    getsum = crorefunc(int(getdf['Registered_Users'].unique().sum()))
    getlist.append([i,getsum])
getover3df = pd.DataFrame(getlist,columns=['Year','Registered Users (In Crores)'])
st.write('')
getdf = pd.concat([getover1df,getover2df['Transactions (In Crores)'],getover3df['Registered Users (In Crores)']],axis=1)
st.line_chart(getdf,x='Year',y='Amount (In Crores)',color='#FF0000')
st.line_chart(getdf,x='Year',y='Transactions (In Crores)',color='#00FF00')
st.line_chart(getdf,x='Year',y='Registered Users (In Crores)',color='#0000FF')

#Transaction status by various sub-category
st.header(':blue[Transaction Category Stats]')
col1,col2,col3 = st.columns(3)
getselcat = col1.selectbox('Category',['Transactions','Users'],index=None)
getselyear = col2.selectbox('Year',getyearlist,index=None)
getselquart = col3.selectbox('Quarter',getquarterlist,index=None)
if(getselcat == 'Transactions'):
    getcatdf = getaggtransquartpd
else:
    getcatdf = getaggusersquartpd
    
if(getselyear):
    getyeardf = getcatdf[getcatdf['Year'].str.contains(getselyear)]
    if(getselquart):
            getquartdf = getyeardf[getyeardf['Year'].str.contains(getselquart)]
            if(getselcat == 'Transactions'):
                getpd = pd.DataFrame([getquartdf['Transaction_Type'],getquartdf['Transaction_Amount'],getquartdf['Transaction_Count']]).T
                getcumsum = crorefunc(int(getpd['Transaction_Amount'].sum()))
                getcumcount = crorefunc(int(getpd['Transaction_Count'].sum()))
                st.write('Total Transaction Amount : ',getcumsum,' Crs')
                st.write('Total No. of Transactions : ',getcumcount,' Crs')
                st.write('')
                col4,col5=st.columns([0.8,1.1])
                with col4:         
                    st.subheader('Payment categories')
                    st.write('')
                    st.write('')
                    st.dataframe(getpd,hide_index=True)
                    st.write('')
                    st.write('')
                    st.subheader('Top 10 Transactions in the Quarter')
                    st.write('')
                    tab1,tab2,tab3 = st.tabs(['States','Districts','Pin Codes'])
                    with tab1:
                        col1,col2=st.columns([1.2,0.1])
                        with col1:
                            getfilt1df = gettoptransquartpd[gettoptransquartpd['Year'].str.contains(getselyear)]
                            getfilt2df = getfilt1df[getfilt1df['Year'].str.contains(getselquart)]
                            getnew1df = pd.DataFrame([getfilt2df['State_Name'],getfilt2df['State_Amount'],getfilt2df['State_Count']]).T
                            st.dataframe(getnew1df,hide_index=True)
                        with col2:
                            latlondf=statelatlongdf[statelatlongdf.State_Name.isin(getnew1df.State_Name)]
                            mapdf = getnew1df.merge(latlondf)
                            st.plotly_chart(px.scatter_geo(mapdf,'lat','lon',hover_name='State_Name',hover_data=['State_Amount','State_Count']))
                    with tab2:
                        col1,col2=st.columns([1.2,0.1])
                        with col1:                                         
                            getfilt1df = gettoptransquartpd[gettoptransquartpd['Year'].str.contains(getselyear)]
                            getfilt2df = getfilt1df[getfilt1df['Year'].str.contains(getselquart)]
                            getnew2df = pd.DataFrame([getfilt2df['District_Name'],getfilt2df['District_Amount'],getfilt2df['District_Count']]).T
                            st.dataframe(getnew2df,hide_index=True)
                        with col2:
                            latlondf=districtlatlongdf[districtlatlongdf.District_Name.isin(getnew2df.District_Name)]
                            mapdf = getnew2df.merge(latlondf)
                            st.plotly_chart(px.scatter_geo(mapdf,'lat','lon',hover_name='District_Name',hover_data=['District_Amount','District_Count']))                            
                    with tab3:
                        col1,col2=st.columns([1.2,0.1])
                        with col1:                             
                            getfilt1df = gettoptransquartpd[gettoptransquartpd['Year'].str.contains(getselyear)]
                            getfilt2df = getfilt1df[getfilt1df['Year'].str.contains(getselquart)]
                            getnew3df = pd.DataFrame([getfilt2df['Pincode'],getfilt2df['Pincode_Amount'],getfilt2df['Pincode_Count']]).T
                            st.dataframe(getnew3df,hide_index=True)
                        with col2:
                            latlondf=pincodelatlongdf[pincodelatlongdf.Pincode.isin(getnew3df.Pincode)]
                            mapdf = getnew3df.merge(latlondf)
                            st.plotly_chart(px.scatter_geo(mapdf,'lat','lon',hover_name='Pincode',hover_data=['City','Pincode_Amount','Pincode_Count']))                              
                with col5:
                    getstatsel = st.selectbox('Select Stat',['Transaction_Amount','Transaction_Count'],index=1)
                    st.plotly_chart(px.pie(getpd,values=getstatsel,names='Transaction_Type'))
                
                #State-wise Stats of India
                st.header(':blue[State-wise Stats]')
                filt1df = getaggtransstatpd[getaggtransstatpd['Year'].str.contains(getselyear)]
                filt2df = filt1df[filt1df['Year'].str.contains(getselquart)]
                filt2df.rename(columns={'State_FileRef':'State_Name'},inplace=True)
                selstate = st.selectbox('Select a State',filt2df['State_Name'].unique().tolist(),index=1)
                if(selstate):
                    filt3df = filt2df[filt2df['State_Name'].str.contains(selstate)]
                    newdf = pd.DataFrame([filt3df['Transaction_Type'],filt3df['Transaction_Amount'],filt3df['Transaction_Count']]).T
                    getamountsum = crorefunc(int(newdf['Transaction_Amount'].sum()))
                    getcountsum = crorefunc(int(newdf['Transaction_Count'].sum()))
                    st.write('Total Transaction Amount:',getamountsum,' Crs')
                    st.write('Total No. of Transactions',getcountsum,' Crs')
                    col4,col5=st.columns([0.8,1.1])
                    with col4:                                         
                        st.subheader('Payment categories')
                        st.write('')
                        st.write('')
                        st.dataframe(newdf,hide_index=True)
                        st.write('')
                        st.write('')
                        getheader = 'Top 10 Transactions in ' + selstate
                        st.subheader(getheader)
                        st.write('')
                        tab1,tab2 = st.tabs(['Districts','Pin Codes'])
                        with tab1:
                            col1,col2=st.columns([1.2,0.1])
                            with col1:                                         
                                getfilt1df = gettoptransstatpd[gettoptransstatpd['Year'].str.contains(getselyear)]
                                getfilt2df = getfilt1df[getfilt1df['Year'].str.contains(getselquart)]
                                getfilt3df = getfilt2df[getfilt2df['State_FileRef'].str.contains(selstate)]
                                getnew2df = pd.DataFrame([getfilt3df['District_Name'],getfilt3df['District_Amount'],getfilt3df['District_Count']]).T
                                st.dataframe(getnew2df,hide_index=True)
                            with col2:
                                latlondf=districtlatlongdf[districtlatlongdf.District_Name.isin(getnew2df.District_Name)]
                                mapdf = getnew2df.merge(latlondf)
                                st.plotly_chart(px.scatter_geo(mapdf,'lat','lon',hover_name='District_Name',hover_data=['District_Amount','District_Count']))                            
                        with tab2:
                            col1,col2=st.columns([1.2,0.1])
                            with col1:                             
                                getfilt1df = gettoptransstatpd[gettoptransstatpd['Year'].str.contains(getselyear)]
                                getfilt2df = getfilt1df[getfilt1df['Year'].str.contains(getselquart)]
                                getfilt3df = getfilt2df[getfilt2df['State_FileRef'].str.contains(selstate)]                                
                                getnew3df = pd.DataFrame([getfilt3df['Pincode'],getfilt3df['Pincode_Amount'],getfilt3df['Pincode_Count']]).T
                                st.dataframe(getnew3df,hide_index=True)
                            with col2:
                                latlondf=pincodelatlongdf[pincodelatlongdf.Pincode.isin(getnew3df.Pincode)]
                                mapdf = getnew3df.merge(latlondf)
                                st.plotly_chart(px.scatter_geo(mapdf,'lat','lon',hover_name='Pincode',hover_data=['City','Pincode_Amount','Pincode_Count']))                              
                    with col5:
                        statsel = st.selectbox('Stat Type',['Transaction_Amount','Transaction_Count'],index=1)
                        st.plotly_chart(px.pie(filt3df,values=statsel,names='Transaction_Type'))

                #Comparison of Overall India vs State
                st.subheader('Overall vs State Comparison')
                getstatdf = gettranspd[gettranspd['State_FileRef'].str.contains(selstate)]
                col1,col2=st.columns([0.8,0.9])
                with col1:
                    getlist = list()
                    for i in getyearlist:
                        getdf = getstatdf[getstatdf['Year'].str.contains(i)]
                        getsum = crorefunc(int(getdf['Transaction_Amount'].sum()))
                        getlist.append([i,getsum])
                    getnewstatdf = pd.DataFrame(getlist,columns=['Year',selstate])
                    getoversum = getover1df['Amount (In Crores)'].sum()
                    getstatsum = getnewstatdf[selstate].sum()
                    getpercent = int(((getstatsum/getoversum)*100))
                    mergedf=getover1df.merge(getnewstatdf)
                    mergedf.rename(columns={'Amount (In Crores)':'Overall'},inplace=True)
                    st.plotly_chart(px.line(mergedf,x='Year',y=['Overall',selstate],title='Transaction Amount'))
                    writetex = selstate + ' contributes to ' + str(getpercent) + '% of cumulative Transaction Amount.'
                    st.write(writetex)
                with col2:
                    getlist = list()
                    for i in getyearlist:
                        getdf = getstatdf[getstatdf['Year'].str.contains(i)]
                        getsum = crorefunc(int(getdf['Transaction_Count'].sum()))
                        getlist.append([i,getsum])
                    getnewstatdf = pd.DataFrame(getlist,columns=['Year',selstate])
                    getoversum = getover2df['Transactions (In Crores)'].sum()
                    getstatsum = getnewstatdf[selstate].sum()
                    getpercent = int(((getstatsum/getoversum)*100))                    
                    mergedf=getover2df.merge(getnewstatdf)
                    mergedf.rename(columns={'Transactions (In Crores)':'Overall'},inplace=True)                
                    st.plotly_chart(px.line(mergedf,x='Year',y=['Overall',selstate],title='Transaction Count'))
                    writetex =' And also, contributes to ' + str(getpercent) + '% of cumulative Transactions.'
                    st.write(writetex)

                #Overall India Contribution Stats
                st.write('')
                st.subheader(':blue[Overall India Contribution Stats]')
                getyear = st.selectbox('Select a Year',getyearlist,index=None)             
                getlist = list()
                for i in getyearlist:
                    getdf = getaggtransstatpd[getaggtransstatpd['Year'].str.contains(i)]
                    for j in getstatelist:
                        getnewdf = getdf[getdf['State_FileRef'].str.contains(j)]
                        getamountsum = crorefunc(int(getnewdf['Transaction_Amount'].sum()))
                        gettranssum = crorefunc(int(getnewdf['Transaction_Count'].sum()))
                        getlist.append([i,j,getamountsum,gettranssum])
                getinddf = pd.DataFrame(getlist,columns=['Year','State_Name','Amount (In Crores)','Transactions (In Crores)'])
                if(getyear):
                    getfiltdf = getinddf[getinddf['Year'].str.contains(getyear)]
                    st.plotly_chart(px.bar(getfiltdf,x='State_Name',y='Amount (In Crores)',color='Year'))
                    st.plotly_chart(px.bar(getfiltdf,x='State_Name',y='Transactions (In Crores)',color='Year'))
                else:
                    st.plotly_chart(px.bar(getinddf,x='State_Name',y='Amount (In Crores)',color='Year'))
                    st.plotly_chart(px.bar(getinddf,x='State_Name',y='Transactions (In Crores)',color='Year'))

            else:
                getpd = pd.DataFrame([getquartdf['Brand'],getquartdf['Brand_Count']]).T
                getcumusers = crorefunc(int(getquartdf['Registered_Users'].unique().sum()))
                st.write('Total No. of Registered Users : ',getcumusers,' Crs')
                col4,col5=st.columns([0.8,1.1])
                with col4:
                    st.subheader('User Brand Categories')
                    st.write('')
                    st.dataframe(getpd,hide_index=True)
                    st.subheader('Top 10 Registered Users')
                    tab1,tab2,tab3 = st.tabs(['States','Districts','Pin Codes'])
                    with tab1:
                        col1,col2=st.columns([1.2,0.1])
                        with col1:                                        
                            getfilt1df = gettopusersquartpd[gettopusersquartpd['Year'].str.contains(getselyear)]
                            getfilt2df = getfilt1df[getfilt1df['Year'].str.contains(getselquart)]
                            getnew1df = pd.DataFrame([getfilt2df['State_Name'],getfilt2df['State_Users']]).T
                            st.dataframe(getnew1df,hide_index=True)
                        with col2:
                            latlondf=statelatlongdf[statelatlongdf.State_Name.isin(getnew1df.State_Name)]
                            mapdf = getnew1df.merge(latlondf)
                            st.plotly_chart(px.scatter_geo(mapdf,'lat','lon',hover_name='State_Name',hover_data='State_Users'))                                              
                    with tab2:
                        col1,col2=st.columns([1.2,0.1])
                        with col1:                        
                            getfilt1df = gettopusersquartpd[gettopusersquartpd['Year'].str.contains(getselyear)]
                            getfilt2df = getfilt1df[getfilt1df['Year'].str.contains(getselquart)]
                            getnew2df = pd.DataFrame([getfilt2df['District_Name'],getfilt2df['District_Users']]).T
                            st.dataframe(getnew2df,hide_index=True)
                        with col2:
                            latlondf=districtlatlongdf[districtlatlongdf.District_Name.isin(getnew2df.District_Name)]
                            mapdf = getnew2df.merge(latlondf)
                            st.plotly_chart(px.scatter_geo(mapdf,'lat','lon',hover_name='District_Name',hover_data='District_Users'))                                                                    
                    with tab3:
                        col1,col2=st.columns([1.2,0.1])
                        with col1:                                            
                            getfilt1df = gettopusersquartpd[gettopusersquartpd['Year'].str.contains(getselyear)]
                            getfilt2df = getfilt1df[getfilt1df['Year'].str.contains(getselquart)]
                            getnew3df = pd.DataFrame([getfilt2df['Pincode'],getfilt2df['Pincode_Users']]).T
                            st.dataframe(getnew3df,hide_index=True)
                        with col2:
                            latlondf=pincodelatlongdf[pincodelatlongdf.Pincode.isin(getnew3df.Pincode)]
                            mapdf = getnew3df.merge(latlondf)
                            st.plotly_chart(px.scatter_geo(mapdf,'lat','lon',hover_name='Pincode',hover_data=['City','Pincode_Users']))                                            
                with col5:
                    st.plotly_chart(px.pie(getpd,values='Brand_Count',names='Brand'))

                #State-wise Stats of India
                st.header(':blue[State-wise Stats]')
                filt1df = getaggusersstattpd[getaggusersstattpd['Year'].str.contains(getselyear)]
                filt2df = filt1df[filt1df['Year'].str.contains(getselquart)]
                filt2df.rename(columns={'State_FileRef':'State_Name'},inplace=True)
                seluserstate = st.selectbox('Select a State',filt2df['State_Name'].unique().tolist(),index=1)                               
                if(seluserstate):
                    filt3df = filt2df[filt2df['State_Name'].str.contains(seluserstate)]
                    newdf = pd.DataFrame([filt3df['Brand'],filt3df['Brand_Count']]).T
                    getsum = crorefunc(int(newdf['Brand_Count'].sum()))
                    st.write('Total No. of Registered Users : ',getsum,' Crs')
                    col4,col5=st.columns([0.8,1.1])
                    with col4:
                        st.subheader('User Brand Categories')
                        st.write('')
                        st.dataframe(newdf,hide_index=True)
                        st.write('')
                        st.write('')
                        getheader = 'Top 10 Transactions in ' + seluserstate
                        st.subheader(getheader)
                        tab1,tab2 = st.tabs(['Districts','Pin Codes'])
                        with tab1:
                            col1,col2=st.columns([1.2,0.1])
                            with col1:                                         
                                getfilt1df = gettopusersstatpd[gettopusersstatpd['Year'].str.contains(getselyear)]
                                getfilt2df = getfilt1df[getfilt1df['Year'].str.contains(getselquart)]
                                getfilt3df = getfilt2df[getfilt2df['State_FileRef'].str.contains(seluserstate)]
                                getnew2df = pd.DataFrame([getfilt3df['District_Name'],getfilt3df['District_Users']]).T
                                st.dataframe(getnew2df,hide_index=True)
                            with col2:
                                latlondf=districtlatlongdf[districtlatlongdf.District_Name.isin(getnew2df.District_Name)]
                                mapdf = getnew2df.merge(latlondf)
                                st.plotly_chart(px.scatter_geo(mapdf,'lat','lon',hover_name='District_Name',hover_data='District_Users'))                          
                        with tab2:
                            col1,col2=st.columns([1.2,0.1])
                            with col1:                                         
                                getfilt1df = gettopusersstatpd[gettopusersstatpd['Year'].str.contains(getselyear)]
                                getfilt2df = getfilt1df[getfilt1df['Year'].str.contains(getselquart)]
                                getfilt3df = getfilt2df[getfilt2df['State_FileRef'].str.contains(seluserstate)]
                                getnew2df = pd.DataFrame([getfilt3df['Pincode'],getfilt3df['Pincode_Users']]).T
                                st.dataframe(getnew2df,hide_index=True)
                            with col2:
                                latlondf=pincodelatlongdf[pincodelatlongdf.Pincode.isin(getnew2df.Pincode)]
                                mapdf = getnew2df.merge(latlondf)
                                st.plotly_chart(px.scatter_geo(mapdf,'lat','lon',hover_name='Pincode',hover_data=['City','Pincode_Users']))  
                    with col5:
                        st.plotly_chart(px.pie(newdf,values='Brand_Count',names='Brand'))

                #Comparison of Overall India vs State
                st.subheader('Overall vs State Comparison')
                getstatdf = getuserspd[getuserspd['State_FileRef'].str.contains(seluserstate)]
                st.write('')
                getlist = list()
                for i in getyearlist:
                    getdf = getstatdf[getstatdf['Year'].str.contains(i)]
                    getsum = crorefunc(int(getdf['Brand_Count'].sum()))
                    getlist.append([i,getsum])
                getnewstatdf = pd.DataFrame(getlist,columns=['Year',seluserstate])
                getoversum = getover3df['Registered Users (In Crores)'].sum()
                getstatsum = getnewstatdf[seluserstate].sum()
                getpercent = int(((getstatsum/getoversum)*100))
                mergedf=getover3df.merge(getnewstatdf)
                mergedf.rename(columns={'Registered Users (In Crores)':'Overall'},inplace=True)
                writetex = seluserstate + ' contributes to ' + str(getpercent) + '% of cumulative no. of Registered Users.'
                st.write(writetex)                
                st.plotly_chart(px.line(mergedf,x='Year',y=['Overall',seluserstate],title='Registered Users'))

                #Overall India Registered Users Stats
                st.write('')
                st.subheader(':blue[Overall India Registered Users Stats]')
                getyear = st.selectbox('Select a Year',getyearlist,index=None)             
                getlist = list()
                for i in getyearlist:
                    getdf = getaggusersstattpd[getaggusersstattpd['Year'].str.contains(i)]
                    for j in getstatelist:
                        getnewdf = getdf[getdf['State_FileRef'].str.contains(j)]
                        getamountsum = crorefunc(int(getnewdf['Brand_Count'].sum()))
                        getlist.append([i,j,getamountsum])
                getinddf = pd.DataFrame(getlist,columns=['Year','State_Name','Registered Users (In Crores)'])
                if(getyear):
                    getfiltdf = getinddf[getinddf['Year'].str.contains(getyear)]
                    st.plotly_chart(px.bar(getfiltdf,x='State_Name',y='Registered Users (In Crores)',color='Year'))
                else:
                    st.plotly_chart(px.bar(getinddf,x='State_Name',y='Registered Users (In Crores)',color='Year'))

#Feedback about the app
if(getselcat and getselyear and getselquart):
    st.title(':blue[Feedback about the Statistics]')
    st.write('This data displayed here was obtained from the Phonepe Pulse Github repository. For more information, refer https://www.phonepe.com/pulse/explore/transaction/2022/4/')
    getresponse = st.radio(label='How would you rate the App?',options= ['Poor','Average','Good','Very Good','Excellent'],index=None)
    getcomments = st.text_area(label='Comments',value='')
    if(getresponse and getcomments):
        st.subheader('Thanks for your feedback... We will improve based on this!!')