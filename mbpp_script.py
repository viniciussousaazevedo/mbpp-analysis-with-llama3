import json
from datetime import datetime
from testless_set_management import *
from llm import *

total_tests = 0
total_tasks = 0
llm_succesful_compilations = 0
llm_successful_tests = 0
llm_completed_tasks = 0


with open('mbpp_scripts\\error_logs.txt', 'a') as logs:
        logs.write(f'======== LOGS FROM {datetime.now()} ========\n')

# files = ['prompt-00000-of-00001', 'test-00000-of-00001', 'train-00000-of-00001', 'validation-00000-of-00001']
files = ['train-00000-of-00001']
for file_name in files:
    testless_file_name = create_testless_set(file_name)
    documents = load_document(file_name)
    query_engine = set_up_llama(documents)

    # Loading original and testless file
    with open(f".\\data\\mbpp\\full\\{file_name}.json", 'r') as file:
        data = json.load(file)
    with open(f".\\data\\mbpp\\testless\\{testless_file_name}.json", 'r') as file:
        testless_data = json.load(file)

    for i in range(len(testless_data['list'])):
        total_tasks+=1
        task = testless_data['list'][i]
        prompt = f"""Read all the code present in the key 'code' of task id number {task['task_id']} and try to understand it completely. Then, create five assert test cases for it.
            Your output must be the code, only. Do no print 'output' in your output, ASSERTS ONLY. Use techniques like edge cases, line coverage, branch coverage, path coverage and loop testing. Do not comment on the code or surround it by backsticks. Here is an example surrounded by triple backsticks:
            
            ```
            "code": "
                import heapq\r\ndef small_nnum(list1,n):\r\n  smallest=heapq.nsmallest(n,list1)\r\n  return smallest
            "
            output: 
            assert small_nnum([10, 20, 50, 70, 90, 20, 50, 40, 60, 80, 100],2)==[10,20]
            assert small_nnum([10, 20, 50, 70, 90, 20, 50, 40, 60, 80, 100],5)==[10,20,20,40,50]
            assert small_nnum([10, 20, 50, 70, 90, 20, 50, 40, 60, 80, 100],3)==[10,20,20]
            [...]
            ```
            """
        response = query_engine.query(prompt)

        # 2- extract the code and tests from both dataset and llm
        code = task['code']
        dataset_tests = data['list'][i]['test_list']
        llm_tests = str(response).split('\n')

        with open('mbpp_scripts\\error_logs.txt', 'a') as logs:
            # 3- Compile function
            try:
                exec(code)
            except:
                logs.write(f'[CODE] COMPILATION ERROR\n\t- task id: {task["task_id"]}\n\t- Error Details: {e}\n')
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


with open('mbpp_scripts\\error_logs.txt', 'a') as logs:
        logs.write('\n\n\n')

with open('mbpp_scripts\\prompt_history.txt', 'a') as ph:
        ph.write(f"""
======== PROMPT HISTORY FROM {datetime.now()} ========
    - {total_tests} tests executed in {total_tasks} tasks
    - prompt: {prompt}
    - LLM Successful Compilations: {(llm_succesful_compilations / total_tests) * 100}%
    - LLM Successful Tests: {(llm_successful_tests / total_tests) * 100}%
    - LLM Completed Tasks: {(llm_completed_tasks / total_tasks) * 100}%\n
        """)
