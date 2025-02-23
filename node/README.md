# Node.js project for interaction with OpenAI API

This Node.js application is designed for interacting with the OpenAI API. It includes scripts like `completion.mjs` and `images.mjs`, which allow users to access OpenAI's various features, such as generating text completions and images. The application is configured using a `.env` file where users can securely store their OpenAI API key and other necessary settings. With this setup, users can easily run the scripts to leverage OpenAI's API for generating creative content, completing text prompts, and more.

## Prerequisites

- Node.js installed on your machine.
- A `.env` file for environment variables.

## Setting Up the Environment

1. **Install Dependencies**  
   Navigate to your project directory and run the following command to install all required dependencies:

   ```
   npm install
   ```

2. **Create a `.env` file**  
   You can create a `.env` file at the root of your project directory or copy from `.env.sample` if available:

   ```
   cp .env.sample .env
   ```

3. **Insert API Key**  
   Open the `.env` file and add your API key in the following format:

   ```
   OPENAI_API_KEY="Your OpenAI API Key"
   ```

   Replace `Your OpenAI API Key` with the actual API key.

## Running Scripts

You can execute different scripts in your project by using the Node.js interpreter.

### Running `completion.mjs`

To run `completion.mjs`, use the following command:

```
node completion.mjs
```

### Running `images.mjs`

To run `images.mjs`, use the following command:

```
node images.mjs
```

Make sure the required environment variables are set in your `.env` file before running these scripts.
