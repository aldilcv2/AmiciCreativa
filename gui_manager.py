import tkinter as tk
from tkinter import ttk, filedialog, colorchooser, messagebox
import json
import os
import shutil
from pathlib import Path

# Configuration
DATA_FILE = 'data/portfolio-data.json'
ASSETS_DIR = 'assets'
PROJECTS_DIR = os.path.join(ASSETS_DIR, 'projects')
VIDEOS_DIR = os.path.join(ASSETS_DIR, 'videos')

class PortfolioManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Portfolio Content Manager")
        self.root.geometry("1000x700")
        
        # Style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Load Data
        self.data = self.load_data()
        
        # Create Notebook (Tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Initialize Tabs
        self.init_general_tab()
        self.init_theme_tab()
        self.init_about_tab()
        self.init_skills_tab()
        self.init_projects_tab()
        self.init_contact_tab()
        
        # Save Button
        save_frame = ttk.Frame(root)
        save_frame.pack(fill='x', padx=10, pady=10)
        ttk.Button(save_frame, text="Save All Changes", command=self.save_data, width=20).pack(side='right')

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
                            "fontHeading": "Poppins",
                            "fontBody": "Inter"
                        },
                        "logo": {"type": "text", "content": "Portfolio"}
                    }
                return data
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")
            return {}

    def save_data(self):
        try:
            # Update data from widgets
            self.update_data_from_ui()
            
            # Save to file
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            
            messagebox.showinfo("Success", "Data saved successfully! Refresh your website to see changes.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {e}")

    def update_data_from_ui(self):
        # General
        self.data['personal']['name'] = self.name_var.get()
        self.data['personal']['title'] = self.title_var.get()
        self.data['personal']['tagline'] = self.tagline_var.get()
        self.data['personal']['heroDescription'] = self.hero_desc_text.get("1.0", "end-1c")
        
        # Logo
        self.data['config']['logo']['type'] = self.logo_type_var.get()
        self.data['config']['logo']['content'] = self.logo_content_var.get()
        
        # Theme
        self.data['config']['theme']['primaryColor'] = self.primary_color_var.get()
        self.data['config']['theme']['secondaryColor'] = self.secondary_color_var.get()
        self.data['config']['theme']['backgroundColor'] = self.bg_color_var.get()
        self.data['config']['theme']['textColor'] = self.text_color_var.get()
        self.data['config']['theme']['fontHeading'] = self.font_heading_var.get()
        self.data['config']['theme']['fontBody'] = self.font_body_var.get()
        
        # About
        self.data['about']['bio'] = self.bio_text.get("1.0", "end-1c")
        self.data['about']['description'] = self.about_desc_text.get("1.0", "end-1c")
        # Expertise is updated in real-time
        
        # Skills & Projects & Contact are updated in real-time or via their specific methods

    # ==========================================
    # TAB 1: GENERAL
    # ==========================================
    def init_general_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="General")
        
        # Personal Info
        frame = ttk.LabelFrame(tab, text="Personal Information", padding=10)
        frame.pack(fill='x', padx=10, pady=10)
        
        self.create_entry(frame, "Name:", self.data['personal'].get('name', ''), 0, "name_var")
        self.create_entry(frame, "Title:", self.data['personal'].get('title', ''), 1, "title_var")
        self.create_entry(frame, "Tagline:", self.data['personal'].get('tagline', ''), 2, "tagline_var")
        
        ttk.Label(frame, text="Hero Description:").grid(row=3, column=0, sticky='nw', pady=5)
        self.hero_desc_text = tk.Text(frame, height=3, width=50)
        self.hero_desc_text.grid(row=3, column=1, sticky='we', pady=5)
        self.hero_desc_text.insert("1.0", self.data['personal'].get('heroDescription', ''))
        
        # Logo
        logo_frame = ttk.LabelFrame(tab, text="Logo Settings", padding=10)
        logo_frame.pack(fill='x', padx=10, pady=10)
        
        self.logo_type_var = tk.StringVar(value=self.data['config']['logo'].get('type', 'text'))
        ttk.Radiobutton(logo_frame, text="Text", variable=self.logo_type_var, value="text").grid(row=0, column=0, padx=5)
        ttk.Radiobutton(logo_frame, text="Image", variable=self.logo_type_var, value="image").grid(row=0, column=1, padx=5)
        
        ttk.Label(logo_frame, text="Content (Text or Image Path):").grid(row=1, column=0, sticky='w', pady=5)
        self.logo_content_var = tk.StringVar(value=self.data['config']['logo'].get('content', ''))
        ttk.Entry(logo_frame, textvariable=self.logo_content_var, width=40).grid(row=1, column=1, padx=5)
        ttk.Button(logo_frame, text="Upload Image", command=self.upload_logo).grid(row=1, column=2, padx=5)

    def upload_logo(self):
        filename = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.svg")])
        if filename:
            dest = os.path.join(ASSETS_DIR, os.path.basename(filename))
            try:
                shutil.copy2(filename, dest)
                self.logo_content_var.set(dest)
                self.logo_type_var.set("image")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to upload logo: {e}")

    # ==========================================
    # TAB 2: THEME
    # ==========================================
    def init_theme_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Theme")
        
        frame = ttk.LabelFrame(tab, text="Color Scheme", padding=10)
        frame.pack(fill='x', padx=10, pady=10)
        
        self.primary_color_var = self.create_color_picker(frame, "Primary Color (Accent):", self.data['config']['theme'].get('primaryColor', '#1E3A8A'), 0)
        self.secondary_color_var = self.create_color_picker(frame, "Secondary Color (Bg):", self.data['config']['theme'].get('secondaryColor', '#F3F4F6'), 1)
        self.bg_color_var = self.create_color_picker(frame, "Base Background:", self.data['config']['theme'].get('backgroundColor', '#FFFFFF'), 2)
        self.text_color_var = self.create_color_picker(frame, "Text Color:", self.data['config']['theme'].get('textColor', '#111827'), 3)
        
        font_frame = ttk.LabelFrame(tab, text="Typography", padding=10)
        font_frame.pack(fill='x', padx=10, pady=10)
        
        fonts = ["Poppins", "Inter", "Montserrat", "Roboto", "Open Sans", "Lato", "Arial"]
        self.create_combobox(font_frame, "Heading Font:", fonts, self.data['config']['theme'].get('fontHeading', 'Poppins'), 0, "font_heading_var")
        self.create_combobox(font_frame, "Body Font:", fonts, self.data['config']['theme'].get('fontBody', 'Inter'), 1, "font_body_var")

    def create_color_picker(self, parent, label, initial_value, row):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky='w', pady=5)
        var = tk.StringVar(value=initial_value)
        entry = ttk.Entry(parent, textvariable=var, width=10)
        entry.grid(row=row, column=1, padx=5)
        
        def pick_color():
            color = colorchooser.askcolor(color=var.get())[1]
            if color:
                var.set(color)
                btn.configure(bg=color) # Note: bg might not work on ttk button on some OS
        
        btn = tk.Button(parent, text="Pick", command=pick_color, bg=initial_value, width=4)
        btn.grid(row=row, column=2, padx=5)
        return var

    # ==========================================
    # TAB 3: ABOUT
    # ==========================================
    def init_about_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="About")
        
        frame = ttk.Frame(tab, padding=10)
        frame.pack(fill='both', expand=True)
        
        ttk.Label(frame, text="Bio:").pack(anchor='w')
        self.bio_text = tk.Text(frame, height=4)
        self.bio_text.pack(fill='x', pady=5)
        self.bio_text.insert("1.0", self.data['about'].get('bio', ''))
        
        ttk.Label(frame, text="Detailed Description:").pack(anchor='w')
        self.about_desc_text = tk.Text(frame, height=6)
        self.about_desc_text.pack(fill='x', pady=5)
        self.about_desc_text.insert("1.0", self.data['about'].get('description', ''))
        
        # Expertise
        ttk.Label(frame, text="Expertise Areas:").pack(anchor='w', pady=(10,0))
        
        exp_frame = ttk.Frame(frame)
        exp_frame.pack(fill='both', expand=True)
        
        self.exp_listbox = tk.Listbox(exp_frame, height=6)
        self.exp_listbox.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(exp_frame, orient="vertical", command=self.exp_listbox.yview)
        scrollbar.pack(side='right', fill='y')
        self.exp_listbox.config(yscrollcommand=scrollbar.set)
        
        for item in self.data['about'].get('expertise', []):
            self.exp_listbox.insert('end', item)
            
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill='x', pady=5)
        
        self.new_exp_var = tk.StringVar()
        ttk.Entry(btn_frame, textvariable=self.new_exp_var).pack(side='left', fill='x', expand=True)
        ttk.Button(btn_frame, text="Add", command=self.add_expertise).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Remove Selected", command=self.remove_expertise).pack(side='left')

    def add_expertise(self):
        val = self.new_exp_var.get().strip()
        if val:
            self.exp_listbox.insert('end', val)
            self.data['about']['expertise'].append(val)
            self.new_exp_var.set("")

    def remove_expertise(self):
        sel = self.exp_listbox.curselection()
        if sel:
            idx = sel[0]
            self.exp_listbox.delete(idx)
            self.data['about']['expertise'].pop(idx)

    # ==========================================
    # TAB 4: SKILLS
    # ==========================================
    def init_skills_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Skills")
        
        # Split into list and editor
        paned = ttk.PanedWindow(tab, orient='horizontal')
        paned.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left: List
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=1)
        
        self.skills_listbox = tk.Listbox(left_frame)
        self.skills_listbox.pack(fill='both', expand=True)
        self.skills_listbox.bind('<<ListboxSelect>>', self.load_selected_skill)
        
        # Right: Editor
        self.skill_editor_frame = ttk.LabelFrame(paned, text="Edit Skill", padding=10)
        paned.add(self.skill_editor_frame, weight=2)
        
        self.skill_name_var = tk.StringVar()
        self.skill_cat_var = tk.StringVar()
        self.skill_icon_var = tk.StringVar()
        self.skill_prof_var = tk.IntVar()
        
        self.create_entry(self.skill_editor_frame, "Name:", "", 0, None, self.skill_name_var)
        self.create_entry(self.skill_editor_frame, "Category:", "", 1, None, self.skill_cat_var)
        self.create_entry(self.skill_editor_frame, "Icon (Emoji):", "", 2, None, self.skill_icon_var)
        
        ttk.Label(self.skill_editor_frame, text="Proficiency:").grid(row=3, column=0, sticky='w')
        self.prof_scale = ttk.Scale(self.skill_editor_frame, from_=0, to=100, variable=self.skill_prof_var, orient='horizontal')
        self.prof_scale.grid(row=3, column=1, sticky='we', padx=5)
        ttk.Label(self.skill_editor_frame, textvariable=self.skill_prof_var).grid(row=3, column=2)
        
        btn_frame = ttk.Frame(self.skill_editor_frame)
        btn_frame.grid(row=4, column=0, columnspan=3, pady=20)
        
        ttk.Button(btn_frame, text="New Skill", command=self.clear_skill_editor).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Save Skill", command=self.save_skill).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Delete Skill", command=self.delete_skill).pack(side='left', padx=5)
        
        self.refresh_skills_list()

    def refresh_skills_list(self):
        self.skills_listbox.delete(0, 'end')
        for skill in self.data['skills']:
            self.skills_listbox.insert('end', skill['name'])

    def load_selected_skill(self, event):
        sel = self.skills_listbox.curselection()
        if sel:
            idx = sel[0]
            skill = self.data['skills'][idx]
            self.skill_name_var.set(skill['name'])
            self.skill_cat_var.set(skill['category'])
            self.skill_icon_var.set(skill['icon'])
            self.skill_prof_var.set(skill['proficiency'])
            self.current_skill_idx = idx
        else:
            self.current_skill_idx = None

    def clear_skill_editor(self):
        self.skill_name_var.set("")
        self.skill_cat_var.set("")
        self.skill_icon_var.set("⚡")
        self.skill_prof_var.set(50)
        self.current_skill_idx = None
        self.skills_listbox.selection_clear(0, 'end')

    def save_skill(self):
        new_skill = {
            "name": self.skill_name_var.get(),
            "category": self.skill_cat_var.get(),
            "proficiency": self.skill_prof_var.get(),
            "icon": self.skill_icon_var.get()
        }
        
        if hasattr(self, 'current_skill_idx') and self.current_skill_idx is not None:
            self.data['skills'][self.current_skill_idx] = new_skill
        else:
            self.data['skills'].append(new_skill)
            
        self.refresh_skills_list()
        self.clear_skill_editor()

    def delete_skill(self):
        if hasattr(self, 'current_skill_idx') and self.current_skill_idx is not None:
            self.data['skills'].pop(self.current_skill_idx)
            self.refresh_skills_list()
            self.clear_skill_editor()

    # ==========================================
    # TAB 5: PROJECTS (PORTFOLIO)
    # ==========================================
    def init_projects_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Projects")
        
        paned = ttk.PanedWindow(tab, orient='horizontal')
        paned.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left: List
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=1)
        
        self.projects_listbox = tk.Listbox(left_frame)
        self.projects_listbox.pack(fill='both', expand=True)
        self.projects_listbox.bind('<<ListboxSelect>>', self.load_selected_project)
        
        # Right: Editor
        self.proj_editor_frame = ttk.LabelFrame(paned, text="Edit Project", padding=10)
        paned.add(self.proj_editor_frame, weight=2)
        
        self.proj_title_var = tk.StringVar()
        self.proj_year_var = tk.StringVar()
        self.proj_tags_var = tk.StringVar()
        self.proj_thumb_var = tk.StringVar()
        self.proj_video_var = tk.StringVar()
        
        self.create_entry(self.proj_editor_frame, "Title:", "", 0, None, self.proj_title_var)
        self.create_entry(self.proj_editor_frame, "Year:", "", 1, None, self.proj_year_var)
        
        ttk.Label(self.proj_editor_frame, text="Description:").grid(row=2, column=0, sticky='nw')
        self.proj_desc_text = tk.Text(self.proj_editor_frame, height=3, width=40)
        self.proj_desc_text.grid(row=2, column=1, columnspan=2, sticky='we', pady=5)
        
        self.create_entry(self.proj_editor_frame, "Tags (comma sep):", "", 3, None, self.proj_tags_var)
        
        # Thumbnail
        ttk.Label(self.proj_editor_frame, text="Thumbnail:").grid(row=4, column=0, sticky='w')
        ttk.Entry(self.proj_editor_frame, textvariable=self.proj_thumb_var).grid(row=4, column=1, sticky='we')
        ttk.Button(self.proj_editor_frame, text="Upload", command=self.upload_thumbnail).grid(row=4, column=2)
        
        # Video
        ttk.Label(self.proj_editor_frame, text="Video (URL or Upload):").grid(row=5, column=0, sticky='w')
        ttk.Entry(self.proj_editor_frame, textvariable=self.proj_video_var).grid(row=5, column=1, sticky='we')
        ttk.Button(self.proj_editor_frame, text="Upload Video", command=self.upload_video).grid(row=5, column=2)
        
        btn_frame = ttk.Frame(self.proj_editor_frame)
        btn_frame.grid(row=6, column=0, columnspan=3, pady=20)
        
        ttk.Button(btn_frame, text="New Project", command=self.clear_project_editor).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Save Project", command=self.save_project).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Delete Project", command=self.delete_project).pack(side='left', padx=5)
        
        self.refresh_projects_list()

    def refresh_projects_list(self):
        self.projects_listbox.delete(0, 'end')
        for proj in self.data['projects']:
            self.projects_listbox.insert('end', proj['title'])

    def load_selected_project(self, event):
        sel = self.projects_listbox.curselection()
        if sel:
            idx = sel[0]
            proj = self.data['projects'][idx]
            self.proj_title_var.set(proj['title'])
            self.proj_year_var.set(proj['year'])
            self.proj_tags_var.set(", ".join(proj['tags']))
            self.proj_thumb_var.set(proj['thumbnail'])
            self.proj_video_var.set(proj.get('videoUrl', ''))
            self.proj_desc_text.delete("1.0", "end")
            self.proj_desc_text.insert("1.0", proj['description'])
            self.current_proj_idx = idx
        else:
            self.current_proj_idx = None

    def clear_project_editor(self):
        self.proj_title_var.set("")
        self.proj_year_var.set("")
        self.proj_tags_var.set("")
        self.proj_thumb_var.set("")
        self.proj_video_var.set("")
        self.proj_desc_text.delete("1.0", "end")
        self.current_proj_idx = None
        self.projects_listbox.selection_clear(0, 'end')

    def upload_thumbnail(self):
        filename = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg")])
        if filename:
            dest = os.path.join(PROJECTS_DIR, os.path.basename(filename))
            try:
                os.makedirs(PROJECTS_DIR, exist_ok=True)
                shutil.copy2(filename, dest)
                self.proj_thumb_var.set(dest)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to upload: {e}")

    def upload_video(self):
        filename = filedialog.askopenfilename(filetypes=[("Videos", "*.mp4 *.webm *.mov")])
        if filename:
            dest = os.path.join(VIDEOS_DIR, os.path.basename(filename))
            try:
                os.makedirs(VIDEOS_DIR, exist_ok=True)
                shutil.copy2(filename, dest)
                self.proj_video_var.set(dest)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to upload: {e}")

    def save_project(self):
        tags = [t.strip() for t in self.proj_tags_var.get().split(',') if t.strip()]
        new_proj = {
            "id": self.data['projects'][self.current_proj_idx]['id'] if hasattr(self, 'current_proj_idx') and self.current_proj_idx is not None else len(self.data['projects']) + 1,
            "title": self.proj_title_var.get(),
            "description": self.proj_desc_text.get("1.0", "end-1c"),
            "thumbnail": self.proj_thumb_var.get(),
            "videoUrl": self.proj_video_var.get(),
            "tags": tags,
            "year": self.proj_year_var.get()
        }
        
        if hasattr(self, 'current_proj_idx') and self.current_proj_idx is not None:
            self.data['projects'][self.current_proj_idx] = new_proj
        else:
            self.data['projects'].append(new_proj)
            
        self.refresh_projects_list()
        self.clear_project_editor()

    def delete_project(self):
        if hasattr(self, 'current_proj_idx') and self.current_proj_idx is not None:
            self.data['projects'].pop(self.current_proj_idx)
            self.refresh_projects_list()
            self.clear_project_editor()

    # ==========================================
    # TAB 6: CONTACT
    # ==========================================
    def init_contact_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Contact")
        
        frame = ttk.LabelFrame(tab, text="Contact Info", padding=10)
        frame.pack(fill='x', padx=10, pady=10)
        
        self.email_var = tk.StringVar(value=self.data['contact'].get('email', ''))
        self.loc_var = tk.StringVar(value=self.data['contact'].get('location', ''))
        self.avail_var = tk.StringVar(value=self.data['contact'].get('availability', ''))
        
        self.create_entry(frame, "Email:", self.data['contact'].get('email', ''), 0, None, self.email_var)
        self.create_entry(frame, "Location:", self.data['contact'].get('location', ''), 1, None, self.loc_var)
        self.create_entry(frame, "Availability:", self.data['contact'].get('availability', ''), 2, None, self.avail_var)
        
        # Socials could be added similarly, but for brevity keeping it simple or adding a text editor for raw JSON if needed.
        # Let's add a simple list for socials
        
        social_frame = ttk.LabelFrame(tab, text="Social Media", padding=10)
        social_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.social_listbox = tk.Listbox(social_frame, height=5)
        self.social_listbox.pack(fill='x', pady=5)
        
        for s in self.data['contact']['social']:
            self.social_listbox.insert('end', f"{s['platform']}: {s['url']}")
            
        ttk.Label(social_frame, text="Note: Use the CLI or edit JSON for advanced social media management for now.").pack()

    # Helper
    def create_entry(self, parent, label, initial, row, var_name=None, variable=None):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky='w', pady=5)
        if variable is None:
            variable = tk.StringVar(value=initial)
        if var_name:
            setattr(self, var_name, variable)
        entry = ttk.Entry(parent, textvariable=variable, width=40)
        entry.grid(row=row, column=1, sticky='we', padx=5)
        return variable

    def create_combobox(self, parent, label, values, initial, row, var_name):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky='w', pady=5)
        var = tk.StringVar(value=initial)
        setattr(self, var_name, var)
        combo = ttk.Combobox(parent, textvariable=var, values=values, state="readonly")
        combo.grid(row=row, column=1, sticky='we', padx=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = PortfolioManagerGUI(root)
    root.mainloop()
