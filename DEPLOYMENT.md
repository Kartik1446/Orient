# Deployment Guide for Orient TechStack Guide

This guide covers deploying the Orient TechStack Guide application to various platforms.

## Prerequisites

- Python 3.8 or higher
- Git repository with the application code
- OpenRouter API key (for AI features)

## Deployment Options

### 1. Streamlit Cloud (Recommended)

Streamlit Cloud is the easiest way to deploy Streamlit applications.

#### Steps:

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Add deployment files"
   git push origin main
   ```

2. **Deploy to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository
   - Set the main file path to: `web_agent.py`
   - Click "Deploy"

3. **Configure Environment Variables** (Optional)
   - In your Streamlit Cloud app settings
   - Add environment variable: `OPENROUTER_API_KEY`
   - Set the value to your OpenRouter API key

#### Benefits:
- Free tier available
- Automatic deployments from GitHub
- Built-in HTTPS
- Easy environment variable management

### 2. Heroku

#### Steps:

1. **Install Heroku CLI**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create Heroku app**
   ```bash
   heroku create your-app-name
   ```

3. **Add buildpacks**
   ```bash
   heroku buildpacks:add heroku/python
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

5. **Set environment variables**
   ```bash
   heroku config:set OPENROUTER_API_KEY=your_api_key_here
   ```

### 3. Railway

#### Steps:

1. **Connect to Railway**
   - Go to [railway.app](https://railway.app)
   - Connect your GitHub repository

2. **Configure deployment**
   - Set the start command: `streamlit run web_agent.py --server.port=$PORT`
   - Add environment variable: `OPENROUTER_API_KEY`

3. **Deploy**
   - Railway will automatically deploy on push to main

### 4. Vercel

#### Steps:

1. **Create vercel.json**
   ```json
   {
     "builds": [
       {
         "src": "web_agent.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "web_agent.py"
       }
     ]
   }
   ```

2. **Deploy**
   ```bash
   npm i -g vercel
   vercel
   ```

## Environment Variables

For AI features to work, set the following environment variable:

- `OPENROUTER_API_KEY`: Your OpenRouter API key (starts with `sk-or-v1-`)

## Local Development

To run locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run web_agent.py
```

## Troubleshooting

### Common Issues:

1. **Import errors**: Ensure all dependencies are in `requirements.txt`
2. **API key issues**: Check environment variable configuration
3. **Port conflicts**: Use `--server.port` flag to specify port
4. **Memory issues**: Consider upgrading deployment plan

### Debugging:

- Check application logs in your deployment platform
- Test API key functionality using the "Test API Key" button
- Verify environment variables are set correctly

## Security Notes

- Never commit API keys to version control
- Use environment variables for sensitive data
- Enable HTTPS in production
- Consider rate limiting for API calls

## Support

For deployment issues:
1. Check the platform's documentation
2. Review application logs
3. Test locally first
4. Verify all dependencies are included
