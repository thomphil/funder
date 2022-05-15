**Getting started**

Run the following commands in a single terminal session:-

- `python -m venv .venv`
- `source .venv/bin/activate`
- `pip install -r requirements.txt`
- `./manage.py migrate`
- `./manage.py runserver`  
-OR-  
- `./manage.py test`

**Functionality Overview**

*Fund List View*

- Shows all funds in the database (Fund Object Manager filtered soft deleted funds) 
- Filterable by dropdown of strategys 
- Results shown and AUM Sum leveraging DB methods
- Delete option implemented


*Upload CSV*

- Form for uploading CSVs - these will be queued for async processing(see CSV Queue in the nav)
- Validation performed on uploads
- conjob process runs ~5 seconds and will process a job from the CSV queue. This "worker" is initialised as part of the runserver command


*REST API*
- API can be accessed via the below URLS:- 
    - `http://127.0.0.1:8000/api/fund/`
    - `http://127.0.0.1:8000/api/fund/<fund id>`
    - `http://127.0.0.1:8000/api/fund/?strategy=<strategy>`
- All views are read only

**Further considerations / Deliberate omissions**
- Fund Model uniquness constraints
- Expand CSV validation
- Auth/Permissions
- REST API permissions
- API Filter uses strategy display name - would likely benefit from having a more URL friendly version similar to how the Fund List View does.
- Test coverage far from 100%
- .env file commited for demo only
