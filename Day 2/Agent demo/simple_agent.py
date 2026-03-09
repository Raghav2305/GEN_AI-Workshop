from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain import hub
from langchain.agents import create_tool_calling_agent, AgentExecutor

# ────────────────────────────────────────────────
# 1. Define ONE very simple tool
# ────────────────────────────────────────────────
@tool
def multiply(a: float, b: float) -> float:
    """Multiplies two numbers.
    Use this when you need to calculate a × b."""
    return a * b

tools = [multiply]

# ────────────────────────────────────────────────
# 2. Create the language model
# ────────────────────────────────────────────────
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",           # or "gemini-1.5-pro" / "gemini-2.5-flash" etc.
    temperature=0,
    google_api_key="YOUR_API_KEY_HERE",  # ← use your real key
)

# ────────────────────────────────────────────────
# 3. Load a good prompt template for tool calling
# ────────────────────────────────────────────────
prompt = hub.pull("hwchase17/openai-tools-agent")

# ────────────────────────────────────────────────
# 4. Create the agent (tool-calling version – correct for Gemini)
# ────────────────────────────────────────────────
agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

# ────────────────────────────────────────────────
# 5. Create the executor that runs the agent + tools
# ────────────────────────────────────────────────
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,               # ← shows thinking steps – very useful for teaching
    handle_parsing_errors=True
)

# ────────────────────────────────────────────────
# 6. Run some example questions
# ────────────────────────────────────────────────
questions = [
    "What is 17 × 24?",
    "Multiply 8.5 by 12",
    "How much is 250 times 6?",
    "I have no idea what 19 × 45 is",
]

print("\n" + "="*60 + "\n")

for q in questions:
    print(f"Question: {q}")
    print("-" * 50)
    
    result = agent_executor.invoke({"input": q})
    
    print("Final answer:", result["output"])
    print("\n" + "="*60 + "\n")