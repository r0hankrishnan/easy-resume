from __future__ import annotations
from typing import Literal

from pydantic import BaseModel, EmailStr, model_validator

class Header(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None
    location: str
    github: str | None = None
    linkedin: str | None = None

class EducationEntry(BaseModel):
    degree: str
    institution: str
    location: str
    dates: str
    bullets: list[str] = []

class ExperienceEntry(BaseModel):
    role: str
    company: str
    location: str
    dates: str
    bullets: list[str]
    
class ProjectEntry(BaseModel):
    name: str
    dates: str
    bullets: list[str]
    
class SkillsInlineEntry(BaseModel):
    skills: list[str]
   
ENTRY_TYPE_MAP = {
    "education": EducationEntry,
    "experience": ExperienceEntry,
    "projects": ProjectEntry,
    "skills_inline": SkillsInlineEntry 
    } 

class Section(BaseModel):
    type: Literal["education", "experience", "projects", "skills_inline"]
    title: str | None = None # Custom title if wanted
    entries: list[EducationEntry| ExperienceEntry | ProjectEntry | SkillsInlineEntry]
    
    @model_validator(mode = "after")
    def validate_entry_types(self) -> Section:
        expected_class = ENTRY_TYPE_MAP[self.type]
        
        for entry in self.entries:
            if not isinstance(entry, expected_class):
                raise ValueError(f"Section entry does not match section type. Expect {expected_class} class for type {self.type} not {type(entry)}.")
        
        return self
               
class Meta(BaseModel):
    theme: Literal["default"]
    section_order: list[Literal["education", "experience", "projects", "skills_inline"]]
    

class Resume(BaseModel):
    meta: Meta
    header: Header
    sections: list[Section]
    
    @model_validator(mode = "after")
    def validate_resume_sections(self) -> Resume:
        sections_types = [section.type for section in self.sections]
        
        for section_type in self.meta.section_order:
            if section_type not in sections_types:
                raise ValueError(f"Meta lists {section_type} in section_order but not section of type {section_type} is found in sections attribute.")
            
        # We do not check for section types existing in section order
        # for now. We'll consider those "draft sections". Either way 
        # we only render the sections listed in section_order.
        
        return self
        