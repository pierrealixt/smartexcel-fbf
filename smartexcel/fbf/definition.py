FBF_DEFINITION = [
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
                'name': 'Flood metadata',
                'type': 'map',
                'position': {
                    'x': 0,
                    'y': 0
                },
                'payload': 'flood',
                'rows': [
                    {
                        'name': 'Acquisition Date',
                        'key': 'flood_acquisition_date',
                        'style': {},

                    },
                    {
                        'name': 'Forecast Date',
                        'key': 'flood_forecast_date',
                        'style': {}
                    },
                    {
                        'name': 'Source',
                        'key': 'flood_source',
                        'style': {}
                    },
                    {
                        'name': 'Notes',
                        'key': 'flood_notes',
                        'style': {}
                    },
                    {
                        'name': 'Link',
                        'key': 'flood_link',
                        'style': {}
                    },
                    {
                        'name': 'Trigger Status',
                        'key': 'flood_trigger_status',
                        'style': {}
                    }
                ]
            },
            {
                'name': 'Flood Summary View',
                'type': 'table',
                'payload': 'districts',
                'position': {
                    'x': 0,
                    'y': 1
                },
                'columns': [
                    {
                        'name': 'District Name',
                        'key': 'district_name',
                        'validations': {}
                    },
                    {
                        'name': 'District ID',
                        'key': 'district_code',
                        'validations': {},
                        'format': 'number'
                    },
                    {
                        'name': 'Total Buildings',
                        'key': 'total_buildings',
                        'validations': {},
                        'format': 'number'
                    },
                    {
                        'name': 'Flooded Buildings',
                        'key': 'flooded_buildings',
                        'validations': {},
                        'format': 'number'
                    },
                    {
                        'name': 'Not Flooded Buildings',
                        'key': 'not_flooded_buildings',
                        'validations': {},
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
                            'name': 'Simple array',
                            'type': 'table',
                            'position': {
                                'x': 0,
                                'y': 0
                            },
                            'columns': [
                                {
                                    'name': 'Sub-district Name',
                                    'key': 'sub_district_name',
                                    'validations': {}
                                },
                                {
                                    'name': 'Sub-district ID',
                                    'key': 'sub_district_id',
                                    'validations': {},
                                    'format': 'number'
                                },
                                {
                                    'name': 'Total Buildings',
                                    'key': 'total_buildings',
                                    'validations': {},
                                    'format': 'number'
                                },
                                {
                                    'name': 'Flooded Buildings',
                                    'key': 'flooded_buildings',
                                    'validations': {},
                                    'format': 'number'
                                },
                                {
                                    'name': 'Not Flooded Buildings',
                                    'key': 'not_flooded_buildings',
                                    'validations': {},
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
                                        'name': 'Villages',
                                        'type': 'table',
                                        'position': {
                                            'x': 0,
                                            'y': 0
                                        },
                                        'columns': [
                                            {
                                                'name': 'Village Name',
                                                'key': 'village_name',
                                                'validations': {}
                                            },
                                            {
                                                'name': 'Village ID',
                                                'key': 'village_id',
                                                'validations': {},
                                            },
                                            {
                                                'name': 'Total Buildings',
                                                'key': 'total_buildings',
                                                'validations': {},
                                                'format': 'number'
                                            },
                                            {
                                                'name': 'Flooded Buildings',
                                                'key': 'flooded_buildings',
                                                'validations': {},
                                                'format': 'number'
                                            },
                                            {
                                                'name': 'Not Flooded Buildings',
                                                'key': 'not_flooded_buildings',
                                                'validations': {},
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