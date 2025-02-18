function checkApiKey() {
  if (!process.env.OPENAI_API_KEY) {
    console.error(
      "Error: The OPENAI_API_KEY environment variable is missing or empty.\nPlease add it to the .env file."
    );
    process.exit(1);
  }
}

export default checkApiKey;
