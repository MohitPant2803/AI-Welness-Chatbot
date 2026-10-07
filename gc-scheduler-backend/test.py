import json

def find_low_mood_employees(json_path="moods.json", threshold=45):
    """
    Find all employees with mood scores below the specified threshold.
    
    Args:
        json_path (str): Path to the moods.json file
        threshold (int): Mood score threshold (employees below this will be returned)
        
    Returns:
        list: List of tuples containing (employee_id, mood_score)
    """
    # Load the mood data
    try:
        with open(json_path, 'r') as file:
            mood_data = json.load(file)
    except Exception as e:
        print(f"Error loading mood data: {e}")
        return []
    
    # Find employees with low mood scores
    low_mood_employees = []
    
    for emp_id, emp_data in mood_data.items():
        mood_score = emp_data.get("moodScore", 0)
        if mood_score < threshold:
            low_mood_employees.append((emp_id, mood_score))
    
    # Sort by mood score (lowest first)
    low_mood_employees.sort(key=lambda x: x[1])
    
    return low_mood_employees

# Example usage
if __name__ == "__main__":
    low_mood_emps = find_low_mood_employees()
    
    if low_mood_emps:
        print(f"Found {len(low_mood_emps)} employees with mood scores below 45:")
        for emp_id, score in low_mood_emps:
            print(f"Employee {emp_id}: {score}")
    else:
        print("No employees found with mood scores below 45.")