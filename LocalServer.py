from fastmcp import FastMCP
import os

mcp = FastMCP("LocalNotes")

# Base directory for all notes on the VM
NOTES_DIR = "/home/azureuser/notes"

# Create the notes directory if it doesn't exist
os.makedirs(NOTES_DIR, exist_ok=True)

@mcp.tool()
def add_note_to_file(content: str, filename: str = "notes.txt") -> str:
    """
    Appends the given content to the user's specified file.
    Args:
        content: The text content to append.
        filename: The name of the file (e.g., 'PersonalInfo.txt', 'work.txt'). 
                  Defaults to 'notes.txt' if not specified.
    """
    # Sanitize filename to prevent path traversal attacks
    safe_filename = os.path.basename(filename)
    filepath = os.path.join(NOTES_DIR, safe_filename)
    
    try:
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(content + "\n")
        return f"Content appended to {safe_filename}."
    except Exception as e:
        return f"Error appending to file {safe_filename}: {e}"

@mcp.tool()
def read_notes(filename: str = "notes.txt") -> str:
    """
    Reads and returns the contents of the specified file.
    Args:
        filename: The name of the file to read (e.g., 'PersonalInfo.txt', 'work.txt').
                  Defaults to 'notes.txt' if not specified.
    """
    # Sanitize filename to prevent path traversal attacks
    safe_filename = os.path.basename(filename)
    filepath = os.path.join(NOTES_DIR, safe_filename)
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            notes = f.read()
        return notes if notes else f"No content in {safe_filename}."
    except FileNotFoundError:
        return f"File {safe_filename} not found."
    except Exception as e:
        return f"Error reading file {safe_filename}: {e}"

@mcp.tool()
def list_note_files() -> str:
    """
    Lists all available note files.
    """
    try:
        files = os.listdir(NOTES_DIR)
        if files:
            return "Available files:\n" + "\n".join(f"- {f}" for f in files)
        else:
            return "No files found."
    except Exception as e:
        return f"Error listing files: {e}"

@mcp.tool()
def delete_note_file(filename: str) -> str:
    """
    Deletes the specified note file.
    Args:
        filename: The name of the file to delete.
    """
    # Sanitize filename
    safe_filename = os.path.basename(filename)
    filepath = os.path.join(NOTES_DIR, safe_filename)
    
    try:
        os.remove(filepath)
        return f"File {safe_filename} deleted successfully."
    except FileNotFoundError:
        return f"File {safe_filename} not found."
    except Exception as e:
        return f"Error deleting file {safe_filename}: {e}"

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
