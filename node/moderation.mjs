import openai from "./utils/openai.mjs";
import { openaiErrorHandler } from "./utils/openaiErrorHandler.mjs";

const model = "omni-moderation-latest";
const testTextInput = "...replace with some hateful speech...";
const testImageUrl = "...some link to the image in internet...";

try {
  //// TEST 1
  // const response = await openai.moderations.create({
  //   model,
  //   input: testTextInput,
  // });

  // console.log(JSON.stringify(response, null, 2));

  // TEST 2
  const response = await openai.moderations.create({
    model,
    input: [
      { type: "text", text: testTextInput },
      { 
        type: "image_url", 
        image_url: { 
          url: "https://images.wallpaperscraft.com/image/single/lake_mountain_tree_36589_2650x1600.jpg"
        } 
      }, // ✅ исправленный блок
    ],
  });

  console.log(JSON.stringify(response, null, 2));
} catch (error) {
  openaiErrorHandler(error);
}
