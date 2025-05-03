# Agent Connect

Agent Connect is a FastAPI-based platform that enables secure, real-time two-way communication between mobile devices and PCs using AI agents. Send queries from your phone and receive intelligent responses or notifications, seamlessly bridging your devices.

## Features

- **AI-Powered Crypto Analysis**: Leverages Google's Gemini 2.0 Flash model to generate concise cryptocurrency market summaries
- **REST API Endpoints**: Simple endpoints for querying crypto data and triggering automated reports
- **Push Notifications**: Sends summarized crypto market updates directly to your devices via Pushcut
- **Secure API Authentication**: API key authentication to ensure secure access
- **Text Formatting**: Cleans up AI responses for optimal readability on notification services

## Architecture

The application consists of three main components:

1. **FastAPI Web Service** (`crypto_agent.py`): Handles HTTP requests and exposes API endpoints
2. **LLM Agent** (`agent.py`): Interfaces with Google's Generative AI to fetch and summarize crypto data
3. **Notification Service**: Delivers processed information to mobile devices via Pushcut

## API Endpoints

### POST /agent-query
Query the agent with a custom request

**Headers:**
- `x-api-key`: Your API key for authentication

**Request Body:**
```json
{
  "message": "What is the current price of Bitcoin?"
}
```

### POST /run-agent
Trigger a standard cryptocurrency price update report

**Headers:**
- `x-api-key`: Your API key for authentication

## Setup

### Prerequisites

- Python 3.9+
- Google API key (for Gemini AI)
- Pushcut API key
- Custom API key for securing your service

### Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/crypto-price-agent.git
cd crypto-price-agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with the following variables:
```
GOOGLE_API_KEY=your_google_api_key
PUSHCUT_API_KEY=your_pushcut_api_key
MY_API_KEY=your_custom_api_key
```

### Running Locally

```bash
python crypto_agent.py
```

The service will start on `http://0.0.0.0:8765`.

### Deployment

The service can be exposed to the internet using Cloudflare Tunnel. A sample configuration is included in the project.

## Usage Examples

### Using curl

```bash
# Custom query
curl -X POST http://localhost:8765/agent-query \
  -H "x-api-key: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{"message": "Compare Bitcoin and Ethereum performance this week"}'

# Standard report
curl -X POST http://localhost:8765/run-agent \
  -H "x-api-key: your_api_key"
```

## Tech Stack

- **FastAPI**: Web framework for building APIs
- **Google ADK**: Google's Agent Development Kit for LLM interactions
- **Gemini 2.0**: Google's large language model for natural language processing
- **Pushcut**: Mobile notification service
- **Uvicorn**: ASGI web server

## Scalability for 2-Way Communication

This architecture is designed to support scalable, real-time, two-way communication between clients (such as an iPhone app or Siri Shortcut) and the AI agent. The use of FastAPI and WebSockets (or HTTP endpoints) allows for both request/response and event-driven interactions. Cloudflare Tunnel enables secure, global access without exposing your local server directly to the internet.

### Example Communication Flow

```
   iPhone (User/Siri Shortcut)
           ↓
    Cloudflare Tunnel (Secure Public Endpoint)
           ↓
        FastAPI (API/WebSocket Server)
           ↓
        AI Agent (Gemini LLM)
           ↓
        Pushcut (Notification Service)
           ↓
   iPhone (Push Notification)
```

- **Outbound**: User sends a query from iPhone → routed via Cloudflare Tunnel → FastAPI receives and processes → AI Agent generates a response → Pushcut sends notification back to iPhone.
- **Inbound**: The architecture can be extended to support real-time updates or actions from the server to the client (e.g., via WebSockets or Pushcut triggers), enabling true two-way communication.

### Scalability Considerations
- **Stateless API**: FastAPI endpoints are stateless, making it easy to scale horizontally (multiple server instances behind a load balancer).
- **Session Management**: The agent uses session services, which can be backed by scalable storage (e.g., Redis) for multi-user support.
- **Cloudflare Tunnel**: Handles secure, scalable ingress without manual firewall or DNS management.
- **Pushcut**: Supports multiple devices and users, enabling broad notification delivery.

This design ensures the system can grow to support more users, devices, and real-time features as needed.

## License

MIT

## Acknowledgments

- Google's Generative AI team for providing the Gemini model API
- Pushcut for notification services