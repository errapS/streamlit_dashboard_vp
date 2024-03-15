import re
import pandas as pd
from pprint import pprint


def prepared_data_popular_content(ctype, file_dfs, prefixes):
    combined_df = pd.concat([df for file_name in file_dfs.keys() for df in file_dfs[file_name]['Popular content']], ignore_index=True)

    if ctype == 'line':
        pass

    elif ctype == 'pie':
        pass

    elif ctype == 'info':
        filtered_df = combined_df[combined_df['Prefix'].isin(prefixes)]
       
        name = '-'.join(prefixes)
        cols = [
            {"field": "content", "headerName": name, "flex": 1},
            {"field": "prefix", "headerName": "Prefix", "flex": 1},
            {"field": "source", "headerName": "Source", "flex": 1},
            {"field": "unique_viewers", "headerName": "Unique viewers", "flex": 1},
            {"field": "visits", "headerName": "Visits", "flex": 1}
        ]
        
        rows = []
        for i, row in filtered_df.iterrows():
            rows.append({
                "id": i,
                "content": row['Content'],
                "prefix": row['Prefix'],
                "source": row['Source'],
                "unique_viewers": row['Last 7 days unique viewers'],
                "visits": row['Last 7 days visits'],
            })
        
        return cols, rows
        
    elif ctype == 'bar':
        pass

    return