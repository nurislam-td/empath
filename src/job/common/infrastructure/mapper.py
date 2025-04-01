from sqlalchemy import RowMapping

from job.recruitment.api.schemas import Skill


def convert_db_to_skill(skill: RowMapping) -> Skill:
    return Skill(name=skill.name, id=skill.id)
