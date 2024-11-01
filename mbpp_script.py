import json
from datetime import datetime
from llm import *

total_tests = 0
total_tasks = 0
llm_succesful_compilations = 0
llm_successful_tests = 0
llm_completed_tasks = 0

with open('./error_logs.txt', 'a') as logs:
        logs.write(f'======== LOGS FROM {datetime.now()} ========\n')

# files = ['prompt-00000-of-00001', 'test-00000-of-00001', 'train-00000-of-00001', 'validation-00000-of-00001']
files = ['validation-00000-of-00001']
for file_name in files:
    # Loading original and testless file
    with open(f"./data/full/{file_name}.json", 'r') as file:
        data = json.load(file)

    for task in data['list']:
        total_tasks+=1
        code = task['code']
        prompt = f"""
Read all the code present in the code snippet bellow (starting right after "```python" and ending right before "```") and try to understand it completely. Then, create exatcly 5 (five) assert test cases for it. Your output must be "assert" code, only. Use techniques like edge cases, line coverage, branch coverage, path coverage and loop testing. Do not make comments on the code. Do not start or end your answer with "```", "```python" or "output", asserts only.
code: 
```python
{code}
```

Here is an example of input and output (starting right after "```python" and ending right before "```"): 
```python
    input: import heapq\r\ndef small_nnum(list1,n):\r\n  smallest=heapq.nsmallest(n,list1)\r\n  return smallest
    output: 
    assert small_nnum([10, 20, 50, 70, 90, 20, 50, 40, 60, 80, 100],2)==[10,20]
    assert small_nnum([10, 20, 50, 70, 90, 20, 50, 40, 60, 80, 100],5)==[10,20,20,40,50]
    assert small_nnum([10, 20, 50, 70, 90, 20, 50, 40, 60, 80, 100],3)==[10,20,20]
    assert small_nnum([10, 20, 50, 70, 90, 20, 50, 40, 60, 80, 100],1)==[10]
    assert small_nnum([10, 20, 50, 70, 90, 30, 50, 40, 60, 80, 100],3)==[10,20,30]
```
        """
        response = get_answer(prompt)

        # 2- extract the code and tests from both dataset and llm
        dataset_tests = task['test_list']
        llm_tests = str(response).split('\n')

        with open('./error_logs.txt', 'a') as logs:
            # 3- Compile function
            try:
                exec(code)
            except:
                logs.write(f'\t[CODE] COMPILATION ERROR\n\t- task id: {task["task_id"]}\n\t- Error Details: {e}\n')
                continue        
            # 4- Execute dataset tests
            for test in dataset_tests:
                try:
                    exec(test)
                except AssertionError as e:
                    logs.write(f'[DATASET] TEST FAILED: {test}\n\t- task id: {task["task_id"]}\n    - Error Details: {e}\n')
                except Exception as e:
                    logs.write(f'[DATASET] COMPILATION ERROR: {test}\n\t- task id: {task["task_id"]}\n\t- Error Details: {e}\n')
            # 5- Execute LLM tests
            task_is_successful = True
            for test in llm_tests:
                total_tests+=1
                try:
                    exec(test)
                    llm_succesful_compilations+=1
                    llm_successful_tests+=1
                except AssertionError as e:
                    llm_succesful_compilations+=1
                    task_is_successful = False
                    logs.write(f'[LLM] TEST FAILED: {test}\n\t- task id: {task["task_id"]}\n')
                except Exception as e:
                    task_is_successful = False
                    logs.write(f'[LLM] COMPILATION ERROR: {test}\n\t- task id: {task["task_id"]}\n\t- Error Details: {e}\n')
            if task_is_successful:
                llm_completed_tasks+=1


with open('./error_logs.txt', 'a') as logs:
        logs.write('\n\n\n')

with open('./prompt_history.md', 'a') as ph:
        ph.write(f"""
# Prompt History from {datetime.now()}
- {total_tests} tests executed in {total_tasks} tasks
- prompt:
{prompt}
- LLM Successful Compilations: {(llm_succesful_compilations / total_tests) * 100}%
- LLM Successful Tests: {(llm_successful_tests / total_tests) * 100}%
- LLM Completed Tasks: {(llm_completed_tasks / total_tasks) * 100}%\n
""")

# TODO: switch to use only the 'text' key on dataset questions