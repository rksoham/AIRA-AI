const express = require('express');
const mysql = require('mysql2/promise');
const cors = require('cors');
const bodyParser = require('body-parser');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(express.static('public'));

// Database connection
const dbConfig = {
    host: 'localhost',
    user: 'root', // your MySQL username
    password: '', // your MySQL password
    database: 'aira_chatbot'
};

// Create database connection pool
let db;
async function initializeDatabase() {
    try {
        db = await mysql.createConnection(dbConfig);
        console.log('Connected to MySQL database');
    } catch (error) {
        console.error('Database connection failed:', error);
        process.exit(1);
    }
}

// Serve main page
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Chatbot API endpoint
app.post('/api/chat', async (req, res) => {
    const { message } = req.body;
    
    if (!message || message.trim() === '') {
        return res.json({ answer: 'Please enter a valid question.' });
    }

    try {
        const userQuestion = message.trim().toLowerCase();
        
        // Search for exact or similar questions in the database
        const [rows] = await db.execute(
            `SELECT question, answer FROM faqs 
             WHERE LOWER(question) LIKE ? OR LOWER(question) LIKE ? OR LOWER(question) LIKE ?`,
            [`%${userQuestion}%`, `${userQuestion}%`, `%${userQuestion}`]
        );

        if (rows.length > 0) {
            // Return the first matching result
            return res.json({ answer: rows[0].answer });
        } else {
            // No match found - try keyword matching
            const keywords = userQuestion.split(' ').filter(word => word.length > 3);
            
            if (keywords.length > 0) {
                const keywordConditions = keywords.map(() => 'LOWER(question) LIKE ?').join(' OR ');
                const keywordParams = keywords.map(keyword => `%${keyword}%`);
                
                const [keywordRows] = await db.execute(
                    `SELECT question, answer FROM faqs WHERE ${keywordConditions} ORDER BY 
                    (CASE WHEN LOWER(question) LIKE ? THEN 1 ELSE 0 END) DESC LIMIT 1`,
                    [...keywordParams, `%${userQuestion}%`]
                );

                if (keywordRows.length > 0) {
                    return res.json({ answer: keywordRows[0].answer });
                }
            }
            
            // Fallback response
            return res.json({ 
                answer: "Sorry, I don't have information about that yet. Please contact the college administration for more details." 
            });
        }
    } catch (error) {
        console.error('Database error:', error);
        return res.json({ 
            answer: "I'm experiencing technical difficulties. Please try again later." 
        });
    }
});

// Health check endpoint
app.get('/api/health', (req, res) => {
    res.json({ status: 'OK', message: 'AIRA Chatbot is running' });
});

// Initialize server
async function startServer() {
    await initializeDatabase();
    app.listen(PORT, () => {
        console.log(`AIRA Chatbot server running on http://localhost:${PORT}`);
    });
}

startServer();