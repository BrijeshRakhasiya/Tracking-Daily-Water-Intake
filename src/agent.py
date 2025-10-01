import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage

# Load .env file
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(
    api_key=GEMINI_API_KEY,  
    model="gemini-2.5-pro",
    temperature=0.5,
)

class WaterIntakeAgent:

    def __init__(self):
        self.history = []

    def analyze_intake(self, intake_ml):
        prompt = f"""
        You are a hydration assistant. 
        The User has consumed {intake_ml} ml of water today.
        Provide a hydration status and suggest if they need to drink more water.
        """
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content
    
if __name__ == "__main__":
    agent = WaterIntakeAgent()
    intake = 1500
    feedback = agent.analyze_intake(intake)
    print(f"Hydration: {feedback}")