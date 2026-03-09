import streamlit as st
from langchain_classic.agents import create_react_agent, AgentExecutor   # ← both here
from langchain_core.tools import Tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic import hub
import os

st.set_page_config(page_title="Smart Shopper Agent", page_icon="🛒", layout="wide")

st.title("🛒 Smart Shopper Agent Demo")
st.markdown("**Watch the AI Agent think and use tools in real-time!**")

# ────────────────────────────────────────────────
# Sidebar
# ────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Google Gemini API Key", type="password", 
                           value=os.environ.get("GOOGLE_API_KEY", "YOUR_API_KEY_HERE"))
    
    if api_key:
        os.environ["GOOGLE_API_KEY"] = api_key
        st.success("✅ API Key Set!")
    else:
        st.warning("⚠️ Enter your Gemini API key to start")
    
    st.markdown("---")
    st.markdown("### Available Products:")
    st.markdown("""
    - iPhone 15 ($799)
    - iPhone 15 Pro ($999)
    - Samsung Galaxy S24 ($799)
    - MacBook Air ($1199)
    - AirPods Pro ($249)
    - iPad Air ($599)
    - PlayStation 5 ($499)
    - Nintendo Switch ($299)
    """)

# ────────────────────────────────────────────────
# Session state
# ────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ────────────────────────────────────────────────
# Tools
# ────────────────────────────────────────────────
def search_price(product_name: str) -> str:
    """Searches for current product prices online."""
    prices = {
        "iphone 15": "$799",
        "iphone 15 pro": "$999",
        "samsung galaxy s24": "$799",
        "macbook air": "$1199",
        "airpods pro": "$249",
        "ipad air": "$599",
        "playstation 5": "$499",
        "nintendo switch": "$299"
    }
    
    product_lower = product_name.lower().strip()
    for key, price in prices.items():
        if key in product_lower:
            return f"Current price for {product_name}: {price}"
    
    return f"Price for {product_name} not found. Available products: iPhone 15, iPhone 15 Pro, Samsung Galaxy S24, MacBook Air, AirPods Pro, iPad Air, PlayStation 5, Nintendo Switch"

def calculator(expression: str) -> str:
    """Performs mathematical calculations."""
    try:
        clean_expr = expression.replace("$", "").replace(",", "").strip()
        result = eval(clean_expr, {"__builtins__": {}})  # safer eval
        return f"${float(result):.2f}"
    except Exception as e:
        return f"Calculation error: {str(e)}"

def calculate_discount(price_and_discount: str) -> str:
    """Calculates discount. Input: 'price, discount_percent' like '799, 20'"""
    try:
        parts = price_and_discount.replace("$", "").split(",")
        if len(parts) != 2:
            return "Error: please provide 'price, discount_percent' like '799, 20'"
        price = float(parts[0].strip())
        discount_pct = float(parts[1].strip())
        
        discount_amount = price * (discount_pct / 100)
        final_price = price - discount_amount
        
        return (f"Original: ${price:.2f} | "
                f"Discount: {discount_pct}% | "
                f"You save: ${discount_amount:.2f} | "
                f"Final price: ${final_price:.2f}")
    except Exception as e:
        return f"Error: {str(e)}. Format example: '799, 20'"

tools = [
    Tool(
        name="PriceSearch",
        func=search_price,
        description="Useful for finding the current price of a product. Input should be the product name (e.g. 'iPhone 15', 'MacBook Air')."
    ),
    Tool(
        name="Calculator",
        func=calculator,
        description="Useful for math calculations. Input is a math expression like '799 * 0.8' or '1000 - 200'."
    ),
    Tool(
        name="DiscountCalculator",
        func=calculate_discount,
        description="Calculates discounted price. Input format: 'original_price, discount_percentage' e.g. '799, 20'"
    )
]

# ────────────────────────────────────────────────
# UI Layout
# ────────────────────────────────────────────────
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("💬 Ask the Agent")
    
    st.markdown("**Try these examples:**")
    sample_questions = [
        "What's the price of iPhone 15?",
        "Find the price of MacBook Air and calculate 25% student discount",
        "Which is cheaper: iPhone 15 with 20% off or Samsung Galaxy S24 with 15% off?",
        "I have $600 budget. Can I buy iPad Air with 10% discount?"
    ]
    
    selected = st.selectbox("Quick examples:", [""] + sample_questions)
    
    user_query = st.text_input(
        "Your question:",
        value=selected if selected else "",
        placeholder="e.g., What's the best deal on AirPods Pro?"
    )
    
    c1, c2 = st.columns(2)
    with c1:
        run_agent = st.button("🤖 Run Agent", type="primary", use_container_width=True)
    with c2:
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

with col2:
    st.subheader("🧠 Agent Thinking")
    thinking_area = st.empty()

# ────────────────────────────────────────────────
# Run agent when button pressed
# ────────────────────────────────────────────────
if run_agent and user_query.strip() and api_key:
    with st.spinner("Agent is working..."):
        try:
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",      # changed to more stable model name
                temperature=0,
                google_api_key=api_key
            )

            prompt = hub.pull("hwchase17/react")

            agent = create_react_agent(
                llm=llm,
                tools=tools,
                prompt=prompt
            )

            agent_executor = AgentExecutor(
                agent=agent,
                tools=tools,
                verbose=True,                      # still shows in terminal (useful for you)
                handle_parsing_errors=True,
                max_iterations=6,
                return_intermediate_steps=True     # ← this is the key addition
            )

            result = agent_executor.invoke({"input": user_query})

            answer = result["output"]
            intermediate_steps = result.get("intermediate_steps", [])  # list of (action, observation) tuples

            # Store both final answer and steps
            st.session_state.messages.append({
                "query": user_query,
                "response": answer,
                "steps": intermediate_steps          # ← new field
            })

        except Exception as e:
            st.error(f"Error running agent:\n{str(e)}")
            st.info("Common fixes:\n• Check API key\n• Try model='gemini-1.5-flash'\n• pip install -U langchain-classic langchain-google-genai")

# ────────────────────────────────────────────────
# Show results + intermediate steps
# ────────────────────────────────────────────────
if st.session_state.messages:
    latest = st.session_state.messages[-1]
    
    with thinking_area.container():
        st.markdown("### 🧠 Agent's Thinking Process")

        if latest.get("steps"):
            with st.expander("Show detailed steps (Thought → Action → Observation)", expanded=True):
                for i, step in enumerate(latest["steps"], 1):
                    action, observation = step

                    # Action / Thought part
                    st.markdown(f"**Step {i} — Thought & Action**")
                    st.code(action.log.strip(), language="text")   # usually contains Thought + Action + Action Input

                    # Tool / Observation
                    st.markdown("**Observation**")
                    st.code(str(observation), language="text")

                    st.markdown("---")

        st.markdown("### ✅ Final Answer")
        st.success(latest["response"])

    # History (optional — can also show steps there if you want)
    if len(st.session_state.messages) > 1:
        with st.expander("📜 Previous Queries"):
            for i, msg in enumerate(reversed(st.session_state.messages[:-1]), 1):
                st.markdown(f"**Q{i}:** {msg['query']}")
                st.markdown(f"**A:** {msg['response']}")
                if msg.get("steps"):
                    with st.expander("Steps for this query"):
                        for j, step in enumerate(msg["steps"], 1):
                            action, obs = step
                            st.markdown(f"**Step {j}**")
                            st.code(action.log.strip())
                            st.code(str(obs))
                st.markdown("---")
# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: gray;">
    <p>Gen AI Workshop Demo | LangChain + Gemini</p>
    </div>
    """,
    unsafe_allow_html=True
)