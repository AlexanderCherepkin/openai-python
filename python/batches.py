import os
import json
import time
from openai import OpenAI
from dotenv import load_dotenv
from pprint import pprint

# Загружаем переменные окружения
load_dotenv()

client = OpenAI()

batches_dir = "batch"
batch_input_file_name = "batch_input.jsonl"
batch_input_file_path = os.path.join(batches_dir, batch_input_file_name)

try:
    # STEP 1 - Uploading file for batch processing
    with open(batch_input_file_path, "rb") as batch_input_file:
        file_upload_response = client.files.create(
            file=batch_input_file, purpose="batch"
        )

    print("File Upload Response:")
    pprint(file_upload_response)

    file_id = file_upload_response.id

    # STEP 2 - Creating a batch processing job
    batch_job_response = client.batches.create(
        input_file_id=file_id,
        endpoint="/v1/chat/completions",
        completion_window="24h",
        metadata={"job": "example_batch"}
    )

    print("Batch Job Response:")
    pprint(batch_job_response)

    batch_id = batch_job_response.id

    # STEP 3 - Checking status of the batch
    while True:
        batch_status_response = client.batches.retrieve(batch_id)
        status = batch_status_response.status
        print(f"Batch Status: {status}")

        if status in ["completed", "failed", "cancelled"]:
            break  # Выход из цикла, если батч завершён
        time.sleep(10)  # Ждём 10 секунд перед следующей проверкой

    # STEP 4 - Retrieving results as file (если статус завершен)
    if batch_status_response.status == "completed":
        output_file_id = batch_status_response.output_file_id
        print(f"Batch Completed. Output File ID: {output_file_id}")

        # Получаем содержимое файла
        file_response = client.files.content(output_file_id)
        file_content = file_response.read()  # Читаем данные

        # Сохраняем файл на диск
        output_file_path = os.path.join(batches_dir, f"{output_file_id}.jsonl")
        with open(output_file_path, "wb") as f:
            f.write(file_content)

        print(f"Saved results to {output_file_path}")

    # STEP 5 - Getting list of all batches
    batches_list_response = client.batches.list()
    print("All Batches:")
    pprint(batches_list_response)

except Exception as e:
    print("Error during OpenAI API communication occurred:", e)


