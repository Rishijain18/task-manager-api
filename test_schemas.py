# test_schemas.py
# Test script to verify Pydantic schemas work correctly
# This should be run on Python 3.11.7 (Render environment)

from schemas import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse, ErrorResponse
from datetime import datetime

def test_schemas():
    print("Testing Pydantic schemas...")

    try:
        # Test TaskCreate
        task_data = {'title': 'Test Task', 'description': 'Test description'}
        task = TaskCreate(**task_data)
        print('✅ TaskCreate validation: OK')

        # Test TaskUpdate
        update_data = {'title': 'Updated Task'}
        update = TaskUpdate(**update_data)
        print('✅ TaskUpdate validation: OK')

        # Test TaskResponse
        response_data = {
            'id': 1,
            'title': 'Test Task',
            'description': 'Test description',
            'completed': False,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        response = TaskResponse(**response_data)
        print('✅ TaskResponse validation: OK')

        # Test TaskListResponse
        list_response = TaskListResponse(tasks=[response], total=1, page=1, limit=10)
        print('✅ TaskListResponse validation: OK')

        # Test ErrorResponse
        error_response = ErrorResponse(error='Test error', detail='Test detail')
        print('✅ ErrorResponse validation: OK')

        # Test validation errors
        try:
            bad_task = TaskCreate(title='')
            print('❌ Should have failed validation')
        except ValueError as e:
            print(f'✅ Validation error caught: {type(e).__name__}: {e}')

        print('All schema validations passed!')

    except Exception as e:
        print(f'❌ Schema error: {e}')
        import traceback
        traceback.print_exc()
        return False

    return True

if __name__ == "__main__":
    test_schemas()