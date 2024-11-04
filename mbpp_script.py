import json
import os
from datetime import datetime
from llm import *
import re

def capture_function_signature(code_line):
    match = re.search(r"def\s+(\w+\s*\(.*?\)):", code_line)
    return match.group(1) if match else None


total_tests = 0
total_tasks = 0
llm_succesful_compilations = 0
llm_successful_tests = 0
llm_completed_tasks = 0

os.makedirs('results', exist_ok=True)
with open('./results/error_logs.txt', 'a') as logs:
        logs.write(f'======== LOGS FROM {datetime.now()} ========\n')

# files = ['prompt-00000-of-00001', 'test-00000-of-00001', 'train-00000-of-00001', 'validation-00000-of-00001']
files = ['validation-00000-of-00001']
for file_name in files:
    # Loading original and testless file
    with open(f"./data/full/{file_name}.json", 'r') as file:
        data = json.load(file)

    for task in data['list']:
        total_tasks+=1
        description = task['text']
        code = task['code']
        function_signature = capture_function_signature(code)
        prompt = f"""
Read the programming problem description present below (starting right after "```bash" and ending right before "```") and try to understand it completely. Only then, create exatcly 5 (five) Python assert test cases for it. Your output must be "assert" code, only. Use techniques like edge cases, line coverage, branch coverage, path coverage and loop testing. Do not make comments on the code. Do not start or end your answer with "```", "```python" or "output", asserts only. Do not use more than 150 characters per assert. Do not use '\\' at all.
description: 
```bash
{description}
```
you must create your tests considering that it was implemented with the name and parameters below (starting right after "```bash" and ending right before "```"):
```bash
{function_signature}
```

Here is an example of input and output (starting right after "```bash" and ending right before "```"): 
```bash
    input: Write a function to get the n smallest items from a dataset.
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

        with open('./results/error_logs.txt', 'a') as logs:
            # 3- Compile function
            try:
                exec(code)
            except:
                logs.write(f'\t[CODE] COMPILATION ERROR\n\t\t- task id: {task["task_id"]}\n\t\t- Error Details: {e}\n')
                continue        
            # 4- Execute dataset tests
            for test in dataset_tests:
                try:
                    exec(test)
                except AssertionError as e:
                    logs.write(f'\t[DATASET] TEST FAILED: {test}\n\t\t- task id: {task["task_id"]}\n    - Error Details: {e}\n')
                except Exception as e:
                    logs.write(f'\t[DATASET] COMPILATION ERROR: {test}\n\t\t- task id: {task["task_id"]}\n\t\t- Error Details: {e}\n')
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
                    logs.write(f'\t[LLM] TEST FAILED: {test}\n\t\t- task id: {task["task_id"]}\n')
                except Exception as e:
                    task_is_successful = False
                    logs.write(f'\t[LLM] COMPILATION ERROR: {test}\n\t\t- task id: {task["task_id"]}\n\t\t- Error Details: {e}\n')
            if task_is_successful:
                llm_completed_tasks+=1
        print(f'✅ - {function_signature}')


with open('./results/error_logs.txt', 'a') as logs:
        logs.write('\n\n\n')

with open('./results/prompt_history.md', 'a') as ph:
        ph.write(f"""
# Prompt History from {datetime.now()}
- {total_tests} tests executed in {total_tasks} tasks
- prompt:
{prompt}
- LLM Successful Compilations: {(llm_succesful_compilations / total_tests) * 100}%
- LLM Successful Tests: {(llm_successful_tests / total_tests) * 100}%
- LLM Completed Tasks: {(llm_completed_tasks / total_tasks) * 100}%\n
""")
