"""
2. Sends cold sales emails

Uses 3 Agents to generate 3 email bodies
A 4th Agent calls sales email picker is used to select one best email of those 3
Finally a function to send emails is called to send the selected email to the recipient
"""

import asyncio
from agents import trace, Runner

from common import GEMINI_URL, GEMINI_MODEL, gemini_ai, send_email


def split_subject_body(text):
    """Splits email subject and body from the text"""
    lines = text.splitlines()
    subject = None
    body_lines = []
    found_subject = False
    for line in lines:
        if not found_subject and line.startswith("Subject:"):
            subject = line[len("Subject:") :].strip()
            found_subject = True
            continue
        if found_subject:
            body_lines.append(line)
    body = "\n".join(body_lines).strip()
    return subject, body


async def main():
    """Sends email"""

    user_info = """
    Sender details:
    Sudeep Pirangi
    Sales Manager
    ComplAI
    sudeep_edu@yahoo.com

    Recipient details:
    Surya Bhai
    CEO
    Surya Exports & Imports
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

    sales_picker_instructions = (
        "You pick the best cold sales email from the given options. \
    Imagine you are a customer and pick the one you are most likely to respond to. \
    Do not give an explanation; reply with the selected email only."
    )

    prompt = "Write a cold sales email"

    try:
        sales_agent1 = await gemini_ai.agent("Professional Sales Agent", instructions1)
        sales_agent2 = await gemini_ai.agent("Engaging Sales Agent", instructions2)
        sales_agent3 = await gemini_ai.agent("Busy Sales Agent", instructions3)

        sales_picker = await gemini_ai.agent("sales_picker", sales_picker_instructions)

        with trace("Selection from sales people"):
            results = await asyncio.gather(
                Runner.run(sales_agent1, prompt),
                Runner.run(sales_agent2, prompt),
                Runner.run(sales_agent3, prompt),
            )
            outputs = [result.final_output for result in results]

            emails = "Cold sales emails:\n\n" + "\n\nEmail:\n\n".join(outputs)

            best = await Runner.run(sales_picker, emails)

            print(f"Best sales email:\n{best.final_output}")

        recipient = "sudeep_edu@yahoo.com"
        subject, email_body = split_subject_body(best.final_output)

        if not subject:
            subject = "ComplAI SOC2 compliance services"

        email_response = send_email(
            sender_email="sudeep.edu@gmail.com",
            recipient_email=recipient,
            subject=subject,
            body=email_body,
        )

        if email_response == 202:
            print("Email sent successfully to", recipient)

    except Exception as e:
        print(f"Error running agent: {e}")
        return "Sorry, I encountered an error processing your request."


if __name__ == "__main__":
    print(f"\nRunning OpenAI Agent with {GEMINI_URL} and model as {GEMINI_MODEL}")
    asyncio.run(main())
