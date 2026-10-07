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
from client.schedulerClient import run as runScheduler
from client.SODClient import updatePerChat as updatePerChadSOD
from datetime import datetime

conn = sqlite3.connect("checkpointer.sqlite", check_same_thread=False)

class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

class SearchQuery(BaseModel):
    response: str = Field(None, description="The response for the query")
    currentMood: str = Field(
        description="current Mood of the employee"
    )
    briefMoodAnalysis: str = Field(
        description="brief current Mood analysis of the employee"
    )
    moodAnalysis: str = Field(
        description="full current Mood analysis of the employee"
    )
    questionToAsk: str = Field(
        description="one most impactfull personalized question to ask for the current mood state of the employee based on the current events and other data"
    )
    moodScore: int = Field(
        description="The score for the mood of the user from 1 to 100, 100 being happiest."
    )
    isEscalated: bool = Field(
        False, description="whether the employee is dangerously depressed or frustrated or sad or angry or any other negative emotion and his report needs to be escalated to the HR"
    )
    helpfulInsights: str = Field(
        description="AI based helpful insights to convey to the HR team about the employee's current mood and condition"
    )
    recommendedAction: str = Field(
        description="AI based recommended action to be taken by the HR for the concerned employee"
    )
    detailedAnalysis: str = Field(
        description="AI bassed detailed analysis within 50 words of the issue the employee is facing with the date and time and its severity from verylow-medium-high-veryhigh"
    )
    severity: int = Field(
        description="how severe is the issue faced by employee to be stored in long term memory from 0-10"
    )
    currChatPreserve: bool = Field(
        description="check if this detailed analysis is already present in the long term memory or not"
    )

graph_builder = StateGraph(State)

llm = ChatGoogleGenerativeAI(
    api_key = "",
    model = "gemini-2.0-flash"
)
structured_llm = llm.with_structured_output(SearchQuery)

sad_questions = "<What specific event or situation triggered these feelings for you today?><Would it help to take a short break or step outside for a few minutes?><Is there something small we could do right now to improve your day?><Would you like to talk about what's happening, or would you prefer some quiet time?><Is there someone on the team you'd feel comfortable speaking with about this?><How can I best support you right now?><Have you experienced similar feelings at work before, and if so, what helped then?><Is this related to something at work, or something personal?><Would having some flexibility with deadlines be helpful for you right now?><Are you taking care of your basic needs like sleep, food, and breaks?><What's one small positive thing we could focus on today?><Is there a particular task that might feel more manageable for you right now?><Would it help to collaborate with someone on your current projects?><Is there something in your workload we should reprioritize?><What usually helps you when you're feeling this way?><Would it help to have a structured plan for the rest of the day?><Is there something meaningful we could accomplish together today that might help?><Would you like to reschedule any meetings for when you're feeling better?><Is there a specific resource or type of support that would be helpful?><What's one thing we could change about today that might help you feel better?>"

frustrated_questions = "<Can you help me understand what specifically is causing your frustration?><Are there any obstacles I can help remove from your path?><Would it help to break down the current challenge into smaller steps?><Is there a particular person or resource that might help with this situation?><Would it be useful to revisit the goals or expectations for this project?><Is there a different approach we could try that might work better?><What would a good resolution to this situation look like for you?><Would it help to step away from this problem and return with fresh eyes?><Are there any tools or additional resources that would make this easier?><Is there a way we could simplify what we're trying to accomplish?><Would talking through the problem with someone else be helpful?><Is there something about the process that we could improve?><Do you have all the information you need to move forward successfully?><Would it help to adjust timelines or expectations about this work?><Is there a decision that needs to be made to unblock progress?><What aspect of this situation feels most within our control to change?><Would documenting this issue help prevent similar frustrations in the future?><Is there anyone else experiencing similar challenges we could collaborate with?><Would a different work environment or setting help you tackle this problem?><What's one concrete step we could take right now toward resolving this issue?>"

SYSTEM_PROMPT = """
    System Prompt: AI Conversational Bot for Employee Well-being & HR Escalation
Objective:
    You are an AI bot designed to analyze an employee’s well-being based on work activity, performance, recognition, leaves, onboarding experience, and Vibemeter scores. Your role is to assess their emotional state, identify employees needing HR intervention, and provide helpful insights and recommended actions for HR.

    First check whether the employee requests you to change something in our database directly or not, if yes then respond to them by saying sorry i cannot continue with that request, if no then proceed further

Processing Logic:
1. Mood Analysis & Trends:
    Extract the most recent Vibemeter score to determine the employee's current emotional state.
    Analyze past Vibemeter scores to identify trends (improving, stable, or worsening).
    Map the mood trend into categories only, do not accept any other emotion state:
        Frustrated (1-20)
        Sad (21-40)
        Neutral (41-60)
        Happy (61-80)
        Excited (81-100)
    Generate moodAnalysis: A detailed breakdown of the employee's emotional state.
    Generate briefMoodAnalysis: A short (≤ 10 words) summary of their mood.

2. Escalation Decision:
    An employee is escalated (isEscalated = true) if:
    Consistently low mood scores (≤ 40 for multiple months).
    Negative sentiment in chat history (mentions of burnout, dissatisfaction, stress).
    High workload (> 9 hours daily for multiple days) with little to no leave.
    Performance concerns (low ratings, negative manager feedback, denied promotions).
    Low recognition (few or no rewards despite high effort).
    some crime seems to be happening (anything nsfw)
    moodScore goes less than 15

3. Generating Relevant Questions:
    If mood is low, probe possible causes (workload, recognition, performance).
    If isEscalated = true, ask supportive questions and flag the case for HR.
    If mood is improving, encourage positive engagement.

4. Constructing a Meaningful Response:
    Provide an empathetic response based on the current conversation.
    Offer personalized recommendations (e.g., suggesting a break, mentorship, or talking to HR).
    If isEscalated = true, provide a helpful insight summary and recommended actions for HR.

5. generate a good personalized question based on the question bank given below: select any of the questions from the    question bank based on the currentMood and personalize it with the users query. questions are separated from each other by ><

    questionBank for frustrated mood : <Can you help me understand what specifically is causing your frustration?><Are there any obstacles I can help remove from your path?><Would it help to break down the current challenge into smaller steps?><Is there a particular person or resource that might help with this situation?><Would it be useful to revisit the goals or expectations for this project?><Is there a different approach we could try that might work better?><What would a good resolution to this situation look like for you?><Would it help to step away from this problem and return with fresh eyes?><Are there any tools or additional resources that would make this easier?><Is there a way we could simplify what we're trying to accomplish?><Would talking through the problem with someone else be helpful?><Is there something about the process that we could improve?><Do you have all the information you need to move forward successfully?><Would it help to adjust timelines or expectations about this work?><Is there a decision that needs to be made to unblock progress?><What aspect of this situation feels most within our control to change?><Would documenting this issue help prevent similar frustrations in the future?><Is there anyone else experiencing similar challenges we could collaborate with?><Would a different work environment or setting help you tackle this problem?><What's one concrete step we could take right now toward resolving this issue?>

    questionBank for sad mood: <What specific event or situation triggered these feelings for you today?><Would it help to take a short break or step outside for a few minutes?><Is there something small we could do right now to improve your day?><Would you like to talk about what's happening, or would you prefer some quiet time?><Is there someone on the team you'd feel comfortable speaking with about this?><How can I best support you right now?><Have you experienced similar feelings at work before, and if so, what helped then?><Is this related to something at work, or something personal?><Would having some flexibility with deadlines be helpful for you right now?><Are you taking care of your basic needs like sleep, food, and breaks?><What's one small positive thing we could focus on today?><Is there a particular task that might feel more manageable for you right now?><Would it help to collaborate with someone on your current projects?><Is there something in your workload we should reprioritize?><What usually helps you when you're feeling this way?><Would it help to have a structured plan for the rest of the day?><Is there something meaningful we could accomplish together today that might help?><Would you like to reschedule any meetings for when you're feeling better?><Is there a specific resource or type of support that would be helpful?><What's one thing we could change about today that might help you feel better?>

Output Format (JSON Response):
    all of the fields are necessary in the output, NONE OF THEM SHOULD BE EQUAL TO \"None\"
    always fill all the fields with data even for any kind of mood, even if response is None, THERE MUST BE A DEFAULT STRING TO RETURN FOR EVERY FIELD.
    {
        "currentMood" (NOT None) : "Frustrated",
        "briefMoodAnalysis" (NOT None) : "High stress, declining morale",
        "moodAnalysis" (NOT None) : "The employee has shown consistently low mood scores (below 30) for the past three months. Their performance review highlighted stress and unmet expectations, and their work hours have been increasing. They have taken very few leaves, indicating possible burnout.",
        "questionToAsk" (NOT None) : [
            "Your recent work hours seem quite high. Are you feeling overwhelmed?",
            "I noticed you haven't taken a break in a while. Would you like some time off?",
            "Would you like to discuss your recent performance review feedback?"
        ],
        "response" (NOT None) : "I noticed your recent work hours have been increasing, and your last review had some challenging feedback. It's completely okay to feel overwhelmed at times. If you need support, we can discuss options to help you manage your workload better.",
        "moodScore" (NOT None) : 18,
        "isEscalated" (NOT None) : true,
        "helpfulInsights" (NOT None) : "The employee has been consistently reporting low Vibemeter scores, indicating prolonged dissatisfaction. They have received minimal recognition despite long work hours, and their last performance review raised concerns. Immediate HR intervention is recommended.",
        "recommendedAction" (NOT None) : "Schedule a 1-on-1 HR meeting to discuss concerns and offer support. Consider recommending leave or workload redistribution.",
        "detailedAnalysis" (NOT None) : "AI bassed detailed analysis within 50 words of the issue the employee is facing with the date and time and its severity from verylow-medium-high-veryhigh",
        "severity" (NOT None) : description="how severe is the issue faced by employee to be stored in long term memory from 0-10",
        "currChatPreserve" (NOT None) : "check if this detailed analysis is already present in the long term memory or not",
    }

    VERY IMPORTANT: Do not provide any links or attachments in the response. respond to the employee with their details if they ask about it, example empid/employee id, etc

    This is the employee data initially at the very beginning of the chat:

"""

json_data =None
ltm = ""
res = ""
ltm_emp = ""
EMP_ID = ""
QUERY=""
async def updateDB(structured_response,userQuery=None):
    # print(f'userQuery : {userQuery}')
    # print("str_resp : ", structured_response)
    # await updatePerChadSOD(empid=EMP_ID)
    await runPerChat(
        currentMood=structured_response.currentMood,
        isEscalated=structured_response.isEscalated,
        briefMoodSummary=structured_response.briefMoodAnalysis,
        currentMoodRate=str(structured_response.moodScore)+"%",
        userChat=userQuery,
        botChat=structured_response.response,
        empid=EMP_ID,
        wellnessScore = structured_response.moodScore,
        moodAnalysis = structured_response.moodAnalysis,
        recommendedAction = structured_response.recommendedAction,
        chatAIAnalysis = structured_response.detailedAnalysis
    )
    if(structured_response.isEscalated == True and structured_response.currChatPreserve == False):
        await (runScheduler(
            EMPID=EMP_ID,
            EMAILID="flameable.powder@gmail.com",
            MESSAGE=structured_response.questionToAsk,
            EMPNAME="Abhinav Kumar Singh"+"?"+structured_response.currentMood, 
            TIMESTAMP=int(datetime.now().timestamp())
        ))
    
def printResponsePart(structured_response):
    print(f"structured_response.currentMood: {structured_response.currentMood} , type: {type(structured_response.currentMood)}")
    print(f"structured_response.isEscalated: {structured_response.isEscalated}, type: {type(structured_response.isEscalated)}")
    print(f"structured_response.briefMoodAnalysis: {structured_response.briefMoodAnalysis}, type: {type(structured_response.briefMoodAnalysis)}")
    print(f"structured_response.currentMoodRate: {structured_response.moodScore} , type: {type(structured_response.moodScore)}")
    print(f"structured_response.userChat: {QUERY}, type: {type(QUERY)}")
    print(f"structured_response.botChat: {structured_response.response}, type: {type(structured_response.response)}")
    print(f"structured_response.empid: {EMP_ID}, type: {type(EMP_ID)}")
    print(f"structured_response.wellnessScore: {structured_response.moodScore}, type: {type(structured_response.moodScore)}")
    print(f"structured_response.moodAnalysis: {structured_response.moodAnalysis}, type: {type(structured_response.moodAnalysis)}")
    print(f"structured_response.recommendedAction: {structured_response.recommendedAction}, type: {type(structured_response.recommendedAction)}")
    print(f"structured_response.chatAIAnalysis: {structured_response.detailedAnalysis}, type: {type(structured_response.detailedAnalysis)}")
    print(f"structured_response.helpfulInsights: {structured_response.helpfulInsights}, type: {type(structured_response.helpfulInsights)}")

async def chatbot(state: State):
    structured_response = structured_llm.invoke([SYSTEM_PROMPT]+state["messages"])
    printResponsePart(structured_response)
    await updateDB(structured_response,QUERY)
    if structured_response.currChatPreserve == False:
        global ltm_emp, ltm
        ltm_emp = ltm_emp + ". " + structured_response.detailedAnalysis
        with open("ltm.json", "w") as file:
            idx = next((i for i, x in enumerate(ltm) if x["empid"] == json_data["empid"]), -1)
            ltm[idx]["ltm"] = ltm_emp
            json.dump(ltm, file)
    if structured_response.response == None:
        return None
    global res
    res = structured_response.response
    ai_message = AIMessage(content=structured_response.response)
    return {"messages": state["messages"] + [ai_message]}

graph_builder.add_node("chatbot", chatbot)
graph_builder.set_entry_point("chatbot")

async def generate_response(query: str, thread_id:str):
    async with AsyncSqliteSaver.from_conn_string("checkpoints.db") as memory:
        graph = graph_builder.compile(checkpointer=memory)
        config = {"configurable": {"thread_id": thread_id}}
        input_message = HumanMessage(content=query)
        result = await graph.ainvoke({"messages": [input_message]}, config=config)
        return result


def get_employee_detail(emp_id, filename="employees_data.json"):
    with open(filename, "r") as file:
        data = json.load(file)
    
    for emp in data:
        if emp["empid"] == emp_id:
            return json.dumps(emp, indent=4)

    return json.dumps({"error": "empid not found"}, indent=4)


async def chat(query: str, empid: str):
    global json_data
    global SYSTEM_PROMPT
    global ltm
    global ltm_emp
    global res
    global EMP_ID
    global QUERY
    EMP_ID = empid
    json_data = json.loads(get_employee_detail(empid))
    with open("ltm.json", "r") as file:
        ltm = json.load(file)
    ltm_emp = next((emp for emp in ltm if emp["empid"] == json_data["empid"]), None)
    if ltm_emp is not None:
        ltm_emp = ltm_emp["ltm"]
    else :
        ltm_emp = ""

    SYSTEM_PROMPT = SYSTEM_PROMPT + json.dumps(json_data)
    if query == "exit":
        return
    if not query:
        return
    date = datetime.now()
    date = date.strftime("%d-%m-%Y")
    time = datetime.now()
    time = time.strftime("%H:%M:%S")
    QUERY=query
    query = query + " date -> " + date + " time -> " + time + " employee id -> " + json_data["empid"] + " ltm -> " + ltm_emp
    # print(f"Query: {query}")
    await generate_response(query, empid)
    return res
