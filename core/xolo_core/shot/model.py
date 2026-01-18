from pydantic import BaseModel
from pathlib import Path




    
    

class Shot(BaseModel):
    shot_name: str
    start: int
    end: int
    fps: int