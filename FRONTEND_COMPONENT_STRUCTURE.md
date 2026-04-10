# Frontend Component Structure

## New Component Architecture

```
src/components/
├── UploadPage.jsx          # Document upload interface
├── UploadPage.css          # Upload page styles
├── AgentRoom.jsx           # Agent orchestration view
├── AgentRoom.css           # Agent room styles
├── ChatFeed.jsx            # Agent message display
├── ChatFeed.css            # Chat feed styles
├── CampaignView.jsx        # Campaign results display
├── CampaignView.css        # Campaign view styles
├── CampaignForm.js         # (Legacy) Campaign form
├── CampaignResult.js       # (Legacy) Campaign results
└── Header.js               # (Legacy) Header component
```

## Component Workflow

### 1. **UploadPage.jsx** - User Entry Point
- **Purpose**: Upload and preview documents
- **Features**:
  - Drag & drop file upload
  - File preview (first 300 characters)
  - File validation (type and size)
  - Submit to enter Agent Room
- **Transitions to**: AgentRoom

### 2. **AgentRoom.jsx** - AI Agent Orchestration
- **Purpose**: Visualize AI agents working on campaign
- **Features**:
  - 4-agent grid display (Research, Copywriter, Editor, Campaign Manager)
  - Real-time agent status updates (idle → processing → completed)
  - Active agent chat feed
  - Campaign generation trigger
- **Child Components**:
  - ChatFeed (displays agent messages)
- **Transitions to**: CampaignView

### 3. **ChatFeed.jsx** - Agent Communication
- **Purpose**: Display agent-specific messages and progress
- **Features**:
  - Message types (start, progress, success, error, info)
  - Auto-scroll to latest message
  - Status indicators with icons
  - Message animations
- **Transitions from**: AgentRoom (selected agent)

### 4. **CampaignView.jsx** - Results Display
- **Purpose**: Display and manage generated campaign
- **Features**:
  - Tabbed interface (Factsheet, Blog, Email, Recommendations)
  - Copy to clipboard functionality
  - Download as file (TXT, JSON, HTML, Markdown)
  - Print support
  - Tweet thread display
  - Recommendation list
- **Actions Available**:
  - Copy individual sections
  - Download content
  - Print campaign
  - Generate another campaign

## User Journey

```
1. User Upload
   ↓
UploadPage (drag & drop or click)
   ↓
2. AI Generation
   ↓
AgentRoom (watch agents work)
   ↓ (with ChatFeed for messages)
   ↓
3. Results Review
   ↓
CampaignView (tabs, copy, download, print)
   ↓
4. Action
   ↓
Restart → Back to UploadPage
```

## Component State Management

### App.js (Main State)
```javascript
const [currentPage, setCurrentPage] = useState('upload')
const [uploadedDocument, setUploadedDocument] = useState(null)
const [generatedCampaign, setGeneratedCampaign] = useState(null)
```

### UploadPage
- Local: `dragActive`, `file`, `preview`, `error`

### AgentRoom
- Local: `agents[]`, `currentAgent`, `isProcessing`, `campaign`
- Manages agent initialization and API calls

### ChatFeed
- Local: `messagesEndRef`
- Handles message display and auto-scroll

### CampaignView
- Local: `activeTab`, `copied`
- Manages content display and user interactions

## API Integration Points

### UploadPage → AgentRoom
- File content passed as `document.content`

### AgentRoom → Backend
```javascript
POST http://localhost:8000/generate-campaign
{
  document_text: content,
  export_format: 'json'
}
```

### AgentRoom → CampaignView
- Campaign data passed through state

## Styling Architecture

### Color Scheme
- **Primary Gradient**: #667eea → #764ba2 (Purple/Blue)
- **Success**: #48bb78 (Green)
- **Warning**: #ed8936 (Orange)
- **Error**: #fc8181 (Red)
- **Background**: #fafafa (Light Gray)
- **Text**: #1a202c (Dark Gray)

### Responsive Breakpoints
- **Desktop**: 1200px+
- **Tablet**: 768px - 1199px
- **Mobile**: < 768px

### Key Features
- Smooth animations and transitions
- Custom scrollbar styling
- Gradient backgrounds
- Shadow depth hierarchy
- Mobile-first responsive design

## File Structure Summary

| Component | Type | Responsibility |
|-----------|------|-----------------|
| UploadPage | Upload | File input and validation |
| AgentRoom | Orchestration | Agent management and workflow |
| ChatFeed | Display | Message rendering |
| CampaignView | Results | Content display and export |

## Next Steps

1. **Install Dependencies**
   ```bash
   npm install react react-dom axios
   ```

2. **Configure Tailwind** (if using Tailwind CSS)
   ```bash
   npm install -D tailwindcss postcss autoprefixer
   npx tailwindcss init -p
   ```

3. **Start Development Server**
   ```bash
   npm start
   ```

4. **Ensure Backend Running**
   ```bash
   cd backend
   python -m uvicorn api:app --reload
   ```

## Environment Configuration

Required `.env` file in frontend root:
```
REACT_APP_API_URL=http://localhost:8000
```

## Testing Workflow

1. Start with UploadPage - upload test document
2. Proceed to AgentRoom - watch agent simulation
3. Review CampaignView - check generated content
4. Test all tab switches and copy/download functions
5. Verify responsive design on mobile view
