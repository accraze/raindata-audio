import pandas as pd
from dateutil import parser, rrule
import calmap
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns
import calendar
import numpy as np

data_raw = pd.read_csv('outfile.txt', sep="    ",
                   header=None,
                   names=["date", "total_rain", "hourly"])

# Give the variables some friendlier names and convert types as necessary.

data_raw['total_rain'] = data_raw['total_rain'].astype(float)
data_raw['date'] = data_raw['date'].apply(parser.parse)

# Extract out only the data we need.
data = data_raw.loc[:, ['date', 'total_rain']]
data = data[(data['date'] >= datetime(2016,1,1)) & (data['date'] <= datetime(2016,12,31))]
print(data)


# Assign the "day" to every date entry
data['day'] = data['date'].apply(lambda x: x.date())

data['day_of_week'] = data['date'].apply(lambda x: x.weekday())
data['month'] = data['date'].apply(lambda x: x.month)
data['month_name'] = data['month'].apply(lambda x: calendar.month_abbr[x])

# If there's any rain at all, mark that!
data['raining'] = data['total_rain'] > 0.0


# Get aggregate stats for each day in the dataset on rain in general - for heatmaps.
rainy_days = data.groupby(['day']).agg({
        "total_rain": {"total_rain": "max"}
        })

# clean up the aggregated data to a more easily analysed set:
rainy_days.reset_index(drop=False, inplace=True) # remove the 'day' as the index
rainy_days.rename(columns={"":"date"}, inplace=True) # The old index column didn't have a name - add "date" as name
rainy_days.columns = rainy_days.columns.droplevel(level=0) # The aggregation left us with a multi-index
                                                           # Remove the top level of this index.
rainy_days['raining'] = rainy_days['total_rain'].astype(bool)  
# Change the "rain" column to True/False values

rainy_days['month'] = rainy_days['date'].apply(lambda x: x.month)
rainy_days['month_name'] = rainy_days['month'].apply(lambda x: calendar.month_abbr[x])
#rainy_days['day'] = rainy_days['date'].apply(lambda x: x.date())

# Add the number of rainy hours per day this to the rainy_days dataset.
temp = data.groupby(["day"])['raining'].any()
temp = temp.groupby(level=[0]).sum().reset_index()
temp.rename(columns={'raining': 'hours_raining'}, inplace=True)
temp['day'] = temp['day']
rainy_days = rainy_days.merge(temp, left_on='date', right_on='day', how='left')
rainy_days.drop('day', axis=1, inplace=True)

temp = rainy_days.copy().set_index(pd.DatetimeIndex(rainy_days['date']))
#temp.set_index('date', inplace=True)
temp.fillna(value=np.nan, inplace=True)
fig, ax = calmap.calendarplot(temp['hours_raining'].astype(int), fig_kws={"figsize":(15,4)})
plt.title("Days with Rain")
fig, ax = calmap.calendarplot(temp['total_rain'], fig_kws={"figsize":(15,4)})
plt.title("Total Rainfall Daily")

plt.show()

