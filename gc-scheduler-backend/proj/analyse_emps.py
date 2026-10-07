import json
import time
import re
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key='')
model = genai.GenerativeModel('gemini-2.0-flash')

# Configuration
REQUEST_DELAY = 3  # Seconds between API calls (adjust based on your quota)
MAX_RETRIES = 3    # Max retry attempts for failed analyses

SYSTEM_PROMPT = """
You are an HR analytics expert analyzing employee mood scores (0-100) based on multiple data points.
Consider these factors logically:

1. **Work Patterns** (Activity Data):
   - Optimal work hours: 6-9 hrs/day (positive)
   - Excessive hours (>10) or low hours (<5) (negative)
   - Communication frequency (messages/emails)
   - Meeting engagement

2. **Recognition & Growth**:
   - Reward points and awards received
   - Promotion consideration status
   - Performance rating trends

3. **Well-being Indicators**:
   - Leave frequency and duration
   - Vibe score history and trends
   - Recent response date freshness

4. **Sentiment Signals**:
   - Manager feedback tone
   - Onboarding experience
   - Training completion status

5. **Temporal Patterns**:
   - Recent improvements/declines
   - Consistency in performance
   - Reward frequency over time

Calculation Rules:
- Start with base score 50
- Add/subtract points based on factors below
- Ensure final score stays 0-100
- Give weightage: Work Patterns (30%), Recognition (25%), Well-being (20%), Sentiment (15%), Temporal (10%)

Provide output ONLY in this JSON format:
{"moodScore": number, "reasons": [string]}
"""

def safe_get(data, *keys, default=None):
    """Safely navigate nested dictionaries/lists"""
    for key in keys:
        try:
            data = data[key]
        except (KeyError, TypeError, IndexError):
            return default
    return data

def analyze_employee(employee_data, attempt=1):
    emp_id = safe_get(employee_data, 'employee_id', default='UNKNOWN')
    
    # Prepare analysis text with safe data access
    text_data = f"""
    Employee Analysis for {emp_id}:
    
    **Onboarding**
    - Joined: {safe_get(employee_data, 'onboarding', 'joining_date', default='N/A')}
    - Feedback: {safe_get(employee_data, 'onboarding', 'onboarding_feedback', default='N/A')}
    - Training Completed: {safe_get(employee_data, 'onboarding', 'initial_training_completed', default='No')}
    
    **Leaves (Last 6 months)**
    - Total leaves: {len(safe_get(employee_data, 'leaves', default=[]))}
    - Recent leave: {safe_get(employee_data, 'leaves', -1, 'leave_type', default='None')}
    
    **Performance**
    - Ratings: {[safe_get(r, 'performance_rating', default=0) for r in safe_get(employee_data, 'performance_reviews', default=[])]}
    - Promotion Considered: {any(str(safe_get(r, 'promotion_consideration', default='No')).lower() == 'yes' for r in safe_get(employee_data, 'performance_reviews', default=[]))}
    
    **Activity (Last 30 days)**
    - Avg work hours: {sum(safe_get(a, 'work_hours', default=0) for a in safe_get(employee_data, 'activities', default=[])) / max(1, len(safe_get(employee_data, 'activities', default=[])))}
    - Daily engagements: {sum(safe_get(a, 'teams_messages_sent', default=0) + safe_get(a, 'emails_sent', default=0) for a in safe_get(employee_data, 'activities', default=[]))}
    
    **Rewards**
    - Total points: {sum(safe_get(r, 'reward_points', default=0) for r in safe_get(employee_data, 'rewards', default=[]))}
    - Awards won: {len(safe_get(employee_data, 'rewards', default=[]))}
    
    **Vibe History**
    - Recent score: {safe_get(employee_data, 'vibe_responses', -1, 'vibe_score', default=0)}
    - Score trend: {[safe_get(v, 'vibe_score', default=0) for v in safe_get(employee_data, 'vibe_responses', default=[])]}
    """
    
    try:
        print(f"\nAnalyzing {emp_id} (Attempt {attempt})...")
        response = model.generate_content(SYSTEM_PROMPT + text_data)
        
        # Extract JSON from response
        response_text = response.text.strip()
        json_match = re.search(r'\{[\s\S]*\}', response_text)
        
        if not json_match:
            raise ValueError("No JSON found in response")
            
        result = json.loads(json_match.group())
        
        if not isinstance(result, dict) or 'moodScore' not in result:
            raise ValueError("Invalid response format")
        
        print(f"✅ {emp_id} Mood Score: {result['moodScore']}")
        return result
        
    except Exception as e:
        print(f"⚠️ Attempt {attempt} failed for {emp_id}: {str(e)}")
        
        if attempt < MAX_RETRIES:
            time.sleep(REQUEST_DELAY * attempt)  # Exponential backoff
            return analyze_employee(employee_data, attempt + 1)
            
        print(f"❌ Max retries reached for {emp_id}")
        return {"moodScore": None, "reasons": ["Analysis failed after retries"]}

def main():
    # Load employee data
    try:
        with open('employees.json', 'r') as f:
            employees = json.load(f)
        print(f"\nLoaded data for {len(employees)} employees")
    except Exception as e:
        print(f"❌ Failed to load employees.json: {str(e)}")
        return

    # Process employees
    results = {}
    for i, (emp_id, data) in enumerate(employees.items(), 1):
        print(f"\nProcessing employee {i}/{len(employees)} ({emp_id})")
        
        result = analyze_employee(data)
        results[emp_id] = {
            'moodScore': result.get('moodScore'),
            'moodFactors': result.get('reasons', [])
        }
        
        time.sleep(REQUEST_DELAY)
        print(f"⏳ Waiting {REQUEST_DELAY} seconds before next request...")

    # Save results
    try:
        with open('employees_with_mood.json', 'w') as f:
            json.dump(results, f, indent=2)
        print("\n🎉 Analysis completed successfully!")
        print(f"Results saved to employees_with_mood.json")
    except Exception as e:
        print(f"❌ Failed to save results: {str(e)}")

if __name__ == "__main__":
    main()
