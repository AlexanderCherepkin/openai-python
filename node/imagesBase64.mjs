import fs from "fs";
import path from "path";
import openai from "./utils/openai.mjs";
import {
  generateFileNameWithExtension,
  saveImageDataToJson,
} from "./utils/fileUtils.mjs";
import { openaiErrorHandler } from "./utils/openaiErrorHandler.mjs";

const __dirname = import.meta.dirname;

const prompt =
  "Rendered in stunning 4K and UHD resolution with Octane Render CGI technology ((Tsundere:1.3)), confused,correct anatomy, Rogue and cute, many details, looking at viewer, full body, solo, creating a vibrant impression, away from the camera, anatomically correct, closed mouth, ringlets, Her expressive, charming eyes and soft, delicate facial features arouse admiration, creating a welcoming and adorable presence";

const model = "dall-e-3";
const size = "1792x1024";

try {
  const response = await openai.images.generate({
    model,
    prompt,
    size,
    response_format: "b64_json",
    n: 1,
  });

  // console.log(response);

  const revisedPrompt = response.data[0].revised_prompt;
  const base64ImageData = response.data[0].b64_json;
  // console.log(base64ImageData);

  if (base64ImageData) {
    const dir = path.join(__dirname, "images");
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }

    const fileName = generateFileNameWithExtension({
      dir,
      prompt,
      extension: "png",
    });
    const filePath = path.join(dir, fileName);

    // Decode base64 and save image
    const imageBuffer = Buffer.from(base64ImageData, "base64");
    fs.writeFileSync(filePath, imageBuffer);
    console.log("Successfully saved image:", fileName);

    // Append image data including Base64 data to the images.json file
    const imageMetaData = { prompt, revisedPrompt, size, model };
    saveImageDataToJson({
      dir,
      imageMetaData,
      base64ImageData,
    });
  } else {
    console.error("Error: Image in base64 format wasn't received");
  }
} catch (error) {
  openaiErrorHandler(error);
}
