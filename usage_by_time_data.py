import re
import pandas as pd
from datetime import datetime


def extract_day_time(hour_str):
    day, *time_range = hour_str.split(" ")

    start = datetime.strptime((' '.join(time_range[0:2])), '%I %p').strftime('%H:%M')
    end = datetime.strptime((' '.join(time_range[3:])), '%I %p').strftime('%H:%M')
    
    return day, f"{start} - {end}"

def prepared_data_usage_by_time(ctype, time_frame, file_dfs, prefixes):
    combined_df = pd.concat([df for file_name in file_dfs.keys() for df in file_dfs[file_name]['Usage by time']], ignore_index=True)

    if ctype == 'heatmap':

        combined_df['Day'], combined_df['Time'] = zip(*combined_df['Hour'].apply(extract_day_time))

        agg_df = combined_df.groupby(['Day', 'Time']).sum().reset_index()

        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        agg_df['Day'] = pd.Categorical(agg_df['Day'], categories=weekday_order, ordered=True)
        heatmap_data = []
        for day, group in agg_df.groupby('Day'):
            if time_frame == 7:

                heatmap_data.append({
                    "id": day,
                    "data": [{"x": row['Time'], "y": row['7 days average unique viewers']} for _, row in group.iterrows()]
                })
            elif time_frame == 30:
                heatmap_data.append({
                "id": day,
                "data": [{"x": row['Time'], "y": row['30 days average unique viewers']} for _, row in group.iterrows()]
            })
            elif time_frame == 90:
                heatmap_data.append({
                "id": day,
                "data": [{"x": row['Time'], "y": row['90 days average unique viewers']} for _, row in group.iterrows()]
            })

        return heatmap_data
    
    
    return 0