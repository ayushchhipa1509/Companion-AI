# 🧠 Companion AI: Memory & Personality Engine

A modular AI system that extracts user memory from chat history and transforms responses based on personality styles. Built for demonstrating structured output parsing, memory management, and personality transformation in companion AI systems.

## 📋 project Overview

This project implements:

1. **Memory Extraction Module** - Analyzes 30 chat messages to extract:

   - User preferences (likes, dislikes, habits)
   - Emotional patterns (mood trends, triggers)
   - Facts worth remembering (name, role, constraints, goals)

2. **Personality Engine** - Transforms AI responses using:

   - Selected personality style (Calm Mentor, Witty Friend, Therapist-Style)
   - Extracted user memory for personalization

3. **Before/After Demo** - Shows how responses change with personality transformation

## 🏗️ Architecture

```
Companion AI-repo/
├── modules/
│   ├── __init__.py
│   ├── memory.py          # Memory extraction logic
│   └── personality.py     # Personality transformation logic
├── data/
│   └── sample_chats.json  # 30 sample chat messages
├── app.py                 # Streamlit UI
├── requirements.txt       # Dependencies
└── README.md             # This file
```

## 🎯 Key Features

### Memory Extraction (`modules/memory.py`)

- Uses LangChain with structured JSON output parsing
- Extracts preferences, emotional patterns, and facts
- Returns clean, parseable dictionary structure
- Includes error handling and fallbacks

### Personality Engine (`modules/personality.py`)

- Three personality styles: Calm Mentor, Witty Friend, Therapist-Style
- Transforms responses while maintaining factual accuracy
- Incorporates user memory for personalization
- Modular design for easy extension

### Streamlit UI (`app.py`)

- Interactive memory extraction
- Before/After personality comparison
- Memory visualization (structured display + raw JSON)
- Sample data included for testing

## 🚀 Setup & Installation

### Local Development

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd Assignment
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

## 📖 Usage

1. **Load Chat Messages**

   - Go to "Chat Input" tab
   - Click "Load Sample Chats" or paste your own messages
   - Click "Save Messages"

2. **Extract Memory**

   - Go to sidebar
   - Click "Extract Memory from Chats"
   - View results in "Memory Display" tab

3. **Compare Responses**
   - Go to "Before/After Demo" tab
   - Select personality style in sidebar
   - Enter a question
   - See standard vs. personality-transformed response

## 🎨 Personality Styles

- **Calm Mentor**: Patient, step-by-step guidance with reassurance
- **Witty Friend**: Casual, humorous, and relatable
- **Therapist-Style**: Empathetic, reflective, and supportive
- **Standard AI**: Neutral, professional baseline

## 🔧 Technical Details

### Prompt Design

- **Memory Extraction**: Uses system prompts with clear instructions for structured extraction
- **Personality Transformation**: Maintains factual accuracy while changing tone/style
- **Structured Output**: Uses LangChain's `JsonOutputParser` for reliable parsing

### Memory Persistence

- Uses Streamlit's `st.session_state` for demo purposes
- In production, would use database (Supabase, PostgreSQL) for persistence
- Session state keeps memory alive during the session

### Error Handling

- Graceful fallbacks if API calls fail
- Validation of extracted memory structure
- User-friendly error messages

## 📊 Evaluation Criteria Met

✅ **Reasoning and Prompt Design**

- Clear system prompts with role definition
- Structured instructions for extraction
- Examples and constraints in prompts

✅ **Structured Output Parsing**

- JSON output parser for reliable extraction
- Validated dictionary structure
- Clean separation of preferences, emotions, facts

✅ **Working with User Memory**

- Memory used in personality transformation
- Personalized responses based on extracted insights
- Memory context displayed in UI

✅ **Modular System Design**

- Separate modules for memory and personality
- Clean separation of concerns
- Easy to extend and maintain

## 🛠️ Dependencies

- `streamlit`: Web UI framework
- `langchain`: LLM orchestration
- `langchain-openai`: OpenAI integration
- `langchain-core`: Core LangChain components

## 📝 Notes

- **API Key**: Required for OpenAI API access
- **Model**: Uses `gpt-4o-mini` by default (cost-efficient)
- **Temperature**: Lower (0.3) for memory extraction, higher (0.7) for personality
- **Sample Data**: 30 messages included for testing

## 🔗 Links

- **GitHub Repository**: [Your repo link]
- **Live Demo**: [Your Streamlit Cloud link]

## 📄 License

This project is created for educational/assignment purposes.

---

**Built with ❤️ using Streamlit, LangChain, and OpenAI**
