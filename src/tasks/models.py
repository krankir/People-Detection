from sqlalchemy import (Boolean, Column, ForeignKey, Integer, Sequence, Text,
                        text)
from sqlalchemy.orm import relationship

from src.db import Base


class Task(Base):
    """
    Модель задачи

    **Параметры**

    * `name`: название
    * `type`: тип
    * `doc_url`: ссылка на документ
    * `csv_url`: ссылка на csv
    * `user_id`: One-To-Many
    * `task_status_id`: One-To-Many
    * `file_path`: путь к файлу
    * `minutes`: минуты
    * `starttimedownload`: начало загрузки
    * `endtimedownload`: конец загрузки
    * `starttimeneirone`: начало работы нейронки
    * `endtimeneirone`: конец работы нейронки
    * `startTimeNeirone`: начало работы нейронки
    * `endTimeNeirone`: конец работы нейронки
    * `startTimeDownload`: начало загрузки
    * `endTimeDownload`: конец загрузки
    * `api`: API
    * `hash`: HASH
    """
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    doc_url = Column(Text)
    task_status_id = Column(ForeignKey('task_status.id'), index=True)
    status = relationship('TaskStatus', back_populates='task', lazy='joined')


class TaskStatus(Base):
    """
    Модель статуса задачи

    **Параметры**

    * `name`: название
    """
    __tablename__ = 'task_status'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    task = relationship('Task', back_populates='status')
