from sqlalchemy.orm import Session
from sqlalchemy import desc
from models.models import ReadingMaterial, Tag, book_tags
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime
import re

def sanitize_id(text: str) -> str:
    """
    Create a safe ID from text input
    """
    if not text:
        return str(uuid.uuid4())
    
    # Replace special characters and spaces with underscores
    safe_id = re.sub(r'[^\w\s-]', '', text).strip().lower()
    safe_id = re.sub(r'[-\s]+', '_', safe_id)
    
    return safe_id

def get_reading_materials(
    db: Session, 
    section: Optional[str] = None, 
    difficulty: Optional[str] = None,
    cursor: Optional[str] = None,
    limit: int = 10
):
    """
    Get reading materials from database, optionally filtered by section and difficulty
    - section: Filter by section (optional)
    - difficulty: Filter by difficulty level (beginner, intermediate, advanced) (optional)
    - cursor: Last material's ID (optional)
    - limit: Maximum number of materials to return
    """
    query = db.query(ReadingMaterial)
    
    # Apply filters
    if section and section.lower() != "all":
        query = query.filter(ReadingMaterial.section == section)
    
    if difficulty:
        query = query.filter(ReadingMaterial.difficulty == difficulty)
    
    # Apply cursor pagination if provided
    if cursor:
        # Simple implementation - in a real app, you'd need a more robust cursor system
        query = query.filter(ReadingMaterial.id > cursor)
    
    # Get one more item than requested to determine if there are more pages
    materials = query.order_by(ReadingMaterial.title).limit(limit + 1).all()
    
    # Check if there are more materials
    has_more = len(materials) > limit
    result_materials = materials[:limit]
    
    # Format the response
    result = []
    next_cursor = None
    
    for material in result_materials:
        # Get tags for the material
        tags = db.query(Tag).join(book_tags).filter(book_tags.c.book_id == material.id).all()
        
        result.append({
            "id": material.id,
            "title": material.title,
            "author": material.author,
            "description": material.description,
            "difficulty": material.difficulty,
            "section": material.section,
            "coverUrl": material.cover_url,
            "pdfUrl": material.pdf_url,
            "audioUrl": material.audio_url,
            "externalUrl": material.external_url,
            "publicationYear": material.publication_year,
            "pages": material.pages,
            "readingTime": material.reading_time,
            "tags": [tag.name for tag in tags]
        })
    
    # Set next cursor to the ID of the last material if there are more
    if has_more and result_materials:
        next_cursor = result_materials[-1].id
    
    return {
        "materials": result,
        "nextCursor": next_cursor
    }

def add_reading_material(db: Session, material_data: Dict[str, Any]):
    """
    Add a new reading material to the database
    """
    try:
        # Create unique ID
        material_id = sanitize_id(f"{material_data['title']}_{material_data['author']}")
        
        # Check if material already exists
        existing_material = db.query(ReadingMaterial).filter(ReadingMaterial.id == material_id).first()
        if existing_material:
            return existing_material
        
        # Handle tags
        tag_names = material_data.pop("tag_names", [])
        
        # Create new material
        new_material = ReadingMaterial(
            id=material_id,
            title=material_data["title"],
            author=material_data["author"],
            description=material_data.get("description", ""),
            difficulty=material_data.get("difficulty", "beginner"),
            section=material_data.get("section", "general"),
            cover_url=material_data.get("cover_url", ""),
            pdf_url=material_data.get("pdf_url", ""),
            audio_url=material_data.get("audio_url", ""),
            external_url=material_data.get("external_url", ""),
            publication_year=material_data.get("publication_year", ""),
            pages=material_data.get("pages", 0),
            reading_time=material_data.get("reading_time", 0)
        )
        
        db.add(new_material)
        db.commit()
        db.refresh(new_material)
        
        # Add tags
        for tag_name in tag_names:
            tag = db.query(Tag).filter(Tag.name == tag_name).first()
            if not tag:
                tag = Tag(id=sanitize_id(tag_name), name=tag_name)
                db.add(tag)
                db.commit()
            
            # Associate tag with material
            new_material.tags.append(tag)
        
        db.commit()
        
        return new_material
    
    except Exception as e:
        print(f"Error adding reading material: {e}")
        db.rollback()
        raise

def import_reading_list_from_csv(db: Session, csv_file_path: str):
    """
    Import reading materials from a CSV file
    """
    import csv
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                # Prepare material data
                material_data = {
                    "title": row.get("title", ""),
                    "author": row.get("author", "Unknown"),
                    "description": row.get("description", ""),
                    "difficulty": row.get("difficulty", "beginner"),
                    "section": row.get("section", "general"),
                    "cover_url": row.get("cover_url", ""),
                    "pdf_url": row.get("pdf_url", ""),
                    "audio_url": row.get("audio_url", ""),
                    "external_url": row.get("external_url", ""),
                    "publication_year": row.get("publication_year", ""),
                    "pages": int(row.get("pages", 0)) if row.get("pages", "").isdigit() else 0,
                    "reading_time": int(row.get("reading_time", 0)) if row.get("reading_time", "").isdigit() else 0
                }
                
                # Handle tags (assuming comma-separated tags in the CSV)
                if "tags" in row and row["tags"]:
                    material_data["tag_names"] = [tag.strip() for tag in row["tags"].split(",")]
                
                # Add material
                add_reading_material(db, material_data)
        
        return True
    
    except Exception as e:
        print(f"Error importing reading list from CSV: {e}")
        return False

def import_marxist_classics(db: Session):
    """
    Import a set of classic Marxist texts to the reading list
    This is a helper function to populate the database with initial data
    """
    classics = [
        {
            "title": "The Communist Manifesto",
            "author": "Karl Marx & Friedrich Engels",
            "description": "A foundational text that outlines the theory of historical materialism and class struggle.",
            "difficulty": "beginner",
            "section": "theory",
            "publication_year": "1848",
            "pages": 48,
            "reading_time": 90,
            "tag_names": ["marxism", "communism", "history", "philosophy", "politics"]
        },
        {
            "title": "Socialism: Utopian and Scientific",
            "author": "Friedrich Engels",
            "description": "A short work explaining the differences between utopian socialism and scientific socialism.",
            "difficulty": "intermediate",
            "section": "theory",
            "publication_year": "1880",
            "pages": 86,
            "reading_time": 180,
            "tag_names": ["marxism", "socialism", "philosophy", "history"]
        },
        {
            "title": "State and Revolution",
            "author": "Vladimir Lenin",
            "description": "An analysis of the state, violent revolution, and the dictatorship of the proletariat.",
            "difficulty": "intermediate",
            "section": "theory",
            "publication_year": "1917",
            "pages": 116,
            "reading_time": 240,
            "tag_names": ["leninism", "state", "revolution", "politics"]
        },
        {
            "title": "The Transitional Program",
            "author": "Leon Trotsky",
            "description": "A political platform adopted by the 1938 founding congress of the Fourth International",
            "difficulty": "intermediate",
            "section": "strategy",
            "publication_year": "1938",
            "pages": 347,
            "reading_time": 160,
            "tag_names": ["marxism", "trotskyism", "revolution", "strategy"]
        }
    ]
    
    for material_data in classics:
        try:
            add_reading_material(db, material_data)
        except Exception as e:
            print(f"Error adding {material_data['title']}: {e}")
            continue
    
    return True
