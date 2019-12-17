FBF_DEFINITION = [
    {
        'type': 'format',
        'key': 'table_header',
        'format': {
            'bold': True,
            'font_size': 14,
            'align': 'center'
        }
    },
    {
        'type': 'format',
        'key': 'map_keys',
        'format': {
            'bold': True,
            'font_size': 14,
        }
    },
    {
        'type': 'format',
        'key': 'sheet_title',
        'format': {
            'align': 'center',
            'valign': 'vcenter',
            'bold': True,
            'font_size': 14,
            'border': 1,
            'border_color': "#527d01"
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
        'type': 'sheet',
        'name': {
            'func': 'flood_summary'
        },
        'components': [
            {
                'type': 'text',
                'name': 'Sheet Title',
                'position': {
                    'x': 0,
                    'y': 0
                },
                'size': {
                    'width': 5,
                    'height': 2
                },
                'text_func': 'main_sheet_title',
                'format': 'sheet_title'
            },
            {
                'name': 'Flood metadata',
                'type': 'map',
                'position': {
                    'x': 0,
                    'y': 1
                },
                'payload': 'flood',
                'format': {
                    'map_key': 'map_keys'
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
                    }
                ]
            },
            {
                'name': 'Flood Summary View',
                'type': 'table',
                'payload': 'districts',
                'position': {
                    'x': 0,
                    'y': 2
                },
                'format': {
                    'header': 'table_header'
                },
                'columns': [
                    {
                        'name': 'District Name',
                        'key': 'district_name',
                        'width': 20
                    },
                    {
                        'name': 'District ID',
                        'key': 'district_code',
                        'width': 20,
                        'format': 'number'
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
                            'position': {
                                'x': 0,
                                'y': 0
                            },
                            'size': {
                                'width': 5,
                                'height': 2
                            },
                            'text_func': 'district_sheet_title',
                            'format': 'sheet_title'
                        },
                        {
                            'name': 'Sub-districts',
                            'type': 'table',
                            'position': {
                                'x': 0,
                                'y': 1
                            },
                            'columns': [
                                {
                                    'name': 'Sub-district Name',
                                    'key': 'sub_district_name',
                                    'width': 22,
                                },
                                {
                                    'name': 'Sub-district ID',
                                    'key': 'sub_district_id',
                                    'width': 20,
                                    'format': 'number'
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
                                        'position': {
                                            'x': 0,
                                            'y': 0
                                        },
                                        'size': {
                                            'width': 5,
                                            'height': 2
                                        },
                                        'text_func': 'sub_district_sheet_title',
                                        'format': 'sheet_title'
                                    },
                                    {
                                        'name': 'Villages',
                                        'type': 'table',
                                        'position': {
                                            'x': 0,
                                            'y': 1
                                        },
                                        'columns': [
                                            {
                                                'name': 'Village Name',
                                                'key': 'village_name',
                                                'width': 20,
                                            },
                                            {
                                                'name': 'Village ID',
                                                'key': 'village_id',
                                                'width': 20,
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