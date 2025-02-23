import { OpenAIError } from "openai";

export function openaiErrorHandler(error) {
  if (error instanceof OpenAIError) {
    console.error("OpenAI Error:", error.message);
  } else {
    console.error("Some error occured:", error.message);
  }
}
