import streamlit as st 
import pandas as pd
import numpy as np
import os
from matplotlib import image
import plotly.express as px

# gets the directory path of the current Python script file that is being executed.
file_dir=os.path.dirname(os.path.abspath(__file__))

# creates a new path by combining the directory path from the previous step with the special string os.pardir. The os.pardir represents the parent directory of the current directory.
parent_dir=os.path.join(file_dir,os.pardir)

# combines the path of the parent directory with the folder name "resources" to create a new path.
dir_of_interest=os.path.join(parent_dir,"resources")

# combines the path of the "resources" folder with the file name "display.csv" to create a new path.
data_path=os.path.join(dir_of_interest,"display.csv")

# It loads the data from the CSV file and stores it in the variable data.
data=pd.read_csv(data_path)


# Cuisine Types
col=['Afghani', 'African', 'American', 'Andhra', 'Arabian', 'Asian',
       'Assamese', 'Awadhi', 'BBQ', 'Bakery', 'Belgian', 'Bengali',
       'Beverages', 'Bihari', 'Bohri', 'British', 'Burmese', 'Cantonese',
       'Chettinad', 'Chinese', 'Continental', 'Desserts', 'European',
       'Fast Food', 'French', 'German', 'Goan', 'Greek', 'Gujarati',
       'Healthy Food', 'Hyderabadi', 'Indonesian', 'Iranian', 'Italian',
       'Japanese', 'Jewish', 'Kashmiri', 'Kerala', 'Konkan', 'Korean',
       'Lebanese', 'Lucknowi', 'Maharashtrian', 'Malaysian',
       'Mangalorean', 'Mediterranean', 'Mexican', 'Middle Eastern',
       'Modern Indian', 'Mughlai', 'Naga', 'Nepalese', 'North Eastern',
       'North Indian', 'Oriya', 'Parsi', 'Portuguese', 'Rajasthani',
       'Russian', 'Seafood', 'Sindhi', 'Singaporean', 'South American',
       'South Indian', 'Spanish', 'Sri Lankan', 'Tamil', 'Thai',
       'Tibetan', 'Turkish', 'Vegan', 'Vietnamese']

#Choose City
st.subheader('City Restaurant Analysis')
City=st.selectbox("City",('Banashankari', 'Bannerghatta Road', 'Basavanagudi', 'Bellandur',
                          'Brigade Road', 'Brookefield', 'BTM', 'Church Street',
                          'Electronic City', 'Frazer Town', 'HSR', 'Indiranagar',
                          'Jayanagar', 'JP Nagar', 'Kalyan Nagar', 'Kammanahalli',
                          'Koramangala 4th Block', 'Koramangala 5th Block',
                          'Koramangala 6th Block', 'Koramangala 7th Block', 'Lavelle Road',
                          'Malleshwaram', 'Marathahalli', 'MG Road', 'New BEL Road',
                          'Old Airport Road', 'Rajajinagar', 'Residency Road',
                          'Sarjapur Road', 'Whitefield'))
# code filters the data based on the selected city.
df=data[data["City"]==City]

#Distribution graph of feature variable

st.subheader('Distribution graph of feature variable')
col1,col2=st.columns(2,gap="medium")
with col1:
    # code sets up a dropdown menu for the user to select a variable for the pie chart.
    var=st.selectbox("Pie Chart",("Delivery","Booking","Category","Price_Category"))
    # calculates the value counts of the selected variable from the filtered DataFrame and assigns it to the inter variable.
    inter=df[var].value_counts()
    # creates a pie chart using the values and names from inter as input.
    fig = px.pie(values=inter.values, names=inter.index)
    # displays the pie chart in the user interface
    st.plotly_chart(fig,use_container_width=True)
with col2:
    # code sets up a dropdown menu for the user to select a variable for the histogram.
    var=st.selectbox("Histogram",( 'No_of_Varieties','Cost_Per_Person', 'Rating','Category','Price_Category'))
    # creates a histogram using the selected variable (var) from the filtered DataFrame (df) as the x-axis variable
    fig = px.histogram(df, x=var)
    # displays the histogram in the user interface
    st.plotly_chart(fig,use_container_width=True)



#dataframe of count of restaurant type and popular cuisine among them.

st.subheader('Numbers of different restaurant type, with most popular cuisine among them')
# groups the DataFrame (df) by the "Type" column and sums up the values of the cuisine types (col) for each group.
inter=df.groupby(["Type"])[col].sum()
#  initializes an empty dictionary called dicton, which will store the most popular cuisines for each restaurant type.
dicton={}


for i in range(len(inter)):
    # retrieves the columns (cuisine types) from the inter DataFrame
    index=inter.columns
    #  retrieves the values of the current row, transposes them, and flattens them into a 1D array.
    val=inter.iloc[i].values.T.flatten()
    #creates a pandas Series with the flattened values and uses the cuisine types as the index
    series=pd.Series(val,index)
    # sorts the values in descending order and selects the top 5 cuisine types.
    vall=list(series.sort_values(ascending=False).head().index)
    # adds an entry to the dicton dictionary, where the key is the restaurant type and the value is the list of most popular cuisine types.
    dicton[inter.index[i]]=vall
    
# converts the dicton dictionary into a DataFrame
frame=pd.DataFrame(dicton,index=['1st','2nd','3rd','4th','5th'])
#  transposed (T) to have the restaurant types as rows and the most popular cuisines as columns.
frame=frame.T

#  groups the DataFrame (df) by the "Type" column and counts the occurrences of each restaurant type. It sorts the resulting counts in descending order and assigns them to inter.
inter=df.groupby("Type")["Type"].count().sort_values(ascending=False)
# merges the inter DataFrame (containing restaurant type counts) with the frame DataFrame (containing most popular cuisines). It performs the merge based on the common key, which is the "Type" column. The resulting DataFrame is assigned to sol.
sol=pd.merge(left=inter,right=frame.loc[inter.index,:],on=inter.index)
#  renames the columns of sol to have more descriptive names. The "key_0" column is renamed to "Restaurant Type", and the "Type" column is renamed to "Numbers".
sol.rename(columns={"key_0":"Restaurant Type","Type":"Numbers"},inplace=True)
# displays the sol DataFrame in the user interface using st.write(), which shows the numbers of different restaurant types and their most popular cuisines.
st.write(sol)



#Barplot showing numbers of restaurant with top five famous cuisine

# line retrieves the unique values of the "Type" column from the DataFrame df and assigns them to the cols variable. It represents the different restaurant types.
cols=df["Type"].unique()
# Initializes an empty DataFrame called idf,  which will store the intermediate results.
idf=pd.DataFrame()
# groups the DataFrame df by the "Type" column and sums up the values of the cuisine types (col) for each group. The resulting DataFrame is transposed (T) to have the cuisine types as columns and the restaurant types as rows. It is assigned to inter.
inter=df.groupby("Type")[col].sum().T


for i in cols:
    # retrieves the counts of cuisine types for the current restaurant type (i). It sorts the values in descending order and selects the top values using head(). It assigns the result to the ser variable.
    ser=inter[i].sort_values(ascending=False).head()
    #  converts the ser Series into a DataFrame called df_inter
    df_inter=pd.DataFrame(ser)
    # line resets the index of df_inter
    df_inter.reset_index(inplace=True)
    # renames the columns of df_inter to have more descriptive names. The column with cuisine counts is renamed to "Count", and the index column (cuisine types) is renamed to "Cuisine".
    df_inter.rename(columns={i:"Count","index":"Cuisine"},inplace=True)
    # adds a new column called "Type" to df_inter and assigns the current restaurant type (i) to all rows of that column.
    df_inter["Type"]=i
    # concatenates df_inter with idf along the row axis (axis=0). It appends the current restaurant type's cuisine count data to the intermediate DataFrame idf.
    idf=pd.concat([idf,df_inter],axis=0)
    
# creates a bar chart using the idf DataFrame as the data source. The "Type" column is used for the x-axis, the "Count" column for the y-axis, and the "Cuisine" column for the color encoding of the bars.
fig = px.bar(idf,x="Type",y="Count",color="Cuisine")

# displays the bar chart in the user interface
st.plotly_chart(fig)



#Plot showing the no of varieties served at restaurants


st.subheader('Plot showing relationship between no of varieties and no of best sellers')

# groups the DataFrame df by the "No_of_Best_Sellers" and "No_of_Varieties" columns and counts the occurrences of the "Menu" column for each combination of these two variables. The resulting DataFrame is assigned to inter.
inter=df.groupby(['No_of_Best_Sellers', 'No_of_Varieties'])[["Menu"]].count()

# renames the "Menu" column in the inter DataFrame to "Count" for better clarity.
inter.rename(columns={"Menu":"Count"},inplace=True)

# resets the index of the inter DataFrame to make the grouped columns ("No_of_Best_Sellers" and "No_of_Varieties") appear as regular columns.
inter.reset_index(inplace=True)

# creates a grouped bar chart using the inter DataFrame as the data source. The "No_of_Varieties" column is used for the x-axis, the "Count" column for the y-axis, and the "No_of_Best_Sellers" column for the color encoding of the bars.
fig = px.bar(inter,x="No_of_Varieties",y="Count",color="No_of_Best_Sellers",barmode="group")

# displays the bar chart in the user interface
st.plotly_chart(fig)



#boxplot showing price for different type,further categorized by their rating

st.subheader("Plot showing relationship between price and rating for different Restaurant type")
# creates a box plot using the DataFrame df as the data source. The "Type" column is used for the x-axis, the "Cost_Per_Person" column for the y-axis, and the "Category" column for the color encoding of the boxes.
fig=px.box(df,x="Type",y="Cost_Per_Person",color="Category")
# displays the box plot in the user interface
st.plotly_chart(fig)



#Most Popular Cuisine Varieties in City's Restaurant

st.subheader("Most Popular Cuisine Varieties in City's Restaurant")

# groups the DataFrame df by the "City" column and calculates the sum of each cuisine type (col) for each city. The resulting DataFrame is assigned to inter.
inter=df.groupby(["City"])[col].sum()

# retrieves the column names (cuisine types) from the inter DataFrame and assigns them to the index variable.
index=inter.columns

# retrieves the values from the inter DataFrame, transposes them (T), and flattens them into a 1-dimensional array. The resulting array represents the sum of cuisine types for each city and is assigned to the val variable.
val=inter.values.T.flatten()

# creates a pandas Series object called series using the val array as the data and the index variable as the index.
series=pd.Series(val,index)

# sorts the values in the series Series in descending order using sort_values(). It selects the top values using head() and assigns the result to the idf variable.
idf=series.sort_values(ascending=False).head()

# creates a bar chart using the idf Series as the data source. The index of the Series is used for the x-axis, and the values of the Series are used for the y-axis.
fig = px.bar(idf,x=idf.index,y=idf.values)

# displays the bar chart in the user interface
st.plotly_chart(fig)



#Most Popular Cuisine Varieties in City's Restaurant Types

# creates a select box in the user interface. select box allows the user to choose a restaurant type from the unique values in the "Type" column of the DataFrame df. 
type=st.selectbox("Restaurant Type",df["Type"].unique())

# divides the user interface into two columns using st.columns(). The first column, col1, occupies two-thirds of the available width, and the second column, col2, occupies one-third of the width. The gap="medium" parameter adds some spacing between the columns.
col1,col2=st.columns([2,1],gap="medium")
with col1:
    # calculates the sum of cuisine types for each restaurant type and assigns the result to inter. The col variable represents the list of cuisine types.
    inter=df.groupby(["Type"])[col].sum()

    # transposes the inter DataFrame to have restaurant types as rows and cuisine types as columns.
    inter=inter.T

    # selects the column corresponding to the chosen type (restaurant type) from the inter DataFrame and assigns it back to inter. This gives the sum of cuisine types for the selected restaurant type.
    inter=inter[type]

    # sorts the values in the inter Series (sum of cuisine types) in descending order, selects the top values using head(), and assigns the result to idf.
    idf=inter.sort_values(ascending=False).head()

    # creates a bar chart using the idf Series as the data source. The index of the Series is used for the y-axis, and the values of the Series are used for the x-axis.
    fig = px.bar(idf,y=idf.index,x=idf.values)

    #  displays the bar chart in the user interface
    st.plotly_chart(fig,use_container_width=True)
with col2:

    # filters the DataFrame df to keep only the rows where the "Type" column matches the selected type.
    inter=df[df['Type']==type]

    # groups the filtered DataFrame inter by the "Name" column and calculates the maximum rating for each name.
    ser=inter.groupby('Name')[['Rating']].max()

    # sorts the ratings in descending order and selects the top 10 names with the highest ratings.
    sol=ser.sort_values(by='Rating',ascending=False).head(10)

    # displays the sol DataFrame in the user interface using st.write().
    st.write(sol,use_container_width=True)
   


#Plot showcasing price and quality of top most famous cuisine in City
st.subheader("Plot showcasing price and quality analysis of top most famous cuisine in City")

# groups the DataFrame df by the "City" column and calculates the sum of each cuisine type (col) for each city. The resulting DataFrame is assigned to inter.
inter=df.groupby(["City"])[col].sum()

# retrieves the column names (cuisine types) from the inter DataFrame and assigns them to the index variable.
index=inter.columns

# retrieves the values from the inter DataFrame, transposes them (T), and flattens them into a 1-dimensional array. The resulting array represents the sum of cuisine types for each city and is assigned to the val variable.
val=inter.values.T.flatten()

# creates a pandas Series object called series using the val array as the data and the index variable as the index.
series=pd.Series(val,index)

# sorts the values in the series Series in descending order and selects the index of the top most famous cuisine types.
sel=series.sort_values(ascending=False).head().index

##1

# creates an empty DataFrame called idf to store the results.
idf=pd.DataFrame()

for i in sel:
    
    # filters the DataFrame df to keep only the rows where the selected cuisine type is present.
    inter=df[df[i]==1]
    
    # groups the filtered DataFrame inter by the "Price_Category" column and counts the number of menus in each price category.
    inter=inter.groupby(["Price_Category"])[["Menu"]].count()
    
    # resets the index of the grouped DataFrame inter
    inter=inter.reset_index()
    
    # renames the "Menu" column to "Count" in the inter DataFrame.
    inter.rename(columns={"Menu":"Count"},inplace=True)
    
    # adds a new column "Cuisine_Type" to the inter DataFrame and assigns the selected cuisine type to all rows.
    inter["Cuisine_Type"]=i
    
    # concatenates the inter DataFrame with the idf DataFrame vertically.
    idf=pd.concat([idf,inter],axis=0)


# creates a bar chart using the idf DataFrame as the data source. The "Cuisine_Type" column is used for the x-axis, the "Count" column is used for the y-axis, and the "Price_Category" column is used for coloring the bars. The barmode="group" parameter ensures that the bars are grouped together.
fig = px.bar(x=idf["Cuisine_Type"], y=idf["Count"], color=idf["Price_Category"],barmode="group")

# displays the first bar chart in the user interface
st.plotly_chart(fig)



##2
# block of code is similar to the previous one, but it analyzes the "Category" column instead of the "Price_Category" column. It creates a second bar chart based on the cuisine type and category.

idf=pd.DataFrame()

for i in sel:
    
    inter=df[df[i]==1]
    inter=inter.groupby(["Category"])[["Menu"]].count()
    inter=inter.reset_index()
    inter.rename(columns={"Menu":"Count"},inplace=True)
    inter["Cuisine_Type"]=i
    idf=pd.concat([idf,inter],axis=0)


fig = px.bar(x=idf["Cuisine_Type"], y=idf["Count"], color=idf["Category"],barmode="group")

st.plotly_chart(fig)



#Plot comparing pricing and quality of Cuisine, plus displaying best rated restaurant

st.subheader("Best Restaurant for a Cuisine Type")

# creates a select box in the user interface. The select box allows the user to choose a cuisine type from the col list of cuisine types.
Cuisine=st.selectbox("Cuisine",col,index=53)

# divides the user interface into two columns
col1,col2=st.columns([2,1],gap="medium")
with col1:
    
    # filters the DataFrame df to keep only the rows where the selected cuisine type is present.
    inter=df[(df[Cuisine]==1)]
    
    # groups the filtered DataFrame inter by the "Price_Category" and "Category" columns and counts the number of menus in each combination.
    inter=inter.groupby(["Price_Category","Category"])[["Menu"]].count()
    
    # resets the index of the grouped DataFrame inter.
    inter=inter.reset_index()
    
    # renames the "Menu" column to "Count" in the inter DataFrame.
    inter.rename(columns={"Menu":"Count"},inplace=True)
    
    # creates a bar chart using the inter DataFrame as the data source. The "Price_Category" column is used for the x-axis, the "Count" column is used for the y-axis, and the "Category" column is used for coloring the bars.
    fig = px.bar(inter,x="Price_Category", y="Count", color="Category",barmode="group")
    
    # displays the bar chart in the user interface
    st.plotly_chart(fig,use_container_width=True)
with col2:
    
    # filters the DataFrame df to keep only the rows where the selected cuisine type is present
    inter=df[df[Cuisine]==1]
    
    # groups the filtered DataFrame inter by the "Name" column and calculates the maximum rating for each name.
    ser=inter.groupby('Name')[['Rating']].max()
    
    # sorts the ratings in descending order and selects the top 10 names with the highest ratings. 
    sol=ser.sort_values(by='Rating',ascending=False).head(10)
    
    # displays the sol DataFrame in the user interface
    st.write(sol,use_container_width=True)
