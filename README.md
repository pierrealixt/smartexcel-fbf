# SmartExcel for Fbf

Report generator for the Fbf project.

This lib needs pyton 3.7 or greater.

## Documentation
Read the code and the tests.

## Development
```
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### environment variables
```
cp .env.template .env
```

Edit `.env` then
```
source .env
```

## Test

### unit tests
```bash
python -m smartexcel.test_smart_excel
```


### Fbf
```bash
python -m smartexcel.test_fbf TestFlood
```
A file `test_fbf.xlsx` is created at the root of this project. Open it and make sure it looks like what you want.


## Deployment


### SmartExcel code
1. Do your change, edit the definition, tweak the data model. Make sure it works by running the test. Then commit and push.
2. Go to rancher > Fbf stack > connect to the shell of the `db` container
3. Run:
```
pip3 install git+https://github.com/kartoza/smartexcel-fbf.git
```
Add the flag `--upgrade` to upgrade the package.

### python/pl code

The function's name is `kartoza_fba_generate_excel_report_for_flood`. It is already present in the database.
If you need to change the code of the function, you must replace it.

```
CREATE OR REPLACE FUNCTION kartoza_fba_generate_excel_report_for_flood (flood_event_id integer)
  RETURNS varchar
 AS $$
   import io
   plpy.execute("select * from satisfy_dependency('xlsxwriter')")
   plpy.execute("select * from satisfy_dependency('openpyxl')")

   from smartexcel.smart_excel import SmartExcel
   from smartexcel.fbf.data_model import FbfFloodData
   from smartexcel.fbf.definition import FBF_DEFINITION

   excel = SmartExcel(
       output=io.BytesIO(),
       definition=FBF_DEFINITION,
       data=FbfFloodData(
           flood_event_id=flood_event_id,
           pl_python_env=True
       )
   )
   excel.dump()

   plan = plpy.prepare("UPDATE flood_event SET spreadsheet = ($1) where id = ($2)", ["bytea", "integer"])
   plpy.execute(plan, [excel.output.getvalue(), flood_event_id])

   return "OK"
$$ LANGUAGE plpython3u;
```


## How to use it

```
select * from kartoza_fba_generate_excel_report_for_flood(15);
```
`15` is an ID present in the table `flood_event`.
