import re, json
import pandas as pd
from streamlit_elements import nivo, mui
from pprint import pprint
from chart_styles import *
from overall_traffic_data import prepared_data_overall_traffic
from popular_content_data import prepared_data_popular_content
from usage_by_device_data import prepared_data_usage_by_device
from usage_by_time_data import prepared_data_usage_by_time


def read_excel_files(excel_files):
    file_names = [file.name for file in excel_files]

    sheets =['Overall traffic',
           'Popular content',
           'Usage by device',
           'Usage by time']

    file_dfs = {file_name: {sheet: [] for sheet in sheets} for file_name in file_names}
    prefixes = set()
    sources = set()

    skip_rows_dict = {
            'Overall traffic': 15,
            'Popular content': 5,
            'Usage by device': 5,
            'Usage by time': 6
        }
    
    for excel_file, file_name in zip(excel_files, file_names):
        date_range = pd.read_excel(excel_file, sheet_name='Overall traffic', skiprows=12)
        null_index = date_range.index[date_range.isnull().all(axis=1)]

        if not null_index.empty:
            date_range = date_range.iloc[:null_index[0]]

        match = re.findall(r'(\d{1,2}-[A-Za-z]{3},\d{4})', date_range.iloc[0][0])
        start_date = pd.to_datetime(match[0].replace(',', '-'), format='%d-%b-%Y') + pd.offsets.MonthEnd(1)
        end_date = pd.to_datetime(match[1].replace(',', '-'), format='%d-%b-%Y')

        prefix = file_name[:4]
        source = re.search(r'\s(.*?)_', file_name)
        prefixes.add(prefix)
        sources.add(source.group(1))

        for sheet, skip_rows in skip_rows_dict.items():
            df = pd.read_excel(excel_file, sheet_name=sheet, skiprows=skip_rows)
            null_index = df.index[df.isnull().all(axis=1)]

            if not null_index.empty:
                df = df.iloc[:null_index[0]]

            df['Prefix'] = prefix
            df['Source'] = source.group(1)
            df['Period'] = start_date.strftime('%m%y') + '-' + end_date.strftime('%m%y')

            file_dfs[file_name][sheet].append(df)

    return file_dfs, prefixes, sources


def generate_text_component(component_type, metadata):
    if component_type.startswith('P_'):
        return mui.Typography(metadata[component_type], paragraph=True)
    
    elif component_type.startswith('H_'): 
        return mui.Typography(children=metadata[component_type], variant="h2", paragraph=False)
    
    elif component_type.startswith('S_'):
        return mui.Typography(children=metadata[component_type], variant="h3", paragraph=False)


def generate_component(component, file_dfs, prefixes, sources):
    component_type, version = component

    if component_type == 'Linechart':
        if version == 'Overall traffic': 
            data = prepared_data_overall_traffic('line', file_dfs, prefixes)

            return nivo.Line(data=data, **line_chart_OT)

    elif component_type == 'Info':
        match = re.search(r'\s\((.*?)\)$', version)
        if match:
            prefix = [match.group(1)]
        else:
            prefix = prefixes

        if version.startswith('Overall traffic'): 
            cols, rows = prepared_data_overall_traffic('info', file_dfs, prefix)

            return mui.DataGrid(
                        columns=cols,
                        rows=rows,
                        **datagrid_style,
                    )
        
        if version.startswith('Popular content'): 
            cols, rows = prepared_data_popular_content('info', file_dfs, prefix)

            return mui.DataGrid(
                        columns=cols,
                        rows=rows,
                        **datagrid_style,
                    )

    elif component_type == 'Piechart':
        match = re.search(r'\s\((.*?)\)$', version)
        if match:
            prefix = [match.group(1)]
        else:
            prefix = prefixes

        if version.startswith('Overall traffic'): 
            data = prepared_data_overall_traffic('pie', file_dfs, prefix)

            return nivo.Pie(data=data, **pie_chart_OT)

    elif component_type == 'Barchart':
        if version == 'Overall traffic': 
            data = prepared_data_overall_traffic('bar', file_dfs, prefixes)

            return nivo.Bar(data=data, **bar_chart_OT)

        elif version == 'Popular content': 
            data = prepared_data_popular_content('bar', file_dfs, prefixes)

            return nivo.Bar(data=data, **bar_chart_OT)
        
        elif version == 'Usage by device': 
            data, keys = prepared_data_usage_by_device('bar', file_dfs, prefixes)

            return nivo.Bar(data=data, keys=keys, **bar_chart_UBD)
        
        elif version == 'Usage by device (H)': 
            data, keys = prepared_data_usage_by_device('bar', file_dfs, prefixes)

            return nivo.Bar(data=data, keys=keys, **bar_chart_UBD_H)

    elif component_type == 'Radar':
        if version == 'Usage by device':
            data, keys = prepared_data_usage_by_device('radar', file_dfs, prefixes)

            return nivo.Radar(data=data,keys=keys,indexBy="visits", **radar_UBD)
        
    elif component_type == 'Heatmap':
        if version == 'Usage by time 7':
            data = prepared_data_usage_by_time('heatmap', 7, file_dfs, prefixes)
            
            return nivo.HeatMap(data=data, **heatmap_UAT)
        
        elif version == 'Usage by time 30':
            data = prepared_data_usage_by_time('heatmap', 30, file_dfs, prefixes)
            
            return nivo.HeatMap(data=data, **heatmap_UAT)
        
        elif version == 'Usage by time 90':
            data = prepared_data_usage_by_time('heatmap', 90, file_dfs, prefixes)
            
            return nivo.HeatMap(data=data, **heatmap_UAT)
        
    else:
        return None
    

def export_layout(session_layout):
    return json.dumps(session_layout, indent=4)
