# Preview Toggle Feature - Implementation Guide

## 📋 Overview

The Preview Toggle feature adds three distinct viewing modes to the CampaignView component, allowing users to preview their generated content in different formats:

1. **Default View** - Tab-based interface with original document and generated outputs
2. **Desktop Blog Preview** - Professional blog article layout
3. **Mobile Twitter Thread Preview** - Social media thread card interface

## 🎯 Features

### 1. Default View (📋 Default)
- **Purpose**: Traditional tab-based navigation
- **Layout**: Split-panel design (original content + generated outputs)
- **Tabs**: Blog Post, Social Media Thread, Email Teaser
- **Actions**: Copy, Download for each content piece

### 2. Desktop Blog Preview (🖥️ Blog Preview)
- **Purpose**: See blog content in article format
- **Layout**: Professional centered blog article
- **Styling**: Georgia serif font, readable typography
- **Features**:
  - Article title
  - Publication date
  - Estimated reading time
  - Professional spacing and typography
  - Word count
  - Share/Save buttons
  - Copy and Download actions

### 3. Mobile Twitter Thread Preview (📱 Twitter Thread)
- **Purpose**: Preview social content as Twitter/X thread
- **Layout**: Mobile-phone sized card interface
- **Features**:
  - Twitter-style profile header
  - Tweet cards with avatars
  - Thread connector lines between tweets
  - Character count (280 char limit)
  - Tweet action buttons (Reply, Retweet, Like, Share)
  - Hover effects and animations
  - Copy and Download actions

## 🔧 Technical Implementation

### Component State
```javascript
const [previewMode, setPreviewMode] = useState('default');
// Values: 'default' | 'desktop-blog' | 'mobile-twitter'
```

### Preview Components
Two new internal React components handle the preview rendering:

#### DesktopBlogPreview
- Displays blog content in professional article format
- Uses Georgia serif font for authenticity
- Includes metadata (date, reading time)
- Centered, max-width container for optimal readability

#### MobileTwitterPreview
- Renders social content as tweet cards
- Splits content by '\n---\n' separator
- Shows thread connectors between tweets
- Includes interactive tweet actions
- Mobile-optimized card design

### Conditional Rendering
```javascript
{previewMode === 'default' ? (
  // Default tab-based view
) : previewMode === 'desktop-blog' ? (
  <DesktopBlogPreview />
) : (
  <MobileTwitterPreview />
)}
```

## 🎨 Styling Details

### Toggle Button Group (.header-controls)
- Positioned in header area
- Three toggle buttons with active state indicator
- Blue (#3b82f6) highlight for active button
- Smooth transitions

### Blog Article Styles
- **Font**: Georgia serif for authentic article feel
- **Max-width**: 800px for optimal readability
- **Padding**: 40px for breathing room
- **Spacing**: 18px paragraph margins
- **Colors**: Professional grays and blacks

### Twitter Card Styles
- **Card width**: 400px max (mobile-sized)
- **Avatar**: 48px circular profile images
- **Thread connector**: Vertical line between tweets
- **Hover effects**: Subtle background change
- **Action buttons**: Icon-based with color coding
  - Reply (💬) - Blue
  - Retweet (🔄) - Green
  - Like (❤️) - Red
  - Share (📤) - Blue

## 📱 Responsive Behavior

### Mobile (< 768px)
- Toggle buttons stack and wrap
- Toggle button text reduced
- Blog article padding reduced to 20px
- Blog title reduced to 24px
- Twitter preview takes full width
- Smaller font sizes throughout

### Desktop (> 768px)
- Toggle buttons in single row
- Full-size blog article (800px max)
- Twitter preview card centered
- Optimal spacing and typography

## 🚀 Usage

### For Users
1. View generated campaign content in default tab view
2. Click "🖥️ Blog Preview" to see how blog will look in article format
3. Click "📱 Twitter Thread" to preview social content as Twitter thread
4. Use Copy and Download buttons in each preview
5. Switch back to "📋 Default" for tab-based navigation

### For Developers
```javascript
// Import the component
import CampaignView from './components/CampaignView';

// Use with campaign data
<CampaignView 
  campaign={{
    blog: "Blog content...",
    social: "Tweet 1\n---\nTweet 2",
    email: "Email content...",
    originalContent: "Original document..."
  }}
  onBack={() => navigate('/')}
/>
```

## 📊 File Changes

### CampaignView.jsx
- **Lines**: 463 (increased from 299)
- **Changes**:
  - Added `previewMode` state
  - Added `DesktopBlogPreview` component
  - Added `MobileTwitterPreview` component
  - Added preview toggle buttons in header
  - Conditional rendering based on preview mode

### CampaignView.css
- **Lines**: 1065 (increased from 679)
- **Changes**:
  - Added `.header-controls` and `.preview-toggle` styles
  - Added `.toggle-btn` and `.toggle-btn.active` styles
  - Added `.preview-container` base styles
  - Added `.desktop-blog-preview` and blog article styles
  - Added `.mobile-twitter-preview` and tweet styles
  - Added responsive media queries for mobile views

## 🎪 CSS Classes Reference

### Layout & Containers
- `.header-controls` - Toggle control container in header
- `.preview-toggle` - Button group wrapper
- `.preview-container` - Main preview content wrapper
- `.desktop-blog-preview` - Blog preview container
- `.mobile-twitter-preview` - Twitter preview container

### Blog Preview
- `.blog-article` - Article wrapper
- `.blog-header` - Article header with title
- `.blog-title` - Article title
- `.blog-meta` - Publication metadata
- `.blog-date` - Publication date
- `.blog-reading-time` - Estimated reading time
- `.blog-body` - Article content area
- `.blog-paragraph` - Individual paragraphs
- `.blog-footer` - Article footer with share options

### Twitter Preview
- `.twitter-header` - Profile header
- `.twitter-profile` - Profile info container
- `.profile-avatar` - Profile picture circle
- `.profile-info` - Profile name and handle
- `.twitter-thread` - Tweet container
- `.tweet-card` - Individual tweet wrapper
- `.tweet-avatar` - Tweet author avatar
- `.tweet-content` - Tweet text and metadata
- `.tweet-header` - Tweet author info
- `.tweet-text` - Tweet body text
- `.tweet-stats` - Character count and stats
- `.tweet-actions` - Action button group

### Interactive Elements
- `.toggle-btn` - Preview mode toggle button
- `.toggle-btn.active` - Active toggle button state
- `.share-btn` - Blog share button
- `.save-btn` - Blog save button
- `.tweet-action` - Tweet action buttons

## ✨ Design Highlights

### User Experience
- **Smooth transitions** between preview modes
- **Instant feedback** with active button highlighting
- **Intuitive icons** for quick mode identification
- **Consistent actions** across all preview modes
- **Responsive design** for all screen sizes

### Visual Consistency
- **Color scheme**: Blue (#3b82f6) for interactive elements
- **Spacing**: Consistent gap sizing (8px, 12px, 16px, 20px)
- **Typography**: Mix of sans-serif and serif fonts
- **Borders**: Subtle gray borders (#e5e7eb)
- **Shadows**: Light, professional shadows for depth

## 🔄 Data Flow

```
Campaign Data Input
         ↓
CampaignView Component
         ↓
    ┌─────────────────────────┐
    │   previewMode State     │
    └─────────────────────────┘
         ↓
    ┌─────────────────┬──────────────────┬──────────────────┐
    ↓                 ↓                  ↓
Default View    Blog Preview      Twitter Preview
(Tabs)          (Article)         (Thread)
    ↓                 ↓                  ↓
Output Actions (Copy/Download)
```

## 🎓 Examples

### Example 1: Simple Blog Content
```
Title: "How to Get Started"
Body paragraphs separated by double line breaks
```

### Example 2: Twitter Thread
```
Tweet 1: "Here's thread about..."
---
Tweet 2: "First point to consider..."
---
Tweet 3: "Another important aspect..."
```

## 🚨 Error Handling

- **No blog content**: Shows "Blog content not available"
- **No tweets**: Shows "Twitter thread content not available"
- **Empty content**: Graceful empty state messages
- **Copy action**: Visual feedback (✓ Copied!) for 2 seconds
- **Download**: Works across all browsers with blob API

## 🌟 Future Enhancements

Potential improvements:
1. Email preview as realistic email client UI
2. LinkedIn post preview
3. Instagram caption preview
4. PDF export from each preview mode
5. Custom brand colors/fonts for blog preview
6. Social platform-specific formatting
7. Preview animation/transition effects
8. Keyboard shortcuts for preview switching
9. Local storage of preview preferences
10. Share preview links

## 📚 Related Files

- **CampaignView.jsx** - Main component file (463 lines)
- **CampaignView.css** - Complete styling (1065 lines)
- **UploadPage.jsx** - Parent component
- **App.jsx** - Main application component

## ✅ Testing Checklist

- [ ] Toggle buttons appear in header
- [ ] Default view shows original split-panel layout
- [ ] Blog preview displays article format
- [ ] Twitter preview shows tweet cards
- [ ] Copy functionality works in all modes
- [ ] Download functionality works in all modes
- [ ] Responsive design on mobile devices
- [ ] Smooth transitions between modes
- [ ] No console errors
- [ ] All buttons are clickable
- [ ] Active button state visible
- [ ] Content renders correctly
- [ ] Empty states show appropriate messages

## 🎉 Summary

The Preview Toggle feature enhances the user experience by providing format-specific content previews. Users can seamlessly switch between traditional tab navigation, professional blog article view, and authentic Twitter thread visualization, making it easier to envision how their content will appear across different platforms.

---

**Version**: 1.0.0  
**Status**: Production Ready ✅  
**Last Updated**: April 2024
