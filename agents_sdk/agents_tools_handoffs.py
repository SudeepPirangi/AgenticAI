"""
2.2. Sends cold sales email in HTML format

Converts the 3 Agents as tools
Has 2 more agents that generate subject and html body of email
A function tool that sends html body to the recipient
Finally an Email Manager agent is created which uses all the above tools to send HTML email
"""

import asyncio
from agents import trace, Runner

from common import perplexity_ai, gemini_ai, send_email_tool


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

    subject_instructions = "You can write a subject for a cold sales email. \
    You are given a message and you need to write a subject for an email that is likely to get a response."

    html_instructions = "You can convert a text email body to an HTML email body. \
    You are given a text email body which might have some markdown \
    and you need to convert it to an HTML email body with simple, clear, compelling layout and design."

    email_manager_instructions = "You are an email formatter and sender. You receive the body of an email to be sent. \
    You first use the subject_writer tool to write a subject for the email, then use the html_converter tool to convert the body to HTML. \
    Finally, you use the send_html_email tool to send the email with the subject and HTML body."

    sales_manager_instructions = """
    You are a Sales Manager at ComplAI. Your goal is to find the single best cold sales email using the sales_agent tools.
    
    Follow these steps carefully:
    1. Generate Drafts: Use all three sales_agent tools to generate three different email drafts. Do not proceed until all three drafts are ready.
    
    2. Evaluate and Select: Review the drafts and choose the single best email using your judgment of which one is most effective.
    You can use the tools multiple times if you're not satisfied with the results from the first try.
    
    3. Handoff for Sending: Pass ONLY the winning email draft to the 'Email Manager' agent. The Email Manager will take care of formatting and sending.
    
    Crucial Rules:
    - You must use the sales agent tools to generate the drafts — do not write them yourself.
    - You must hand off exactly ONE email to the Email Manager — never more than one.
    """

    sales_manager_message = (
        f"Send a cold sales email address to the recipient {recipient_email}"
    )

    try:
        # 3 different sales agents
        sales_agent1 = await perplexity_ai.agent(
            "Professional Sales Agent", instructions1
        )
        sales_agent2 = await perplexity_ai.agent("Engaging Sales Agent", instructions2)
        sales_agent3 = await perplexity_ai.agent("Busy Sales Agent", instructions3)

        # Tools that generate 3 different email bodies
        tool1 = sales_agent1.as_tool(
            tool_name="sales_agent1", tool_description=description
        )
        tool2 = sales_agent2.as_tool(
            tool_name="sales_agent2", tool_description=description
        )
        tool3 = sales_agent3.as_tool(
            tool_name="sales_agent3", tool_description=description
        )

        # Subject writer and HTML Converter agents
        subject_writer = await perplexity_ai.agent(
            name="Email subject writer", instructions=subject_instructions
        )
        html_converter = await perplexity_ai.agent(
            name="HTML email body converter", instructions=html_instructions
        )

        # Tools to generate subject and html body
        subject_tool = subject_writer.as_tool(
            tool_name="subject_writer",
            tool_description="Write a subject for a cold sales email",
        )
        html_tool = html_converter.as_tool(
            tool_name="html_converter",
            tool_description="Convert a text email body to an HTML email body",
        )

        html_email_tools = [subject_tool, html_tool, send_email_tool]

        # Agent that takes an email content and generates its
        # subject and HTML body and send it to the recipient
        emailer_agent = await gemini_ai.agent(
            name="Email Manager",
            instructions=email_manager_instructions,
            tools=html_email_tools,
            handoff_description="Convert an email to HTML and send it",
        )

        sales_content_tools = [tool1, tool2, tool3]
        handoffs = [emailer_agent]

        # Sales Manager agent who orchestrates all the process/workflow
        sales_manager = await gemini_ai.agent(
            name="Sales Manager",
            instructions=sales_manager_instructions,
            tools=sales_content_tools,
            handoffs=handoffs,
        )

        with trace("Automated SDR"):
            results = await Runner.run(sales_manager, sales_manager_message)
            print(f"Best sales email:\n{results.final_output}")

    except Exception as e:
        print(f"Error running agent: {e}")
        return "Sorry, I encountered an error processing your request."


if __name__ == "__main__":
    asyncio.run(main())
