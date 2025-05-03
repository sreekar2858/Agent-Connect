# Agent Connect

Agent Connect is a FastAPI-based platform that enables secure, real-time two-way communication between mobile devices and PCs using AI agents. Send queries from your phone and receive intelligent responses or notifications, seamlessly bridging your devices.

## Features

- **AI-Powered Crypto Analysis**: Leverages Google's Gemini 2.0 Flash model to generate concise cryptocurrency market summaries
- **REST API Endpoints**: Simple endpoints for querying crypto data and triggering automated reports
- **Push Notifications**: Sends summarized crypto market updates directly to your devices via Pushcut
- **Secure API Authentication**: API key authentication to ensure secure access
- **Text Formatting**: Cleans up AI responses for optimal readability on notification services

## Architecture & Communication Flow

Agent Connect is designed for seamless, scalable, two-way communication between your mobile device and PC using AI agents. The architecture supports both request/response and event-driven interactions.

### Visual Flow
```
iPhone (User/Siri Shortcut)
        ↓
Cloudflare Tunnel (Secure Public Endpoint)
        ↓
FastAPI Server (Agent Connect)
        ↓
AI Agent (Gemini LLM via Google ADK)
        ↓
Pushcut (Notification Service)
        ↓
iPhone (Receives Notification)
```

### How It Works
1. The user sends a query from their iPhone (e.g., via Siri Shortcut or app).
2. The request is securely routed through Cloudflare Tunnel to your FastAPI server running Agent Connect. Cloudflare Tunnel is free, but requires a domain name (which can be obtained from providers like Namecheap, DotTech, or others). If you don’t have a custom domain, you can use ngrok as an alternative to expose your local server. See the section below for setup details.
3. FastAPI processes the request and forwards it to the AI Agent (Gemini LLM).
4. The AI Agent generates a response (e.g., crypto price summary).
5. The response is sent to Pushcut, which delivers a notification to the user’s iPhone.
6. The user receives the AI-generated update as a push notification.

This flow supports two-way communication: users can send queries and receive real-time, AI-powered responses on their mobile device.

## Scalability for 2-Way Communication

- **Stateless API**: FastAPI endpoints are stateless, making it easy to scale horizontally (multiple server instances behind a load balancer).
- **Session Management**: The agent uses session services, which can be backed by scalable storage (e.g., Redis) for multi-user support.
- **Cloudflare Tunnel**: Handles secure, scalable ingress without manual firewall or DNS management.
- **Pushcut**: Supports multiple devices and users, enabling broad notification delivery.

This design ensures the system can grow to support more users, devices, and real-time features as needed.

## Exposing Your Local Server: Cloudflare Tunnel & Alternatives

To make your local FastAPI server accessible from the internet (for mobile device communication), you need a secure tunneling solution.

### Cloudflare Tunnel (Recommended)
- **Requirements:**
  - A free [Cloudflare account](https://dash.cloudflare.com/)
  - Install [cloudflared](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/) on your machine
  - Configure your tunnel and DNS as per Cloudflare documentation
- **Benefits:**
  - Free for most use cases
  - Secure, stable, and production-ready
  - Custom domain support

### Alternative: ngrok
- **Requirements:**
  - [ngrok account](https://ngrok.com/)
  - Download and install [ngrok](https://ngrok.com/download)
    ```bash
    choco install ngrok
    ```
    ```bash
    ngrok config add-authtoken your_auth_token
    ```
- **Workflow:**
  1. Start your FastAPI server locally (e.g., `python crypto_agent.py`)
  2. In a new terminal, run:
     ```bash
     ngrok http 8765
     ```
  3. ngrok will provide a public HTTPS URL (e.g., `https://18d9-2a00-8a60-c010-1-b8c9-83dc-eae9-8881.ngrok-free.app`)
  4. Use this URL in your mobile app or webhook configuration
- **Notes:**
  - Free tier has time/session limits and random URLs
  - Paid plans offer custom domains and reserved URLs

Both Cloudflare Tunnel and ngrok allow you to securely test and deploy your agent for remote access from mobile devices or other clients.

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

## License

MIT

## Acknowledgments

- Google's Generative AI team for providing the Gemini model API
- Pushcut for notification services
