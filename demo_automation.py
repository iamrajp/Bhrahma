"""
Automated Demo Script for Bhrahma
Run this to generate sample interactions for demo video
"""
import requests
import time
import json
from datetime import datetime

# Configuration
API_URL = "http://localhost:8000"  # Change to Railway URL if deployed
SESSION_ID = f"demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

def print_banner(text):
    """Print a formatted banner"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def send_message(content):
    """Send a message to Bhrahma"""
    print(f"📤 USER: {content}")
    print("-" * 60)

    response = requests.post(
        f"{API_URL}/chat",
        json={"content": content, "session_id": SESSION_ID}
    )

    if response.status_code == 200:
        result = response.json()
        print(f"✅ Queued: Task {result['task_id']}")

        # Wait for response
        print("⏳ Waiting for response...\n")
        time.sleep(3)

        # Get messages
        messages_response = requests.get(f"{API_URL}/chat/{SESSION_ID}/messages")
        if messages_response.status_code == 200:
            messages = messages_response.json()
            if messages:
                last_message = messages[-1]
                if last_message['role'] == 'assistant':
                    print(f"🤖 BHRAHMA: {last_message['content']}\n")

                    # Show skills used
                    skills_used = last_message.get('meta_data', {}).get('skills_used', [])
                    if skills_used:
                        print(f"🔧 Skills used: {', '.join(skills_used)}\n")
                else:
                    print("⏳ Still processing... (check frontend for response)\n")

        time.sleep(2)
    else:
        print(f"❌ Error: {response.text}\n")

def check_health():
    """Check system health"""
    print_banner("Checking System Health")
    response = requests.get(f"{API_URL}/health")
    if response.status_code == 200:
        health = response.json()
        print(f"Status: {health['status']}")
        print(f"Database: {health['database']}")
        print(f"Queue: {health['queue']}")
        print(f"Available LLMs: {', '.join(health['available_llms'])}\n")
    else:
        print("❌ Health check failed!")

def list_skills():
    """List available skills"""
    print_banner("Available Skills")
    response = requests.get(f"{API_URL}/skills")
    if response.status_code == 200:
        skills = response.json()
        print(f"Total skills: {len(skills)}\n")
        for skill in skills:
            print(f"📚 {skill['name']}")
            print(f"   Category: {skill['category']}")
            print(f"   Description: {skill['description'][:100]}...")
            print()
    else:
        print("❌ Failed to fetch skills")

def run_demo():
    """Run the complete demo"""
    print("\n" + "🧠 "*20)
    print("     BHRAHMA AI AGENT SYSTEM - AUTOMATED DEMO")
    print("🧠 "*20 + "\n")

    # Check health
    check_health()
    time.sleep(2)

    # List initial skills
    list_skills()
    time.sleep(2)

    # Demo Interaction 1: Introduction
    print_banner("Demo 1: Introduction")
    send_message("Hello! What can you do?")
    time.sleep(3)

    # Demo Interaction 2: Learn a skill
    print_banner("Demo 2: Learning a New Skill")
    print("📖 Teaching Bhrahma about pytest from documentation...\n")
    send_message("Learn about pytest testing framework from https://docs.pytest.org")
    time.sleep(8)  # Learning takes longer

    # Show updated skills
    list_skills()
    time.sleep(2)

    # Demo Interaction 3: Use the learned skill
    print_banner("Demo 3: Using the Learned Skill")
    send_message("Create a pytest test for a function that calculates factorial")
    time.sleep(5)

    # Demo Interaction 4: Complex task with parallel execution
    print_banner("Demo 4: Parallel Task Execution")
    print("🔄 This task will be decomposed into subtasks...\n")
    send_message("Compare Python, JavaScript, and Go for building REST APIs")
    time.sleep(10)

    # Demo Interaction 5: Skill reuse
    print_banner("Demo 5: Skill Reusability")
    send_message("Write pytest tests for a Calculator class with add, subtract, multiply, divide methods")
    time.sleep(5)

    # Final status
    print_banner("Demo Complete!")
    print(f"Session ID: {SESSION_ID}")
    print(f"View full conversation at: http://localhost:8501")
    print("\n✅ All demo interactions completed successfully!\n")

    # Get final queue status
    queue_response = requests.get(f"{API_URL}/queue/status")
    if queue_response.status_code == 200:
        queue = queue_response.json()
        print(f"Queue size: {queue['queue_size']}")
        print(f"Processing: {queue['is_processing']}")

if __name__ == "__main__":
    try:
        run_demo()
    except KeyboardInterrupt:
        print("\n\n⏸️  Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error during demo: {str(e)}")
        print("Make sure the backend is running at http://localhost:8000")
