import os
import shutil
from datetime import datetime

def create_backup():
    """Create timestamped backup of LogX source code"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"backup_{timestamp}"
    
    print(f"Creating backup: {backup_dir}")
    os.makedirs(backup_dir, exist_ok=True)
    
    # Files to backup
    files_to_backup = [
        "app.py", "ai_agent.py", "database.py", 
        "requirements.txt", ".env", "README.md",
        "backup.py", "export_chat.py"
    ]
    
    # Optional files
    optional_files = ["logo.png", "business.db", "dev_chat_history_*.json"]
    
    # Copy main files
    for file in files_to_backup:
        if os.path.exists(file):
            shutil.copy2(file, backup_dir)
            print(f"Backed up: {file}")
    
    # Copy optional files
    for pattern in optional_files:
        if "*" in pattern:
            import glob
            for file in glob.glob(pattern):
                shutil.copy2(file, backup_dir)
                print(f"Backed up: {file}")
        elif os.path.exists(pattern):
            shutil.copy2(pattern, backup_dir)
            print(f"Backed up: {pattern}")
    
    # Export development chat history
    try:
        from export_chat import export_chat_history
        chat_file = export_chat_history()
        shutil.move(chat_file, os.path.join(backup_dir, chat_file))
        print(f"Backed up: {chat_file}")
    except:
        pass
    
    print(f"\n🎯 Backup completed: {backup_dir}")
    return backup_dir

if __name__ == "__main__":
    create_backup()