
# AI Agent Platform – Documentation

## 1. 📘 Introduction
The **AI Agent Platform** is a modular productivity application powered by AI, featuring tools such as a writing assistant, code assistant, image generator, text-to-speech converter, and presentation generator. It provides an interactive frontend (Streamlit) and a FastAPI-based backend, offering a unified AI toolset for content creators, developers, and researchers.

## 2. 🧱 System Architecture

**Components:**
- **Backend** (FastAPI) — API services for AI-powered features.
- **Frontend** (Streamlit) — User-facing application interface.
- **Database** (SQLite) — Local data persistence.
- **Environment Configuration** (.env) — Manages API keys and sensitive settings.

**Flow:**
```
User ─▶ Streamlit UI ─▶ FastAPI ─▶ AI Modules ─▶ Results
                             │
                          SQLite
```

## 3. 📂 Project Structure

```
ai-agent-platform/
├── app/                 # FastAPI backend services
├── frontend/            # Streamlit frontend interface
├── commands/            # CLI utilities (optional)
├── requirements.txt     # Project dependencies
├── .env, .env.save      # Environment configs
├── ai_platform.db       # SQLite database
└── README.md            # Project overview
```

## 4. ⚙️ Setup & Installation

### Prerequisites:
- Python 3.8+
- pip
- (optional) virtualenv

### Installation Steps:
1. **Clone the Repository**
   ```bash
   git clone https://github.com/kartavya4874/ai-agent-platform.git
   cd ai-agent-platform
   ```
2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Environment Variables**
   ```bash
   cp .env.save .env
   ```
   Add API keys and configurations in `.env` as required.

4. **Run Backend**
   ```bash
   cd app
   uvicorn main:app --reload
   ```

5. **Run Frontend**
   ```bash
   cd frontend
   streamlit run app.py
   ```

## 5. 🧩 Module Workflows & Functionality

### ✍️ Writing Assistant
- **Purpose:** Generates articles, summaries, or creative content.
- **Frontend:** writing_tool.py  
- **Backend:** POST request to `/generate-text`
- **Workflow:**  
  - User submits topic and instructions.
  - Frontend sends request to backend.
  - AI model generates content.
  - Response displayed in the frontend.

### 💻 Code Assistant
- **Purpose:** Generates, autocompletes, or explains code.
- **Frontend:** code_assistant.py
- **Backend:** POST request to `/generate-code`
- **Workflow:**  
  - User enters code prompt or context.
  - Request sent to backend.
  - AI responds with code block or explanation.
  - Displayed in frontend editor.

### 🔊 Text-to-Speech (TTS)
- **Purpose:** Converts text to spoken audio.
- **Frontend:** text_to_speech.py
- **Backend:** POST request to `/tts`
- **Workflow:**  
  - User enters text.
  - Backend converts text using TTS libraries.
  - Audio played or downloaded via frontend.

### 🖼️ Image Generator
- **Purpose:** Generates AI-powered images from text prompts.
- **Frontend:** image_generator.py
- **Backend:** POST request to `/generate-image`
- **Workflow:**  
  - User provides image description.
  - Backend invokes image generation model.
  - Image returned and rendered in frontend.

### 📽️ PPT Generator
- **Purpose:** Creates slide content for presentations using AI.
- **Frontend:** ppt_generator.py
- **Backend:** POST request to `/generate-ppt`
- **Workflow:**  
  - User submits topic and slides count.
  - AI generates slide content outlines.
  - Results presented as downloadable or viewable text blocks.


**Example Endpoints:**

| Method | Endpoint          | Description                |
|--------|-------------------|----------------------------|
| POST   | /generate-text     | AI text generation          |
| POST   | /generate-code     | AI code generation          |
| POST   | /tts               | Text-to-speech conversion   |
| POST   | /generate-image    | AI-based image creation      |
| POST   | /generate-ppt      | AI-powered presentation content |

## 7. 🗃 Database Schema

**Database:** ai_platform.db (SQLite)

**Key Tables:**
- users — stores user preferences and authentication data.
- history — logs actions, prompts, and AI responses.
- files — references saved/generated assets.

**Tool:** Use DB Browser for SQLite to inspect the schema.

## 8. 📊 Testing & Validation

- Test backend endpoints using Swagger (/docs).
- Test frontend modules via Streamlit interface.
- Validate environment variables by running both backend and frontend without errors.

## 9. 🚀 Deployment

**Backend:**
- Host using Uvicorn + Gunicorn on services like Render, Heroku, or EC2.

**Frontend:**
- Deploy via Streamlit Community Cloud or containerize using Docker.

## 10. ❓ Troubleshooting

| Problem                       | Solution                              |
|--------------------------------|----------------------------------------|
| Missing API keys               | Check .env setup                     |
| Backend not responding         | Ensure Uvicorn is running on port 8000 |
| Streamlit UI not loading       | Confirm Python version and Streamlit installation |
| Database not updating          | Check SQLite file permissions and path |

## 📬 Contact

For any queries, suggestions, or contributions:

- 📧 Email: kartavyabaluja453@gmail.com
