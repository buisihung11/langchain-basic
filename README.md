# 🤖 LangChain Streamlit Chatbot

A modern, interactive chatbot built with LangChain and Streamlit that provides a user-friendly web interface for conversing with OpenAI's language models.

## ✨ Features

- **Interactive Web UI**: Beautiful Streamlit interface with chat bubbles
- **Multiple Models**: Support for GPT-3.5-turbo, GPT-4, and GPT-4-turbo
- **Customizable Settings**: Adjust temperature and system messages
- **Chat History**: Persistent conversation history during the session
- **Responsive Design**: Works on desktop and mobile devices
- **Example Prompts**: Quick-start buttons for common use cases

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit the `.env` file and add your OpenAI API key:

```env
OPENAI_API_KEY=your_actual_api_key_here
```

### 3. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 🛠️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | Yes |

### Streamlit Settings

You can customize the following settings in the sidebar:

- **Model**: Choose between GPT-3.5-turbo, GPT-4, or GPT-4-turbo
- **Temperature**: Control randomness (0.0 = focused, 2.0 = creative)
- **System Message**: Set custom instructions for the AI assistant

## 📁 Project Structure

```
chatbot/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env.example       # Environment variables template
├── .env              # Your environment variables (create this)
└── README.md         # This file
```

## 🎯 Usage

1. **Start a conversation**: Type your message in the chat input at the bottom
2. **Use example prompts**: Click the example buttons for quick starts
3. **Adjust settings**: Use the sidebar to change model, temperature, or system message
4. **Clear chat**: Click "Clear Chat" in the sidebar to start fresh

## 🔧 Customization

### Adding New Models

To add support for new models, edit the model selection in `app.py`:

```python
st.session_state.model = st.sidebar.selectbox(
    "Select Model",
    ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview", "your-new-model"],
    index=0
)
```

### Modifying the UI

The app uses custom CSS for styling. You can modify the styles in the `st.markdown()` section of `app.py`.

### Adding New Features

The modular structure makes it easy to add new features:
- Add new functions for specific functionalities
- Extend the `ChatbotApp` class for new capabilities
- Add new sidebar options for additional settings

## 🔒 Security Notes

- Keep your OpenAI API key secure and never commit it to version control
- The `.env` file is gitignored by default
- Consider using Streamlit secrets for production deployments

## 📝 Requirements

- Python 3.8+
- OpenAI API key
- Internet connection for API calls

## 🐛 Troubleshooting

### Common Issues

1. **"OpenAI API key not found"**
   - Make sure you've created a `.env` file with your API key
   - Verify the key is correct and has sufficient credits

2. **"Module not found" errors**
   - Run `pip install -r requirements.txt` to install dependencies
   - Make sure you're using the correct Python environment

3. **Slow responses**
   - Check your internet connection
   - Try reducing the temperature setting
   - Consider using a faster model like GPT-3.5-turbo

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the chatbot!

## 📄 License

This project is open source and available under the MIT License.
