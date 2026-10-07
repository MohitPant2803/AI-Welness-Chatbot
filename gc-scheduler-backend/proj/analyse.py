import json
import google.generativeai as genai
import re
import difflib
import time

DELAY = 1

def analyze_employee_moods(json_path="moods.json", output_path="employee_questions.json"):
    genai.configure(api_key="")

    QUESTION_BANK = {
        "I. Workload & Role Clarity": [
            "How would you describe your current workload? Is it manageable, overwhelming, or unpredictable?",
            "Have your responsibilities shifted recently in ways that feel unclear or unsustainable?",
            "What percentage of your workweek is spent on tasks that align with your core strengths?",
            "Do you have the tools/resources needed to meet client or project expectations effectively?",
            "How often do you work beyond standard hours to meet deadlines?",
            "Are you involved in overlapping projects that create conflicting priorities?"
        ],
        "II. Recognition & Career Growth": [
            "When was the last time you received meaningful recognition for your contributions?",
            "Do you feel your career progression aligns with your current role and aspirations?",
            "What opportunities (training, certifications, mentorship) would help you grow here?",
            "How transparent is the promotion process in your practice area?",
            "Have you discussed your career goals with your manager in the past six months?",
            "Do you feel your skills are underutilized in your current projects?"
        ],
        "III. Well-being & Work-Life Balance": [
            "How often does work stress impact your personal life or health?",
            "Are you able to fully disconnect during vacations or weekends?",
            "Have you taken unplanned leave recently due to work-related fatigue?",
            "How supportive is Deloitte in accommodating personal/family needs?",
            "What changes to your schedule or workload would improve your well-being?",
            "Do you feel pressured to prioritize client demands over personal health?"
        ],
        "IV. Relationships & Team Dynamics": [
            "How would you rate your communication with your direct manager?",
            "Do you feel comfortable voicing concerns or ideas in team settings?",
            "Have recent team changes (e.g., new leadership, restructuring) affected your morale?",
            "How inclusive is your team's culture in valuing diverse perspectives?",
            "Are there unresolved conflicts affecting collaboration on your projects?",
            "Do you feel socially connected to your peers, or isolated in your role?"
        ],
        "V. Alignment & Feedback": [
            "What feedback have you received that you feel was unfair or unclear?",
            "How actionable is the feedback you receive from managers or peers?",
            "Would you recommend Deloitte as a workplace to others in your network? Why or why not?",
            "What one policy change would most improve your day-to-day experience?",
            "If you could redesign your role, what would you prioritize?",
            "How closely do your daily tasks align with Deloitte's stated values (e.g., sustainability, integrity)?"
        ]
    }

    ALL_QUESTIONS = []
    for category, questions in QUESTION_BANK.items():
        ALL_QUESTIONS.extend(questions)

    def load_mood_data(file_path):
        """Load mood data from JSON file."""
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading mood data: {e}")
            return {}

    def get_question_with_gemini(employee_id, mood_data):
        """Use Gemini to analyze mood factors and select a relevant question from the question bank."""
        employee_mood = mood_data.get(employee_id, {})
        if not employee_mood:
            return f"No data found for employee {employee_id}", None
        
        mood_score = employee_mood.get("moodScore", 0)
        mood_factors = employee_mood.get("moodFactors", [])

        print(f"Analyzing employee {employee_id}...")
        
        formatted_questions = []
        for category, questions in QUESTION_BANK.items():
            formatted_questions.append(f"{category}")
            for i, question in enumerate(questions, 1):
                formatted_questions.append(f"{i}. {question}")
            formatted_questions.append("")
        
        questions_text = "\n".join(formatted_questions)
        
        prompt = f"""
        Analyze the following employee mood data and select exactly ONE question from the question bank 
        that would be most appropriate to ask this employee based on their mood factors and score.
        
        Employee ID: {employee_id}
        Mood Score: {mood_score}/100
        Mood Factors:
        {json.dumps(mood_factors, indent=2)}
        
        Question Bank:
        {questions_text}
        
        IMPORTANT: Your task is to select EXACTLY ONE question from the question bank above that is most relevant 
        to this employee's situation. DO NOT modify or create new questions. The selected question must be word-for-word 
        from the question bank. Now PERSONALIZE that question with user's moodScore and moodFactors
        
        Consider:
        - Their mood score ({mood_score}/100) indicates their overall satisfaction
        - Negative indicators in the mood factors (items with negative values)
        - Positive indicators in the mood factors (items with positive values)
        - Areas where they might need additional support
        
        Format your response ONLY as:
        QUESTION: [copy and paste the exact question from the question bank]
        """
        
        model = genai.GenerativeModel('gemini-2.0-flash')
        try:
            response = model.generate_content(prompt)
            response_text = response.text
            
            question_match = re.search(r"QUESTION:\s*(.+?)(?=CATEGORY:|$)", response_text, re.DOTALL)
            category_match = re.search(r"CATEGORY:\s*(.+?)(?=REASON:|$)", response_text, re.DOTALL)
            reason_match = re.search(r"REASON:\s*(.+)", response_text, re.DOTALL)
            
            if question_match:
                question = question_match.group(1).strip()
                category = category_match.group(1).strip() if category_match else "Unknown"
                reason = reason_match.group(1).strip() if reason_match else ""
                
                if question in ALL_QUESTIONS:
                    return question, {"category": category, "reason": reason}
                else:
                    closest_match = difflib.get_close_matches(question, ALL_QUESTIONS, n=1, cutoff=0.7)
                    if closest_match:
                        return closest_match[0], {"category": category, "reason": reason + " (Matched to closest question in bank)"}
                    else:
                        return "Could not match to a question in the question bank", None
            else:
                return "Could not parse a clear question from Gemini's response", None
            
        except Exception as e:
            return f"Error getting question recommendation: {e}", None

    def analyze_all_employees(mood_data):
        """Analyze all employees and generate recommended questions."""
        results = {}
        for employee_id in mood_data.keys():
            employee_mood = mood_data.get(employee_id, {})
            if not employee_mood:
                return f"No data found for employee {employee_id}", None

            mood_score = employee_mood.get("moodScore", 0)
            if mood_score > 45:
                continue
            question, metadata = get_question_with_gemini(employee_id, mood_data)
            time.sleep(DELAY)
            results[employee_id] = {
                "recommended_question": question,
                "mood_score": mood_data[employee_id].get("moodScore", 0),
                "email":"",
                "name":""
            }
        return results

    print("Starting employee mood analysis...")
    
    mood_data = load_mood_data(json_path)
    if not mood_data:
        print("No mood data available. Please check the file path.")
        return {}
    
    print(f"Analyzing {len(mood_data)} employees...")
    results = analyze_all_employees(mood_data)
    
    with open(output_path, "w") as outfile:
        json.dump(results, outfile, indent=2)
    
    print("\nAnalysis complete.")

if __name__ == "__main__":
    analyze_employee_moods()
