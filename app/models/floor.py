from typing import List, Dict, Any
from pydantic import BaseModel

class SLFloor(BaseModel):
    number: int
    name: str
    requirements: Dict[str, Any]  # ex: {"type": "Blast", "alignment": "Villain"}
    description: str = ""
    
    def get_recommendation_score(self, character: Any) -> int:
        """
        Calcula quão 'ideal' o personagem é para este andar.
        Prioriza personagens mais fracos que ainda atendem aos requisitos.
        """
        score = 0
        # Tiers: T1 < T2 < Transcended < T3 < T4
        tier_values = {
            "T1": 100,
            "T2": 200,
            "Transcended": 300,
            "T3": 400,
            "T4": 500
        }
        
        # Queremos o MENOR score possível para recomendar (usar os fracos primeiro)
        # Se for um andar baixo, T2 é melhor que T3.
        base_tier_score = tier_values.get(character.current_tier, 0)
        
        # Ajuste baseado no número do andar
        if self.number < 15:
            # Para andares baixos, penalizamos personagens T3/T4
            if character.current_tier in ["T3", "T4"]:
                return 1000 # Não usar!
        
        return base_tier_score
