from pydantic import BaseModel
from typing import List, Dict


class LabRequest(BaseModel):
    test_name: str # название анализа
    values: Dict[str, float] # словарь показателей
    temperature: float = 0.2


class AbnormalValue(BaseModel):
    name: str # показатель
    status: str # low / high / normal - отклонение от нормы/норма
    possible_reasons: List[str] # список причин


class LabResponse(BaseModel):
    summary: str # общий вывод
    abnormal_values: List[AbnormalValue] # список отклонений
    recommendations: List[str] # рекомендации
