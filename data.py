import pandas as pd


csv_file = r'/Users/mingfondberg/kunskapskontroll2/stockholmslän.csv'


data = pd.read_csv(csv_file)


print(data.head())

# Skriv ut information om kolumnerna och datatyperna
print(data.info())
sorted_data = data.sort_values(by='Pris', ascending=False)
print(sorted_data.head())
data['Period'] = pd.to_datetime(data['Period'])
print(data.info())  
filtered_data = data[data['Pris'] > 37000]
print(filtered_data.head())
print(data.describe())  



data['Period'] = pd.to_datetime(data['Period'])

print(data.head())
filtered_data.to_csv('filtered_data.csv', index=False)



