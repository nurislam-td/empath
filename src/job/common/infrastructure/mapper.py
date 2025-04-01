from recruitment.api.schemas import Skill
from sqlalchemy import RowMapping


def convert_db_to_skill(skill: RowMapping) -> Skill:
    return Skill(name=skill.name, id=skill.id)
