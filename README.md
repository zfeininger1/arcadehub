# 🎮 Arcade Hub

A modern arcade-themed web application featuring games and tools with AWS serverless backend integration.

## 📁 Project Structure

```
MathToThePowerOf/
├── public/                 # Frontend files (served by web server)
│   ├── index.html         # Home page (arcade hub)
│   ├── games/            # Game pages
│   │   └── snake.html    # Snake game
│   └── tools/            # Utility tools
│       └── calculator.html  # Quantum calculator
│
├── backend/              # AWS Lambda functions
│   ├── lamdba_function.py        # Calculator operations handler
│   └── snake_score_lambda.py    # Snake game score handler
│
├── docs/                 # Documentation
│   └── AWS_SETUP_GUIDE.md       # AWS deployment guide
│
├── archives/             # Old/backup files
│   └── *.zip            # Archived zip files
│
└── README.md            # This file
```

## 🚀 Getting Started

### Local Development

1. **Start local server**:
   ```bash
   python3 -m http.server 8000
   ```

2. **Open in browser**:
   ```
   http://localhost:8000/public/
   ```

### Project Components

#### 🏠 Home Page
- Arcade-themed landing page
- Links to all games and tools
- Retro neon aesthetic with animated grid background

#### 🎮 Games
- **Snake**: Classic snake game with neon graphics
  - Score tracking with AWS DynamoDB
  - Real-time score display
  - Click-to-start gameplay

#### 🛠️ Tools
- **Quantum Calculator**: Advanced math operations
  - Addition, subtraction, multiplication, division, exponentiation
  - Modern glassmorphism UI
  - AWS Lambda backend for calculations

## ☁️ AWS Backend

### Architecture
- **DynamoDB Tables**:
  - `PowerOfMathDatabase` - Calculator results
  - `SnakeScores` - Game scores
  
- **Lambda Functions**:
  - `calculator-handler` - Processes math operations
  - `snake-score-handler` - Saves and retrieves game scores

- **API Gateway**:
  - REST API endpoints for frontend-backend communication
  - CORS enabled for local development

### Deployment
See [AWS_SETUP_GUIDE.md](docs/AWS_SETUP_GUIDE.md) for detailed deployment instructions.

## 🎨 Design Features

- **Arcade Theme**: Retro gaming aesthetic with modern polish
- **Neon Effects**: Glowing text and borders
- **Glassmorphism**: Semi-transparent frosted glass effects
- **Smooth Animations**: Hover effects, transitions, and micro-interactions
- **Responsive**: Works on desktop and mobile devices

## 🛠️ Tech Stack

### Frontend
- HTML5
- CSS3 (Vanilla, no frameworks)
- JavaScript (ES6+)
- Google Fonts (Press Start 2P, Poppins)

### Backend
- AWS Lambda (Python 3.12)
- Amazon DynamoDB
- AWS API Gateway
- Boto3 (AWS SDK for Python)

## 📝 Development

### Adding New Games
1. Create new HTML file in `public/games/`
2. Add link to home page (`public/index.html`)
3. Follow existing design patterns for consistency

### Adding New Tools
1. Create new HTML file in `public/tools/`
2. Add link to home page (`public/index.html`)
3. Consider adding Lambda function if backend needed

## 📦 File Descriptions

| File | Purpose |
|------|---------|
| `public/index.html` | Arcade hub home page |
| `public/games/snake.html` | Snake game with score tracking |
| `public/tools/calculator.html` | Math operations calculator |
| `backend/lamdba_function.py` | Lambda for calculator operations |
| `backend/snake_score_lambda.py` | Lambda for game scores |
| `docs/AWS_SETUP_GUIDE.md` | AWS deployment documentation |

## 🎯 Future Enhancements

- [ ] User authentication with AWS Cognito
- [ ] Leaderboards for Snake game
- [ ] More games (Tetris, Pong, etc.)
- [ ] Additional tools
- [ ] Score analytics dashboard
- [ ] Multiplayer capabilities

## 📄 License

This is a personal project for learning AWS serverless architecture and modern web development.

---

**Built with ❤️ using AWS Serverless Architecture**
