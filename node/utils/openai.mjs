import OpenAI from "openai";
import "dotenv/config";
import checkApiKey from "./checkApiKey.mjs";

// console.log(process.env.OPENAI_API_KEY);

checkApiKey();

export default new OpenAI();
