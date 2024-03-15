import re
import pandas as pd
from pprint import pprint


def prepared_data_usage_by_device(ctype, file_dfs, prefixes):
    combined_df = pd.concat([df for file_name in file_dfs.keys() for df in file_dfs[file_name]['Usage by device']], ignore_index=True)

    if ctype == 'line':
        pass

    elif ctype == 'pie':
        pass

    elif ctype == 'info':
        pass
        
    elif ctype == 'bar':
        combined_df['Source_Prefix'] = combined_df['Source'] + "_" + combined_df['Prefix']
        result = []
        summary_df = combined_df.groupby('Source_Prefix').agg({
            'Desktop visits': 'sum',
            'Mobile app visits': 'sum',
            'Mobile web visits': 'sum',
            'Tablet visits': 'sum',
            'Other device visits': 'sum'
        }).reset_index()

        keys = summary_df['Source_Prefix'].unique()
        
        # transposed_df = summary_df.T
        grouped_df = summary_df.melt(id_vars='Source_Prefix', var_name='Type', value_name='Value')
        grouped_df = grouped_df.groupby('Type').apply(lambda x: x.set_index('Source_Prefix')['Value'].to_dict()).reset_index()

        for index, row in grouped_df.iterrows():
            visit_type = row['Type']
         
            for prefix, value in row.drop('Type').to_dict().items():
                r = {"Type": visit_type}
                for k, v in value.items():
                    r[k] = v
                result.append(r)
                
        return result, keys

    elif ctype == 'radar':
        combined_df['Source_Prefix'] = combined_df['Source'] + "_" + combined_df['Prefix']
        result = []
        summary_df = combined_df.groupby('Source_Prefix').agg({
            'Desktop visits': 'sum',
            'Mobile app visits': 'sum',
            'Mobile web visits': 'sum',
            'Tablet visits': 'sum',
            'Other device visits': 'sum'
        }).reset_index()

        fields = ['Desktop visits',
            'Mobile app visits',
            'Mobile web visits',
            'Tablet visits',
            'Other device visits']
        
        for field in fields:
            entry = {'visits': field}
            for _, row in summary_df.iterrows():
                entry[row['Source_Prefix']] = row[field]
            result.append(entry)

        return result, combined_df['Source_Prefix'].unique()
    return