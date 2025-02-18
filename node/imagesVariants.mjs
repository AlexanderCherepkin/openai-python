import fs from "fs";
import path from "path";
import openai from "./utils/openai.mjs";
import { openaiErrorHandler } from "./utils/openaiErrorHandler.mjs";

const __dirname = import.meta.dirname;

const model = "dall-e-2";
const size = "1024x1024";
const inputFileName = "input.png";
const outputFileName = "output.png";

const imagesDir = path.join(__dirname, "images_variants");
if (!fs.existsSync(imagesDir)) {
  fs.mkdirSync(imagesDir, { recursive: true });
}

try {
  const response = await openai.images.createVariation({
    model,
    size,
    image: fs.createReadStream(path.join(imagesDir, inputFileName)),
    response_format: "b64_json",
    n: 1,
  });

  // console.log(response);

  const base64ImageData = response.data[0].b64_json;

  if (base64ImageData) {
    const filePath = path.join(imagesDir, outputFileName);

    // Decode base64 and save image
    const imageBuffer = Buffer.from(base64ImageData, "base64");
    fs.writeFileSync(filePath, imageBuffer);
    console.log("Successfully saved image:", outputFileName);
  } else {
    console.error("Error: Image in base64 format wasn't received");
  }
} catch (error) {
  openaiErrorHandler(error);
}
