from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import google.generativeai as genai
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///interview_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
db = SQLAlchemy(app)
    # Configure Gemini AI directly with API key
GEMINI_API_KEY = "AIzaSyB2MvIWhBllHCdqIdC4xGrR7JtBIlMLHwo"  
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Simple Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    question_text = db.Column(db.Text, nullable=False)
    ai_response = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# AI Assistant Class
class InterviewAI:
    def __init__(self):
        self.model = model
    
    def get_interview_response(self, question, category="General"):
        """Generate AI response for interview questions"""
        prompt = f"""
        You are an expert interview coach and AI assistant. A user has asked the following interview-related question:
        
        Category: {category}
        Question: {question}
        
        Please provide a comprehensive, helpful response that includes:
        1. A direct answer to their question
        2. Practical tips and advice
        3. Example responses if applicable
        4. Best practices for interviews
        5. Common mistakes to avoid
        
        Keep your response professional, encouraging, and actionable. Format your response in a clear, easy-to-read manner.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating AI response: {e}")
            return """I apologize, but I'm having trouble generating a response right now. Here are some general tips:
            
            1. Research the company and role thoroughly
            2. Practice common interview questions
            3. Prepare specific examples using the STAR method
            4. Dress appropriately and arrive early
            5. Ask thoughtful questions about the role and company
            
            Please try asking your question again, or check if your Gemini API key is properly configured."""
    
    def generate_practice_question(self, category="Technical"):
        """Generate a practice interview question"""
        prompt = f"""
        Generate a realistic {category} interview question that would be commonly asked in job interviews.
        Make it specific and relevant to the {category} category.
        Just return the question without any additional formatting or explanation.
        Make it challenging but fair for someone preparing for interviews.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error generating question: {e}")
            # Fallback questions for each category
            fallback_questions = {
                "Technical": "Explain the difference between a stack and a queue data structure, and provide use cases for each.",
                "Behavioral": "Tell me about a time when you had to work with a difficult team member. How did you handle the situation?",
                "HR": "Why are you interested in this position and our company?",
                "Situational": "How would you handle a situation where you disagree with your manager's decision?",
                "General": "What are your greatest strengths and how do they relate to this role?"
            }
            return fallback_questions.get(category, fallback_questions["General"])
    
    def get_answer_help(self, question, category="General"):
        """Get help on how to answer a specific question"""
        prompt = f"""
        A user is practicing for an interview and needs help answering this {category} question:
        "{question}"
        
        Please provide:
        1. A framework or approach for answering this question
        2. Key points they should cover
        3. A sample answer structure
        4. Tips for making their answer stand out
        5. Common mistakes to avoid when answering this type of question
        
        Be specific and actionable in your advice.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error generating answer help: {e}")
            return "I'm having trouble generating specific help right now. Generally, structure your answer with a clear beginning, middle, and end. Use specific examples and quantify your achievements when possible."

# Initialize AI Assistant
ai_assistant = InterviewAI()

    # Routes
@app.route('/')
def index():
        return render_template('index.html')
    
@app.route('/register', methods=['GET', 'POST'])
def register():
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            
            # Check if user exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('Email already registered!')
                return redirect(url_for('register'))
            
            # Create new user
            user = User(name=name, email=email)
            db.session.add(user)
            db.session.commit()
            
            session['user_id'] = user.id
            session['user_name'] = user.name
            flash('Registration successful!')
            return redirect(url_for('dashboard'))
        
        return render_template('register.html')
    
@app.route('/login', methods=['GET', 'POST'])
def login():
        if request.method == 'POST':
            email = request.form['email']
            user = User.query.filter_by(email=email).first()
            
            if user:
                session['user_id'] = user.id
                session['user_name'] = user.name
                flash('Login successful!')
                return redirect(url_for('dashboard'))
            else:
                flash('User not found!')
        
        return render_template('login.html')
    
@app.route('/logout')
def logout():
        session.clear()
        flash('Logged out successfully!')
        return redirect(url_for('index'))
    
@app.route('/dashboard')
def dashboard():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        user_questions = Question.query.filter_by(user_id=session['user_id']).order_by(Question.created_at.desc()).limit(5).all()
        return render_template('dashboard.html', questions=user_questions)
    
@app.route('/ask', methods=['GET', 'POST'])
def ask_question():
        if request.method == 'POST':
            question_text = request.form['question']
            category = request.form.get('category', 'General')
            
            # Get AI response
            ai_response = ai_assistant.get_interview_response(question_text, category)
            
            # Save to database
            question = Question(
                user_id=session.get('user_id'),
                question_text=question_text,
                ai_response=ai_response,
                category=category
            )
            db.session.add(question)
            db.session.commit()
            
            return render_template('result.html', 
                                question=question_text, 
                                response=ai_response, 
                                category=category,
                                question_id=question.id)
        
        return render_template('ask.html')
    
@app.route('/practice')
def practice():
        category = request.args.get('category', 'Technical')
        practice_question = ai_assistant.generate_practice_question(category)
        return render_template('practice.html', question=practice_question, category=category)
    
@app.route('/get_answer_help', methods=['POST'])
def get_answer_help():
        question_text = request.form['question']
        category = request.form.get('category', 'General')
        
        # Get AI help for answering the question
        help_response = ai_assistant.get_answer_help(question_text, category)
        
        return render_template('answer_help.html', 
                            question=question_text, 
                            help_response=help_response, 
                            category=category)
    
@app.route('/history')
def history():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        user_questions = Question.query.filter_by(user_id=session['user_id']).order_by(Question.created_at.desc()).all()
        return render_template('history.html', questions=user_questions)
    
@app.route('/api/quick_question', methods=['POST'])
def quick_question():
        """API endpoint for quick questions without saving to database"""
        data = request.get_json()
        question_text = data.get('question', '')
        category = data.get('category', 'General')
        
        if not question_text:
            return {'error': 'Question is required'}, 400
        
        try:
            ai_response = ai_assistant.get_interview_response(question_text, category)
            return {
                'question': question_text,
                'response': ai_response,
                'category': category
            }
        except Exception as e:
            return {'error': 'Failed to generate response'}, 500
    
    # Initialize database
def init_db():
        with app.app_context():
            db.create_all()
            print("Database initialized successfully!")
    
if __name__ == '__main__':
        # Check if API key is set
        if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
            print("⚠️  WARNING: Please replace 'YOUR_GEMINI_API_KEY_HERE' with your actual Gemini API key!")
            print("   Get your API key from: https://makersuite.google.com/app/apikey")
            print("   Then replace the GEMINI_API_KEY variable in app.py")
        else:
            print("✅ Gemini API key configured!")
        
        init_db()
        print("🚀 Starting AI Interview Assistant...")
        print("📝 Visit http://localhost:5000 to start using the application")
        app.run(debug=True)