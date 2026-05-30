# Swaddle Assistant API Documentation

## Base URL

**Production:** `https://swaddle-assistant-v2-prod-935085797789.europe-west1.run.app`  
**Local:** `http://localhost:8000`

---

## Endpoints

### 1. Health Check

**Endpoint:** `GET /health`

**Description:** Check if the API is running.

**Example Request:**
```bash
curl https://swaddle-assistant-v2-prod-935085797789.europe-west1.run.app/health
```

**Example Response:**
```json
{
  "status": "ok"
}
```

---

## Chat Endpoints

### 2. General Chat

**Endpoint:** `POST /chat`

**Description:** General conversation with the assistant using your persona and user context.

**Request Body:**
```json
{
  "prompt": "Hello, how are you?",
  "user_id": 1,
  "timezone": "Africa/Lagos"
}
```

**Example Response:**
```json
{
  "token": "Hello",
  "token": "!",
  "token": " I'm",
  ...
  "meta": {
    "duration_ms": 1234.56,
    "input_tokens": 150,
    "output_tokens": 45,
    "total_tokens": 195
  }
}
```

**Note:** This endpoint returns a Server-Sent Events (SSE) stream. Each token is sent as it's generated.

---

### 3. Schedule Create

**Endpoint:** `POST /chat`

**Description:** Create a schedule/reminder. The AI extracts scheduling information from natural language.

**Keywords that trigger this intent:**
- remind, schedule, book, set up, bedtime, alarm, remember

**Request Body:**
```json
{
  "prompt": "Remind me to pick up Sandra from school at 3pm tomorrow",
  "user_id": 1,
  "timezone": "Africa/Lagos"
}
```

**Example Response:**
```json
{
  "response": {
    "action_suggested": "create",
    "title": "Pick up Sandra from school",
    "start_time": "2026-05-31T15:00:00",
    "task_frequency": "Once",
    "location": "School",
    "child_refs": [
      {
        "id": 101,
        "name": "Sandra"
      }
    ],
    "can_book": true,
    "message": "I'll remind you to pick up Sandra from school at 3pm tomorrow!"
  },
  "benchmark": {
    "duration_ms": 2345.67,
    "input_tokens": 320,
    "output_tokens": 85,
    "total_tokens": 405
  }
}
```

**Fields:**
- `action_suggested`: Always "create" for valid scheduling requests
- `title`: Extracted task title
- `start_time`: ISO datetime in the user's timezone
- `task_frequency`: "Once", "Daily", "Weekly", or "Monthly"
- `location`: Extracted location (can be null)
- `child_refs`: Array of children involved (resolved from user context)
- `can_book`: `true` if all required info is present, `false` if missing start_time
- `message`: Human-friendly confirmation or request for more info

**Example with missing information:**
```json
{
  "prompt": "Book swimming for Zara",
  "user_id": 1,
  "timezone": "Africa/Lagos"
}
```

**Response:**
```json
{
  "response": {
    "action_suggested": null,
    "title": "Swimming",
    "start_time": null,
    "task_frequency": null,
    "location": null,
    "child_refs": [
      {
        "id": 102,
        "name": "Zara"
      }
    ],
    "can_book": false,
    "message": "What time would you like to book swimming for Zara?"
  },
  "benchmark": { ... }
}
```

---

### 4. Schedule View

**Endpoint:** `POST /chat`

**Description:** View your scheduled tasks for a date range. The AI extracts dates from natural language.

**Keywords that trigger this intent:**
- my schedule, what's scheduled, what is scheduled, upcoming, my reminders

**Request Body:**
```json
{
  "prompt": "What's my schedule today?",
  "user_id": 1,
  "timezone": "Africa/Lagos"
}
```

**Example Response:**
```json
{
  "response": "You have 2 tasks scheduled:\n\n- School Run at 2025-02-10T07:30:00.000+01:00\n  Children: Sandra, David\n  Location: Home\n\n- Swimming Lesson at 2025-02-10T16:00:00.000+01:00\n  Children: Zara\n  Location: Community Pool\n",
  "benchmark": {
    "duration_ms": 1567.89,
    "input_tokens": 280,
    "output_tokens": 120,
    "total_tokens": 400
  }
}
```

**Other valid prompts:**
- "Show my upcoming schedule"
- "What's scheduled this week?"
- "My reminders for tomorrow"
- "What do I have planned next week?"

**Example with no tasks:**
```json
{
  "response": "You have no scheduled tasks for this period.",
  "benchmark": { ... }
}
```

---

## Chat History Endpoints

### 5. Add Message

**Endpoint:** `POST /chat-history`

**Description:** Add a message to chat history (manually). Note: The chat endpoint automatically uses history context.

**Request Body:**
```json
{
  "userId": 1,
  "role": "user",
  "content": "Hello!"
}
```

**Example Response:**
```json
{
  "ok": true,
  "data": {
    "id": 1,
    "userId": 1,
    "role": "user",
    "content": "Hello!",
    "created_at": "2026-05-30T12:34:56.789Z"
  }
}
```

---

### 6. Get All Messages

**Endpoint:** `GET /chat-history/{user_id}`

**Description:** Get all chat history for a user (limited by auto-pruning to 3 user + 3 assistant messages).

**Example Request:**
```bash
curl https://swaddle-assistant-v2-prod-935085797789.europe-west1.run.app/chat-history/1
```

**Example Response:**
```json
{
  "ok": true,
  "count": 6,
  "data": [
    {
      "id": 1,
      "userId": 1,
      "role": "user",
      "content": "Hello!",
      "created_at": "2026-05-30T12:34:56.789Z"
    },
    {
      "id": 2,
      "userId": 1,
      "role": "assistant",
      "content": "Hi! How can I help you today?",
      "created_at": "2026-05-30T12:35:01.234Z"
    }
  ]
}
```

---

### 7. Get Recent Messages

**Endpoint:** `GET /chat-history/recent/{user_id}?limit={limit}`

**Description:** Get the most recent N messages for a user.

**Query Parameters:**
- `limit` (optional, default: 50): Number of messages to retrieve

**Example Request:**
```bash
curl "https://swaddle-assistant-v2-prod-935085797789.europe-west1.run.app/chat-history/recent/1?limit=6"
```

**Example Response:**
```json
{
  "ok": true,
  "count": 6,
  "data": [
    {
      "id": 1,
      "userId": 1,
      "role": "user",
      "content": "What's my schedule today?",
      "created_at": "2026-05-30T12:00:00.000Z"
    }
  ]
}
```

---

### 8. Delete Message

**Endpoint:** `DELETE /chat-history/{user_id}/message/{message_id}`

**Description:** Delete a specific message from chat history.

**Example Request:**
```bash
curl -X DELETE https://swaddle-assistant-v2-prod-935085797789.europe-west1.run.app/chat-history/1/message/5
```

**Example Response:**
```json
{
  "ok": true,
  "deletedMessageId": 5
}
```

---

### 9. Delete All Messages

**Endpoint:** `DELETE /chat-history/{user_id}/messages`

**Description:** Clear all chat history for a user.

**Example Request:**
```bash
curl -X DELETE https://swaddle-assistant-v2-prod-935085797789.europe-west1.run.app/chat-history/1/messages
```

**Example Response:**
```json
{
  "ok": true,
  "message": "All messages deleted for user 1"
}
```

---

## Configuration

### Environment Variables

```bash
ANTHROPIC_API_KEY=your_api_key_here
MODEL_NAME=claude-sonnet-4-20250514
ENVIRONMENT=development
USER_CONTEXT_URL=https://user-context-url.com
CHAT_HISTORY_LIMIT=3
TASK_MANAGER_URL=https://task-manager-url.com/task-manager
DEFAULT_MAX_TOKENS=512
```

**Key Settings:**
- `CHAT_HISTORY_LIMIT`: Number of messages (per role) to keep in history (default: 3)
- `DEFAULT_MAX_TOKENS`: Maximum tokens for AI responses (default: 512)
- `MODEL_NAME`: Claude model to use

---

## Best Practices

### 1. Chat History
- History is automatically pruned to maintain only the most recent 3 user + 3 assistant messages
- History is stored in-memory and resets on server restart
- The chat endpoint automatically includes history for context

### 2. Intent Detection
- Use clear keywords for scheduling: "remind", "schedule", "book"
- Use clear keywords for viewing: "my schedule", "upcoming", "what's scheduled"
- If unsure, the system defaults to general chat

### 3. Timezone
- Always provide the user's timezone for accurate scheduling
- Use IANA timezone names (e.g., "Africa/Lagos", "America/New_York")

### 4. Date/Time Extraction
- The AI understands natural language: "tomorrow at 3pm", "next Tuesday", "this week"
- Be specific about times for schedule creation
- Schedule view can infer ranges from keywords like "today", "this week"

---

## Testing with Postman

Import the `postman_collection.json` file to get started quickly:

1. Open Postman
2. Click **Import**
3. Select `postman_collection.json`
4. The collection uses `{{base_url}}` variable set to production by default

---

## Error Handling

**400 Bad Request:**
```json
{
  "detail": "limit must be >= 0"
}
```

**404 Not Found:**
```json
{
  "detail": "Not Found"
}
```

**502 Bad Gateway:**
```json
{
  "detail": "Unable to fetch user context"
}
```

---

## Rate Limits

No specific rate limits are enforced at the application level, but be mindful of:
- Anthropic API rate limits
- Cloud Run instance limits
- External service (user context, task manager) rate limits
