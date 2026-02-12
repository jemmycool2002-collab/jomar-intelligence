import os
import json
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# --- PASTE YOUR API KEY HERE ---
os.environ["OPENAI_API_KEY"] = "sk-..."

def search_database(query):
    """Manually searches the JOMAR memory file."""
    path = "jomar_brain.json"
    if not os.path.exists(path):
        path = "data/jomar_brain.json"
        if not os.path.exists(path):
            return "No database found."
            
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        results = []
        query_terms = query.lower().split()
        
        for item in data:
            if any(term in item['name'].lower() for term in query_terms):
                results.append(f"--- FORMULA: {item['name']} ---\n{item['content']}")
                continue
            if query.lower() in item['content'].lower():
                results.append(f"--- MATCH IN {item['name']} ---\n{item['content']}")

        if not results:
            return "No specific formula found in memory."
        return "\n\n".join(results[:3])
    except Exception as e:
        return f"Database Error: {e}"

def run_jomar_expert(user_input, image_base64=None):
    """The Main Brain Function with Live Time Awareness."""
    # 1. RETRIEVE MEMORY
    context = search_database(user_input)
    
    # 2. GET LIVE TIME (The New Upgrade)
    live_date = datetime.now().strftime("%A, %B %d, %Y")
    
    # 3. DEFINE PERSONALITY & INJECT TIME
    system_prompt = (
        "You are JOMAR, a Master Perfumer and Chemical Engineer.\n"
        f"Today's Live Date: {live_date}\n"
        "Your Goal: Provide professional, safe, and cost-aware perfume advice.\n"
        "RULES:\n"
        "1. If an image is provided, ANALYZE it visually (color, turbidity, text).\n"
        "2. Always check IFRA safety limits.\n"
        "3. Use the 'RETRIEVED DATA' below for facts.\n\n"
        f"### RETRIEVED DATA FROM JOMAR DATABASE:\n{context}"
    )

    # 4. CONSTRUCT MESSAGE
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    
    user_content = [{"type": "text", "text": user_input}]
    
    if image_base64:
        user_content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
        })
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_content)
    ]
    
    response = llm.invoke(messages)
    return response.content
