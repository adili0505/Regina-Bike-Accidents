# The purpose of this simple app is to visualize bike accidents occurred in the City of Regina 2010-2019
# All Rights Reserved @2021, Adili Masanika

# Packages used
import streamlit as st
import altair as alt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import os

# disable chained assignments
pd.options.mode.chained_assignment = None

# st.write("Has environment variables been set:",
# os.environ["db_username"] == st.secrets["db_username"]
# )

# st.write("DB username:", st.secrets["db_username"])
# st.write("DB password:", st.secrets["db_password"])

st.set_option('deprecation.showPyplotGlobalUse', False)
# st.set_page_config(layout="wide")


st.title("Analysis on Severity of Bike Accidents in the City of Regina 2010 - 2019")

# Data loading and cleaning
@st.cache
def load_data():
    bikedata = pd.read_excel('BicycleCollisions-Regina-2010-2019.xlsx',parse_dates=True)
    bikedata.set_index('ACCDATE')
    #ACCDATE = datetime.datetime.strptime('ACCDATE','%Y-%m-%d').date()
    bikedata['weekday'] = bikedata['ACCDATE'].dt.strftime("%a")
    bikedata['month'] = bikedata['ACCDATE'].dt.strftime("%b")
    bikedata['hour'] = bikedata.ACCTIME.astype(str).str[:-2]
    bikedata.fillna(method='ffill', inplace=True)
    bikedata.loc[bikedata['hour']=='99', 'hour'] = 0
    bikedata.loc[bikedata['hour']=='', 'hour'] = 0
    bikedata['ROADAUTH'].astype(str).astype(int)
    bikedata['hour'] = bikedata.hour.astype(int)
    return bikedata

def format_radio(p):
    format = {
        'WEATHER':'Weather',
        "ROADSURF":'Road surface',
        "ROADCOND":'Road condition',
        'ACCSITE':'Accident site',
        "NATLIGHT":'Natural light',
        "ARTLIGHT":'Artificial light',
        "ROADAUTH":'Road authority'
        }
    return format[p]

def format_radio_time(p):
    return p.title()

st.header('Summary')
st.markdown(
    """
    <div style="text-align: justify"> 
        This brief report focuses on analyzing severity of bike collisions occurred in the city of Regina between 2010 and 2019. The data provided include 555 reported accidents from different locations of the city particularly at  intersections with streets, private approach and driveway between 4th Ave, 7th Ave, Albert St, Broad St, Dewdney Ave, Victoria Ave, Winnipeg St and Saskatchewan Dr. Out of 555 traffic collisions, 465 injuries were recorded, 5 cyclists were killed and costed more than $1.5 million for the entire period of 10 years. Many accidents which resulted into personal injuries happened during the evening rush hours on weekdays from Tuesday to Thursday in the summer. Likewise, most of the traffic collisions occurred in clear weather conditions, dry and normal road surfaces. Street authorities are responsible for maintenance and traffic safety of the roads where many accidents took place.
    </div>
    """
,unsafe_allow_html=True)


st.header('Acknowledgement')
st.markdown(
    """
    <div style="text-align: justify"> 
        I would like to express my sincerely gratitudes to the organizers of Data Visualization Challenge #2 - <a href = "https://regina.dataforgood.ca">Dataforgood, Regina</a>; <a href="https://saskpolytech.ca">Saskatchewan Polytechnic</a> for sponsoring this contest; and <a href="https://www.sgi.sk.ca">Saskatchewan Government Insurance</a> for donating the dataset used in this study. May you please receive my heartfelt appreciations.
    </div>
    """
,unsafe_allow_html=True)


st.header("1. Introduction")
st.markdown(
    """
    <div style="text-align: justify">
        <style>
            a { text-decoration: none; }
        </style>
        According to <a href= "https://www.sgi.sk.ca/safety-stats">Saskatchewan's Traffic Safety Statistics</a>,  there were 142 traffic collisions involving a motorcycle, resulting in 95 injuries and 5 deaths in 2019 in Saskatchewan.  Also it was noted that, 110 cyclists were injured as a result of a traffic collision in Saskatchewan in the same year.  In this report, we focus on bike accidents which occurred between 2010 and 2019 in the city of Regina. 
    <br><br>
        There were 555 observed bike collisions for ten years period from different streets of the city.  Bike accidents can occur due to many associated factors such as the location where the collision took place (i.e., accident site), lighting available at the collision site which can be either natural or artificial, relative position of the vehicle and environmental conditions at the time and scene of the collision. This include the predominant weather condition, road surface condition as well as the prevailing road condition.  Also it can be a combination of the above factors.  Regardless of any of the aforementioned causes, there might be an associated effect when an accident takes place. 
    </div>
    """
,unsafe_allow_html=True) 

st.markdown(
    """
    <div tyle="text-align: none">
    <br>
        Taking into consideration of the variables under study, we particularly intend to:
        <ul>
            <li> illustrate the total accidents occurred by severity level by year, month, weekday and hour.</li>
            <li> visualize the traffic collisions by severity levels by:
                <ul>
                    <li> accident site,</li>
                    <li> weather condition,</li>
                    <li> road surface,</li>
                    <li> light, and</li>
                    <li> road authority.</li>
                </ul>
            </li>
            <li> examine accidents per street.</li>
        </ul>
    </div>
    """
,unsafe_allow_html=True) 

st.markdown(
    """
    <div style="text-align: justify"> 
        This study will be useful to the government authorities on identifying potential locations in the city with the most severe rate of bike accidents and take necessary measures.
    <br><br>
        The rest of the report is organized as follows. Sec. 2 describes the data and model used in this study.  We provide a brief visualization and analysis in Sec. 3. Lastly, we summarize the study and plan for the future research in Sec. 4.
    </div>
    """
,unsafe_allow_html=True) 


bikedata = load_data()
bikes = bikedata[['ACCDATE','year','month','weekday','hour','NOINJ','NOKILLED','ACCSITE','SEVERITY','ROADAUTH','NATLIGHT','ARTLIGHT','WEATHER','ROADSURF','ROADCOND','USTREET1','USTREET2']]
bikes = bikes.sort_values(by='ACCDATE').set_index('ACCDATE')


st.header("2. Data and Model")
st.markdown(
    """
    <div style="text-align: justify"> 
        To demonstrate the construction and interpretation of the tables and plots, data for bike accidents from the city of Regina for ten years were used. The table below shows the given dataset, there are  with 46 variables and 555 observations.
    </div>
    """
,unsafe_allow_html=True)
st.write(bikedata)

st.markdown(
    """
    <div style="text-align: justify"> 
        The nature of the variables given in this data are mostly categorical, where by there are different classes for each each given variable. Since we focus our analysis on severity of 555 reported cases of collisions in terms of other variables, it is wise to describe the severity levels in brief as follows:
        <ul>
            <li> Level 1: Property Damage Only </li>
            <li> Level 2: Personal Injury </li>
            <li> Level 3: Fatal </li>
        </ul>
        The description of other variables is available <a href = "https://github.com/adili0505/Regina-Bike-Accidents">here</a>
        <br>
        Upon data extraction which involved dropping off null variables, we obtained the following table.
        <br><br>
    </div>
    """
,unsafe_allow_html=True)

st.write(bikes)

st.markdown(
    """
    <div style="text-align: justify"> 
        The proposed plots use bar charts to illustrate the distribution of categorical variables, with different colours to depict different severity levels so that accidents can be easily tracked among other parameters. The data is also presented in tabular form for different levels of severity. The plots and tables were produced by using Python which is a standard software for data visualization and analysis.
    </div>
    """
,unsafe_allow_html=True)


st.header("3. Data Visualization")
st.write(
    """
    In the previous section we summarized about the data and model used in the report. Herein we provide the results of the report.
    """
)

# CSS to inject contained in a string
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)


# Total injuries and fatalities
tot_inj = bikes.groupby(['year']).NOINJ.sum().reset_index(name='injuries')
tot_kil = bikes.groupby(['year']).NOKILLED.sum().reset_index(name='fatalities')
tot_acc = pd.merge(tot_inj, tot_kil,how='right', on='year')

tot_acc['perc of injuries'] = (tot_acc['injuries']/tot_acc['injuries'].sum())*100
new_row = {'year':'Total','injuries':tot_acc['injuries'].sum(),'fatalities':tot_acc['fatalities'].sum(),'perc of injuries':tot_acc['perc of injuries'].sum()}

tot_acc1 = tot_acc.append(new_row, ignore_index=True)

st.subheader('3.1. Injuries and fatalities')
st.table(tot_acc1)

st.markdown(
    """
    <div style="text-align: justify"> 
        In 2018 and 2019, there was a decrease in the percentage of accidents (which is equivalent to an average of 31 injuries per year) as compared to the previous years (which is an average of 50 injuries per year). Also we observe that only 5 cyclists died out of 555 reported cases of accidents.
    </div>
    """
,unsafe_allow_html=True)

st.subheader('3.2. Severity of accidents')

# Navigation bar for severity levels with respect to time and other parameters
st.sidebar.title('Navigation')
severityby = st.sidebar.radio('Severity levels by', 
                                    (
                                    'WEATHER',
                                    "ROADSURF",
                                    "ROADCOND",
                                    'ACCSITE',
                                    "NATLIGHT",
                                    "ARTLIGHT",
                                    "ROADAUTH"
                                    # 'CONFIG'
                                    ), format_func=format_radio)

time = st.sidebar.radio('Time',
                            options = ['year', 
                                       'month',
                                       'weekday',
                                        'hour'], format_func=format_radio_time)

# Total severity 
def severity(sev_data,time):
    sns.set(font_scale = 3)
    sev_data = bikes.groupby(time,sort=False).SEVERITY.value_counts().reset_index(name='total_severity')
    sns.catplot(x = time,       # x variable name
                y = 'total_severity',       # y variable name
                hue = 'SEVERITY',  # group variable name
                data = sev_data,     # dataframe to plot
                height=10, 
                aspect=2, legend=False,
                # order=sev_data,
                kind = "bar")
    plt.legend(title = 'SEVERITY', loc='upper right') #loc='upper right', bbox_to_anchor = (1, 1)
    plt.ylabel('Total severity')
    plt.xlabel(time)
    st.pyplot()
st.write(f"""Total accidents by severity levels for each {time.lower()}.""")
severity(bikes,time)

# Total severity with other parameters
st.subheader('3.3. Severity levels by time and other parameters')
def plot(data,condition,time):
    data = bikes.groupby([time,condition],sort=False)['SEVERITY'].count().reset_index(name='total_severe')
    sns.barplot(x = time,       # x variable name
            y = 'total_severe',       # y variable name
            hue = condition,  # group variable name
            data = data)
    plt.legend(title = condition,loc='upper right') #loc='upper right', bbox_to_anchor = (1, 1)
    plt.ylabel('Total severity')
    plt.xlabel(time)
    st.pyplot()

st.write(f"""The figure below shows accidents count as a function of {time.lower()}
         and for severity level parameter {severityby.lower()}.""")
plot(bikes, severityby.upper(), time)



st.subheader('3.4. Accident cases per streets')
st.write(
    """
    There were many streets where the accidents took place but we select those with at least 5 reported collisions. 
    """
)

# Accidents per street
street1 = bikes.USTREET1.value_counts().rename_axis('street').reset_index(name='accidents')
street2 = bikes.USTREET2.value_counts().rename_axis('street').reset_index(name='accidents')

streets = street1.loc[street1['accidents'] >= 5]
streets2 = street2.loc[street2['accidents'] >= 5]

def streetplot(streetdata):
    splot = alt.Chart(streetdata).mark_bar().encode(
        x=alt.X('street', axis=alt.Axis(title='Street name')),
        y=alt.Y('accidents', axis=alt.Axis(title='Accidents reported'))
        )
    splot

st.subheader('3.4.1. Accidents per USTREET1')
streetplot(streets)

st.subheader('3.4.2. Accidents per USTREET2')
streetplot(streets2)

st.markdown(
    """
    ** Observations made from the figures above:**
    <div style="text-align: justify"> 
        <ul style="list-style-type: disc">
            <li> 
                Intersections with streets, private approach and driveway resulted into numerous accidents occurred during the evening peak hours on weekdays in the summer.</li>
            <li> 
                Over the past ten years many traffic collisions happened in clear weather conditions.
            </li> 
            <li> 
                Dry and wet road surfaces led to a high number of bike accidents in every year between 2010 and 2019 as compared to others. 
            </li>
            <li> 
                Severity of many bike accidents cases took place in normal road conditions with no cases happened in roads under construction or repair. This shows discipline of obeying traffic rules and regulations among cyclists in the construction zones.
            </li>
            <li> 
                Collision analysis by light condition revealed that most accidents occurred during the daylight time. In the case of artificial light, lights were available but were not on. This calls for a serious intervention such as increasing fines for those who will be caught riding with no light turned on.
            </li>
            <li> 
                Furthermore, the results show that street road authorities are responsible for the maintenance where most of the traffic collisions occurred.
            </li>
            <li> 
                The following streets are responsible for a high number of accidents; 4th, 7th, 12th, and 13th Avenues, Albert St, Broad St, Dewdney Ave, Victoria Ave, Winnipeg St, Elphinstone St and Saskatchewan Dr.
            </li>
        </ul>
    </div>
    """
,unsafe_allow_html=True)


st.header('4. Final Thoughts')
st.subheader('4.1. Conclusion and Suggestions')
st.markdown(
    """
    <div style="text-align: justify"> 
        The main purpose of this study was to examine the severity of bike accidents occurred in the city of Regina for the period of 10 years (2010-2019). We discovered that, most of accidents which resulted to personal injuries occurred at street intersections during evening rush hours in the weekdays (mostly, Tuesday to Thursday) of summer season.
    <br><br>
        The authorities (i.e., street authorities) need to allocate more resources to reduce the number of traffic collisions. For example, increasing the number of road signs and symbols which might include constructing humps in the stated streets in Sec. 3.4. In addition to that, where possible the authorities need to increase road patrolmen in areas with a notable higher rate of bike accidents particularly during the peak hours.
    <br><br>
        Likewise, education to the entire community must be continually provided for safety driving to avoid unnecessary collisions. In extreme circumstances, fines must be doubled or more as a consequence of violating traffic rules and regulations stipulated by both the government of Saskatchewan and the Federal government. This might be an alternative to cover the accident costs incurred by the authorities for treating injured cyclists and repairing damaged properties.
    </div>
    """
,unsafe_allow_html=True)

st.subheader('4.2. Possible Future Research')

st.markdown('''
<div style="text-align: justify"> 
    Despite of the interesting results presented in this brief report, among the most important variables (i.e., longitude and latitude) were null which posed a great challenge for sketching a map of the city showing the areas with high rate of accidents. We plan to use the unstructured grids to sketch a required map as part of our future work.
</div>'''
,unsafe_allow_html=True)

st.markdown('''
<div style="text-align: center; border:2px solid DodgerBlue"> 
    <footer>
        <p> Created by Adili Masanika. <span>&#169;</span> 2021</p>
    </footer>
</div>''',unsafe_allow_html=True)
