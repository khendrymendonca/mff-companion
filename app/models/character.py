from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

class CharacterType(str, Enum):
    COMBAT = "Combat"
    BLAST = "Blast"
    SPEED = "Speed"
    UNIVERSAL = "Universal"

class Alignment(str, Enum):
    HERO = "Hero"
    VILLAIN = "Villain"
    NEUTRAL = "Neutral"

class Tier(str, Enum):
    T1 = "T1"
    T2 = "T2"
    T3 = "T3"
    T4 = "T4"
    TRANSCENDED = "Transcended"

class Character(BaseModel):
    id: Optional[int] = None
    name: str
    base_type: CharacterType
    base_alignment: Alignment
    abilities: List[str] = []

class UserCharacter(Character):
    current_tier: Tier = Tier.T1
    level: int = 60
    is_used: bool = False
    
    def can_enter_floor(self, floor_requirements: dict) -> bool:
        """
        Verifica se o personagem atende aos requisitos do andar.
        floor_requirements ex: {"type": "Combat", "alignment": "Villain"}
        """
        if self.is_used:
            return False
            
        req_type = floor_requirements.get("type")
        if req_type and self.base_type != req_type:
            # Universal geralmente entra em quase tudo, mas vamos seguir a regra estrita primeiro
            if self.base_type != CharacterType.UNIVERSAL:
                return False
                
        req_alignment = floor_requirements.get("alignment")
        if req_alignment and self.base_alignment != req_alignment:
            return False
            
        return True
