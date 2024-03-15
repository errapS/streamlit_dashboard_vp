import streamlit as st
from streamlit_elements import elements, mui, dashboard
from streamlit_float import *
from helpers import *
import json


def main():

    st.title('Excel Data Visualization')

    excel_files = st.file_uploader("Upload Excel", type=['xlsx'], accept_multiple_files=True)
    files = [file.name for file in excel_files]
    
    st.sidebar.header("Choose your filter: ")
   
    file_dfs, prefixes, sources = read_excel_files(excel_files)
    
    sheet_to_component = {
            'Overall traffic': ['Linechart - Overall traffic', 'Barchart - Overall traffic',
                                'Info - Overall traffic']
                                   + [f'Piechart - Overall traffic ({p})' for p in prefixes]
                                   + [f'Info - Overall traffic ({p})' for p in prefixes],
            'Popular content': ['Info - Popular content'] + [f'Info - Popular content ({p})' for p in prefixes],
            'Usage by device': ['Radar - Usage by device', 'Barchart - Usage by device', 'Barchart - Usage by device (H)'],
            'Usage by time': ['Heatmap - Usage by time 7', 'Heatmap - Usage by time 30', 'Heatmap - Usage by time 90']
        }
    
    if 'selected_components' not in st.session_state:
        st.session_state.selected_components = {'overall_traffic': [],
                                                'popular_content': [],
                                                'usage_by_device': [],
                                                'usage_by_time': [],
                                                'text_components': []}
    
    if 'last_selected_components' not in st.session_state:
        st.session_state.last_selected_components = {'overall_traffic': [],
                                                'popular_content': [],
                                                'usage_by_device': [],
                                                'usage_by_time': [],
                                                'text_components': []}

    if 'new_components' not in st.session_state:
        st.session_state.new_components = {}

    if 'imported_layout' not in st.session_state:
        st.session_state.imported_layout = False

    if 'required_files' not in st.session_state:
        st.session_state.required_files = []

    # if 'selected_components' not in st.session_state:
    #     st.session_state.selected_components = {}
    
    if 'rendered_components' not in st.session_state:
        st.session_state.rendered_components = []
    
    if 'session_layout' not in st.session_state:
        st.session_state.session_layout = {}
    
    if 'last_session_layout' not in st.session_state:
        st.session_state.last_session_layout = {}

    if 'layout' not in st.session_state:
        st.session_state.layout = []


    st.session_state.selected_components['overall_traffic'] = st.sidebar.multiselect("Overall traffic", default=st.session_state.selected_components['overall_traffic'], options=sheet_to_component["Overall traffic"])

    st.session_state.selected_components['popular_content'] = st.sidebar.multiselect("Popular content", default=st.session_state.selected_components['popular_content'], options=sheet_to_component["Popular content"])

    st.session_state.selected_components['usage_by_device'] = st.sidebar.multiselect("Usage by device", default=st.session_state.selected_components['usage_by_device'], options=sheet_to_component["Usage by device"])
    
    st.session_state.selected_components['usage_by_time'] = st.sidebar.multiselect("Usage by time", default=st.session_state.selected_components['usage_by_time'], options=sheet_to_component["Usage by time"])

    st.session_state.selected_components['text_components'] = st.sidebar.multiselect("Text components", default=st.session_state.selected_components['text_components'], options=st.session_state.new_components.keys())

    if any(st.session_state.selected_components[key] != st.session_state.last_selected_components.get(key) for key in st.session_state.selected_components.keys()):
            st.session_state.last_selected_components = st.session_state.selected_components
            st.experimental_rerun()()


    float_init()

    if "show" not in st.session_state:
        st.session_state.show = (False, None)

    dialog_container = float_dialog(st.session_state.show[0], background="white")

    with dialog_container:
        _, component = st.session_state.show

        if component == 'edit':
            comp = st.selectbox("Enter name of component", key="name", options=st.session_state.new_components.keys())
            if comp:
                new_text = st.text_area("Enter text", key="text", value=st.session_state.new_components[comp])

            # b1, _, b2= st.columns([0.1,0.81,0.09])

            # with b1:
            if st.button('Cancel', key='cancel'):
                st.session_state.show = (False, None)
                st.experimental_rerun()()
            # with b2:
            if st.button("Save", key="save"):
                st.session_state.new_components[comp] = new_text
                st.session_state.show = (False, None)
                st.experimental_rerun()()
        else:
            st.header("Add text")
            name_input = st.text_input("Enter name of component", key="name")
            text_input = st.text_area("Enter text", key="text")

            # b1, _, b2= st.columns([0.1,0.81,0.09])

            # with b1:
            if st.button('Cancel', key='cancel'):
                st.session_state.show = (False, None)
                st.experimental_rerun()()
            # with b2:
            if st.button("Send", key="send"):
                st.session_state.new_components[component + name_input] = text_input
                st.session_state.show = (False, None)
                st.experimental_rerun()()

    col1, col2, col3, col4 = st.sidebar.columns([1,1,1,1])  

    with col1:
        if st.button("H"):
            st.session_state.show = (True, 'H_')
            st.experimental_rerun()()

    with col2:
        if st.button("S"):
            st.session_state.show = (True, 'S_')
            st.experimental_rerun()()

    with col3:
        if st.button("P"):
            st.session_state.show = (True, 'P_')
            st.experimental_rerun()()

    with col4:
        if st.button("🔧"):
            st.session_state.show = (True, 'edit')
            st.experimental_rerun()()

    st.sidebar.download_button('Export layout', export_layout(st.session_state.last_session_layout), file_name='layout.json')
    
    if not st.session_state.imported_layout:
        file = st.sidebar.file_uploader('Import layout')
        if file:
            content = file.getvalue()
            imported_layout = json.loads(content.decode('utf-8'))
            st.session_state.selected_components = imported_layout['selected_components']
            st.session_state.rendered_components = imported_layout['rendered_components']
            st.session_state.layout = imported_layout['layout']
            st.session_state.required_files = imported_layout['files']
            st.session_state.imported_layout = True
            st.session_state.new_components = imported_layout['custom_components']

    rendered_components =  st.session_state.rendered_components
    selected_components = []
    for v in st.session_state.selected_components.values():
        if v:
            selected_components.extend(v)

    missing_files = [file for file in st.session_state.required_files if file not in files]
    msg = f"Missing files: {', '.join(missing_files)}"
    if missing_files:
        st.warning(msg)

    def handle_layout_change(updated_layout):
        for i, component in enumerate(updated_layout):
            if component["w"] == 1 and component["h"] == 1:
                updated_layout[i]["w"] = 4 
                updated_layout[i]["h"] = 2 

        st.session_state.layout = updated_layout

    with elements("dashboard"):
        with dashboard.Grid(st.session_state.layout, onLayoutChange=handle_layout_change):
            for component_type in selected_components:
                rendered_components.append(component_type)

                if component_type.startswith(('H_', 'S_', 'P_')):
                    with mui.Box(sx={"height": 100, "display": "flex", "justifyContent": "flex-start", "alignItems": "flex-end"}, key=component_type):
                        generate_text_component(component_type, metadata=st.session_state.new_components)
                else:
                    with mui.Box(sx={"height": 200}, key=component_type):
                        component = (re.search(r'(.*?)\s', component_type).group(1), re.search(r'-\s(.*)$', component_type).group(1))
                        generate_component(component, file_dfs, prefixes, sources)

        st.session_state.session_layout = {'files': files, 'selected_components': st.session_state.selected_components, 'rendered_components': rendered_components, 'custom_components': st.session_state.new_components, 'layout': st.session_state.layout}
        if any(st.session_state.session_layout[key] != st.session_state.last_session_layout.get(key) for key in st.session_state.session_layout.keys()):
            st.session_state.last_session_layout = st.session_state.session_layout
            st.experimental_rerun()()

if __name__ == "__main__":
    st.set_page_config(
        page_title="PAUL",
        page_icon="💡",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    main()
