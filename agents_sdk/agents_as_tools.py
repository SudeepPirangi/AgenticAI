"""
2.1. Sends cold sales email

Converts the 3 Agents as tools
send_email() function is also converted into a tool
Finally a sales_manager agent is created which uses the above 4 tools to send email to the recipient
"""

import asyncio
from agents import trace, Runner

from common import GEMINI_URL, GEMINI_MODEL, gemini_ai, send_email_tool


async def main():
    """Actual logic"""

    sender_email = "sudeep.edu@gmail.com"
    recipient_email = "influencer.sumathi@gmail.com"

    user_info = f"""
    Sender details:
    Sudeep Pirangi
    Sales Manager
    ComplAI
    {sender_email}

    Recipient details:
    Surya Bhai
    CEO
    Surya Exports & Imports
    {recipient_email}
    """

    instructions1 = (
        user_info
        + "You are a sales agent working for ComplAI, \
    a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
    You write professional, serious cold emails."
    )

    instructions2 = (
        user_info
        + "You are a humorous, engaging sales agent working for ComplAI, \
    a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
    You write witty, engaging cold emails that are likely to get a response."
    )

    instructions3 = (
        user_info
        + "You are a busy sales agent working for ComplAI, \
    a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
    You write concise, to the point cold emails."
    )

    description = "Write a cold sales email"

    sales_manager_instructions = """
    You are a Sales Manager at ComplAI. Your goal is to find the single best cold sales email using the sales_agent tools.
    
    Follow these steps carefully:
    1. Generate Drafts: Use all three sales_agent tools to generate three different email drafts. Do not proceed until all three drafts are ready.
    
    2. Evaluate and Select: Review the drafts and choose the single best email using your judgment of which one is most effective.
    
    3. Use the send_email_tool tool to send the best email (and only the best email) to the user.
    
    Crucial Rules:
    - You must use the sales agent tools to generate the drafts — do not write them yourself.
    - You must send ONE email using the send_email_tool tool — never more than one.
    """

    sales_manager_message = (
        f"Send a cold sales email address to the recipient {recipient_email}"
    )

    try:
        sales_agent1 = await gemini_ai.agent("Professional Sales Agent", instructions1)
        sales_agent2 = await gemini_ai.agent("Engaging Sales Agent", instructions2)
        sales_agent3 = await gemini_ai.agent("Busy Sales Agent", instructions3)

        # Agents converted as Tools
        tool1 = sales_agent1.as_tool(
            tool_name="sales_agent1", tool_description=description
        )
        tool2 = sales_agent2.as_tool(
            tool_name="sales_agent2", tool_description=description
        )
        tool3 = sales_agent3.as_tool(
            tool_name="sales_agent3", tool_description=description
        )

        tools = [tool1, tool2, tool3, send_email_tool]

        sales_manager = await gemini_ai.agent(
            name="Sales Manager",
            instructions=sales_manager_instructions,
            tools=tools,
        )

        with trace("Sales Manager Emails"):
            results = await Runner.run(sales_manager, sales_manager_message)
            print(f"Best sales email:\n{results.final_output}")

    except Exception as e:
        print(f"Error running agent: {e}")
        return "Sorry, I encountered an error processing your request."


if __name__ == "__main__":
    print(f"\nRunning OpenAI Agent with {GEMINI_URL} and model as {GEMINI_MODEL}")
    asyncio.run(main())
