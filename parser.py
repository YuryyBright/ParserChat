from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.errors import ChatAdminRequiredError
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.types import User, Channel, Chat
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
import logging
import asyncio
import os
from datetime import datetime

# Конфігурація логування
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


@dataclass
class ParticipantInfo:
    """Клас для зберігання інформації про учасника чату."""
    id: int
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    is_bot: bool
    is_premium: bool
    joined_date: Optional[datetime] = None


class ParticipantRepository:
    """Відповідає за збереження і отримання даних про учасників."""

    def __init__(self):
        self.participants: Dict[int, ParticipantInfo] = {}

    def add(self, participant: ParticipantInfo) -> None:
        """Додає учасника до репозиторію."""
        self.participants[participant.id] = participant

    def get_all(self) -> List[ParticipantInfo]:
        """Повертає всіх учасників."""
        return list(self.participants.values())

    def get_by_id(self, user_id: int) -> Optional[ParticipantInfo]:
        """Повертає учасника за ідентифікатором."""
        return self.participants.get(user_id)

    def export_to_csv(self, filepath: str) -> None:
        """Експортує дані учасників у CSV файл."""
        import csv

        with open(filepath, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Запис заголовків
            writer.writerow(
                ['ID', 'Username', 'First Name', 'Last Name', 'Phone', 'Is Bot', 'Is Premium', 'Joined Date'])

            # Запис даних
            for participant in self.participants.values():
                writer.writerow([
                    participant.id,
                    participant.username,
                    participant.first_name,
                    participant.last_name,
                    participant.phone,
                    participant.is_bot,
                    participant.is_premium,
                    participant.joined_date
                ])

        logger.info(f"Дані експортовано в {filepath}")


class ChatParticipantParser:
    """Клас для отримання інформації про учасників чату."""

    def __init__(self, client: TelegramClient):
        self.client = client
        self.repository = ParticipantRepository()

    @staticmethod
    def _extract_participant_info(participant: User) -> ParticipantInfo:
        """Витягує необхідну інформацію з об'єкта User."""

        return ParticipantInfo(
            id=participant.id,
            username=participant.username,
            first_name=participant.first_name,
            last_name=participant.last_name,
            phone=participant.phone if hasattr(participant, 'phone') else None,
            is_bot=participant.bot if hasattr(participant, 'bot') else False,
            is_premium=participant.premium if hasattr(participant, 'premium') else False
        )

    async def get_chat_list(self):
        """Отримання списку чатів"""
        chats = []
        async for dialog in self.client.iter_dialogs():
            chats.append((dialog.id, dialog.title))
        return chats

    async def parse_chat_participants(self, chat_id: int, limit: int = 300) -> List[ParticipantInfo]:
        """Отримує та парсить учасників заданого чату."""
        try:
            logger.info(f"Початок парсингу учасників для чату {chat_id}")

            # Отримання інформації про учасників
            offset = 0
            all_participants = []

            while True:
                try:
                    participants = await self.client(GetParticipantsRequest(
                        channel=chat_id,
                        filter=ChannelParticipantsSearch(''),
                        offset=offset,
                        limit=limit,
                        hash=0
                    ))
                except ChatAdminRequiredError:
                    logger.error(f"Необхідно бути адміністратором чату {chat_id}, щоб отримати список учасників.")
                    return []

                if not participants.users:
                    break

                all_participants.extend(participants.users)
                offset += len(participants.users)

                # Обмеження кількості учасників, якщо потрібно
                if limit and offset >= limit:
                    break
                await asyncio.sleep(1)

            # Парсинг інформації про кожного учасника
            for participant in all_participants:
                if isinstance(participant, User):
                    participant_info = self._extract_participant_info(participant)
                    self.repository.add(participant_info)

            logger.info(f"Завершено парсингу {len(self.repository.get_all())} учасників")
            return self.repository.get_all()

        except Exception as e:
            logger.error(f"Помилка при парсингу учасників: {e}")
            raise

    def export_data(self, format_type: str = 'csv', filepath: str = None) -> None:
        """Експортує дані у вказаний формат."""
        if not filepath:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"chat_participants_{timestamp}.{format_type}"

        if format_type.lower() == 'csv':
            self.repository.export_to_csv(filepath)
        else:
            raise ValueError(f"Формат {format_type} не підтримується")


class TelegramClientFactory:
    """Фабрика для створення клієнтів Telegram."""

    @staticmethod
    def create_client(api_id: int, api_hash: str, session_name: str = 'new_session') -> TelegramClient:
        """Створює та повертає налаштований TelegramClient."""
        client = TelegramClient(session_name, api_id, api_hash)
        return client


async def main():
    load_dotenv()
    API_ID = int(os.getenv('TELEGRAM_API_ID', 0))
    API_HASH = os.getenv('TELEGRAM_API_HASH', '')
    if not API_ID or not API_HASH:
        logger.error("Не вказано необхідні параметри. Встановіть змінні середовища.")
        return

    # Створення клієнта
    client = TelegramClientFactory.create_client(API_ID, API_HASH)

    async with client:

        parser = ChatParticipantParser(client)

        # Отримання та вивід списку чатів
        chat_list = await parser.get_chat_list()
        if not chat_list:
            logger.info("Немає доступних чатів.")
            return

        logger.info("Доступні чати:")
        for idx, (chat_id, chat_title) in enumerate(chat_list, 1):
            print(f"{idx}. {chat_title} (ID: {chat_id})")

        # Вибір чату користувачем
        try:
            choice = int(input("Введіть номер чату: ")) - 1
            if choice < 0 or choice >= len(chat_list):
                logger.error("Невірний вибір.")
                return
            chat_id = chat_list[choice][0]
        except ValueError:
            logger.error("Введено некоректне значення.")
            return

        # Отримання учасників
        participants = await parser.parse_chat_participants(chat_id)

        # Експорт даних
        parser.export_data(format_type='csv')

        # Виведення інформації
        logger.info(f"Всього учасників: {len(participants)}")
        for participant in participants[:5]:  # Виводимо перших 5 для прикладу
            logger.info(f"ID: {participant.id}, Username: {participant.username}")


if __name__ == "__main__":
    # Запуск головної функції
    asyncio.run(main())

