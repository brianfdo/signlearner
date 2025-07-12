# SignLearner - Multi-Modal ASL Learning Assistant

An AI-powered app that helps children learn American Sign Language!

## What This App Does

- **Search ASL Videos**: Type any word and find relevant ASL videos
- **Text to ASL**: Convert sentences into ASL video sequences  
- **AI Lesson Plans**: Get personalized learning plans for kids
- **Kid-Friendly**: Colorful, easy-to-use interface designed for children

## 🚀 Multi-Modal RAG Application

SignLearner is a comprehensive **Multi-Modal RAG (Retrieval-Augmented Generation)** system that assists with ASL learning:

### 🧠 Enhanced AI with LangChain
- **Advanced Lesson Generation**: LangChain-powered agents for sophisticated, contextual lesson planning
- **ASL-Specific Querying**: Optimized vector database queries tailored to ASL linguistic patterns
- **Adaptive Learning Paths**: Intelligent curriculum that adapts to individual learning styles and progress

### 👁️ Computer Vision Integration (Coming Soon)
- **Real-Time Gesture Recognition**: MediaPipe-powered hand tracking for live gesture analysis
- **Sign Validation**: Pre-trained computer vision models to assess gesture accuracy
- **Interactive Feedback**: Instant feedback on hand position, movement, and sign correctness
- **Progress Tracking**: Visual analytics of learning improvement over time

### 🎯 Multi-Modal Features (Coming Soon)
- **Video + Gesture Learning**: Watch videos, then practice with real-time validation
- **Voice Commands**: Natural language interaction with the learning assistant
- **Gamification**: Achievement systems and interactive challenges
- **Social Learning**: Share progress and compete with friends
- **Accessibility**: Support for different learning abilities and styles

This represents the next generation of educational technology - where AI, computer vision, and natural language processing combine to create truly personalized learning experiences.

---

## How to Run the App (Current Version)

### Step 1: Install Requirements
- Python 3.11 or newer
- Node.js 16 or newer
- Poetry (install with: `curl -sSL https://install.python-poetry.org | python3 -`)

### Step 2: Start the Backend
```bash
cd backend
poetry install
poetry run uvicorn api.main:app --reload --port 8000
```

### Step 3: Start the Frontend (New Terminal)
```bash
cd signlearner-frontend
npm install
npm start
```

### Step 4: Use the App
1. Open http://localhost:3000 in your browser
2. Type what you want to learn (like "hello world" or "eat food")
3. Click one of the buttons:
   - **Translate to ASL Videos** - See videos for each word
   - **Search ASL Videos** - Find related videos
   - **Generate Lesson Plan** - Get a learning plan

## Example Searches

Try these in the app:
- "hello goodbye"
- "eat food hungry"
- "family mom dad"
- "happy sad angry"
- "school teacher student"
---

Made with ❤️ by Brian Fernando