from sqladmin import ModelView
from sqladmin_litestar_plugin import SQLAdminPlugin

from job.common.infrastructure.models import CV, WorkExp

from .config import async_engine


class CvAdmin(ModelView, model=CV):
    column_list = [CV.title, CV.author_id, CV.id]


class WorkExpAdmin(ModelView, model=WorkExp):
    column_list = [WorkExp.company_name, WorkExp.title]


admin = SQLAdminPlugin(views=[CvAdmin, WorkExpAdmin], engine=async_engine)
