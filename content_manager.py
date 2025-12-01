#!/usr/bin/env python3
"""
Portfolio Content Manager
---------------------------
A Python CLI tool to manage portfolio content dynamically.
All changes are saved to portfolio-data.json and automatically
reflected on the website.

Usage:
    python content_manager.py                  # Interactive mode
    python content_manager.py --help           # Show help
    python content_manager.py --update-name "Your Name"
    python content_manager.py --update-bio "Your new bio"
    python content_manager.py --add-skill "Tool Name" "Category" 85
    python content_manager.py --add-project "Project Title"
"""

import json
import os
import sys
import shutil
from datetime import datetime
from pathlib import Path

# Configuration
DATA_FILE = 'data/portfolio-data.json'
BACKUP_DIR = 'data/backups'

class Colors:
    """ANSI color codes for terminal output"""
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    """Print styled header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(60)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_warning(text):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def load_data():
    """Load portfolio data from JSON file"""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print_error(f"Data file not found: {DATA_FILE}")
        sys.exit(1)
    except json.JSONDecodeError:
        print_error("Invalid JSON format in data file")
        sys.exit(1)

def save_data(data, create_backup=True):
    """Save portfolio data to JSON file"""
    if create_backup:
        backup_data()
    
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print_success("Data saved successfully!")
        return True
    except Exception as e:
        print_error(f"Failed to save data: {str(e)}")
        return False

def backup_data():
    """Create a backup of the current data file"""
    try:
        os.makedirs(BACKUP_DIR, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f"{BACKUP_DIR}/portfolio-data_{timestamp}.json"
        shutil.copy2(DATA_FILE, backup_file)
        print(f"{Colors.YELLOW}📦 Backup created: {backup_file}{Colors.END}")
    except Exception as e:
        print_warning(f"Failed to create backup: {str(e)}")

# ========================================
# PERSONAL INFO MANAGEMENT
# ========================================

def update_personal_info(data):
    """Update personal information"""
    print_header("Update Personal Information")
    
    print(f"Current name: {Colors.BOLD}{data['personal']['name']}{Colors.END}")
    name = input("New name (press Enter to skip): ").strip()
    if name:
        data['personal']['name'] = name
    
    print(f"\nCurrent title: {Colors.BOLD}{data['personal']['title']}{Colors.END}")
    title = input("New title (press Enter to skip): ").strip()
    if title:
        data['personal']['title'] = title
    
    print(f"\nCurrent tagline: {Colors.BOLD}{data['personal']['tagline']}{Colors.END}")
    tagline = input("New tagline (press Enter to skip): ").strip()
    if tagline:
        data['personal']['tagline'] = tagline
    
    print(f"\nCurrent hero description: {Colors.BOLD}{data['personal']['heroDescription']}{Colors.END}")
    hero = input("New hero description (press Enter to skip): ").strip()
    if hero:
        data['personal']['heroDescription'] = hero
    
    return data

# ========================================
# ABOUT SECTION MANAGEMENT
# ========================================

def update_about(data):
    """Update about section"""
    print_header("Update About Section")
    
    print("1. Update bio")
    print("2. Update description")
    print("3. Update expertise areas")
    print("4. Back to main menu")
    
    choice = input("\nSelect option: ").strip()
    
    if choice == '1':
        print(f"\nCurrent bio: {Colors.BOLD}{data['about']['bio']}{Colors.END}")
        bio = input("New bio (press Enter to skip): ").strip()
        if bio:
            data['about']['bio'] = bio
    
    elif choice == '2':
        print(f"\nCurrent description: {Colors.BOLD}{data['about']['description']}{Colors.END}")
        desc = input("New description (press Enter to skip): ").strip()
        if desc:
            data['about']['description'] = desc
    
    elif choice == '3':
        print(f"\nCurrent expertise areas:")
        for i, exp in enumerate(data['about']['expertise'], 1):
            print(f"  {i}. {exp}")
        
        print("\n1. Add expertise area")
        print("2. Remove expertise area")
        sub_choice = input("Select option: ").strip()
        
        if sub_choice == '1':
            new_exp = input("Enter new expertise area: ").strip()
            if new_exp:
                data['about']['expertise'].append(new_exp)
                print_success(f"Added: {new_exp}")
        
        elif sub_choice == '2':
            try:
                idx = int(input("Enter number to remove: ")) - 1
                removed = data['about']['expertise'].pop(idx)
                print_success(f"Removed: {removed}")
            except (ValueError, IndexError):
                print_error("Invalid selection")
    
    return data

# ========================================
# SKILLS MANAGEMENT
# ========================================

def manage_skills(data):
    """Manage skills section"""
    print_header("Skills Management")
    
    print("Current skills:")
    for i, skill in enumerate(data['skills'], 1):
        print(f"  {i}. {skill['icon']} {skill['name']} ({skill['category']}) - {skill['proficiency']}%")
    
    print("\n1. Add new skill")
    print("2. Edit skill")
    print("3. Remove skill")
    print("4. Back to main menu")
    
    choice = input("\nSelect option: ").strip()
    
    if choice == '1':
        name = input("Skill name: ").strip()
        category = input("Category (e.g., '2D Animation', '3D Modeling'): ").strip()
        icon = input("Icon emoji (default ⚡): ").strip() or "⚡"
        try:
            proficiency = int(input("Proficiency (0-100): "))
            proficiency = max(0, min(100, proficiency))
            
            new_skill = {
                "name": name,
                "category": category,
                "proficiency": proficiency,
                "icon": icon
            }
            data['skills'].append(new_skill)
            print_success(f"Added skill: {name}")
        except ValueError:
            print_error("Invalid proficiency value")
    
    elif choice == '2':
        try:
            idx = int(input("Enter skill number to edit: ")) - 1
            skill = data['skills'][idx]
            
            print(f"\nEditing: {skill['name']}")
            name = input(f"Name [{skill['name']}]: ").strip() or skill['name']
            category = input(f"Category [{skill['category']}]: ").strip() or skill['category']
            icon = input(f"Icon [{skill['icon']}]: ").strip() or skill['icon']
            prof_input = input(f"Proficiency [{skill['proficiency']}]: ").strip()
            proficiency = int(prof_input) if prof_input else skill['proficiency']
            
            data['skills'][idx] = {
                "name": name,
                "category": category,
                "proficiency": max(0, min(100, proficiency)),
                "icon": icon
            }
            print_success("Skill updated!")
        except (ValueError, IndexError):
            print_error("Invalid selection")
    
    elif choice == '3':
        try:
            idx = int(input("Enter skill number to remove: ")) - 1
            removed = data['skills'].pop(idx)
            print_success(f"Removed: {removed['name']}")
        except (ValueError, IndexError):
            print_error("Invalid selection")
    
    return data

# ========================================
# PROJECT MANAGEMENT
# ========================================

def manage_projects(data):
    """Manage projects/showcase section"""
    print_header("Projects Management")
    
    print("Current projects:")
    for i, project in enumerate(data['projects'], 1):
        print(f"  {i}. {project['title']} ({project['year']})")
    
    print("\n1. Add new project")
    print("2. Edit project")
    print("3. Remove project")
    print("4. Back to main menu")
    
    choice = input("\nSelect option: ").strip()
    
    if choice == '1':
        title = input("Project title: ").strip()
        description = input("Description: ").strip()
        thumbnail = input("Thumbnail path (e.g., assets/projects/project.jpg): ").strip()
        video_url = input("Video URL (optional): ").strip()
        tags = input("Tags (comma-separated): ").strip().split(',')
        tags = [tag.strip() for tag in tags if tag.strip()]
        year = int(input("Year: ").strip() or datetime.now().year)
        
        new_id = max([p['id'] for p in data['projects']], default=0) + 1
        
        new_project = {
            "id": new_id,
            "title": title,
            "description": description,
            "thumbnail": thumbnail,
            "videoUrl": video_url,
            "tags": tags,
            "year": year
        }
        data['projects'].append(new_project)
        print_success(f"Added project: {title}")
    
    elif choice == '2':
        try:
            idx = int(input("Enter project number to edit: ")) - 1
            project = data['projects'][idx]
            
            print(f"\nEditing: {project['title']}")
            title = input(f"Title [{project['title']}]: ").strip() or project['title']
            description = input(f"Description [{project['description']}]: ").strip() or project['description']
            thumbnail = input(f"Thumbnail [{project['thumbnail']}]: ").strip() or project['thumbnail']
            video_url = input(f"Video URL [{project['videoUrl']}]: ").strip() or project['videoUrl']
            tags_input = input(f"Tags [{', '.join(project['tags'])}]: ").strip()
            tags = [tag.strip() for tag in tags_input.split(',')] if tags_input else project['tags']
            year_input = input(f"Year [{project['year']}]: ").strip()
            year = int(year_input) if year_input else project['year']
            
            data['projects'][idx] = {
                "id": project['id'],
                "title": title,
                "description": description,
                "thumbnail": thumbnail,
                "videoUrl": video_url,
                "tags": tags,
                "year": year
            }
            print_success("Project updated!")
        except (ValueError, IndexError):
            print_error("Invalid selection")
    
    elif choice == '3':
        try:
            idx = int(input("Enter project number to remove: ")) - 1
            removed = data['projects'].pop(idx)
            print_success(f"Removed: {removed['title']}")
        except (ValueError, IndexError):
            print_error("Invalid selection")
    
    return data

# ========================================
# CONTACT INFO MANAGEMENT
# ========================================

def update_contact(data):
    """Update contact information"""
    print_header("Update Contact Information")
    
    print(f"Current email: {Colors.BOLD}{data['contact']['email']}{Colors.END}")
    email = input("New email (press Enter to skip): ").strip()
    if email:
        data['contact']['email'] = email
    
    print(f"\nCurrent location: {Colors.BOLD}{data['contact']['location']}{Colors.END}")
    location = input("New location (press Enter to skip): ").strip()
    if location:
        data['contact']['location'] = location
    
    print(f"\nCurrent availability: {Colors.BOLD}{data['contact']['availability']}{Colors.END}")
    availability = input("New availability status (press Enter to skip): ").strip()
    if availability:
        data['contact']['availability'] = availability
    
    print("\nManage social media links:")
    print("Current social links:")
    for i, social in enumerate(data['contact']['social'], 1):
        print(f"  {i}. {social['icon']} {social['platform']}: {social['url']}")
    
    print("\n1. Add social link")
    print("2. Update social link")
    print("3. Remove social link")
    print("4. Skip")
    
    choice = input("Select option: ").strip()
    
    if choice == '1':
        platform = input("Platform name (e.g., Instagram): ").strip()
        url = input("URL: ").strip()
        icon = input("Icon emoji (default 🔗): ").strip() or "🔗"
        
        data['contact']['social'].append({
            "platform": platform,
            "url": url,
            "icon": icon
        })
        print_success(f"Added {platform}")
    
    elif choice == '2':
        try:
            idx = int(input("Enter social link number to update: ")) - 1
            social = data['contact']['social'][idx]
            
            platform = input(f"Platform [{social['platform']}]: ").strip() or social['platform']
            url = input(f"URL [{social['url']}]: ").strip() or social['url']
            icon = input(f"Icon [{social['icon']}]: ").strip() or social['icon']
            
            data['contact']['social'][idx] = {
                "platform": platform,
                "url": url,
                "icon": icon
            }
            print_success("Social link updated!")
        except (ValueError, IndexError):
            print_error("Invalid selection")
    
    elif choice == '3':
        try:
            idx = int(input("Enter social link number to remove: ")) - 1
            removed = data['contact']['social'].pop(idx)
            print_success(f"Removed: {removed['platform']}")
        except (ValueError, IndexError):
            print_error("Invalid selection")
    
    return data

# ========================================
# MAIN MENU
# ========================================

def main_menu():
    """Display main menu and handle user interaction"""
    while True:
        print_header("Portfolio Content Manager")
        
        print("1. Update Personal Information")
        print("2. Update About Section")
        print("3. Manage Skills")
        print("4. Manage Projects")
        print("5. Update Contact Information")
        print("6. View Current Data")
        print("7. Exit")
        
        choice = input("\nSelect an option (1-7): ").strip()
        
        if choice == '7':
            print(f"\n{Colors.GREEN}Goodbye! 👋{Colors.END}\n")
            break
        
        data = load_data()
        
        if choice == '1':
            data = update_personal_info(data)
            save_data(data)
        elif choice == '2':
            data = update_about(data)
            save_data(data)
        elif choice == '3':
            data = manage_skills(data)
            save_data(data)
        elif choice == '4':
            data = manage_projects(data)
            save_data(data)
        elif choice == '5':
            data = update_contact(data)
            save_data(data)
        elif choice == '6':
            print_header("Current Portfolio Data")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            input("\nPress Enter to continue...")
        else:
            print_error("Invalid option. Please try again.")

# ========================================
# CLI ARGUMENTS
# ========================================

def handle_cli_args():
    """Handle command-line arguments"""
    if len(sys.argv) < 2:
        return False
    
    data = load_data()
    
    if sys.argv[1] == '--help':
        print(__doc__)
        return True
    
    elif sys.argv[1] == '--update-name' and len(sys.argv) > 2:
        data['personal']['name'] = sys.argv[2]
        save_data(data)
        return True
    
    elif sys.argv[1] == '--update-bio' and len(sys.argv) > 2:
        data['about']['bio'] = sys.argv[2]
        save_data(data)
        return True
    
    elif sys.argv[1] == '--add-skill' and len(sys.argv) > 4:
        name, category, proficiency = sys.argv[2], sys.argv[3], int(sys.argv[4])
        icon = sys.argv[5] if len(sys.argv) > 5 else "⚡"
        data['skills'].append({
            "name": name,
            "category": category,
            "proficiency": proficiency,
            "icon": icon
        })
        save_data(data)
        return True
    
    else:
        print_error("Invalid arguments. Use --help for usage information.")
        return True

# ========================================
# ENTRY POINT
# ========================================

if __name__ == '__main__':
    try:
        # Check if CLI arguments provided
        if not handle_cli_args():
            # No CLI args, run interactive mode
            main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Operation cancelled by user.{Colors.END}\n")
        sys.exit(0)
    except Exception as e:
        print_error(f"An error occurred: {str(e)}")
        sys.exit(1)
