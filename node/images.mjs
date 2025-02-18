import fs from "fs";
import path from "path";
import { Readable } from "stream";
import { finished } from "stream/promises";
import openai from "./utils/openai.mjs";
import { generateFileNameWithExtension } from "./utils/fileUtils.mjs";
import { openaiErrorHandler } from "./utils/openaiErrorHandler.mjs";

const __dirname = import.meta.dirname;

const prompt =
  "Create a super photo-like realistic image The as two experienced fishermen sit quietly by a sparkling river. The stunning painting captures the scene with exquisite detail: the weathered faces of the fishermen, the worn fishing gear and the serene beauty of the flowing river. The image is rich in warm tones and skillfully rendered textures, emphasizing the rugged beauty of the fishermen and the tranquil environment they inhabit. Each brushstroke radiates a sense of calm and authenticity, inviting viewers to immerse themselves in this peaceful moment on the riverbank.Translated with DeepL.com (free version)";

try {
  const response = await openai.images.generate({
    model: "dall-e-3",
    prompt,
    n: 1,
    size: "1024x1024",
  });

  // console.log(response);

  const imageUrl = response.data[0].url;
  // console.log(imageUrl);

  const dir = path.join(__dirname, "images");
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }

  const fileName = generateFileNameWithExtension({
    prompt,
    url: imageUrl,
    dir,
    extension: "png",
  });
  const filePath = path.join(dir, fileName);

  try {
    // Attempt to download the image
    const imageResponse = await fetch(imageUrl);
    if (!imageResponse.ok)
      throw new Error(`Failed to download image: ${imageResponse.statusText}`);

    // Check if the response is an image
    const contentType = imageResponse.headers.get("content-type");
    if (!contentType || !contentType.startsWith("image/")) {
      throw new Error(
        `The URL does not point to an image. Content-Type: ${contentType}`
      );
    }

    // Create a write stream and pipe the response to it
    const writeStream = fs.createWriteStream(filePath);
    await finished(Readable.fromWeb(imageResponse.body).pipe(writeStream));
    console.log("Successfully saved image:", fileName);
  } catch (error) {
    console.error("Error downloading image:", error);
  }
} catch (error) {
  openaiErrorHandler(error);
}
