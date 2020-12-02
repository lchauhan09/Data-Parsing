#imported libraries
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


count = 100
#Webpage variable, changing for every 100 entries.
offset = [0,100,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400]
#Initialized empty arrays to store data
list_rows = []
list_heads = []

#Loop to parse multiple webpage, for data
for offset_url in offset:
	r = requests.get('https://ca.finance.yahoo.com/mutualfunds?offset=' + str(offset_url) + '&count=' + str(count))
	soup = BeautifulSoup(r.text, 'html.parser')

	#Loop to select tables on each webpage	
	for row in soup.select('table tbody'):
		rows = row.find_all('tr')	#Find all tr tags
		#Loop to find data of the rows
		for row in rows:
			row_td = row.find_all('td')	#Find all td tags
			str_row = str(row_td)		#Convert the raw data in string datatype
			clean = re.compile('<.*?>')	#Find and match all tags (content between < and >)
			cleanrow = re.sub(clean, '',str_row)	#Delete all the useless data between the tags and store only the valuable data
			list_rows.append(cleanrow)	#Append the data
		df_row = pd.DataFrame(list_rows)	#Convert the data into pandas dataframe to process it further

#Request the URL again to get the headers
r = requests.get('https://ca.finance.yahoo.com/mutualfunds')
soup = BeautifulSoup(r.text, 'html.parser')
#Loopfor all the headers
for head in soup.select('table thead'):
	heads = head.find_all('tr')	#Find all tr tags
	for head in heads:
		head_th = head.find_all('th')	#Find all th tags to get the headers
		str_head = str(head_th)		#Convert the raw data to string datatype
		clean = re.compile('<.*?>')	#Find and match all tags (content between < and >)
		cleanhead = (re.sub(clean, '',str_head))	#Delete all the useless data between the tags and store only the valuable data
		list_heads.append(cleanhead)	#Append the headers
	df_head = pd.DataFrame(list_heads)	#Convert the data to pandas dataframe to process it further

df1 = df_row[0].str.split(',', expand=True)	#Split the rows and make columns at each ','
df2 = df_head[0].str.split(',', expand=True)
frames = [df2,df1]		#Merged the two lists, df1 and df2
df_merged = pd.concat(frames)	#Converted the list in dataframe
df_merged[0] = df_merged[0].str.strip('[')	#Removed useless character '[' from the first column
df_merged = df_merged.drop([9,10,11,12,13], axis=1)	#Removed useless columns 9 till 13
df_merged = df_merged.rename(columns=df_merged.iloc[0])	#Replaced the column indices with the column names
df_merged = df_merged.drop(df_merged.index[0])		#Dropped the indices column for rows
df_merged.to_csv('Data.csv', index=False)		#Converted the dataframe to .csv format and made a file
print ('Done')		#Printed a message to show that everything was done successfully without error
