import os
from collections import namedtuple
import shutil
import requests
import psycopg2
try:
    import plpy
except:
    pass

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


class FbfFloodData():
    trigger_status = [
        {'id': 0, 'status': 'No activation', 'color': '#72CA7A'},
        {'id': 1, 'status': 'Pre-activation', 'color': '#D39858'},
        {'id': 2, 'status': 'Activation', 'color': '#CA6060'},
        {'id': 3, 'status': 'Stop', 'color': '#FF0000'}
    ]

    def __init__(self, flood_event_id, pl_python_env=None):
        self.flood_event_id = flood_event_id

        if pl_python_env:
            self.pl_python_env = pl_python_env
        else:
            self.connection = psycopg2.connect(
                user = os.environ['DB_USER'],
                password = os.environ['DB_PASSWORD'],
                host = os.environ['DB_HOST'],
                port = os.environ['DB_PORT'],
                database = os.environ['DB_DATABASE'])
            self.pl_python_env = False

        self.results = {
            'flood': self.get_flood(flood_event_id),
            'districts': self.get_districts(flood_event_id),
        }

    def execute_query(self, query):
        if self.pl_python_env:
            res = plpy.execute(query)
            try:
                fields = list(res[0].keys())

                def_meta_res = namedtuple('Result', ', '.join(fields))

                results = [
                    def_meta_res(*list(res[index].values()))
                    for index in range(0, len(res))
                ]
            except IndexError:
                results = []
            return results

        else:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                results = namedtuplefetchall(cursor)

        return results

    def get_districts(self, flood_event_id):

        query = """
            SELECT
                area.name as district_name,
                area.dc_code as district_code,
                summary.total_vulnerability_score as vulnerability_total_score,
                summary.building_count as total_buildings,
                summary.flooded_building_count as flooded_buildings,
                summary.trigger_status as activation_state

            FROM
                flood_event fe,
                mv_flood_event_district_summary summary,
                district area
            WHERE
                fe.id = summary.flood_event_id
                and summary.district_id = area.dc_code
                and fe.id = {flood_event_id}
            ;
        """.format(
            flood_event_id=flood_event_id
        )

        return self.execute_query(query)


    def get_subdistricts(self, flood_event_id, district_code):

        query = """
            SELECT
                area.name as sub_district_name,
                area.sub_dc_code as sub_district_code,
                summary.total_vulnerability_score as vulnerability_total_score,
                summary.building_count as total_buildings,
                summary.flooded_building_count as flooded_buildings,
                summary.trigger_status as activation_state

            FROM
                flood_event fe,
                mv_flood_event_sub_district_summary summary,
                sub_district area
            WHERE
                fe.id = summary.flood_event_id
                and summary.sub_district_id = area.sub_dc_code
                and area.dc_code = {district_code}
                and fe.id = {flood_event_id}
            ;
        """.format(
            district_code=district_code,
            flood_event_id=flood_event_id
        )

        return self.execute_query(query)


    def get_villages(self, flood_event_id, sub_district_code):
        query = """
            SELECT
                area.name as village_name,
                area.village_code as village_code,
                summary.total_vulnerability_score as vulnerability_total_score,
                summary.building_count as total_buildings,
                summary.flooded_building_count as flooded_buildings,
                summary.trigger_status as activation_state

            FROM
                flood_event fe,
                mv_flood_event_village_summary summary,
                village area
            WHERE
                fe.id = summary.flood_event_id
                and summary.village_id = area.village_code
                and area.sub_dc_code = {sub_district_code}
                and fe.id = {flood_event_id}
            ;
        """.format(
            sub_district_code=sub_district_code,
            flood_event_id=flood_event_id
        )

        return self.execute_query(query)


    def get_flood(self, flood_event_id):
        query = """
            SELECT
                *
            FROM
                flood_event fe
            WHERE
                fe.id = {flood_event_id}
        """.format(
            flood_event_id=flood_event_id
        )

        return self.execute_query(query)

    def get_flood_extent(self, flood_event_id):
        query = """
            SELECT *
            FROM vw_flood_event_extent fee
            WHERE fee.id = {flood_event_id}
        """.format(
            flood_event_id=flood_event_id
        )
        return self.execute_query(query)

    def get_area_extent(self, params, area_code):
        query = """
            SELECT
                st_xmin(st_extent((st_buffer(geom, 0.25)::geography)::geometry)) as x_min,
                st_ymin(st_extent((st_buffer(geom, 0.25)::geography)::geometry)) as y_min,
                st_xmax(st_extent((st_buffer(geom, 0.25)::geography)::geometry)) as x_max,
                st_ymax(st_extent((st_buffer(geom, 0.25)::geography)::geometry)) as y_max
            FROM {table}
            WHERE {foreign_key} = '{area_code}'
        """.format(
            table=params['table'],
            foreign_key=params['foreign_key'],
            area_code=area_code
        )
        return self.execute_query(query)

    def get_payload_subdistricts(self, instance, foreign_key):
        district_code = int(getattr(instance, foreign_key))
        return self.get_subdistricts(self.flood_event_id, district_code)

    def get_payload_villages(self, instance, foreign_key):
        sub_district_code = int(getattr(instance, foreign_key))
        return self.get_villages(self.flood_event_id, sub_district_code)

    def get_payload_village_detail(self, instance, foreign_key):
        return [instance]

    def get_sheet_name_for_flood_summary(self, kwargs={}):
        return f"Flood Summary"

    def get_sheet_name_for_subdistrict_summary(self, instance, kwargs={}):
        name = f"District {instance.district_name} Summary"
        return name[0:30]

    def get_sheet_name_for_village_summary(self, instance, kwargs={}):
        name = f"Sub district {instance.sub_district_name} Summary"
        return name[0:30]

    def get_sheet_name_for_village_detail(self, instance, kwargs={}):
        name = f"Village {instance.village_name} Summary"
        return name[0:30]

    def write_flood_title(self, instance, kwargs={}):
        return f"Flood {instance.id}"

    def write_flood_acquisition_date(self, instance, kwargs={}):
        try:
            if isinstance(instance.acquisition_date, str):
                return instance.acquisition_date
            else:
                return instance.acquisition_date.strftime('%Y-%m-%d')
        except Exception:
            return None

    def write_flood_forecast_date(self, instance, kwargs={}):
        try:
            if isinstance(instance.forecast_date, str):
                return instance.forecast_date
            else:
                return instance.forecast_date.strftime('%Y-%m-%d')
        except Exception:
            return None

    def write_flood_source(self, instance, kwargs={}):
        return instance.source

    def write_flood_notes(self, instance, kwargs={}):
        return instance.notes

    def write_flood_link(self, instance, kwargs={}):
        return instance.link

    def write_flood_trigger_status(self, instance, kwargs={}):
        for status in self.trigger_status:
            if status['id'] == instance.trigger_status:
                return status['status']
        return 'No action'

    def get_format_for_trigger_status(self, instance):
        cell_format = {
            'bold': True,
            'align': 'center',
            'bg_color': ''
        }

        for status in self.trigger_status:
            if status['id'] == instance.trigger_status:
                cell_format['bg_color'] = status['color']
                return cell_format

        cell_format['bg_color'] = '#ddddd'
        return cell_format

    def write_district_name(self, instance, kwargs={}):
        return instance.district_name

    def write_district_code(self, instance, kwargs={}):
        return instance.district_code

    def write_sub_district_name(self, instance, kwargs={}):
        return instance.sub_district_name

    def write_sub_district_id(self, instance, kwargs={}):
        return instance.sub_district_code

    def write_village_name(self, instance, kwargs={}):
        return instance.village_name

    def write_village_id(self, instance, kwargs={}):
        # village_id : 3201160018.0
        # cast to int to remove the decimal
        # then to str because 3,201,160,018 is bigger than 2,147,483,647
        return str(int(instance.village_code))

    def write_total_buildings(self, instance, kwargs={}):
        return instance.total_buildings

    def write_flooded_buildings(self, instance, kwargs={}):
        return instance.flooded_buildings

    def write_not_flooded_buildings(self, instance, kwargs={}):
        try:
            return instance.total_buildings - instance.flooded_buildings
        except Exception:
            return 0

    def write_vulnerability_total_score(self, instance, kwargs={}):
        return instance[kwargs['index']]['vulnerability_total_score']

    def write_building_count(self, instance, kwargs={}):
        return instance.building_count

    def write_flooded_building_count(self, instance, kwargs={}):
        return instance.flooded_building_count

    def write_residential_building_count(self, instance, kwargs={}):
        return instance.residential_building_count

    def write_residential_flooded_building_count(self, instance, kwargs={}):
        return instance.residential_flooded_building_count

    def write_clinic_dr_building_count(self, instance, kwargs={}):
        return instance.clinic_dr_building_count

    def write_clinic_dr_flooded_building_count(self, instance, kwargs={}):
        return instance.clinic_dr_flooded_building_count

    def get_text_for_main_sheet_title(self):
        return 'FbF Flood Summary Report'

    def get_text_for_main_sheet_sub_title(self):
        return 'Overview Map'

    def get_text_for_district_sheet_title(self, instance):
        return f'District: {instance.district_name}'

    def get_text_for_sub_district_sheet_title(self, instance):
        return f'Sub-district: {instance.sub_district_name}'

    def get_text_for_village_sheet_title(self, instance):
        return f'Village: {instance.village_name}'

    def get_text_for_kartoza(self):
        return 'Made with love by Kartoza'

    def get_image_partner_logos(self, size):
        return path_to_image('partner_logos_medium.png')

    def get_image_fba_logo(self, size):
        return path_to_image('fba-inasafe.png')

    def get_image_kartoza_logo(self, size):
        return path_to_image('kartoza2.png')

    def get_image_flood_summary_map(self, size):
        # substract x_max and x_min => width
        # substract y_max and y_min => height

        # with width and height, get the ratio

        # compare ratio (e.g: 7/3) with `size` ratio (700x400)
        # if bigger, scale the height
        # y_max * image_ratio / extent_radio
        # if smaller, scale the width
        extent = self.get_flood_extent(self.flood_event_id)[0]
        bbox = extent_to_string(extent)

        url = build_wms_url(self.flood_event_id, bbox, size)
        path_map = download_map(url, f'flood_summary_map_{self.flood_event_id}.png')

        return path_map

    def get_image_district_flood_summary_map(self, instance, size):
        params = {
            'size': size,
            'table': 'district',
            'foreign_key': 'dc_code',
            'area_code': int(instance.district_code),
            'image_name': f'district_{instance.district_code}_flood_summary_map_{self.flood_event_id}.png'
        }

        return self.get_map_path(params)

    def get_image_sub_district_flood_summary_map(self, instance, size):
        params = {
            'size': size,
            'table': 'sub_district',
            'foreign_key': 'sub_dc_code',
            'area_code': int(instance.sub_district_code),
            'image_name': f'sub_district_{instance.sub_district_code}_flood_summary_map_{self.flood_event_id}.png'
        }

        return self.get_map_path(params)

    def get_image_village_flood_summary_map(self, instance, size):
        params = {
            'size': size,
            'table': 'village',
            'foreign_key': 'village_code',
            'area_code': int(instance.village_code),
            'image_name': f'village_{instance.village_code}_flood_summary_map_{self.flood_event_id}.png'
        }

        return self.get_map_path(params)

    def get_map_path(self, params):
        extent = self.get_area_extent({
            'table': params['table'],
            'foreign_key': params['foreign_key']
        }, params['area_code'])[0]

        bbox = extent_to_string(extent)

        url = build_wms_url(self.flood_event_id, bbox, params['size'])

        path_map = download_map(url, params['image_name'])
        return path_map

def build_wms_url(flood_event_id, bbox, size):
    width = size['width']
    height = size['height']
    layer = 'kartoza:flood_map'
    cql_filter = f'flood_event_id={flood_event_id}'
    image_format = 'image/png8'

    return f'http://78.47.62.69/geoserver/kartoza/wms?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&FORMAT={image_format}&TRANSPARENT=true&LAYERS={layer}&cql_filter={cql_filter}&exceptions=application/vnd.ogc.se_inimage&SRS=EPSG:4326&STYLES=&WIDTH={width}&HEIGHT={height}&BBOX={bbox}'

def extent_to_string(extent):
    return ','.join([
        str(extent.x_min),
        str(extent.y_min),
        str(extent.x_max),
        str(extent.y_max)
    ])

def download_map(url, image):
    maps_dir = '/tmp/fba-maps'

    if not os.path.exists(maps_dir):
        os.mkdir(maps_dir)

    path = os.path.join(
        maps_dir,
        image)

    response = requests.get(url, stream=True)

    with open(path, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)

    return path

def path_to_image(image):
    return os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'images',
        image)