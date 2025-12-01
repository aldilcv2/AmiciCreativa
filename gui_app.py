import sys
import json
import os
import shutil
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTabWidget, QLabel, QLineEdit, QTextEdit, QPushButton, 
                             QColorDialog, QFileDialog, QMessageBox, QFormLayout, 
                             QListWidget, QScrollArea, QFrame, QComboBox, QSplitter, QSlider)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont, QColor

# Configuration
DATA_FILE = 'data/portfolio-data.json'
ASSETS_DIR = 'assets'
PROJECTS_DIR = os.path.join(ASSETS_DIR, 'projects')
VIDEOS_DIR = os.path.join(ASSETS_DIR, 'videos')

class PortfolioApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Portfolio Content Manager (Professional)")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("""
            QMainWindow { background-color: #f0f2f5; }
            QTabWidget::pane { border: 1px solid #d1d5db; background: white; border-radius: 5px; }
            QTabBar::tab { background: #e5e7eb; padding: 10px 20px; border-top-left-radius: 5px; border-top-right-radius: 5px; margin-right: 2px; }
            QTabBar::tab:selected { background: white; border-bottom: 2px solid #3b82f6; font-weight: bold; }
            QLabel { font-size: 14px; color: #374151; }
            QLineEdit, QTextEdit, QComboBox { padding: 8px; border: 1px solid #d1d5db; border-radius: 4px; background: #f9fafb; }
            QLineEdit:focus, QTextEdit:focus { border: 1px solid #3b82f6; }
            QPushButton { background-color: #3b82f6; color: white; padding: 8px 16px; border-radius: 4px; border: none; font-weight: bold; }
            QPushButton:hover { background-color: #2563eb; }
            QPushButton#DeleteBtn { background-color: #ef4444; }
            QPushButton#DeleteBtn:hover { background-color: #dc2626; }
            QListWidget { border: 1px solid #d1d5db; border-radius: 4px; padding: 5px; }
        """)
        
        self.data = self.load_data()
        self.init_ui()

    def load_data(self):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Ensure config exists
                if 'config' not in data:
                    data['config'] = {
                        "theme": {
                            "primaryColor": "#1E3A8A",
                            "secondaryColor": "#F3F4F6",
                            "backgroundColor": "#FFFFFF",
                            "textColor": "#111827",
                            "fontHeading": "Outfit",
                            "fontBody": "Plus Jakarta Sans"
                        },
                        "logo": {"type": "text", "content": "Portfolio"}
                    }
                return data
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load data: {e}")
            return {}

    def save_data(self):
        try:
            self.update_data_from_ui()
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            QMessageBox.information(self, "Success", "Data saved successfully! Refresh your website to see changes.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save data: {e}")

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Portfolio Manager")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #111827;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        save_btn = QPushButton("Save All Changes")
        save_btn.clicked.connect(self.save_data)
        save_btn.setMinimumWidth(150)
        header_layout.addWidget(save_btn)
        layout.addLayout(header_layout)
        
        # Tabs
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        self.init_general_tab()
        self.init_theme_tab()
        self.init_about_tab()
        self.init_skills_tab()
        self.init_projects_tab()
        self.init_contact_tab()

    def create_form_row(self, layout, label_text, value, var_attr=None):
        row = QHBoxLayout()
        label = QLabel(label_text)
        label.setMinimumWidth(120)
        widget = QLineEdit(str(value))
        row.addWidget(label)
        row.addWidget(widget)
        layout.addLayout(row)
        if var_attr:
            setattr(self, var_attr, widget)
        return widget

    # ==========================================
    # TAB 1: GENERAL
    # ==========================================
    def init_general_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Personal Info Group
        group = QFrame()
        group.setStyleSheet("QFrame { background: white; border-radius: 8px; padding: 10px; }")
        group_layout = QVBoxLayout(group)
        group_layout.addWidget(QLabel("Personal Information"))
        
        self.name_input = self.create_form_row(group_layout, "Name:", self.data['personal'].get('name', ''))
        self.title_input = self.create_form_row(group_layout, "Title:", self.data['personal'].get('title', ''))
        self.tagline_input = self.create_form_row(group_layout, "Tagline:", self.data['personal'].get('tagline', ''))
        
        group_layout.addWidget(QLabel("Hero Description:"))
        self.hero_desc_input = QTextEdit()
        self.hero_desc_input.setPlainText(self.data['personal'].get('heroDescription', ''))
        self.hero_desc_input.setMaximumHeight(80)
        group_layout.addWidget(self.hero_desc_input)
        
        layout.addWidget(group)
        
        # Logo Group
        logo_group = QFrame()
        logo_group.setStyleSheet("QFrame { background: white; border-radius: 8px; padding: 10px; margin-top: 10px; }")
        logo_layout = QVBoxLayout(logo_group)
        logo_layout.addWidget(QLabel("Logo Settings"))
        
        type_row = QHBoxLayout()
        type_row.addWidget(QLabel("Type:"))
        self.logo_type_combo = QComboBox()
        self.logo_type_combo.addItems(["text", "image"])
        self.logo_type_combo.setCurrentText(self.data['config']['logo'].get('type', 'text'))
        type_row.addWidget(self.logo_type_combo)
        logo_layout.addLayout(type_row)
        
        content_row = QHBoxLayout()
        content_row.addWidget(QLabel("Content:"))
        self.logo_content_input = QLineEdit(self.data['config']['logo'].get('content', ''))
        content_row.addWidget(self.logo_content_input)
        upload_btn = QPushButton("Upload Image")
        upload_btn.clicked.connect(self.upload_logo)
        content_row.addWidget(upload_btn)
        logo_layout.addLayout(content_row)
        
        layout.addWidget(logo_group)
        layout.addStretch()
        self.tabs.addTab(tab, "General")

    def upload_logo(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', '', "Image files (*.jpg *.png *.svg)")
        if fname:
            dest = os.path.join(ASSETS_DIR, os.path.basename(fname))
            try:
                shutil.copy2(fname, dest)
                self.logo_content_input.setText(dest)
                self.logo_type_combo.setCurrentText("image")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    # ==========================================
    # TAB 2: THEME
    # ==========================================
    def init_theme_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Colors
        color_group = QFrame()
        color_group.setStyleSheet("QFrame { background: white; border-radius: 8px; padding: 10px; }")
        color_layout = QFormLayout(color_group)
        color_layout.addRow(QLabel("<b>Color Scheme</b>"))
        
        self.colors = {}
        theme_data = self.data['config']['theme']
        
        for key, label in [
            ('primaryColor', 'Primary Color (Accent)'),
            ('secondaryColor', 'Secondary Color (Bg)'),
            ('backgroundColor', 'Base Background'),
            ('textColor', 'Text Color')
        ]:
            row = QHBoxLayout()
            input_field = QLineEdit(theme_data.get(key, '#000000'))
            btn = QPushButton("Pick")
            btn.setFixedWidth(60)
            # Use closure to capture current key/input
            btn.clicked.connect(lambda checked, k=key, i=input_field: self.pick_color(i))
            
            row.addWidget(input_field)
            row.addWidget(btn)
            color_layout.addRow(label, row)
            self.colors[key] = input_field
            
        layout.addWidget(color_group)
        
        # Fonts
        font_group = QFrame()
        font_group.setStyleSheet("QFrame { background: white; border-radius: 8px; padding: 10px; margin-top: 10px; }")
        font_layout = QFormLayout(font_group)
        font_layout.addRow(QLabel("<b>Typography</b>"))
        
        fonts = ["Outfit", "Plus Jakarta Sans", "Poppins", "Inter", "Montserrat", "Roboto", "Open Sans"]
        
        self.font_heading = QComboBox()
        self.font_heading.addItems(fonts)
        self.font_heading.setCurrentText(theme_data.get('fontHeading', 'Outfit'))
        
        self.font_body = QComboBox()
        self.font_body.addItems(fonts)
        self.font_body.setCurrentText(theme_data.get('fontBody', 'Plus Jakarta Sans'))
        
        font_layout.addRow("Heading Font:", self.font_heading)
        font_layout.addRow("Body Font:", self.font_body)
        
        layout.addWidget(font_group)
        layout.addStretch()
        self.tabs.addTab(tab, "Theme")

    def pick_color(self, input_field):
        color = QColorDialog.getColor(QColor(input_field.text()))
        if color.isValid():
            input_field.setText(color.name())

    # ==========================================
    # TAB 3: ABOUT
    # ==========================================
    def init_about_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        layout.addWidget(QLabel("Bio:"))
        self.bio_input = QTextEdit()
        self.bio_input.setPlainText(self.data['about'].get('bio', ''))
        self.bio_input.setMaximumHeight(80)
        layout.addWidget(self.bio_input)
        
        layout.addWidget(QLabel("Detailed Description:"))
        self.about_desc_input = QTextEdit()
        self.about_desc_input.setPlainText(self.data['about'].get('description', ''))
        self.about_desc_input.setMaximumHeight(120)
        layout.addWidget(self.about_desc_input)
        
        # Expertise
        layout.addWidget(QLabel("Expertise Areas:"))
        exp_layout = QHBoxLayout()
        self.exp_list = QListWidget()
        self.exp_list.addItems(self.data['about'].get('expertise', []))
        exp_layout.addWidget(self.exp_list)
        
        btn_layout = QVBoxLayout()
        self.new_exp_input = QLineEdit()
        self.new_exp_input.setPlaceholderText("New expertise...")
        add_btn = QPushButton("Add")
        add_btn.clicked.connect(self.add_expertise)
        del_btn = QPushButton("Remove")
        del_btn.setObjectName("DeleteBtn")
        del_btn.clicked.connect(self.remove_expertise)
        
        btn_layout.addWidget(self.new_exp_input)
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(del_btn)
        btn_layout.addStretch()
        
        exp_layout.addLayout(btn_layout)
        layout.addLayout(exp_layout)
        
        self.tabs.addTab(tab, "About")

    def add_expertise(self):
        val = self.new_exp_input.text().strip()
        if val:
            self.exp_list.addItem(val)
            self.new_exp_input.clear()

    def remove_expertise(self):
        row = self.exp_list.currentRow()
        if row >= 0:
            self.exp_list.takeItem(row)

    # ==========================================
    # TAB 4: SKILLS
    # ==========================================
    def init_skills_tab(self):
        tab = QWidget()
        layout = QHBoxLayout(tab)
        
        # Left: List
        left_layout = QVBoxLayout()
        self.skills_list_widget = QListWidget()
        self.skills_list_widget.currentRowChanged.connect(self.load_skill)
        left_layout.addWidget(self.skills_list_widget)
        
        new_skill_btn = QPushButton("New Skill")
        new_skill_btn.clicked.connect(self.new_skill)
        left_layout.addWidget(new_skill_btn)
        layout.addLayout(left_layout, 1)
        
        # Right: Editor
        self.skill_editor = QFrame()
        self.skill_editor.setStyleSheet("QFrame { background: white; border-radius: 8px; padding: 10px; }")
        right_layout = QFormLayout(self.skill_editor)
        
        self.skill_name = QLineEdit()
        self.skill_cat = QLineEdit()
        self.skill_icon = QLineEdit()
        self.skill_prof = QSlider(Qt.Horizontal)
        self.skill_prof.setRange(0, 100)
        self.skill_prof_label = QLabel("50%")
        self.skill_prof.valueChanged.connect(lambda v: self.skill_prof_label.setText(f"{v}%"))
        
        right_layout.addRow("Name:", self.skill_name)
        right_layout.addRow("Category:", self.skill_cat)
        right_layout.addRow("Icon (Emoji):", self.skill_icon)
        
        prof_row = QHBoxLayout()
        prof_row.addWidget(self.skill_prof)
        prof_row.addWidget(self.skill_prof_label)
        right_layout.addRow("Proficiency:", prof_row)
        
        btn_row = QHBoxLayout()
        save_btn = QPushButton("Save Skill")
        save_btn.clicked.connect(self.save_skill)
        del_btn = QPushButton("Delete Skill")
        del_btn.setObjectName("DeleteBtn")
        del_btn.clicked.connect(self.delete_skill)
        btn_row.addWidget(save_btn)
        btn_row.addWidget(del_btn)
        right_layout.addRow(btn_row)
        
        layout.addWidget(self.skill_editor, 2)
        
        self.refresh_skills_list()
        self.tabs.addTab(tab, "Skills")
        
    def refresh_skills_list(self):
        self.skills_list_widget.clear()
        for skill in self.data['skills']:
            self.skills_list_widget.addItem(skill['name'])
            
    def load_skill(self, idx):
        if idx >= 0:
            skill = self.data['skills'][idx]
            self.skill_name.setText(skill['name'])
            self.skill_cat.setText(skill['category'])
            self.skill_icon.setText(skill['icon'])
            self.skill_prof.setValue(skill['proficiency'])
            self.current_skill_idx = idx
            
    def new_skill(self):
        self.skills_list_widget.clearSelection()
        self.skill_name.clear()
        self.skill_cat.clear()
        self.skill_icon.setText("⚡")
        self.skill_prof.setValue(50)
        self.current_skill_idx = None
        
    def save_skill(self):
        new_skill = {
            "name": self.skill_name.text(),
            "category": self.skill_cat.text(),
            "proficiency": self.skill_prof.value(),
            "icon": self.skill_icon.text()
        }
        
        if hasattr(self, 'current_skill_idx') and self.current_skill_idx is not None:
            self.data['skills'][self.current_skill_idx] = new_skill
        else:
            self.data['skills'].append(new_skill)
            
        self.refresh_skills_list()
        
    def delete_skill(self):
        if hasattr(self, 'current_skill_idx') and self.current_skill_idx is not None:
            self.data['skills'].pop(self.current_skill_idx)
            self.refresh_skills_list()
            self.new_skill()

    # ==========================================
    # TAB 5: PROJECTS
    # ==========================================
    def init_projects_tab(self):
        tab = QWidget()
        layout = QHBoxLayout(tab)
        
        # Left: List
        left_layout = QVBoxLayout()
        self.proj_list_widget = QListWidget()
        self.proj_list_widget.currentRowChanged.connect(self.load_project)
        left_layout.addWidget(self.proj_list_widget)
        
        new_proj_btn = QPushButton("New Project")
        new_proj_btn.clicked.connect(self.new_project)
        left_layout.addWidget(new_proj_btn)
        layout.addLayout(left_layout, 1)
        
        # Right: Editor
        self.proj_editor = QFrame()
        self.proj_editor.setStyleSheet("QFrame { background: white; border-radius: 8px; padding: 10px; }")
        right_layout = QFormLayout(self.proj_editor)
        
        self.proj_title = QLineEdit()
        self.proj_year = QLineEdit()
        self.proj_desc = QTextEdit()
        self.proj_desc.setMaximumHeight(80)
        self.proj_tags = QLineEdit()
        
        # Thumbnail
        thumb_row = QHBoxLayout()
        self.proj_thumb = QLineEdit()
        thumb_btn = QPushButton("Upload")
        thumb_btn.clicked.connect(lambda: self.upload_file(self.proj_thumb, PROJECTS_DIR))
        thumb_row.addWidget(self.proj_thumb)
        thumb_row.addWidget(thumb_btn)
        
        # Video
        video_row = QHBoxLayout()
        self.proj_video = QLineEdit()
        video_btn = QPushButton("Upload")
        video_btn.clicked.connect(lambda: self.upload_file(self.proj_video, VIDEOS_DIR))
        video_row.addWidget(self.proj_video)
        video_row.addWidget(video_btn)
        
        right_layout.addRow("Title:", self.proj_title)
        right_layout.addRow("Year:", self.proj_year)
        right_layout.addRow("Description:", self.proj_desc)
        right_layout.addRow("Tags (comma sep):", self.proj_tags)
        right_layout.addRow("Thumbnail:", thumb_row)
        right_layout.addRow("Video:", video_row)
        
        btn_row = QHBoxLayout()
        save_btn = QPushButton("Save Project")
        save_btn.clicked.connect(self.save_project)
        del_btn = QPushButton("Delete Project")
        del_btn.setObjectName("DeleteBtn")
        del_btn.clicked.connect(self.delete_project)
        btn_row.addWidget(save_btn)
        btn_row.addWidget(del_btn)
        right_layout.addRow(btn_row)
        
        layout.addWidget(self.proj_editor, 2)
        
        self.refresh_projects_list()
        self.tabs.addTab(tab, "Projects")

    def upload_file(self, input_field, target_dir):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', '')
        if fname:
            os.makedirs(target_dir, exist_ok=True)
            dest = os.path.join(target_dir, os.path.basename(fname))
            try:
                shutil.copy2(fname, dest)
                input_field.setText(dest)
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def refresh_projects_list(self):
        self.proj_list_widget.clear()
        for proj in self.data['projects']:
            self.proj_list_widget.addItem(proj['title'])

    def load_project(self, idx):
        if idx >= 0:
            proj = self.data['projects'][idx]
            self.proj_title.setText(proj['title'])
            self.proj_year.setText(proj['year'])
            self.proj_desc.setPlainText(proj['description'])
            self.proj_tags.setText(", ".join(proj['tags']))
            self.proj_thumb.setText(proj['thumbnail'])
            self.proj_video.setText(proj.get('videoUrl', ''))
            self.current_proj_idx = idx

    def new_project(self):
        self.proj_list_widget.clearSelection()
        self.proj_title.clear()
        self.proj_year.clear()
        self.proj_desc.clear()
        self.proj_tags.clear()
        self.proj_thumb.clear()
        self.proj_video.clear()
        self.current_proj_idx = None

    def save_project(self):
        tags = [t.strip() for t in self.proj_tags.text().split(',') if t.strip()]
        new_proj = {
            "id": self.data['projects'][self.current_proj_idx]['id'] if hasattr(self, 'current_proj_idx') and self.current_proj_idx is not None else len(self.data['projects']) + 1,
            "title": self.proj_title.text(),
            "description": self.proj_desc.toPlainText(),
            "thumbnail": self.proj_thumb.text(),
            "videoUrl": self.proj_video.text(),
            "tags": tags,
            "year": self.proj_year.text()
        }
        
        if hasattr(self, 'current_proj_idx') and self.current_proj_idx is not None:
            self.data['projects'][self.current_proj_idx] = new_proj
        else:
            self.data['projects'].append(new_proj)
            
        self.refresh_projects_list()
        self.new_project()

    def delete_project(self):
        if hasattr(self, 'current_proj_idx') and self.current_proj_idx is not None:
            self.data['projects'].pop(self.current_proj_idx)
            self.refresh_projects_list()
            self.new_project()

    # ==========================================
    # TAB 6: CONTACT
    # ==========================================
    def init_contact_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        group = QFrame()
        group.setStyleSheet("QFrame { background: white; border-radius: 8px; padding: 10px; }")
        group_layout = QFormLayout(group)
        
        self.email_input = QLineEdit(self.data['contact'].get('email', ''))
        self.loc_input = QLineEdit(self.data['contact'].get('location', ''))
        self.avail_input = QLineEdit(self.data['contact'].get('availability', ''))
        
        group_layout.addRow("Email:", self.email_input)
        group_layout.addRow("Location:", self.loc_input)
        group_layout.addRow("Availability:", self.avail_input)
        
        layout.addWidget(group)
        layout.addStretch()
        self.tabs.addTab(tab, "Contact")

    def update_data_from_ui(self):
        # General
        self.data['personal']['name'] = self.name_input.text()
        self.data['personal']['title'] = self.title_input.text()
        self.data['personal']['tagline'] = self.tagline_input.text()
        self.data['personal']['heroDescription'] = self.hero_desc_input.toPlainText()
        
        self.data['config']['logo']['type'] = self.logo_type_combo.currentText()
        self.data['config']['logo']['content'] = self.logo_content_input.text()
        
        # Theme
        self.data['config']['theme']['primaryColor'] = self.colors['primaryColor'].text()
        self.data['config']['theme']['secondaryColor'] = self.colors['secondaryColor'].text()
        self.data['config']['theme']['backgroundColor'] = self.colors['backgroundColor'].text()
        self.data['config']['theme']['textColor'] = self.colors['textColor'].text()
        self.data['config']['theme']['fontHeading'] = self.font_heading.currentText()
        self.data['config']['theme']['fontBody'] = self.font_body.currentText()
        
        # About
        self.data['about']['bio'] = self.bio_input.toPlainText()
        self.data['about']['description'] = self.about_desc_input.toPlainText()
        
        # Expertise
        expertise = []
        for i in range(self.exp_list.count()):
            expertise.append(self.exp_list.item(i).text())
        self.data['about']['expertise'] = expertise
        
        # Contact
        self.data['contact']['email'] = self.email_input.text()
        self.data['contact']['location'] = self.loc_input.text()
        self.data['contact']['availability'] = self.avail_input.text()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set global font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = PortfolioApp()
    window.show()
    sys.exit(app.exec_())
