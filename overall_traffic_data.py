import re
import pandas as pd

def prepared_data_overall_traffic(ctype, file_dfs, prefixes):
    combined_df = pd.concat([df for file_name in file_dfs.keys() for df in file_dfs[file_name]['Overall traffic']], ignore_index=True)

    if ctype == 'line':
        sp_df = combined_df.groupby(['Date', 'Source', 'Prefix']).sum().reset_index()
        sp_df['Source_Prefix'] = sp_df['Source'] + "_" + sp_df['Prefix']
        sp_df['Date'] = sp_df['Date'].dt.strftime('%Y-%m-%d')

        grouped_data = sp_df.groupby(['Source_Prefix', 'Date']).sum().reset_index()

        final_list = []
        for group_name, group_data in grouped_data.groupby('Source_Prefix'):
            data_list = []
            for _, row in group_data.iterrows():
                data_list.append({"x": str(row['Date']), "y": row['Site visits']})
            final_list.append({"id": group_name + '_SV', "data": data_list})
        
        for group_name, group_data in grouped_data.groupby('Source_Prefix'):
            data_list = []
            for _, row in group_data.iterrows():
                data_list.append({"x": str(row['Date']), "y": row['Unique viewers']})
            final_list.append({"id": group_name + '_UV', "data": data_list})

        return final_list

    elif ctype == 'pie':
        filtered_df = combined_df[combined_df['Prefix'].isin(prefixes)]

        filtered_df['Source_Prefix'] = filtered_df['Source'] + "_" + filtered_df['Prefix']

        grouped_df = filtered_df.groupby('Source_Prefix').agg({'Site visits': 'sum', 'Unique viewers': 'sum'})
        result = []

        for index, row in grouped_df.iterrows():
            result.append({
                "id": index + '_SV',
                "label": "Site visits",
                "value": row['Site visits']
            })
            result.append({
                "id": index + '_UV',
                "label": "Unique viewers",
                "value": row['Unique viewers']
            })

        return result

    elif ctype == 'info':
        prefix_df = combined_df[combined_df['Prefix'].isin(prefixes)]
        summary_keys = ['Average Unique viewers',
            'Max Unique viewers',
            'Min Unique viewers',
            'Total Unique viewers',
            'Average Site visits',
            'Max Site visits',
            'Min Site visits',
            'Total Site visits'
        ]

        name = '-'.join(prefixes)   # TODO - update with the period?

        summaries = {}
        rows = []
        cols = [{"field": "type", "headerName": name, "flex": 1}]

        if len(prefixes) > 1:
            prefix_df['Source_Prefix'] = prefix_df['Source'] + "_" + prefix_df['Prefix']

            for source in prefix_df['Source_Prefix'].unique():
                cols.append({"field": source, "headerName": source, "flex": 1})
                
                filtered_df = prefix_df[prefix_df['Source_Prefix'] == source]

                summaries[source] = {
                    "Average Unique viewers": round(filtered_df['Unique viewers'].mean(), 2),
                    "Max Unique viewers": filtered_df['Unique viewers'].max(),
                    "Min Unique viewers": filtered_df['Unique viewers'].min(),
                    "Total Unique viewers": filtered_df['Unique viewers'].sum(),
                    "Average Site visits": round(filtered_df['Site visits'].mean(), 2),
                    "Max Site visits": filtered_df['Site visits'].max(),
                    "Min Site visits": filtered_df['Site visits'].min(),
                    "Total Site visits": filtered_df['Site visits'].sum()
                }

            for i, key in enumerate(summary_keys):
                row = {"id": i, "type": key}
                for source in prefix_df['Source_Prefix'].unique():
                    row[source] = summaries[source][key]
                rows.append(row)

            return cols, rows
            
        else:
            for source in prefix_df['Source'].unique():
                cols.append({"field": source, "headerName": source, "flex": 1})
                
                filtered_df = prefix_df[prefix_df['Source'] == source]

                summaries[source] = {
                    "Average Unique viewers": round(filtered_df['Unique viewers'].mean(), 2),
                    "Max Unique viewers": filtered_df['Unique viewers'].max(),
                    "Min Unique viewers": filtered_df['Unique viewers'].min(),
                    "Average Site visits": round(filtered_df['Site visits'].mean(), 2),
                    "Max Site visits": filtered_df['Site visits'].max(),
                    "Min Site visits": filtered_df['Site visits'].min(),
                }

            for i, key in enumerate(summary_keys):
                row = {"id": i, "type": key}
                for source in combined_df['Source'].unique():
                    row[source] = summaries[source][key]
                rows.append(row)

            return cols, rows
        
    elif ctype == 'bar':
        combined_df['Source_Prefix'] = combined_df['Source'] + "_" + combined_df['Prefix']
        grouped_data = combined_df.groupby('Source_Prefix').agg({'Site visits': 'sum', 'Unique viewers': 'sum'})

        result = []

        for index, row in grouped_data.iterrows():
            data_entry = {
                "Source_prefix": index,
                "Site visits": row['Site visits'],
                "Unique viewers": row['Unique viewers']
            }
            result.append(data_entry)
        
        return result

    return