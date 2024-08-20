import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


# Указываем путь к файлу CSV, содержащему исходные данные для импорта
csv_file_path = '/home/s/Code/dbt/input_data/Marketing.csv'


# Создаем подключение к базе данных SQLite
engine = create_engine('sqlite:///marketing.db')
Base = declarative_base()


# Определяем схему таблицы Channel для хранения информации о каналах
class Channel(Base):
    __tablename__ = 'channel'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    marketing_data = relationship("MarketingData", back_populates="channel")


# Определяем схему основной таблицы MarketingData для хранения данных маркетинговых кампаний
class MarketingData(Base):
    __tablename__ = 'marketing_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    c_date = Column(String, nullable=False)  # Дата кампании
    campaign_name = Column(String, nullable=False)  # Название кампании
    category = Column(String, nullable=False)  # Категория кампании
    campaign_id = Column(Integer, nullable=False)  # Уникальный идентификатор кампании
    impressions = Column(Integer, nullable=False)  # Количество показов
    mark_spent = Column(Float, nullable=False)  # Сумма затрат на маркетинг
    clicks = Column(Integer, nullable=False)  # Количество кликов
    leads = Column(Integer, nullable=False)  # Количество лидов
    orders = Column(Integer, nullable=False)  # Количество заказов
    revenue = Column(Float, nullable=False)  # Полученный доход
    channel_id = Column(Integer, ForeignKey('channel.id'))  # Внешний ключ для связи с таблицей Channel

    channel = relationship("Channel", back_populates="marketing_data")


# Создаем таблицы на основе определенной схемы
Base.metadata.create_all(engine)


# Загрузка данных из CSV файла в DataFrame с использованием pandas
df = pd.read_csv(csv_file_path)


# Если в CSV файле присутствует колонка 'channel', то обрабатываем её отдельно
if 'channel' in df.columns:
    # Извлекаем уникальные значения каналов из данных
    channels = df['channel'].unique()

    # Заполняем таблицу каналов уникальными значениями
    with engine.connect() as conn:
        for channel in channels:
            conn.execute(Channel.__table__.insert().values(name=channel))

    # Заменяем названия каналов на их ID для связи с таблицей MarketingData
    channels_df = pd.read_sql('channel', conn)
    df = df.merge(channels_df, left_on='channel', right_on='name').drop(columns=['channel', 'name'])


# Импортируем данные из DataFrame в таблицу MarketingData в базе данных SQLite
df.to_sql('marketing_data', con=engine, if_exists='append', index=False)


# Выводим одно строковое сообщение о завершении процесса
print("Database and data import completed.")
