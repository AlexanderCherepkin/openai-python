import { encoding_for_model as encodingForModel } from "tiktoken";

const models = ["o1-mini", "gpt-4o-mini", "gpt-3.5-turbo"];

function countTokens(text, model) {
  const encoding = encodingForModel(model);
  const tokens = encoding.encode(text);
  const tokenCount = tokens.length;
  encoding.free();
  return tokenCount;
}

const testTexts = {
  en: "Creativity and innovation drive the future, inspiring progress and discovery. Every idea starts with a spark, growing into something unique. Together, we can create solutions that shape tomorrow.",
  jp: "創造性と革新は未来を切り拓き、進歩と発見を促します。すべてのアイデアは小さなひらめきから始まり、独自のものに成長していきます。共に、明日を形作る解決策を生み出しましょう。",
  ru: "Креативность и инновации движут будущее, вдохновляя на прогресс и открытия. Каждая идея начинается с искры, превращаясь во что-то уникальное. Вместе мы можем создать решения, формирующие завтра.",
  de: "Kreativität und Innovation treiben die Zukunft voran und inspirieren Fortschritt und Entdeckung. Jede Idee beginnt mit einem Funken und wird zu etwas Einzigartigem. Gemeinsam können wir Lösungen für morgen schaffen.",
  fr: "La créativité et l'innovation façonnent l'avenir, inspirant progrès et découvertes. Chaque idée commence par une étincelle, devenant quelque chose d'unique. Ensemble, nous pouvons créer des solutions pour demain.",
};

models.forEach((model) => {
  console.log("Calculating tokens count for model", model, "\n");

  Object.entries(testTexts).forEach(([lang, testText]) => {
    const tokenCount = countTokens(testText, model);
    const message = `Tokens count for text in "${lang}" with length ${testText.length} is ${tokenCount}`;
    console.log(message);
  });

  console.log("_______________\n");
});
