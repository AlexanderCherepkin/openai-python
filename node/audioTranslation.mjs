import fs from "fs";
import path from "path";
import openai from "./utils/openai.mjs";
import { openaiErrorHandler } from "./utils/openaiErrorHandler.mjs";

const __dirname = import.meta.dirname;

const model = "whisper-1";
const fileName = "mymp3.mp3";

const dir = path.join(__dirname, "audio", "mp3");
const filePath = path.join(dir, fileName);

try {
  const response = await openai.audio.translations.create({
    model,
    file: fs.createReadStream(filePath),
    response_format: "json", // default
  });

  console.log(response);

  fs.appendFileSync(path.join(dir, "translations.txt"), `${response.text}\n\n`);
} catch (error) {
  openaiErrorHandler(error);
}
