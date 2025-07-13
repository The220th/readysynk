# coding: utf-8


from ksupk import singleton_decorator
from threading import Lock
from pathlib import Path
from pdf2image import convert_from_path
from PIL import Image


@singleton_decorator
class RAMDB:

    def __init__(self):
        self.pr_lock: Lock = Lock()
        self.ready_lock: Lock = Lock()

        self.users: dict = {}
        self.presentation: list[Image.Image] | None = None
        self.presentation_slide_num: int | None = None

        self.presentation_not_yet_ready_text: str = "Презентация ещё не загружена"

    def get_users(self) -> dict:
        with self.ready_lock:
            return self.users

    def get_ready_users_table(self) -> tuple[list[list[str]], list[str]]:
        """Returns table (Dataframe) and list of hashes"""
        res, res_hashes = [], []
        with self.ready_lock:
            for user_i in self.users:
                user_hash = user_i
                user_name = self.users[user_hash]["name"]
                user_ready = "✅" if self.users[user_hash]["ready"] == True else "❌"
                res.append([f"{user_hash}", f"{user_name}", f"{user_ready}"])
                res_hashes.append(f"{user_hash}")
        return res, res_hashes

    def set_unready(self, user_hash: str):
        with self.ready_lock:
            self.users[user_hash]["ready"] = False

    def set_all_unready(self):
        with self.ready_lock:
            for user_i in self.users:
                self.users[user_i]["ready"] = False

    def do_ready(self, user_hash: str, user_name: str):
        with self.ready_lock:
            if user_hash not in self.users:
                self.users[user_hash] = {}
            self.users[user_hash]["ready"] = True
            self.users[user_hash]["name"] = user_name

    def remove_user(self, user_hash: str):
        with self.ready_lock:
            self.users.pop(user_hash)

    def init_presentation(self, pr_file_path: Path | str):
        pr_file_path = Path(pr_file_path)

        with self.pr_lock:
            images = convert_from_path(pr_file_path)
            self.presentation = images

    def get_all_presentation(self) -> list[Image.Image]:
        with self.pr_lock:
            if self.presentation is not None:
                return self.presentation
            else:
                raise RuntimeError(self.presentation_not_yet_ready_text)

    def get_slide(self, slide_num: int) -> Image.Image:
        slide_num = slide_num - 1
        with self.pr_lock:
            if self.presentation is not None:
                return self.presentation[slide_num]
            else:
                raise RuntimeError(self.presentation_not_yet_ready_text)

    def get_slides_num(self) -> int:
        with self.pr_lock:
            if self.presentation is not None:
                return len(self.presentation)
            else:
                raise RuntimeError(self.presentation_not_yet_ready_text)

    def get_cur_slide_num(self) -> int:
        with self.pr_lock:
            if self.presentation_slide_num is not None:
                return self.presentation_slide_num
            else:
                raise RuntimeError(self.presentation_not_yet_ready_text)

    def set_cur_slide(self, slide_num: int):
        with self.pr_lock:
            if slide_num > len(self.presentation) or slide_num < 1:
                raise ValueError(f"Слайд номер {slide_num} вышел за пределы презентации (максимально в ней может быть {len(self.presentation)} слайдов).")
            if self.presentation is None:
                raise RuntimeError(self.presentation_not_yet_ready_text)
            self.presentation_slide_num = slide_num
