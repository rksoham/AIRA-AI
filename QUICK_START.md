# AIRA AI Chatbot - Quick Start Guide

## Prerequisites
- Python 3.10 or higher
- Virtual environment (`.venv-1`) already created
- Windows PowerShell or Command Prompt

## Quick Start (5 minutes)

### 1. Install Conda (if not already installed)
Download from: https://www.anaconda.com/download

### 2. Create Conda Environment
```powershell
conda create -n aira-ai python=3.10 -y
conda activate aira-ai
```

### 3. Install Rasa
```powershell
conda install -c conda-forge rasa=3.6.0 -y
pip install -r requirements.txt
```

### 4. Train Model
```powershell
cd c:\Users\soham\OneDrive\Desktop\AIRA-AI\rasa_minimal
python -m rasa train --domain domain.yml --data nlu.yml --stories stories.yml --config config.yml --out models
```

### 5. Start Rasa Server (Terminal 1)
```powershell
conda activate aira-ai
cd c:\Users\soham\OneDrive\Desktop\AIRA-AI\rasa_minimal
python -m rasa run -m models --enable-api --cors "*" --port 5005
```

### 6. Start Flask Server (Terminal 2)
```powershell
cd c:\Users\soham\OneDrive\Desktop\AIRA-AI
.\.venv-1\Scripts\activate
python app.py
```

### 7. Open Chat UI
Go to: **http://localhost:5000**

---

## Test Messages

Try these to verify it's working:
- "hello" → Should greet you
- "what courses do you offer?" → Should mention courses
- "how much does it cost?" → Should provide fee information
- "tell me about admissions" → Should explain admission process
- "goodbye" → Should say goodbye

---

## Using Batch Scripts (Optional)

Instead of manual terminal commands, you can use Windows batch files:

1. **train_model.bat** - Trains the Rasa model
2. **start_rasa.bat** - Starts Rasa server
3. **start_flask.bat** - Starts Flask server

Just double-click them! (Requires conda environment setup first)

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "rasa command not found" | Activate conda first: `conda activate aira-ai` |
| "Cannot connect to Rasa" | Check that Rasa server is running on port 5005 |
| "Model not found" | Train the model using `python -m rasa train ...` |
| "PyYAML error" | Use Conda instead of pip (avoids Windows build issues) |

---

## File Structure
```
rasa_minimal/
├── domain.yml          # Intent definitions
├── nlu.yml             # Training examples
├── stories.yml         # Dialogue flows
├── config.yml          # ML pipeline
├── rules.yml           # Fallback rules
├── credentials.yml     # Server config
├── actions.py          # Custom handlers
└── models/             # Trained models
```

---

## Next Steps

- Add more NLU training examples to `nlu.yml`
- Customize responses in `domain.yml`
- Create more dialogue flows in `stories.yml`
- Read full guide: `RASA_COMPLETE_SETUP.md`

---

**For detailed setup, see: RASA_COMPLETE_SETUP.md**
