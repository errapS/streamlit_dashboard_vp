
line_chart_OT = {
    "margin": {"top": 50, "right": 100, "bottom": 50, "left": 100},
    "xScale": {"type": "time", "format": "%Y-%m-%d"},
    "xFormat": {"time": "%Y-%m-%d"},
    "yScale": {"type": "linear", "min": "auto", "max": "auto", "stacked": False, "reverse": False},
    "curve": "monotoneX",
    "enablePointLabel": False,
    "useMesh": True,
    "legends": [
        {
            "anchor": "top",
            "direction": "row",
            "justify": False,
            "translateX": 0,
            "translateY": -30,
            "itemsSpacing": 40,
            "itemDirection": "left-to-right",
            "itemWidth": 100,
            "itemHeight": 20,
            "itemOpacity": 0.75,
            "symbolSize": 12,
            "symbolShape": "circle",
            "symbolBorderColor": "rgba(0, 0, 0, .5)",
            "effects": [
                {
                    "on": "hover",
                    "style": {
                        "itemTextColor": "#000"
                    }
                }
            ]
        }
    ],
    "axisBottom": {
        "format": "%b %d",
        "tickValues": "every 20 days",
        "legend": "Date",
        "legendPosition": "middle",
        "legendOffset": 30
    },
    "axisLeft": {
        "orient": "left",
        "legend": "Site visits / unique viewers",
        "legendOffset": -40,
        "legendPosition": "middle"
    },
    "enableSlices": "x",
    "enableTouchCrosshair": True,
    "enableArea": True,
    "fill": [{"id": 'gradientA', "match": '*'}],
    # "colors": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]
}


datagrid_style = {
    "pageSize": 6,
    "rowsPerPageOptions": [6],
    "checkboxSelection": False,
    "disableSelectionOnClick": True,
    "density": "comfortable",
    # "style": {
    #     "fontSize": "16px", 
    #     "fontWeight": "bold",
    # }
}

pie_chart_OT = {
    "margin": {"top": 50, "right": 100, "bottom": 50, "left": 100},
    "innerRadius": 0.5,
    "padAngle": 0.7,
    "cornerRadius": 3,
    "activeOuterRadiusOffset": 8,
    "borderWidth": 1,
    "borderColor": {"from": "color", "modifiers": [["darker", 0.2]]},
    "arcLinkLabelsSkipAngle": 10,
    "arcLinkLabelsTextColor": "#333333",
    "arcLinkLabelsThickness": 2,
    "arcLinkLabelsColor": {"from": "color"},
    "arcLabelsSkipAngle": 10,
    "arcLabelsTextColor": {"from": "color", "modifiers": [["darker", 2]]},
    "defs": [
        {
            "id": "dots",
            "type": "patternDots",
            "background": "inherit",
            "color": "rgba(255, 255, 255, 0.3)",
            "size": 4,
            "padding": 1,
            "stagger": True
        },
        {
            "id": "lines",
            "type": "patternLines",
            "background": "inherit",
            "color": "rgba(255, 255, 255, 0.3)",
            "rotation": -45,
            "lineWidth": 6,
            "spacing": 10
        }
    ]
}

bar_chart_OT = {
    "keys": ['Site visits', 'Unique viewers'],
    "indexBy": "Source_prefix",
    "margin": {"top": 50, "right": 50, "bottom": 50, "left": 50},
    "padding": 0.3,
    "valueScale": {"type": "linear"},
    "indexScale": {"type": "band", "round": True},
    "colors": {"scheme": "nivo"},
}

radar_UBD = {
    "margin": { "top": 50, "right": 80, "bottom": 40, "left": 80 },
}

bar_chart_UBD = {
    "indexBy": "Type",
    "margin": {"top": 50, "right": 150, "bottom": 50, "left": 50},
    "padding": 0.3,
    "valueScale": {"type": "linear"},
    "indexScale": {"type": "band", "round": True},
    "colors": {"scheme": "nivo"},
    "legends":[
            {
                "dataFrom": 'keys',
                "anchor": 'bottom-right',
                "direction": 'column',
                "justify": False,
                "translateX": 120,
                "translateY": 0,
                "itemsSpacing": 2,
                "itemWidth": 100,
                "itemHeight": 20,
                "itemDirection": 'left-to-right',
                "itemOpacity": 0.85,
                "symbolSize": 20
            }
        ]
    
}

bar_chart_UBD_H = {
    "indexBy": "Type",
    "margin": {"top": 50, "right": 150, "bottom": 50, "left": 150},
    "padding": 0.3,
    "layout":"horizontal",
    "valueScale": {"type": "linear"},
    "indexScale": {"type": "band", "round": True},
    "colors": {"scheme": "nivo"},
    "legends":[
            {
                "dataFrom": 'keys',
                "anchor": 'bottom-right',
                "direction": 'column',
                "justify": False,
                "translateX": 120,
                "translateY": 0,
                "itemsSpacing": 2,
                "itemWidth": 100,
                "itemHeight": 20,
                "itemDirection": 'left-to-right',
                "itemOpacity": 0.85,
                "symbolSize": 20
            }
        ]
}

heatmap_UAT = {
        "margin" : {"top": 50, "right": 90, "bottom": 50, "left": 90 },
        "axisTop": False,
        # {   
        #     # "tickSize": 5,
        #     # "tickPadding": 5,
        #     # "tickRotation": -90,
        #     # "legend": '',
        #     # "legendOffset": 46,
        #     # "truncateTickAt": 0
        # },
        "axisLeft":{
            "tickSize": 5,
            "tickPadding": 5,
            "tickRotation": 0,
            # "legend": 'day',
            # "legendPosition": 'middle',
            # "legendOffset": -80,
            "truncateTickAt": 3
        },
        "colors":{
            "type": 'diverging',
            "scheme": 'red_yellow_blue',
            "divergeAt": 0,
            "minValue": 0,
            "maxValue": 5
        },
        "emptyColor": "#F1F2FF"
        # legends={[
        #     {
        #         anchor: 'bottom',
        #         translateX: 0,
        #         translateY: 30,
        #         length: 400,
        #         thickness: 8,
        #         direction: 'row',
        #         tickPosition: 'after',
        #         tickSize: 3,
        #         tickSpacing: 4,
        #         tickOverlap: false,
        #         tickFormat: '>-.2s',
        #         title: 'Value →',
        #         titleAlign: 'start',
        #         titleOffset: 4
        #     }
        # ]}
}