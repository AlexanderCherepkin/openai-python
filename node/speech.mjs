import fs from "fs";
import path from "path";
import openai from "./utils/openai.mjs";
import { openaiErrorHandler } from "./utils/openaiErrorHandler.mjs";
import { generateFileNameWithExtension } from "./utils/fileUtils.mjs";

const __dirname = import.meta.dirname;

const input =
  "The President of the United States will announce the imposition of new trade tariffs on several countries next week, without specifying which ones, in order to equalize the rates these nations impose on American products.";
const model = "tts-1";
const voice = "onyx";
const extension = "mp3";

try {
  const response = await openai.audio.speech.create({
    model,
    input,
    voice,
    response_format: extension,
  });

  // console.log(response);

  const audioData = await response.arrayBuffer();

  if (audioData) {
    const dir = path.join(__dirname, "audio", extension);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }

    const fileName = generateFileNameWithExtension({
      dir,
      prompt: input,
      extension,
    });
    const filePath = path.join(dir, fileName);

    // Save audio file
    const audioBuffer = Buffer.from(audioData);
    fs.writeFileSync(filePath, audioBuffer);
    console.log("Successfully saved audio:", fileName);
  } else {
    console.error("Error: Audio data wasn't received");
  }
} catch (error) {
  openaiErrorHandler(error);
}
