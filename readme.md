# Postify Commit

A Python tool that analyzes your GitHub commits from the last 30 days and generates a professional LinkedIn post summarizing your development activities using AI.

## Features

- Fetches commits from GitHub for a specified time period
- Groups commits by repository
- Generates AI-powered summaries optimized for LinkedIn posts
- Uses Groq AI for intelligent content generation

## Prerequisites

- Python 3.10 or higher
- A GitHub account
- A Groq AI API account

## Installation

1. Clone this repository

2. Create a Python virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment:

   **On Windows:**

   ```bash
   venv\Scripts\activate
   ```

   **On macOS/Linux:**

   ```bash
   source venv/bin/activate
   ```

4. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

### 1. Create GitHub Personal Access Token

1. Go to [GitHub Settings > Developer settings > Personal access tokens > Tokens (classic)](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Give it a descriptive name (e.g., "Postify Commit Access")
4. Select the following scopes:
   - `repo` (Full control of private repositories)
5. Click "Generate token"
6. **Important**: Copy the token **immediately** - you won't be able to see it again!

### 2. Get Groq AI API Key

1. Go to [Groq Console](https://console.groq.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Click "Create API Key"
5. Give it a name and copy the key

### 3. Set Up Environment Variables

1. Copy the example environment file:

```bash
cp .env.example .env
```

2. Edit the `.env` file with your credentials:

```
GITHUB_USERNAME=your_github_username
GITHUB_TOKEN=ghp_your_github_token_here
AI_API_KEY=gsk_your_groq_api_key_here
```

Replace:

- `your_github_username` -> with your actual GitHub username
- `ghp_your_github_token_here` -> with the token you generated
- `gsk_your_groq_api_key_here` -> with your Groq API key

## Usage

Run the script:

```bash
python postify_commit.py
```

The script will:

1. Fetch all your commits from the last defined (default: 30) days
2. Display the total number of commits found
3. Generate a LinkedIn-ready post summarizing your activities

## Security Notes

- Never commit your `.env` file to version control (it's already in `.gitignore`)
- Keep your tokens and API keys secure

## License

This project is open source and available for personal and commercial use.
