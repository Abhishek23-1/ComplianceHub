import os
import sys
import threading
import time
import traceback
from pathlib import Path

import httpx
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, Response
import ngrok

from agentmail import AgentMail
from openai import OpenAI

# ----------------------------------------
# Configuration
# ----------------------------------------

PORT = int(os.getenv("PORT", "8000"))
INBOX_USERNAME = os.getenv("INBOX_USERNAME", "myagent")
BASE_DIR = Path(__file__).resolve().parent
ATTACHMENTS_DIR = Path(os.getenv("ATTACHMENTS_DIR", BASE_DIR / "attachments"))

agentmail = AgentMail()

groq = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

app = Flask(__name__)

processed_messages = set()


class ExternalNgrokListener:
    def __init__(self, domain: str):
        self._url = f"https://{domain}"

    def url(self) -> str:
        return self._url


def normalize_webhook_domain(raw_domain: str) -> str:
    return (
        raw_domain.strip()
        .removeprefix("https://")
        .removeprefix("http://")
        .rstrip("/")
    )


def register_webhook(inbox_id: str, webhook_url: str):
    client_id = f"{INBOX_USERNAME}-webhook"

    try:
        existing = agentmail.inboxes.webhooks.list(inbox_id=inbox_id)
        for webhook in getattr(existing, "webhooks", []) or []:
            if getattr(webhook, "url", None) == webhook_url:
                print("Webhook already registered:", webhook_url)
                return webhook
    except Exception:
        pass

    try:
        webhook = agentmail.inboxes.webhooks.create(
            inbox_id=inbox_id,
            url=webhook_url,
            event_types=["message.received"],
            client_id=client_id,
        )
        print("Webhook registered:", webhook_url)
        return webhook
    except Exception as inbox_error:
        try:
            webhook = agentmail.webhooks.create(
                url=webhook_url,
                event_types=["message.received"],
                client_id=client_id,
            )
            print("Webhook registered:", webhook_url)
            return webhook
        except Exception as org_error:
            print("Webhook registration failed:", org_error)
            print("(inbox-scoped attempt:", inbox_error, ")")
            return None


def parse_sender(message: dict) -> tuple[str, str]:
    sender = message.get("from_") or message.get("from") or ""

    if isinstance(sender, list):
        sender = sender[0] if sender else ""

    sender = str(sender).strip()

    if "<" in sender:
        sender_email = sender.split("<")[1].replace(">", "").strip()
        sender_name = sender.split("<")[0].strip() or sender_email.split("@")[0].title()
    else:
        sender_email = sender
        sender_name = sender_email.split("@")[0].title() if sender_email else "there"

    return sender_email, sender_name


def extract_message_body(message: dict) -> str:
    return (
        message.get("text")
        or message.get("body")
        or message.get("preview")
        or message.get("html")
        or ""
    )


def sanitize_filename(name: str) -> str:
    cleaned = os.path.basename(str(name).strip()) or "attachment"
    return "".join(c if c.isalnum() or c in "._-" else "_" for c in cleaned)


def unique_path(directory: Path, filename: str) -> Path:
    path = directory / filename
    if not path.exists():
        return path

    stem = path.stem
    suffix = path.suffix
    counter = 1
    while path.exists():
        path = directory / f"{stem}_{counter}{suffix}"
        counter += 1
    return path


def save_message_attachments(
    inbox_id: str,
    message_id: str,
    attachments,
    sender_email: str,
) -> list[str]:
    if not attachments:
        return []

    ATTACHMENTS_DIR.mkdir(parents=True, exist_ok=True)

    safe_message_id = "".join(
        c if c.isalnum() or c in "-_" else "_"
        for c in message_id
    )[:80]
    sender_folder = sender_email.split("@")[0] if sender_email else "unknown"
    message_dir = ATTACHMENTS_DIR / sanitize_filename(sender_folder) / safe_message_id
    message_dir.mkdir(parents=True, exist_ok=True)

    saved_paths = []

    for attachment in attachments:
        if isinstance(attachment, dict):
            attachment_id = attachment.get("attachment_id")
            filename = attachment.get("filename") or f"{attachment_id}.bin"
        else:
            attachment_id = getattr(attachment, "attachment_id", None)
            filename = getattr(attachment, "filename", None) or f"{attachment_id}.bin"

        if not attachment_id:
            continue

        try:
            info = agentmail.inboxes.messages.get_attachment(
                inbox_id=inbox_id,
                message_id=message_id,
                attachment_id=attachment_id,
            )

            file_path = unique_path(message_dir, sanitize_filename(filename))

            with httpx.Client(timeout=60.0) as client:
                response = client.get(info.download_url)
                response.raise_for_status()
                file_path.write_bytes(response.content)

            saved_paths.append(str(file_path))
            print(f"Saved attachment: {file_path}")

        except Exception as error:
            print(f"Failed to save attachment {attachment_id}: {error}")

    return saved_paths


def start_ngrok_listener(webhook_domain: str):
    use_external = os.getenv("NGROK_EXTERNAL", "").lower() in {"1", "true", "yes"}

    if use_external:
        print(f"Using external ngrok tunnel at {webhook_domain}")
        print(f"Ensure ngrok forwards to port {PORT}, e.g.:")
        print(f"  ngrok http --url={webhook_domain} {PORT}")
        return ExternalNgrokListener(webhook_domain)

    try:
        return ngrok.forward(
            PORT,
            domain=webhook_domain,
            authtoken_from_env=True,
        )
    except ValueError as error:
        message = str(error)
        if "already online" in message or "ERR_NGROK_334" in message:
            print(
                f"Ngrok domain already in use externally; reusing https://{webhook_domain}"
            )
            print(f"Ensure ngrok forwards to port {PORT}, e.g.:")
            print(f"  ngrok http --url={webhook_domain} {PORT}")
            return ExternalNgrokListener(webhook_domain)
        raise


# ----------------------------------------
# Setup AgentMail
# ----------------------------------------

def setup():

    print("Setting up AgentMail...")

    try:
        inbox = agentmail.inboxes.create(
            username=INBOX_USERNAME,
            client_id=f"{INBOX_USERNAME}-inbox"
        )

    except Exception:

        class Inbox:
            pass

        inbox = Inbox()
        inbox.inbox_id = f"{INBOX_USERNAME}@agentmail.to"

    webhook_domain = normalize_webhook_domain(os.getenv("WEBHOOK_DOMAIN", ""))
    listener = start_ngrok_listener(webhook_domain)
    webhook_url = f"{listener.url()}/webhook"
    register_webhook(inbox.inbox_id, webhook_url)

    print()
    print("Inbox :", inbox.inbox_id)
    print("Webhook :", webhook_url)
    print(f"Local server port: {PORT}")
    print()

    return inbox


# ----------------------------------------
# Fetch Thread History
# ----------------------------------------

def get_thread_history(thread_id):

    if not thread_id:
        return ""

    try:

        thread = agentmail.threads.get(thread_id=thread_id)

        messages = getattr(thread, "messages", [])

        history = []

        for msg in messages:

            sender = getattr(msg, "from_", "")

            body = (
                getattr(msg, "text", "")
                or getattr(msg, "body", "")
                or getattr(msg, "html", "")
            )

            if sender and body:
                history.append(
                    f"From: {sender}\n{body}"
                )

        return "\n\n--------------------\n\n".join(history)

    except Exception as e:
        print("Thread fetch failed:", e)
        return ""


# ----------------------------------------
# Generate AI Reply
# ----------------------------------------

def generate_ai_reply(sender_name, subject, body, history, saved_attachments=None):

    attachment_note = ""
    if saved_attachments:
        names = [Path(path).name for path in saved_attachments]
        attachment_note = f"""
The sender included {len(saved_attachments)} attachment(s): {", ".join(names)}.
Acknowledge that you received and saved their attachment(s).
"""

    prompt = f"""
You are an intelligent email assistant.

Previous conversation:

{history}

------------------------

Latest email

Sender: {sender_name}

Subject:
{subject}

Message:
{body}
{attachment_note}
Write a helpful professional reply.

Keep it under 150 words.
"""

    for attempt in range(3):

        try:

            response = groq.chat.completions.create(

                model="llama-3.3-70b-versatile",

                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional email assistant."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=0.7,
                max_tokens=300,
            )

            return response.choices[0].message.content

        except Exception as e:

            print(f"Groq failed ({attempt+1}/3):", e)

            time.sleep(2)

    return f"""
Hi {sender_name},

Thank you for your email.

I have received your message and will respond as soon as possible.

Best regards,
AI Assistant
"""


# ----------------------------------------
# Process Email
# ----------------------------------------

def process_email(message):

    try:

        message_id = message["message_id"]
        inbox_id = message["inbox_id"]

        sender_email, sender_name = parse_sender(message)

        if not sender_email:
            print("Skipping message with no sender")
            return

        if sender_email.lower() == inbox_id.lower():
            print("Skipping message sent by the inbox itself")
            return

        subject = message.get("subject", "(No Subject)")
        body = extract_message_body(message)
        thread_id = message.get("thread_id")
        attachments = message.get("attachments") or []

        print(f"Email received from {sender_email}")

        saved_attachments = save_message_attachments(
            inbox_id=inbox_id,
            message_id=message_id,
            attachments=attachments,
            sender_email=sender_email,
        )

        history = get_thread_history(thread_id)

        reply = generate_ai_reply(
            sender_name,
            subject,
            body,
            history,
            saved_attachments,
        )

        agentmail.inboxes.messages.reply(
            inbox_id=inbox_id,
            message_id=message_id,
            to=[sender_email],
            text=reply
        )

        print("Reply sent.\n")

    except Exception as e:

        print("Processing Error:", e)
        traceback.print_exc()


# ----------------------------------------
# Webhook
# ----------------------------------------

@app.route("/webhook", methods=["POST"])
def webhook():
    """
    Deprecated — use the Next.js route POST /api/webhooks/agentmail instead.
    This legacy endpoint is disabled to prevent unauthenticated duplicate intake.
    """
    return {"error": "Deprecated. Use /api/webhooks/agentmail on the Next.js app."}, 410


# ----------------------------------------
# Run
# ----------------------------------------

if __name__ == "__main__":

    if os.getenv("AGENT_PY_ENABLED", "").lower() not in ("1", "true", "yes"):
        print(
            "agent.py is disabled. Set AGENT_PY_ENABLED=true for local development only."
        )
        sys.exit(0)

    inbox = setup()

    print("=" * 50)
    print("AgentMail AI Auto Reply Agent")
    print("=" * 50)
    print("Inbox:", inbox.inbox_id)
    print("Attachments folder:", ATTACHMENTS_DIR)
    print("Waiting for emails...\n")

    app.run(port=PORT)