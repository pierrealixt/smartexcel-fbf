FBF_DEFINITION = [
    {
        'type': 'format',
        'key': 'table_header',
        'format': {
            'bold': True,
            'font_size': 14,
            'align': 'center',
            'valign': 'vcenter',
            'font_color': 'white',
            'border': 1,
            'bg_color': '#2F87A6',
            'border_color': 'black'
        }
    },
    {
        'type': 'format',
        'key': 'map_keys',
        'format': {
            'bold': True,
            'font_size': 12
        }
    },
    {
        'type': 'format',
        'key': 'map_values',
        'format': {
            'font_size': 12
        }
    },
    {
        'type': 'format',
        'key': 'sheet_title',
        'format': {
            'align': 'center',
            'valign': 'vcenter',
            'bold': True,
            'font_size': 18,
            'font_color': 'white',
            'border': 1,
            'bg_color': '#2F87A6',
            'border_color': 'black'
        }
    },
    {
        'type': 'format',
        'key': 'sheet_sub_title',
        'format': {
            'align': 'center',
            'valign': 'vcenter',
            'bold': True,
            'font_size': 16,
            'font_color': 'white',
            'border': 1,
            'bg_color': '#2F87A6',
            'border_color': 'black'
        }
    },
    {
        'type': 'format',
        'key': 'number',
        'format': {
        },
        'num_format': '0'
    },
    {
        'type': 'format',
        'key': 'bold',
        'format': {
            'bold': True
        }
    },
    {
        'type': 'sheet',
        'settings': {
            'set_paper': 8,
            'center_horizontally': None
        },
        'name': {
            'func': 'flood_summary'
        },
        'components': [
            {
                'type': 'text',
                'name': 'Sheet Title',
                'size': {
                    'width': 4,
                    'height': 2
                },
                'text_func': 'main_sheet_title',
                'format': 'sheet_title'
            },
            {
                'type': 'image',
                'name': 'FbA logo',
                'key': 'fba_logo',
                'position': {
                    'x': 0,
                    'y': 0,
                    'float': True
                },
                'size': {
                    'width': 140,
                    'height': 40
                },
            },
            {
                'type': 'image',
                'name': 'Partner logos',
                'key': 'partner_logos',
                'size': {
                    'width': 700,
                    'height': 110
                },
            },
            {
                'name': 'Flood metadata',
                'type': 'map',
                'position': {
                    'margin': {
                        'left': 1
                    },
                    'middle': 1
                },
                'payload': 'flood',
                'format': {
                    'map_key': 'map_keys',
                    'map_value': 'map_values'
                },
                'rows': [
                    {
                        'name': 'Acquisition Date',
                        'key': 'flood_acquisition_date',
                    },
                    {
                        'name': 'Forecast Date',
                        'key': 'flood_forecast_date',
                    },
                    {
                        'name': 'Source',
                        'key': 'flood_source',
                    },
                    {
                        'name': 'Notes',
                        'key': 'flood_notes',
                    },
                    {
                        'name': 'Link',
                        'key': 'flood_link',
                    },
                    {
                        'name': 'Trigger Status',
                        'key': 'flood_trigger_status',
                        'format_func': 'trigger_status'
                    }
                ]
            },
            {
                'type': 'text',
                'name': 'Overview Map',
                'size': {
                    'width': 4,
                    'height': 1
                },
                'text_func': 'main_sheet_sub_title',
                'format': 'sheet_sub_title'
            },
            {
                'type': 'image',
                'name': 'Flood summary Map',
                'key': 'flood_summary_map',
                'size': {
                    'width': 700,
                    'height': 400
                }
            },
            {
                'name': 'Flood Summary View',
                'type': 'table',
                'payload': 'districts',
                'format': {
                    'header': 'table_header'
                },
                'columns': [
                    {
                        'name': 'District Name',
                        'key': 'district_name',
                        'width': 20,
                        'format': 'bold'
                    },
                    {
                        'name': 'Total Buildings',
                        'key': 'total_buildings',
                        'width': 20,
                        'format': 'number'
                    },
                    {
                        'name': 'Flooded Buildings',
                        'key': 'flooded_buildings',
                        'width': 25,
                        'format': 'number'
                    },
                    {
                        'name': 'Not Flooded Buildings',
                        'key': 'not_flooded_buildings',
                        'width': 30,
                        'format': 'number'
                    },
                ],
                'recursive': {
                    # create a sheet for each instance of payload
                    'name': {
                        'func': 'subdistrict_summary'
                    },
                    'foreign_key': 'district_code',
                    'payload_func': 'subdistricts',
                    'components': [
                        {
                            'type': 'text',
                            'name': 'District Sheet Title',
                            'size': {
                                'width': 4,
                                'height': 2
                            },
                            'text_func': 'district_sheet_title',
                            'format': 'sheet_title'
                        },
                        {
                            'type': 'image',
                            'name': 'District Flood summary Map',
                            'key': 'district_flood_summary_map',
                            'size': {
                                'width': 600,
                                'height': 400
                            }
                        },
                        {
                            'name': 'Sub-districts',
                            'type': 'table',
                            'columns': [
                                {
                                    'name': 'Sub-district Name',
                                    'key': 'sub_district_name',
                                    'width': 22,
                                    'format': 'bold'
                                },
                                {
                                    'name': 'Total Buildings',
                                    'key': 'total_buildings',
                                    'width': 20,
                                    'format': 'number'
                                },
                                {
                                    'name': 'Flooded Buildings',
                                    'key': 'flooded_buildings',
                                    'width': 25,
                                    'format': 'number'
                                },
                                {
                                    'name': 'Not Flooded Buildings',
                                    'key': 'not_flooded_buildings',
                                    'width': 30,
                                    'format': 'number'
                                },

                            ],
                            'recursive': {
                                'name': {
                                    'func': 'village_summary'
                                },
                                'foreign_key': 'sub_district_code',
                                'payload_func': 'villages',
                                'components': [
                                    {
                                        'type': 'text',
                                        'name': 'Sub-district Sheet Title',
                                        'size': {
                                            'width': 4,
                                            'height': 2
                                        },
                                        'text_func': 'sub_district_sheet_title',
                                        'format': 'sheet_title'
                                    },
                                    {
                                        'type': 'image',
                                        'name': 'Sub-district Flood summary Map',
                                        'key': 'sub_district_flood_summary_map',
                                        'size': {
                                            'width': 600,
                                            'height': 400
                                        }
                                    },
                                    {
                                        'name': 'Villages',
                                        'type': 'table',
                                        'columns': [
                                            {
                                                'name': 'Village Name',
                                                'key': 'village_name',
                                                'width': 20,
                                                'format': 'bold'
                                            },
                                            {
                                                'name': 'Total Buildings',
                                                'key': 'total_buildings',
                                                'width': 20,
                                                'format': 'number'
                                            },
                                            {
                                                'name': 'Flooded Buildings',
                                                'key': 'flooded_buildings',
                                                'width': 25,
                                                'format': 'number'
                                            },
                                            {
                                                'name': 'Not Flooded Buildings',
                                                'key': 'not_flooded_buildings',
                                                'width': 30,
                                                'format': 'number'
                                            },
                                        ]
                                    }
                                ]
                            }
                        }
                    ]
                }
            },
        ]
    }
]