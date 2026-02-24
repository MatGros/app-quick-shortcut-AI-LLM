# Spécification Fonctionnelle - Quick Shortcut AI LLM Assistant
## Technology-Agnostic Application Specification

**Version**: 1.0
**Date**: 24 février 2026
**Purpose**: Define application features and architecture independent of technology stack

---

# TABLE OF CONTENTS

1. [Executive Overview](#executive-overview)
2. [Core Concept](#core-concept)
3. [Features List](#features-list)
4. [User Workflows](#user-workflows)
5. [System Architecture](#system-architecture)
6. [Non-Functional Requirements](#non-functional-requirements)
7. [Data Model](#data-model)
8. [Integration Points](#integration-points)

---

# EXECUTIVE OVERVIEW

## Product Name
**Quick Shortcut AI LLM Assistant**

## Mission
Provide instant AI assistance via global keyboard shortcuts without context switching. Users can invoke AI operations (summarization, translation, question-answering) from anywhere on the system while maintaining focus on their current work.

## Target Platform
- **Primary**: Windows desktop (Windows 10+, Windows 11)
- **Secondary**: Cross-platform capability (future consideration)

## Target Users
- Knowledge workers
- Software developers
- Researchers
- Anyone who repeatedly needs quick AI assistance

## Key Value Proposition
- **No context switching**: AI accessible via keyboard shortcut from any application
- **Zero setup**: Works out of the box with sensible defaults
- **Multi-provider support**: Use any LLM provider (local or cloud)
- **Smart response delivery**: Inline previews for quick tasks, full windows for conversations
- **Fully customizable**: Configure shortcuts, prompts, appearance, behavior

---

# CORE CONCEPT

## How It Works

```
User Context             Global Shortcut          LLM Processing        Response Delivery
─────────────            ────────────             ──────────────         ─────────────
┌──────────────┐        ┌──────────────┐         ┌──────────────┐       ┌──────────────┐
│ In any app   │        │ Press hotkey │ ◄────► │ Send to LLM  │ ◄──► │ Show result  │
│ (browser,    │        │ at cursor    │  (auto │ provider     │ │    │ (popup or    │
│ editor, etc) │        │ position)    │  send) │ (Ollama,     │ │    │ full window) │
│              │        │              │        │ OpenAI, etc) │ │    │              │
└──────────────┘        └──────────────┘        └──────────────┘       └──────────────┘
```

## Execution Modes

### Mode 1: Quick Context Menu
User presses shortcut → **Context menu appears at cursor** → Select action → Execute

**Use Cases**:
- Summarize selected text
- Translate to another language
- Answer quick question about selected text
- Generate code snippet from template

**Response**: Inline popup (small window) or clipboard paste

### Mode 2: Full Chat Window
User presses shortcut → **Full chat window opens** → Multi-turn conversation → Continuous context

**Use Cases**:
- Detailed analysis or brainstorming
- Back-and-forth questions
- Complex code reviews
- Research-heavy tasks

**Response**: Full window with conversation history

### Mode 3: Inline Response
User presses shortcut with selection → **Inline result appears at selection** → Can accept or reject → Auto-paste if enabled

**Use Cases**:
- Quick writing improvements
- Code completion
- Format conversions
- Text rewrites

**Response**: Floating popup near cursor with accept/reject buttons

---

# FEATURES LIST

## Core Features (P0 - Required for MVP)

### F-01: Global Keyboard Shortcuts
**What**: Detect and respond to global keyboard combinations without blocking other applications

**Behavior**:
- User presses configured hotkey (e.g., Ctrl+Shift+A)
- System immediately responds (< 100ms latency)
- Works in any application
- Does not prevent hotkey from reaching the application (if configured)

**Configurability**:
- User can change hotkey combinations
- System detects and warns of conflicts
- Support multiple different shortcuts for different actions

**Status**: ✅ Implemented (mostly working, has blocking issues)

---

### F-02: Context Menu (Floating UI)
**What**: Display modern, frameless context menu at cursor position with available actions

**Design Requirements**:
- Appears at exact cursor position
- Modern appearance (no native OS widgets)
- Smooth fade-in animation (200ms)
- Keyboard navigation support (arrow keys, Enter, Escape)
- Automatically positions to stay on-screen (multi-monitor aware)
- Click on item to execute action

**Actions Available**:
- Summarize (selected text or page context)
- Translate (to configurable language)
- Explain (code, concepts, text)
- Custom prompt (user-defined)
- Ask question (about selected content)
- Generate (based on template)

**Status**: ✅ Implemented (non-responsive click issue)

---

### F-03: Multi-Provider LLM Support
**What**: Abstract interface to work with different LLM providers seamlessly

**Supported Providers**:
- **Local**: Ollama (self-hosted models)
- **Cloud**: OpenAI (ChatGPT API)
- **Cloud**: Anthropic (Claude API)
- **Cloud**: OpenRouter (model aggregator)

**Behavior**:
- User configures which provider and model to use
- Application handles all API differences transparently
- Automatic fallback if provider unavailable (configurable)
- Support for vision models (image understanding)

**User Experience**:
- Single configuration point for all providers
- Switch providers without restarting
- Test connection before saving config

**Status**: ✅ Implemented (core + 3 providers)

---

### F-04: Response Windows
**What**: Display LLM responses in appropriate UI containers

**Window Types**:

#### A. Full Chat Window
- Persistent conversation history
- Multi-turn interaction
- Markdown rendering with syntax highlighting
- Copy response (text, HTML, markdown formats)
- Stop button (for long responses)
- Settings quick-access

#### B. Inline Popup
- Small floating window near cursor/selection
- Shows response (not full conversation)
- Auto-resize based on content
- Accept/Reject buttons
- Can copy to clipboard or paste to active application

#### C. Embedded (Optional)
- Response appears directly in context (advanced feature)
- Low priority, may not implement

**Status**: ✅ Implemented (both window types, some issues)

---

### F-10: Configuration Interface
**What**: User-friendly settings for all application options

**Configuration Categories**:
1. **LLM Provider Settings**
   - Select provider (Ollama, OpenAI, etc.)
   - API key or endpoint configuration
   - Model selection
   - Test connection button

2. **Keyboard Shortcuts**
   - Configure hotkeys for different actions
   - Visual conflict detection
   - Reset to defaults button
   - Import/export shortcuts

3. **Appearance**
   - Dark/Light theme selection
   - Custom prompt templates
   - Response format preferences

4. **Behavior**
   - Auto-paste responses to active application
   - Notification preferences
   - Response window behavior
   - Performance settings

**Storage**: Persistent (saved to file)

**Status**: ✅ Implemented (incomplete, closing issue)

---

### F-11: System Health Checks
**What**: Verify application readiness on startup and monitor during use

**Checks Performed**:
1. Configuration validity (config file exists and is readable)
2. LLM connectivity (can reach configured provider)
3. System permissions (can read/write configuration, access clipboard)
4. Required dependencies available

**User Feedback**:
- Status indicator (green = ready, red = error)
- Detailed error messages
- Suggestions for fixing issues

**Timing**:
- Run on startup
- Run when configuration changes
- Run periodically (optional)

**Status**: ✅ Implemented (icon update issue)

---

### F-13: Customizable Keyboard Shortcuts
**What**: Allow users to change which keyboard combinations trigger which actions

**Behavior**:
- User opens settings
- Clicks on shortcut field
- Presses desired key combination
- System validates (no conflicts with system shortcuts)
- Changes take effect immediately
- Persisted for next session

**Supported Actions**:
- Show context menu
- Open chat window
- Summarize selected text
- Open settings
- Quit application

**Status**: ✅ Implemented

---

### F-14: System Tray Integration
**What**: Application presence in system tray with quick access and status indication

**Tray Icon Features**:
- Status indicator (color-coded health status)
- Quick menu
  - Open chat window
  - Open settings
  - Quit
- Tooltip showing status

**Status Visualization**:
- Green: Application ready
- Red: Configuration error or LLM unavailable
- Yellow: Checking connection

**Status**: ✅ Implemented

---

## Secondary Features (P1 - Important)

### F-05: Clipboard Management
**What**: Read and write to system clipboard

**Capabilities**:
- Read text from clipboard
- Read images from clipboard
- Write text to clipboard
- Handle various text formats (plain, HTML, markdown)
- Robust error handling (permission issues, large content)

**Use Cases**:
- Auto-detect selected text (user can copy first, then hotkey)
- Send clipboard image to vision model
- Auto-paste results to previous application

**Status**: ✅ Implemented

---

### F-06: Auto-Paste
**What**: Automatically paste LLM response to the previous active application

**Behavior**:
- User enables auto-paste in settings
- LLM response generated
- Application automatically focuses previous window
- Pastes response as if user typed it
- Returns focus to application

**Considerations**:
- Must preserve focus correctly
- Must handle different application types (editors, browsers, messaging)
- Configurable delay (safety margin)
- User can disable per-response

**Status**: ✅ Implemented (partial)

---

### F-07: Screenshot Capture
**What**: Capture screen region and send to vision models

**Capture Modes**:
1. Full screen capture
2. Region selection (user draws rectangle)
3. Active window capture
4. Clipboard image detection

**Processing**:
- Convert image to base64 or appropriate format
- Send to vision-capable LLM (e.g., GPT-4V, Claude Vision)
- Include with text prompt

**Use Cases**:
- Describe screenshot content
- Extract text from image
- Debug visual issues
- Document pages

**Status**: 📋 Planned (not implemented)

---

### F-08: Notifications
**What**: Inform user of important events without interrupting

**Notification Types**:
- Response complete
- Error occurred
- Configuration changed
- Long-running operation status

**Delivery**:
- Custom notifications (app-native, not system notifications)
- Auto-dismiss after timeout
- Varying styles (info, success, warning, error)
- Optional sound

**Status**: 📋 Planned (not implemented)

---

### F-09: History & Search
**What**: Maintain searchable history of past interactions

**Data Stored**:
- Question asked
- Response received
- Provider used
- Model used
- Timestamp
- Status (success/error)

**Capabilities**:
- Search history by keyword
- Filter by date range
- Filter by action type
- Export as JSON or markdown
- Statistics (usage patterns, favorite features)

**Storage**: Persistent database (local, encrypted)

**Status**: 📋 Planned (not implemented)

---

### F-12: Theme System
**What**: Allow customization of application appearance

**Theme Options**:
- Dark mode (default)
- Light mode
- Custom color schemes (future)

**Application Scope**:
- Windows and dialogs
- Menu styling
- Text highlighting
- Icon rendering

**Persistence**: User preference saved

**Status**: 📋 Planned (partial dark mode exists)

---

### F-15: Prompt Templates
**What**: Pre-built prompt templates for common tasks

**Examples**:
- "Summarize in 3 sentences"
- "Translate to French"
- "Explain for 10-year-old"
- "Find bugs in this code"
- "Generate unit tests"

**Customization**:
- Create custom templates
- Use variables (e.g., {language}, {style})
- Save favorites
- Share templates (optional, future)

**Status**: 📋 Planned (not implemented)

---

### F-16: Markdown Rendering
**What**: Display LLM responses with proper formatting and syntax highlighting

**Rendering Features**:
- Headers (various levels)
- Bold, italic, underline
- Code blocks with syntax highlighting (for programming languages)
- Lists (ordered and unordered)
- Tables
- Links
- Blockquotes
- Horizontal rules

**Code Highlighting**: Support for 50+ programming languages

**Status**: ✅ Implemented

---

### F-17: Response Export
**What**: Copy or export response in various formats

**Formats**:
- Plain text (unformatted)
- Markdown (preserves structure)
- HTML (rich formatting)
- Copy to clipboard
- Save to file

**Status**: 📋 Planned (partial - copy works)

---

### F-18: Retry Mechanism
**What**: Automatically retry failed requests with exponential backoff

**Behavior**:
- Request fails (timeout, error, network issue)
- Show retry button to user
- Optional auto-retry with exponential backoff
- Maximum retry attempts configurable
- Preserve conversation context

**Status**: 📋 Planned (not implemented)

---

### F-19: Conversation Context
**What**: Maintain multi-turn conversations with context management

**Features**:
- Keep recent messages in memory
- Send context with new questions
- Truncate old messages if too long (preserve relevance)
- Clear conversation button
- Show conversation length/token count (if available)

**Status**: 📋 Planned (partial - framework exists)

---

### F-20: Portable Mode
**What**: Standalone executable with no installation required

**Requirements**:
- Single .exe file
- Configuration stored locally (not in system directories)
- No dependencies required
- Can run from USB drive
- No administrator privileges needed (for execution)

**Status**: 📋 Planned (build infrastructure exists)

---

# USER WORKFLOWS

## Workflow 1: Quick Summarization
```
1. User selects text in any application
2. User presses configured shortcut (e.g., Ctrl+Shift+S)
3. Application detects shortcut
4. Context menu appears at cursor with action options
5. User clicks "Summarize"
6. Application sends selected text to LLM
7. Response appears in inline popup near cursor
8. User can:
   a. Copy result to clipboard
   b. Paste to active application (auto-paste)
   c. Ask follow-up question
   d. Dismiss popup
```

**Time from action to response**: < 2 seconds (assuming API is fast)

---

## Workflow 2: Multi-turn Conversation
```
1. User presses shortcut (no selection needed)
2. Full chat window opens
3. Window contains:
   - Text input area
   - Chat history area (empty if new)
   - Settings/options bar
4. User types question
5. User presses Enter (or clicks Send)
6. Application sends to LLM with context
7. Response streams in (token by token if supported)
8. User can:
   a. Ask follow-up question (builds context)
   b. Copy entire response
   c. Export to file
   d. Clear conversation
   e. Close window
```

**Typical duration**: 5-30 minutes (user decides when done)

---

## Workflow 3: Configuration
```
1. User right-clicks tray icon → Settings
2. Settings window opens with tabs:
   - LLM Provider (configure Ollama, OpenAI, etc.)
   - Shortcuts (remap keyboard combinations)
   - Appearance (dark/light theme)
   - Behavior (auto-paste, notifications, etc.)
3. User modifies settings
4. User clicks "Test Connection" (if LLM settings changed)
5. System validates changes
6. User clicks "Save"
7. Changes take effect immediately
8. Health check runs automatically
9. User sees status update (green/red icon in tray)
```

**Time**: 2-5 minutes (one-time or periodic)

---

## Workflow 4: Screenshot Analysis
```
1. User presses shortcut for "Screenshot"
2. Screen overlay appears
3. User draws rectangle to select region
4. Application captures selected area
5. Image automatically sent to vision-capable LLM
6. LLM responds with analysis
7. Response displayed in popup or window
8. User can copy, paste, or follow up
```

**Time**: 3-10 seconds (depending on LLM)

---

## Workflow 5: Application Startup
```
1. User runs application
2. Application:
   a. Loads configuration
   b. Performs health checks
      - Config validity ✓
      - LLM connectivity ✓
      - Permissions ✓
   c. If all checks pass:
      - Tray icon shows green
      - Keyboard hooks activated
      - Ready to respond to shortcuts
   d. If check fails:
      - Tray icon shows red
      - Error message shown
      - User directed to fix configuration
3. Application minimizes to tray
4. User can access via hotkey or tray menu
```

**Time**: < 2 seconds (startup)

---

# SYSTEM ARCHITECTURE

## Architectural Components (Technology-Agnostic)

### Layer 1: Input Detection
**Responsibility**: Detect global keyboard shortcuts

**Inputs**:
- System-wide keyboard events
- Mouse position (for context menu placement)

**Outputs**:
- Detected shortcut event (which hotkey + context)
- Cursor coordinates

**Considerations**:
- Must not block system
- Must run continuously (background)
- Low latency (< 50ms detection time)
- Requires system-level access (privileged)

---

### Layer 2: Core Business Logic
**Responsibility**: Orchestrate application workflow

**Responsibilities**:
- Route input to appropriate handler
- Manage state (which window is open, what's in context)
- Coordinate between components
- Handle error scenarios
- Apply business rules (rate limiting, error retry, etc.)

**Input**:
- User actions (shortcut, menu click, text input)
- System events (window focus change, config change)
- External events (LLM response received)

**Output**:
- UI updates
- Network requests
- File operations
- Status changes

---

### Layer 3: LLM Integration
**Responsibility**: Abstract different LLM providers

**Responsibilities**:
- Translate application requests to provider APIs
- Handle provider-specific authentication
- Support streaming responses
- Handle provider errors
- Detect provider capabilities (vision support, etc.)

**Providers to Support**:
- Local models (Ollama)
- OpenAI (ChatGPT)
- Anthropic (Claude)
- OpenRouter (aggregator)

**Abstraction**: Common interface that all providers implement

---

### Layer 4: User Interface
**Responsibility**: Display application to user

**UI Components**:
1. **Context Menu**
   - Floating window at cursor position
   - List of available actions
   - Keyboard-navigable
   - Custom styled (no native OS widgets)

2. **Chat Window**
   - Message display area
   - Text input area
   - Toolbar (settings, copy, etc.)
   - Status bar

3. **Settings Dialog**
   - Tabbed interface
   - Form controls for configuration
   - Validation feedback
   - Connection testing

4. **System Tray**
   - Status indicator
   - Quick menu
   - Icon

5. **Inline Response**
   - Small popup at cursor
   - Shows response
   - Action buttons

**Design Principles**:
- Modern, frameless windows
- Smooth animations
- Responsive to user interaction
- Dark and light themes
- Keyboard accessible

---

### Layer 5: Data Management
**Responsibility**: Persist and retrieve data

**Data Types**:
1. **Configuration**
   - User settings (LLM provider, shortcuts, appearance)
   - Credentials (API keys)
   - Preferences

2. **History**
   - Past interactions
   - Responses
   - Metadata (timestamp, provider, model)

**Storage**:
- Configuration: Local file (JSON or similar)
- Credentials: Encrypted storage
- History: Local database
- Conversation context: In-memory (current session)

**Requirements**:
- Secure (don't expose API keys)
- Portable (can move/backup easily)
- Efficient (quick reads/writes)

---

### Layer 6: System Integration
**Responsibility**: Interact with OS

**Interactions**:
- Read/write clipboard
- Get active window information
- Focus windows
- Send keyboard input to other applications
- Access configuration directories
- System notifications
- System tray presence

**Requirements**:
- Platform-specific (Windows focus initially)
- Low-level access (may require privileges)
- Error handling (application may not have permission)

---

## Data Flow Diagram

```
User Input
    │
    ▼
┌─────────────────────────────────────┐
│ Input Detection Layer               │
│ - Detect global keyboard shortcuts  │
│ - Get mouse/context info            │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ Core Business Logic                 │
│ - Route to handler                  │
│ - Validate input                    │
│ - Load context                      │
└────────────┬────────────────────────┘
             │
             ├──────────────────────────────┐
             │                              │
             ▼                              ▼
      ┌─────────────┐             ┌──────────────────┐
      │ UI Layer    │             │ LLM Integration  │
      │ - Show menu │             │ - Format request │
      │ - Get input │             │ - API call       │
      └──────┬──────┘             │ - Parse response │
             │                    └────────┬─────────┘
             │                             │
             ▼                             ▼
      ┌──────────────┐            ┌──────────────────┐
      │ User chooses │            │ LLM Provider     │
      │ action       │            │ (Ollama/OpenAI)  │
      └──────┬───────┘            └──────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ Process Selected Action             │
├─────────────────────────────────────┤
│ 1. Gather context (selection, etc)  │
│ 2. Prepare prompt                   │
│ 3. Send to LLM                      │
│ 4. Receive response                 │
│ 5. Format response                  │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│ Deliver Response                    │
├─────────────────────────────────────┤
│ - Show in UI (popup/window)         │
│ - Save to history (optional)        │
│ - Auto-paste (optional)             │
│ - Update status                     │
└─────────────────────────────────────┘
```

---

# NON-FUNCTIONAL REQUIREMENTS

## Performance

### Response Time
- **Input to menu appearance**: < 100ms (critical)
- **Menu response to action click**: < 50ms
- **LLM request submission**: < 200ms
- **Startup time**: < 2 seconds
- **Configuration save**: < 500ms

### Responsiveness
- **UI must remain responsive** during LLM requests
- Streaming responses must appear progressively (not wait for complete response)
- Window dragging/resizing must not be blocked by API calls

### Memory
- **Baseline**: < 100 MB (at idle)
- **During conversation**: < 300 MB
- **Streaming response**: Constant memory (no accumulation)

### CPU
- **Idle**: Near 0% (no spinning threads)
- **During API call**: Reasonable (<20%)
- **Animations**: Smooth 60 FPS (no stuttering)

---

## Reliability

### Error Handling
- **Graceful degradation**: If LLM unavailable, show helpful error message
- **Retry logic**: Transient errors should retry automatically
- **Fallback**: If configured provider fails, try alternative (if available)

### Data Integrity
- **Configuration persistence**: Changes must survive application restart
- **History accuracy**: Every interaction correctly recorded
- **Credentials security**: API keys never logged or exposed

### Availability
- **Startup**: Always starts successfully (even if LLM unavailable)
- **Shortcuts**: Always detected, even during API calls
- **Recovery**: Graceful shutdown (no hung processes)

---

## Usability

### Accessibility
- **Keyboard navigation**: All features accessible via keyboard
- **Screen reader support**: Information conveyed to screen readers
- **High contrast**: Readable on various monitor types
- **Resizable text**: User can increase text size

### Discoverability
- **Intuitive defaults**: Works without configuration
- **First-run experience**: Guides new users
- **Context-sensitive help**: Help available where needed

### Customization
- **Configuration**: All major behaviors customizable
- **Prompts**: Users can create/share templates
- **Shortcuts**: Users can remap hotkeys
- **Appearance**: Dark/light themes minimum

---

## Security & Privacy

### Credential Protection
- **API keys**: Encrypted at rest
- **Passwords**: Never stored in plain text
- **Tokens**: Rotated/refreshed appropriately

### Data Privacy
- **User content**: Not logged or shared (except to LLM provider as configured)
- **History**: Stored locally, not synced (unless user opts in)
- **Configuration**: Contains sensitive info (encrypt or secure storage)

### Permissions
- **Minimal elevation**: Only request necessary permissions
- **Transparency**: Clearly state what permissions needed
- **User control**: Users can revoke permissions

---

## Maintainability

### Code Quality
- **Modular design**: Components loosely coupled
- **Well-documented**: Code comments explain non-obvious logic
- **Testable**: Functions have single responsibility
- **Type safety**: Strong typing where language allows

### Compatibility
- **Version support**: Document minimum OS versions
- **Dependency management**: Clear list of requirements
- **Breaking changes**: Documented in release notes

---

# DATA MODEL

## Configuration Data

```
Configuration {
  version: "1.0"
  provider: {
    type: "ollama|openai|anthropic|openrouter"
    endpoint: "http://localhost:11434"  // for local
    apiKey: "encrypted:..."            // for cloud
    model: "gpt-4|claude-3|..."
  }

  shortcuts: {
    showMenu: "ctrl+shift+right"
    openChat: "ctrl+shift+a"
    summarize: "ctrl+shift+s"
    translate: "ctrl+shift+t"
  }

  appearance: {
    theme: "dark|light"
    fontSize: 13
    fontFamily: "default|custom"
  }

  behavior: {
    autoPaste: true|false
    notifications: true|false
    streamingResponses: true|false
    retryOnError: true|false
  }

  prompts: {
    summarize: "Summarize the following in 3 sentences: {text}"
    translate: "Translate to {language}: {text}"
    // ... user-defined prompts
  }
}
```

## History Record

```
HistoryEntry {
  id: "unique-id"
  timestamp: "2026-02-24T10:30:00Z"
  action: "summarize|translate|question|..."

  input: {
    text: "original text or question"
    context: "clipboard|selection|screenshot"
  }

  output: {
    response: "LLM response text"
    format: "markdown|html|text"
  }

  metadata: {
    provider: "ollama"
    model: "llama2"
    tokensUsed: 150
    responseTime: 2.3 // seconds
    status: "success|error"
  }
}
```

## Conversation Context

```
ConversationState {
  isActive: true|false
  messages: [
    {
      role: "user|assistant"
      content: "message text"
      timestamp: "..."
    }
  ]

  context: {
    originalSelection: "text from first query"
    model: "gpt-4"
    provider: "openai"
  }

  metadata: {
    totalTokens: 1000
    startTime: "..."
    lastUpdate: "..."
  }
}
```

---

# INTEGRATION POINTS

## External Systems

### LLM Providers
- **Ollama**: Local API (HTTP endpoint)
- **OpenAI**: Cloud API (REST + streaming)
- **Anthropic**: Cloud API (REST + streaming)
- **OpenRouter**: Aggregator API (REST)

**Integration Method**: HTTP/REST
**Authentication**: API keys or tokens
**Features**: Some have streaming, some have vision models

---

### Operating System
- **Clipboard**: Read/write operations
- **Window focus**: Get/set focus on windows
- **Keyboard input**: Send synthetic keystrokes
- **Mouse position**: Get cursor location
- **System tray**: Register and receive tray events
- **Notifications**: Display toast notifications
- **File system**: Read/write configuration and history

**Integration Method**: Native OS APIs

---

### File System
- **Configuration**: Persistent storage (local directory)
- **History database**: Local database file
- **Logs**: Optional debug logs
- **Credentials**: Encrypted credential storage

**Locations**: User's local app data directory (platform-specific)

---

# ARCHITECTURAL CONSIDERATIONS FOR RE-ARCHITECTURE

## What Should NOT Change
These are core to the product and should be preserved:

1. **Global shortcut detection**: Ability to respond to keyboard hotkeys from any application
2. **Multi-provider support**: Abstract interface to different LLMs
3. **Instant availability**: No startup delay (always ready)
4. **Modern UI**: Clean, frameless, smooth animations
5. **User customization**: Configurable shortcuts, prompts, appearance

## What Could Be Improved

### UI/Rendering
- Current: Custom-drawn windows, platform-specific styling
- Consider: Modern cross-platform UI framework that supports:
  - Frameless windows
  - Hardware-accelerated rendering (smooth animations)
  - Native look-and-feel on each platform
  - Responsive design

### Input Detection
- Current: Low-level keyboard hook (platform-specific, complex)
- Consider: Cleaner abstraction for global shortcuts
- Note: This is the most platform-specific piece

### LLM Integration
- Current: REST-based, request-response model
- Consider: WebSocket support for better streaming
- Consider: Built-in rate limiting and retry logic
- Consider: Provider-agnostic request/response format

### Data Management
- Current: Configuration in JSON, history in SQLite
- Consider: More robust storage (encryption, validation)
- Consider: Cloud sync option (with privacy preservation)

### Architecture Pattern
- Current: Monolithic with layered architecture
- Consider: Event-driven architecture (more reactive)
- Consider: Plugin system (custom actions/providers)

---

# SUMMARY FOR ARCHITECTS

## Core Requirements
This application must:
1. Detect global keyboard shortcuts in real-time (< 100ms)
2. Communicate with LLM providers (Ollama, OpenAI, Anthropic, OpenRouter)
3. Display responses in modern, responsive UI (frameless, animated)
4. Allow users to configure all major behaviors
5. Store user configuration and history locally
6. Work on Windows (initially), extensible to other platforms

## Key Constraints
- **Input latency**: Critical (< 100ms shortcut detection)
- **UI responsiveness**: Critical (don't block on API calls)
- **Cross-provider support**: Important (abstract interface)
- **User customization**: Important (all major options configurable)
- **Portable deployment**: Important (standalone executable)

## Known Pain Points (From Current Implementation)
1. Global shortcut handling is complex and error-prone
2. UI/Core coupling is tight (threading/signal issues)
3. Settings dialog closing entire app (parent/child issue)
4. Health check not updating appropriately
5. Menu interaction issues (click event handling)

## Opportunities for Improvement
- **Cleaner input abstraction**: Hide platform-specific shortcut handling
- **Better threading model**: Separate UI from network operations more cleanly
- **Plugin architecture**: Allow users to add custom LLM providers or actions
- **Cross-platform support**: Design from the start for Windows, Mac, Linux
- **Modern framework**: Consider frameworks that handle UI/threading better

---

**This specification defines WHAT the application does, independent of HOW it's built.**

**An architect using this specification should be able to design the application in any technology stack (C#/.NET, Electron/JavaScript, Rust/Tauri, or continue with Python) while preserving all functionality.**
