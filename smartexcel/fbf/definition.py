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
                'image_func': 'fba_logo',
                'position': {
                    'x': 0,
                    'y': 0,
                    'float': True
                },
                'size': {
                    'width': 140,  # in pixel
                    'height': 40
                },
            },
            {
                'type': 'image',
                'name': 'Partner logos',
                'image_func': 'partner_logos',
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
                        'data_func': 'flood_acquisition_date',
                    },
                    {
                        'name': 'Forecast Date',
                        'data_func': 'flood_forecast_date',
                    },
                    {
                        'name': 'Source',
                        'data_func': 'flood_source',
                    },
                    {
                        'name': 'Notes',
                        'data_func': 'flood_notes',
                    },
                    {
                        'name': 'Link',
                        'data_func': 'flood_link',
                    },
                    {
                        'name': 'Trigger Status',
                        'data_func': 'flood_trigger_status',
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
                'image_func': 'flood_summary_map',
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
                        'data_func': 'district_name',
                        'width': 20,
                        'format': 'bold'
                    },
                    {
                        'name': 'Total Buildings',
                        'data_func': 'total_buildings',
                        'width': 20,
                        'format': 'number'
                    },
                    {
                        'name': 'Flooded Buildings',
                        'data_func': 'flooded_buildings',
                        'width': 25,
                        'format': 'number'
                    },
                    {
                        'name': 'Not Flooded Buildings',
                        'data_func': 'not_flooded_buildings',
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
                            'image_func': 'district_flood_summary_map',
                            'size': {
                                'width': 700,
                                'height': 400
                            }
                        },
                        {
                            'name': 'Sub-districts',
                            'type': 'table',
                            'columns': [
                                {
                                    'name': 'Sub-district Name',
                                    'data_func': 'sub_district_name',
                                    'width': 22,
                                    'format': 'bold'
                                },
                                {
                                    'name': 'Total Buildings',
                                    'data_func': 'total_buildings',
                                    'width': 20,
                                    'format': 'number'
                                },
                                {
                                    'name': 'Flooded Buildings',
                                    'data_func': 'flooded_buildings',
                                    'width': 25,
                                    'format': 'number'
                                },
                                {
                                    'name': 'Not Flooded Buildings',
                                    'data_func': 'not_flooded_buildings',
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
                                        'image_func': 'sub_district_flood_summary_map',
                                        'size': {
                                            'width': 700,
                                            'height': 400
                                        }
                                    },
                                    {
                                        'name': 'Villages',
                                        'type': 'table',
                                        'columns': [
                                            {
                                                'name': 'Village Name',
                                                'data_func': 'village_name',
                                                'width': 20,
                                                'format': 'bold'
                                            },
                                            {
                                                'name': 'Total Buildings',
                                                'data_func': 'total_buildings',
                                                'width': 20,
                                                'format': 'number'
                                            },
                                            {
                                                'name': 'Flooded Buildings',
                                                'data_func': 'flooded_buildings',
                                                'width': 25,
                                                'format': 'number'
                                            },
                                            {
                                                'name': 'Not Flooded Buildings',
                                                'data_func': 'not_flooded_buildings',
                                                'width': 30,
                                                'format': 'number'
                                            },
                                        ],
                                        'recursive': {
                                            'name': {
                                                'func': 'village_detail'
                                            },
                                            'foreign_key': 'village_code',
                                            'payload_func': 'village_detail',
                                            'components': [
                                                {
                                                    'type': 'text',
                                                    'name': 'Village Sheet Title',
                                                    'size': {
                                                        'width': 4,
                                                        'height': 2
                                                    },
                                                    'text_func': 'village_sheet_title',
                                                    'format': 'sheet_title'
                                                },
                                                {
                                                    'type': 'image',
                                                    'name': 'Village Flood summary Map',
                                                    'image_func': 'village_flood_summary_map',
                                                    'size': {
                                                        'width': 700,
                                                        'height': 400
                                                    }
                                                },
                                                {
                                                    'type': 'table',
                                                    'name': 'Village detail summary',
                                                    'columns': [
                                                        {
                                                            'name': 'Village Name',
                                                            'data_func': 'village_name',
                                                            'width': 20,
                                                            'format': 'bold'
                                                        },
                                                        {
                                                            'name': 'Total Buildings',
                                                            'data_func': 'total_buildings',
                                                            'format': 'number',
                                                            'width': 20,
                                                        },
                                                        {
                                                            'name': 'Flooded Buildings',
                                                            'data_func': 'flooded_buildings',
                                                            'format': 'number',
                                                            'width': 25,
                                                        },
                                                        {
                                                            'name': 'Not Flooded Buildings',
                                                            'data_func': 'not_flooded_buildings',
                                                            'format': 'number',
                                                            'width': 30,
                                                        },
                                                    ]
                                                },
                                            ]
                                        }
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