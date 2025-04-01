from enum import Enum


class WorkExpEnum(str, Enum):
    NO_EXPERIENCE = "no_experience"
    JUNIOR = "1-3 year"
    MIDDLE = "3-5 year"
    SENIOR = "over 5 year"


class WorkFormatEnum(str, Enum):
    REMOTE = "remote"
    ONSITE = "onsite"
    HYBRID = "hybrid"


class EducationEnum(str, Enum):
    SCHOOL = "school"
    BACHELOR = "bachelor"
    MASTER = "master"
    DOCTORATE = "doctorate"
