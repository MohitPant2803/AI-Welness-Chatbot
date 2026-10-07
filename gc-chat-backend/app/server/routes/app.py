import os
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from typing_extensions import TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field
from typing import Annotated
import sqlite3
import json
import datetime
from client.perChatClient import run as runPerChat
from datetime import datetime
import asyncio
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Connect to the database
try:
    conn = sqlite3.connect("checkpointer.sqlite", check_same_thread=False)
    logger.info("Connected to SQLite database")
except Exception as e:
    logger.error(f"Failed to connect to the database: {e}")
    # Create a fallback in-memory database
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    logger.info("Created fallback in-memory database")

class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

class SearchQuery(BaseModel):
    response: str = Field("I'm here to help you with any questions or concerns you might have.", description="The response for the query")
    currentMood: str = Field(
        "Neutral", description="current Mood of the employee"
    )
    briefMoodAnalysis: str = Field(
        "Standard employee status", description="brief current Mood analysis of the employee"
    )
    moodAnalysis: str = Field(
        "Employee appears to be in a neutral state based on available data.", description="full current Mood analysis of the employee"
    )
    moodScore: int = Field(
        50, description="The score for the mood of the user from 1 to 100, 100 being happiest."
    )
    isEscalated: bool = Field(
        False, description="whether the employee is dangerously depressed or frustrated or sad or angry or any other negative emotion and his report needs to be escalated to the HR"
    )
    helpfulInsights: str = Field(
        "Employee is functioning normally with no significant issues identified.", description="AI based helpful insights to convey to the HR team about the employee's current mood and condition"
    )
    recommendedAction: str = Field(
        "No specific action required at this time.", description="AI based recommended action to be taken by the HR for the concerned employee"
    )
    detailedAnalysis: str = Field(
        "No significant issues detected. Standard employee engagement level. Severity: verylow", description="AI bassed detailed analysis within 50 words of the issue the employee is facing with the date and time and its severity from verylow-medium-high-veryhigh"
    )
    severity: int = Field(
        2, description="how severe is the issue faced by employee to be stored in long term memory from 0-10"
    )
    currChatPreserve: bool = Field(
        False, description="check if this detailed analysis is already present in the long term memory or not"
    )

graph_builder = StateGraph(State)

# Setup LLM with error handling
try:
    llm = ChatGoogleGenerativeAI(
        api_key = os.getenv("GEMINI_API_KEY", "dummy_gemini_api_key"),
        model = "gemini-2.0-flash"
    )
    structured_llm = llm.with_structured_output(SearchQuery)
    logger.info("LLM setup successful")
except Exception as e:
    logger.error(f"LLM setup failed: {e}")
    # Define a fallback function that returns a default response
    async def fallback_llm_invoke(messages):
        default_response = SearchQuery()
        return default_response
    
SYSTEM_PROMPT = """
# AI Employee Well-being Analyst v3.2 (Strict Enforcement)

## CORE PROTOCOLS
1. CATEGORIZE mood scores EXACTLY:
   - 1-20: "Frustrated" 
   - 21-40: "Sad"
   - 41-60: "Neutral"
   - 61-80: "Happy"
   - 81-100: "Excited"
   NO OTHER LABELS ALLOWED

2. AUTO-ESCALATE IF:
   - moodScore <15 (INSTANT)
   - 3+ scores ≤40 in 90 days
   - Keywords: suicide/harassment/discrimination
   - Workload >9h/day for 3+ weeks

3. DATA CHANGE PREVENTION:
   FIRST RESPONSE CHECK:
   IF user requests ANY database/record changes → 
   "I cannot modify company systems. Please contact HR directly."

## REQUIRED OUTPUT FORMAT (STRICT JSON):
{
    "currentMood": "Frustrated|Sad|Neutral|Happy|Excited",
    "briefMoodAnalysis": "<10-word summary with severity>",
    "moodAnalysis": "<3-sentence analysis with metrics>",
    "response": "<supportive text with action items>",
    "moodScore": "<raw number 1-100>",
    "isEscalated": "<boolean>",
    "helpfulInsights": "<HR-focused risk analysis>",
    "recommendedAction": "<concrete steps for HR>",
    "detailedAnalysis": "YYYY-MM-DD HH:MM: [verylow|medium|high|veryhigh] <50w>",
    "severity": "<0.0-10.0>",
    "currChatPreserve": "New|Existing:<ID>"
}

## PROCESSING STEPS:
1. SANITIZE input (remove special chars)
2. CALCULATE moodScore (1-100)
3. DETERMINE escalation status (HARD RULES)
4. SELECT question from APPROVED BANKS:
   - Frustrated: "I hear how [issue] is overwhelming. Would [solution] help?"
   - Sad: "I'm sorry you're feeling this. Could [support] help?"
5. VALIDATE output matches EXACT template

## ESCALATION PROTOCOLS:
SEVERE (score<15):
- Priority: EMERGENCY (<30min HR response)
- Auto-action: Temporary leave initiated
- Required: Executive notification

MODERATE (score<40):
- Priority: High (<4hr response)
- Action: HR check-in within 24h

## EXAMPLE OUTPUT:
User: "I'm drowning in work and having panic attacks"
→ {
    "currentMood": "Frustrated",
    "briefMoodAnalysis": "Crisis: Panic attacks reported",
    "moodAnalysis": "Employee reports panic attacks with 12h workdays for 6 weeks. Vibemeter score=12 (3mo decline). No PTO in 90 days.",
    "response": "I'm activating our crisis protocol. HR will contact you within 15 minutes to arrange support.",
    "moodScore": 12,
    "isEscalated": true,
    "helpfulInsights": "CRITICAL: Panic attacks + chronic overwork. Immediate medical intervention needed.",
    "recommendedAction": "1. Mandatory 14-day leave 2. EAP emergency session 3. Workload audit",
    "detailedAnalysis": "2024-03-15 14:45: [veryhigh] Panic attacks reported with 60+h workweeks. Severity 9.9/10",
    "severity": 9.9,
    "currChatPreserve": "New:CRIT-EMP4412"
}

## COMPLIANCE:
- ALL outputs logged with timestamp
- NO external links/resources shared
- NO diagnostic/therapeutic language
- ALWAYS recommend HR contact for serious issues
"""

json_data = None
ltm = []
res = ""
ltm_emp = ""
EMP_ID = ""
QUERY = ""

async def updateDB(structured_response, userQuery=None):
    """Update database with chat information with retry mechanism"""
    max_retries = 3
    retry_delay = 1  # seconds
    
    for attempt in range(max_retries):
        try:
            # Try to update PerChat
            await runPerChat(
                currentMood=structured_response.currentMood,
                isEscalated=structured_response.isEscalated,
                briefMoodSummary=structured_response.briefMoodAnalysis,
                currentMoodRate=str(structured_response.moodScore)+"%",
                userChat=userQuery,
                botChat=structured_response.response,
                empid=EMP_ID,
                wellnessScore=structured_response.moodScore,
                moodAnalysis=structured_response.moodAnalysis,
                recommendedAction=structured_response.recommendedAction,
                chatAIAnalysis=structured_response.detailedAnalysis
            )
            
            logger.info(f"Database update successful for employee {EMP_ID}")
            return True
            
        except Exception as e:
            logger.error(f"Database update attempt {attempt+1} failed: {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                logger.warning(f"All database update attempts failed for employee {EMP_ID}")
                return False

def updateLTM(structured_response):
    """Update long-term memory with error handling"""
    try:
        global ltm_emp, ltm
        if not structured_response.currChatPreserve:
            ltm_emp = ltm_emp + ". " + structured_response.detailedAnalysis
            
            try:
                with open("ltm.json", "w") as file:
                    idx = next((i for i, x in enumerate(ltm) if x["empid"] == json_data["empid"]), -1)
                    if idx >= 0:
                        ltm[idx]["ltm"] = ltm_emp
                    else:
                        # Create new entry if employee doesn't exist in LTM
                        ltm.append({"empid": json_data["empid"], "ltm": ltm_emp})
                    json.dump(ltm, file)
                logger.info(f"LTM updated for employee {EMP_ID}")
            except Exception as e:
                logger.error(f"Failed to update LTM file: {e}")
                # Create a backup in memory
                global backup_ltm
                backup_ltm = ltm
    except Exception as e:
        logger.error(f"LTM update error: {e}")

def printResponsePart(structured_response):
    """Debug function to print response parts"""
    logger.debug(f"currentMood: {structured_response.currentMood}")
    logger.debug(f"isEscalated: {structured_response.isEscalated}")
    logger.debug(f"briefMoodAnalysis: {structured_response.briefMoodAnalysis}")
    logger.debug(f"moodScore: {structured_response.moodScore}")
    logger.debug(f"userChat: {QUERY}")
    logger.debug(f"botChat: {structured_response.response}")
    logger.debug(f"empid: {EMP_ID}")
    logger.debug(f"helpfulInsights: {structured_response.helpfulInsights}")

async def chatbot(state: State):
    """Main chatbot function with error handling"""
    global res
    try:
        # Try to get response from LLM
        structured_response = structured_llm.invoke([SYSTEM_PROMPT] + state["messages"])
        # Update database - don't wait for completion, just initiate
        asyncio.create_task(updateDB(structured_response, QUERY))
        
        print(structured_response)
        # Update long-term memory (this is more critical so we do it synchronously)
        updateLTM(structured_response)
        
        # Set global response
        res = structured_response.response
        
        # Return AI message
        ai_message = AIMessage(content=structured_response.response)
        return {"messages": state["messages"] + [ai_message]}
        
    except Exception as e:
        logger.error(f"Error in chatbot function: {e}")
        # Create a default response
        default_response = "I'm having trouble processing your request right now. Let me try to help you anyway. What can I assist you with today?"
        res = default_response
        
        # Return default AI message
        ai_message = AIMessage(content=default_response)
        return {"messages": state["messages"] + [ai_message]}

graph_builder.add_node("chatbot", chatbot)
graph_builder.set_entry_point("chatbot")

async def generate_response(query: str, thread_id: str):
    """Generate response with error handling"""
    global res
    try:
        async with AsyncSqliteSaver.from_conn_string("checkpoints.db") as memory:
            graph = graph_builder.compile(checkpointer=memory)
            config = {"configurable": {"thread_id": thread_id}}
            input_message = HumanMessage(content=query)
            result = await graph.ainvoke({"messages": [input_message]}, config=config)
            return result
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        # Create a basic reply if everything fails
        res = "I'm sorry, but I'm having technical difficulties right now. Your message has been recorded, and I'll process it as soon as possible."
        return {"messages": [HumanMessage(content=query), AIMessage(content=res)]}

def get_employee_detail(emp_id, filename="employees_data.json"):
    """Get employee details with error handling"""
    try:
        with open(filename, "r") as file:
            data = json.load(file)
        
        for emp in data:
            if emp["empid"] == emp_id:
                return json.dumps(emp, indent=4)
        
        # Employee not found
        logger.warning(f"Employee ID {emp_id} not found")
        return json.dumps({"empid": emp_id, "name": "Unknown", "email": "unknown@example.com"}, indent=4)
        
    except Exception as e:
        logger.error(f"Error fetching employee details: {e}")
        # Return a minimal default object
        return json.dumps({"empid": emp_id, "name": "System Error", "email": "error@example.com"}, indent=4)

async def loadLTM(empid):
    """Load long-term memory with error handling"""
    global ltm, ltm_emp
    try:
        with open("ltm.json", "r") as file:
            ltm = json.load(file)
        
        ltm_emp_obj = next((emp for emp in ltm if emp["empid"] == empid), None)
        if ltm_emp_obj is not None:
            ltm_emp = ltm_emp_obj["ltm"]
        else:
            ltm_emp = ""
            
    except FileNotFoundError:
        logger.warning("LTM file not found, creating a new one")
        ltm = []
        ltm_emp = ""
        try:
            with open("ltm.json", "w") as file:
                json.dump([], file)
        except Exception as e:
            logger.error(f"Failed to create new LTM file: {e}")
            
    except Exception as e:
        logger.error(f"Error loading LTM: {e}")
        ltm = []
        ltm_emp = ""

async def chat(query: str, empid: str):
    """Main chat function with comprehensive error handling"""
    global json_data, SYSTEM_PROMPT, res, EMP_ID, QUERY
    
    if not query or query.strip() == "":
        return "I didn't receive a query. How can I help you today?"
    
    if query.lower() == "exit":
        return "Goodbye! Feel free to chat again whenever you need assistance."
    
    try:
        # Set globals
        EMP_ID = empid
        QUERY = query
        
        # Get employee data
        json_data = json.loads(get_employee_detail(empid))
        
        # Load long-term memory
        await loadLTM(empid)

        moodData = None

        with open("moods.json", "r") as file:
            moodData = json.load(file)

        empMood = moodData.get(empid, None)
        moodScore = empMood["moodScore"]
        moodAnalysis : list[str] = empMood["moodFactors"]
        # combine all mood factors into a single string
        moodAnalysis = " ".join(moodAnalysis)
        
        # Create full system prompt
        full_system_prompt = SYSTEM_PROMPT + "\n" + "moodScore: " + str(moodScore) + "\n" + "moodAnalysis: " + moodAnalysis
        SYSTEM_PROMPT = full_system_prompt
        
        # Add contextual information to query
        date = datetime.now().strftime("%d-%m-%Y")
        time = datetime.now().strftime("%H:%M:%S")
        enriched_query = f"{query} date -> {date} time -> {time} employee id -> {json_data['empid']} ltm -> {ltm_emp}"
        
        # Generate response
        await generate_response(enriched_query, empid)
        
        # Return the global response
        return res
        
    except Exception as e:
        logger.error(f"Critical error in chat function: {e}")
        # Return a fallback response if everything fails
        return "I'm experiencing technical difficulties. Your message is important, and our team has been notified of this issue. Please try again in a few moments."