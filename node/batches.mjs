import fs from "fs";
import path from "path";
import openai from "./utils/openai.mjs";
import { openaiErrorHandler } from "./utils/openaiErrorHandler.mjs";

const __dirname = import.meta.dirname;

const fileName = "batchInput.jsonl";

const dir = path.join(__dirname, "data");
const filePath = path.join(dir, fileName);

try {
  // // STEP 1 - Uploading file for batch processing
  // const response = await openai.files.create({
  //   file: fs.createReadStream(filePath),
  //   purpose: "batch",
  // });

  // console.log(response);
  // {
  //   object: 'file',
  //   id: 'file-D0u3s4mvLZlvbggh9po37CVs',
  //   purpose: 'batch',
  //   filename: 'batchinput.jsonl',
  //   bytes: 516,
  //   created_at: 1731400090,
  //   status: 'processed',
  //   status_details: null
  // }

  // STEP 2 - Creating a batch processing job
  const batch = await openai.batches.create({
    input_file_id: "file-D0u3s4mvLZlvbggh9po37CVs",
    endpoint: "/v1/chat/completions",
    completion_window: "24h",
  });

  console.log(batch);
  // // {
  // //   id: 'batch_6733120ddc8c81909868512632c838c4',
  // //   object: 'batch',
  // //   endpoint: '/v1/chat/completions',
  // //   errors: null,
  // //   input_file_id: 'file-D0u3s4mvLZlvbggh9po37CVs',
  // //   completion_window: '24h',
  // //   status: 'validating',
  // //   output_file_id: null,
  // //   error_file_id: null,
  // //   created_at: 1731400205,
  // //   in_progress_at: null,
  // //   expires_at: 1731486605,
  // //   finalizing_at: null,
  // //   completed_at: null,
  // //   failed_at: null,
  // //   expired_at: null,
  // //   cancelling_at: null,
  // //   cancelled_at: null,
  // //   request_counts: { total: 0, completed: 0, failed: 0 },
  // //   metadata: null
  // // }

  // // STEP 3 - Checking status of the batch
  // const batchStatus = await openai.batches.retrieve(
  //   "batch_6733120ddc8c81909868512632c838c4"
  // );

  // console.log(batchStatus);
  // // {
  // //   id: 'batch_6733120ddc8c81909868512632c838c4',
  // //   object: 'batch',
  // //   endpoint: '/v1/chat/completions',
  // //   errors: null,
  // //   input_file_id: 'file-D0u3s4mvLZlvbggh9po37CVs',
  // //   completion_window: '24h',
  // //   status: 'completed',
  // //   output_file_id: 'file-tcqVSAgvkvHDv8C3Q08EfUXh',
  // //   error_file_id: null,
  // //   created_at: 1731400205,
  // //   in_progress_at: 1731400266,
  // //   expires_at: 1731486605,
  // //   finalizing_at: 1731400267,
  // //   completed_at: 1731400268,
  // //   failed_at: null,
  // //   expired_at: null,
  // //   cancelling_at: null,
  // //   cancelled_at: null,
  // //   request_counts: { total: 2, completed: 2, failed: 0 },
  // //   metadata: null
  // // }

  // // STEP 4 - Retrieving results as file
  // const fileResponse = await openai.files.content(
  //   "file-tcqVSAgvkvHDv8C3Q08EfUXh"
  // );
  // const fileContents = await fileResponse.text();

  // console.log(fileContents);
  // // {"id": "batch_req_6733124c230c8190b556dc66a74a111b", "custom_id": "request-1", "response": {"status_code": 200, "request_id": "08a3291463ee894ca30252c6762301fc", "body": {"id": "chatcmpl-ASgah56K9pUGS6oF4evr7ePy7E8b7", "object": "chat.completion", "created": 1731400267, "model": "gpt-3.5-turbo-0125", "choices": [{"index": 0, "message": {"role": "assistant", "content": "Hello! How can I assist you today?", "refusal": null}, "logprobs": null, "finish_reason": "stop"}], "usage": {"prompt_tokens": 20, "completion_tokens": 9, "total_tokens": 29, "prompt_tokens_details": {"cached_tokens": 0, "audio_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 0, "audio_tokens": 0, "accepted_prediction_tokens": 0, "rejected_prediction_tokens": 0}}, "system_fingerprint": null}}, "error": null}
  // // {"id": "batch_req_6733124c32848190a033028316df7bd5", "custom_id": "request-2", "response": {"status_code": 200, "request_id": "ca71ff5c483e2d3f8fb528a0b56c139e", "body": {"id": "chatcmpl-ASgahElP7DWWSfQMSq8124FFkG2If", "object": "chat.completion", "created": 1731400267, "model": "gpt-3.5-turbo-0125", "choices": [{"index": 0, "message": {"role": "assistant", "content": "Hello. What can I not help you with today?", "refusal": null}, "logprobs": null, "finish_reason": "stop"}], "usage": {"prompt_tokens": 22, "completion_tokens": 11, "total_tokens": 33, "prompt_tokens_details": {"cached_tokens": 0, "audio_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 0, "audio_tokens": 0, "accepted_prediction_tokens": 0, "rejected_prediction_tokens": 0}}, "system_fingerprint": null}}, "error": null}

  // // STEP 5 - Getting list of all batches
  // const batches = await openai.batches.list();

  // for await (const batch of batches) {
  //   console.log(batch);
  // }
} catch (error) {
  openaiErrorHandler(error);
}
