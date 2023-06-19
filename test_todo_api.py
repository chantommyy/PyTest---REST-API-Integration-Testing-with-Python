import requests
import uuid
ENDPOINT = 'https://todo.pixegami.io'

# test can create and get the task
def test_can_create_task():
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    data = create_task_response.json()

    task_id = data['task']['task_id']
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data['content'] == payload['content']
    assert get_task_data['user_id'] == payload['user_id']

# test can update the task
# step 1 - create the task
# step 2 - update the task
# step 3 - get the task

def test_can_update_task():
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    data = create_task_response.json()
    task_id = data['task']['task_id']

    new_payload = {
        'user_id': payload['user_id'],
        'task_id': task_id,
        'content': 'updated_content',
        'is_done': True,
    }

    update_task_response = update_task(new_payload)
    assert update_task_response.status_code == 200

    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data['content'] == new_payload['content']
    assert get_task_data['is_done'] == new_payload['is_done']

# test can list the tasks
# step 1 - create the tasks
# step 2 - list the tasks

def test_can_list_tasks():
    n = 3
    payload = new_task_payload()
    for _ in range(n):
        create_task_response = create_task(payload)
        assert create_task_response.status_code == 200

    user_id = payload['user_id']
    list_task_response = list_tasks(user_id)
    assert list_task_response.status_code == 200
    data = list_task_response.json()

    tasks = data['tasks']
    assert len(tasks) == n
    print


# test can delete task
# step 1 - create the task
# step 2 - delete the task
# step 3 - get the task and check it's not found

def test_can_delete_task():
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    data = create_task_response.json()
    task_id = data['task']['task_id']

    delete_task_response = delete_task(task_id)
    assert delete_task_response.status_code == 200

    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 404

def create_task(payload):
    return requests.put(ENDPOINT + '/create-task', json=payload)

def get_task(task_id):
    return requests.get(ENDPOINT + f'/get-task/{task_id}')

def update_task(payload):
    return requests.put(ENDPOINT + '/update-task', json=payload)

def list_tasks(user_id):
       return requests.get(ENDPOINT + f'/list-tasks/{user_id}')

def delete_task(task_id):
        return requests.delete(ENDPOINT + f'/delete-task/{task_id}')

def new_task_payload():
    user_id = f'test_user_{uuid.uuid4().hex}'
    content = f'test_content_{uuid.uuid4().hex}'

    print(f'Creating task for user {user_id} with content {content}')
    return {
        'content': content,
        'user_id': user_id,
        'is_done': False,
    }
