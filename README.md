# Motion Graphics Portfolio Website

A premium, modern portfolio website for motion graphics artists with Python-based content management.

![Portfolio Preview](https://img.shields.io/badge/Status-Ready-success?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.7+-blue?style=for-the-badge&logo=python)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

## ✨ Features

- **Premium Design**: Modern, clean aesthetic with dark blue accents and light gray backgrounds
- **Fully Responsive**: Optimized for mobile, tablet, and desktop devices
- **Smooth Animations**: Fade-in effects, hover interactions, and micro-animations
- **Dynamic Content**: All content loaded from JSON - no hard-coded text
- **Python Content Manager**: Easy-to-use CLI tool for updating portfolio content
- **SEO Optimized**: Proper meta tags, semantic HTML, and structured data
- **Performance**: Lightweight, fast-loading with optimized assets

## 🎨 Design Features

### Color Scheme
- **White** (`#FFFFFF`) - Base UI and text
- **Dark Blue** (`#1E3A8A`) - Main accent for headlines, buttons, highlights
- **Light Gray** (`#F3F4F6`) - Section backgrounds

### Typography
- **Headings**: Poppins (Google Fonts)
- **Body**: Inter (Google Fonts)

### Sections
1. **Hero** - Full-screen introduction with animated gradients
2. **About** - Personal narrative and expertise areas
3. **Skills** - Software and tools with proficiency levels
4. **Showcase** - Project gallery with hover effects
5. **Contact** - Professional contact information and social links

## 📁 Project Structure

```
Naufal_project/
├── index.html              # Main HTML file
├── css/
│   └── styles.css          # All styles and animations
├── js/
│   └── main.js             # Dynamic content loading and interactions
├── data/
│   ├── portfolio-data.json # Portfolio content (editable)
│   └── backups/            # Automatic backups
├── assets/
│   └── projects/           # Project thumbnails
├── content_manager.py      # Python content management tool
└── README.md               # This file
```

## 🚀 Getting Started

### Prerequisites

- Modern web browser (Chrome, Firefox, Safari, Edge)
- Python 3.7+ (for content management)
- Local web server (optional, for development)

### Installation

1. **Clone or download** this repository

2. **Run the GUI Manager**:
   - **Windows**: Double-click `run_gui.bat`
   - **Linux/Mac**: Run `./run_gui.sh` in terminal (or double-click if configured)

   Alternatively, use the command line:
   ```bash
   python3 gui_manager.py
   ```

3. **Open the website**:
   - Simply open `index.html` in your browser, or
   - Use a local server (recommended):
     ```bash
     # Python 3
     python -m http.server 8000
     
     # Then visit http://localhost:8000
     ```

## 🛠️ Content Management

### GUI Manager (Recommended)

The easiest way to manage your portfolio is using the GUI application.

1. Run `run_gui.bat` (Windows) or `./run_gui.sh` (Linux)
2. Use the tabs to navigate between sections:
   - **General**: Update name, title, and **upload logo**
   - **Theme**: Customize colors and fonts
   - **About**: Edit bio and expertise
   - **Skills**: Manage skills with visual sliders
   - **Projects**: Add projects and **upload videos**
   - **Contact**: Update contact info
3. Click **Save All Changes** to apply updates

### CLI Manager (Advanced)

Run the content manager in interactive mode:

```bash
python content_manager.py
```

This will show a menu where you can:
1. Update personal information (name, title, tagline)
2. Update about section (bio, description, expertise)
3. Manage skills (add/edit/remove)
4. Manage projects (add/edit/remove)
5. Update contact information (email, location, social links)

### Command-Line Mode

Quick updates via command-line arguments:

```bash
# Update your name
python content_manager.py --update-name "Your Name"

# Update bio
python content_manager.py --update-bio "Your new bio text here"

# Add a new skill
python content_manager.py --add-skill "After Effects" "2D Animation" 95 "⚡"

# View help
python content_manager.py --help
```

### Data Structure

All content is stored in `data/portfolio-data.json`:

```json
{
  "personal": {
    "name": "Your Name",
    "title": "Motion Graphics Artist",
    "tagline": "Your tagline",
    "heroDescription": "Your description"
  },
  "about": {
    "bio": "Your bio",
    "description": "Extended description",
    "expertise": ["Expertise 1", "Expertise 2"]
  },
  "skills": [
    {
      "name": "After Effects",
      "category": "2D Animation",
      "proficiency": 95,
      "icon": "⚡"
    }
  ],
  "projects": [
    {
      "id": 1,
      "title": "Project Name",
      "description": "Project description",
      "thumbnail": "assets/projects/project1.jpg",
      "videoUrl": "https://vimeo.com/your-video",
      "tags": ["Tag1", "Tag2"],
      "year": 2024
    }
  ],
  "contact": {
    "email": "your.email@example.com",
    "location": "Your City",
    "availability": "Available for freelance",
    "social": [
      {
        "platform": "Behance",
        "url": "https://behance.net/you",
        "icon": "🎨"
      }
    ]
  }
}
```

## 🎬 Adding Projects

1. **Add project images** to `assets/projects/` folder
2. **Run content manager**:
   ```bash
   python content_manager.py
   ```
3. Select **"4. Manage Projects"** → **"1. Add new project"**
4. Fill in the details:
   - Title
   - Description
   - Thumbnail path (e.g., `assets/projects/myproject.jpg`)
   - Video URL (Vimeo, YouTube, etc.)
   - Tags
   - Year

## 🌐 Deployment

### GitHub Pages

1. Create a new GitHub repository
2. Push your code:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/portfolio.git
   git push -u origin main
   ```
3. Go to repository **Settings** → **Pages**
4. Select **main** branch and **Save**
5. Your site will be live at `https://yourusername.github.io/portfolio`

### Netlify

1. Drag and drop your project folder to [Netlify Drop](https://app.netlify.com/drop)
2. Your site will be live instantly!

### Vercel

1. Install Vercel CLI: `npm i -g vercel`
2. Run: `vercel`
3. Follow the prompts

## 🎯 Customization

### Change Colors

Edit `css/styles.css` and modify CSS custom properties:

```css
:root {
    --color-dark-blue: #1E3A8A;      /* Main accent */
    --color-light-gray: #F3F4F6;     /* Background */
    /* ... */
}
```

### Change Fonts

Update the Google Fonts link in `index.html`:

```html
<link href="https://fonts.googleapis.com/css2?family=YourFont&display=swap" rel="stylesheet">
```

Then update CSS:

```css
:root {
    --font-heading: 'YourFont', sans-serif;
}
```

### Modify Animations

Animation timing and effects can be adjusted in `css/styles.css`:

- `@keyframes` sections define animations
- `transition` properties control hover effects
- `animation` properties set timing and duration

## 📱 Browser Support

- ✅ Chrome (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Edge (latest)
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## 🔧 Troubleshooting

### Content Not Loading

1. Check browser console for errors (F12)
2. Ensure `portfolio-data.json` is valid JSON
3. Use a local server instead of opening HTML directly

### Images Not Showing

1. Verify image paths in `portfolio-data.json`
2. Ensure images exist in `assets/projects/` folder
3. Check image file extensions match exactly

### Python Script Issues

1. Ensure Python 3.7+ is installed: `python --version`
2. Run from project root directory
3. Check `data/portfolio-data.json` exists

## 📄 License

This project is free to use for personal and commercial purposes.

## 🤝 Support

For issues or questions:
- Check this README
- Review `portfolio-data.json` for correct format
- Ensure all files are in correct directories

## 🎓 Tips for Motion Graphics Artists

### Portfolio Best Practices

1. **Quality over Quantity**: Show 6-8 of your absolute best projects
2. **Update Regularly**: Keep your portfolio current with recent work
3. **Tell a Story**: Each project should have a clear narrative
4. **Show Process**: Consider adding breakdown videos or case studies
5. **Optimize Videos**: Use Vimeo Pro for better quality and no ads
6. **Professional Thumbnails**: Create eye-catching preview images

### Recommended Platforms

- **Vimeo**: Best for high-quality video hosting
- **Behance**: Showcase detailed project breakdowns
- **Instagram**: Share behind-the-scenes and WIP content
- **LinkedIn**: Connect with industry professionals

### Skills to Highlight

Make sure to include:
- Primary software (After Effects, Cinema 4D, Blender)
- Editing tools (Premiere, DaVinci Resolve)
- Design tools (Illustrator, Photoshop)
- Specialized skills (Compositing, Character Animation, VFX)

---

**Built with creativity and code** ✨

Ready to showcase your motion graphics work professionally!
