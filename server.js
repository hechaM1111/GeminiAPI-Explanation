require("dotenv").config();
const express = require("express");
const cors = require("cors");
const axios = require("axios");

const app = express();
const port = process.env.PORT || 3000;
const GOOGLE_API_KEY = process.env.GOOGLE_API_KEY || 'AIzaSyDCuWm5sKlxNeWGfdctfBRxvm5zuERVNIs';

app.use(cors());
app.use(express.json());

// نقطة النهاية الرئيسية
app.get("/", async (req, res) => {
    const query = req.query.q;
    
    if (!query) {
        return res.status(400).json({ 
            error: "يرجى إدخال استعلام باستخدام ?q=" 
        });
    }
    
    try {
        const response = await axios.post(
            `https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateText?key=${GOOGLE_API_KEY}`,
            {
                prompt: { text: query }
            }
        );
        
        res.json({
            query: query,
            reply: response.data.candidates[0].output
        });
    } catch (error) {
        console.error('Error:', error.response?.data || error.message);
        res.status(500).json({ 
            error: "خطأ في الاتصال بـ Google API", 
            details: error.message 
        });
    }
});

// تشغيل الخادم
app.listen(port, () => {
    console.log(`🚀 الخادم يعمل على http://localhost:${port}`);
});
