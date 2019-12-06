from collections import namedtuple
import psycopg2

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def get_connection():
    import os
    return psycopg2.connect(
        user = os.environ['DB_USER'],
        password = os.environ['DB_PASSWORD'],
        host = os.environ['DB_HOST'],
        port = os.environ['DB_PORT'],
        database = os.environ['DB_DATABASE'])

def get_districts(flood_event_id):
    connection = get_connection()

    query = """
        SELECT
            area.name as district_name,
            area.dc_code as district_code,
            summary.vulnerability_total_score as vulnerability_total_score,
            summary.building_count as total_buildings,
            summary.flooded_building_count as flooded_buildings,
            summary.residential_building_count as residential_building_count,
            summary.residential_flooded_building_count as residential_flooded_building_count,
            summary.clinic_dr_building_count as clinic_dr_building_count,
            summary.clinic_dr_flooded_building_count as clinic_dr_flooded_building_count

        FROM
            flood_event fe,
            flood_event_district_summary summary,
            district area
        WHERE
            fe.id = summary.flood_event_id
            and summary.district_id = area.dc_code
            and fe.id = {flood_event_id}
        ;
    """.format(
        flood_event_id=flood_event_id
    )
    with connection.cursor() as cursor:
        cursor.execute(query)
        results = namedtuplefetchall(cursor)

    connection.close()

    return results


def get_subdistricts(flood_event_id, district_code):
    connection = get_connection()

    query = """
        SELECT
            area.name as sub_district_name,
            area.sub_dc_code as sub_district_code,
            summary.vulnerability_total_score as vulnerability_total_score,
            summary.building_count as total_buildings,
            summary.flooded_building_count as flooded_buildings,
            summary.residential_building_count as residential_building_count,
            summary.residential_flooded_building_count as residential_flooded_building_count,
            summary.clinic_dr_building_count as clinic_dr_building_count,
            summary.clinic_dr_flooded_building_count as clinic_dr_flooded_building_count

        FROM
            flood_event fe,
            flood_event_sub_district_summary summary,
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

    with connection.cursor() as cursor:
        cursor.execute(query)
        results = namedtuplefetchall(cursor)

    connection.close()
    return results


def get_villages(flood_event_id, sub_district_code):
    connection = get_connection()

    query = """
        SELECT
            area.name as village_name,
            area.village_code as village_code,
            summary.vulnerability_total_score as vulnerability_total_score,
            summary.building_count as total_buildings,
            summary.flooded_building_count as flooded_buildings,
            summary.residential_building_count as residential_building_count,
            summary.residential_flooded_building_count as residential_flooded_building_count,
            summary.clinic_dr_building_count as clinic_dr_building_count,
            summary.clinic_dr_flooded_building_count as clinic_dr_flooded_building_count

        FROM
            flood_event fe,
            flood_event_village_summary summary,
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

    with connection.cursor() as cursor:
        cursor.execute(query)
        results = namedtuplefetchall(cursor)

    connection.close()
    return results


def get_flood(flood_event_id):
    connection = get_connection()
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
    with connection.cursor() as cursor:
        cursor.execute(query)
        results = namedtuplefetchall(cursor)

    connection.close()
    return results

class FbfFloodData():
    def __init__(self, flood_event_id):
        self.flood_event_id = flood_event_id

        self.results = {
            'flood': get_flood(flood_event_id),
            # 'villages': get_results(flood_event_id, 'village'),
            'districts': get_districts(flood_event_id),
            # 'sub_districts': get_results('sub_district'),
        }

    def get_payload_subdistricts(self, instance, foreign_key):
        district_code = int(getattr(instance, foreign_key))

        return get_subdistricts(self.flood_event_id, district_code)

    def get_payload_villages(self, instance, foreign_key):
        sub_district_code = int(getattr(instance, foreign_key))

        return get_villages(self.flood_event_id, sub_district_code)


    def get_sheet_name_for_flood_summary(self, kwargs={}):
        return f"Flood Summary"

    def get_sheet_name_for_subdistrict_summary(self, instance, kwargs={}):
        return f"District {instance.district_name} Summary"

    def get_sheet_name_for_village_summary(self, instance, kwargs={}):
        name = f"Sub district {instance.sub_district_name} Summary"
        return name[0:30]
        # return f"{instance[kwargs['index']].area_name} Summary"

    def write_flood_title(self, instance, kwargs={}):
        return f"Flood {instance.id}"

    def write_flood_acquisition_date(self, instance, kwargs={}):
        return instance.acquisition_date.strftime('%Y-%m-%d')

    def write_flood_forecast_date(self, instance, kwargs={}):
        return instance.forecast_date

    def write_flood_source(self, instance, kwargs={}):
        return instance.source

    def write_flood_notes(self, instance, kwargs={}):
        return instance.notes

    def write_flood_link(self, instance, kwargs={}):
        return instance.link

    def write_flood_trigger_status(self, instance, kwargs={}):
        return instance.trigger_status

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
        return int(instance.village_code)

    def write_total_buildings(self, instance, kwargs={}):
        return instance.total_buildings

    def write_flooded_buildings(self, instance, kwargs={}):
        return instance.flooded_buildings

    def write_not_flooded_buildings(self, instance, kwargs={}):
        return instance.total_buildings - instance.flooded_buildings

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

