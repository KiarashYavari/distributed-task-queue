clone the project and cd to prj root dir

```bash
git clone <repo-url>
cd <project-root>
```
create virtualenv in there:
```bash
python -m venv .venv
```
activate the virtualenv
```bash
source .venv/bin/activate
```

install requirements from requirements.txt
```bash
pip install -r requirements.txt
```

change directory to the task_service_api
```bash
cd task_service_api
```

run the task microservice with uvicorn
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

run the worker_service with a seprate terminal
```bash
cd worker_service
uvicorn main:app --reload --host 127.0.0.1 --port 8001
```

use curl to test the API:
```bash
curl -X POST http://localhost:8000/tasks   -H "Content-Type: application/json"   -d '{"task_type": "echo", "payload": "hello"}'
```

output:
{"task_id":"94012b0f-0aa5-4004-b916-03734bb4b4fe"}

then use this to do the GET /tasks/{task_id} and see results
```bash
curl -X GET http://localhost:8000/tasks/94012b0f-0aa5-4004-b916-03734bb4b4fe
```
output:
{"task_id":"94012b0f-0aa5-4004-b916-03734bb4b4fe","status":"completed","result":"hello"}

 I got short on time as I have to work during the weekends to cover one of my colleagues.
 so I couldn't finish the test codes with pytest.
 but the code is tested and workd with curl.
 Dockerfiles being generated but not tested.
 tasks.db should be created after the task_service_api is started