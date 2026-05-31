from io import BytesIO

from bs4 import BeautifulSoup
from epublib import epub
from re import sub

from ..models import Story
from .types import AbstractGenerator


class EPUBGenerator(AbstractGenerator):
    def __init__(
        self,
        metadata: Story,
        part_trees: list[BeautifulSoup],
        cover: bytes,
        images: list[list[bytes | None]],
    ):
        self.story = metadata
        self.parts = part_trees
        self.cover = cover
        self.images = images

        self.book: epub.EpubBook = epub.EpubBook()

    def add_metadata(self):
        """Add metadata to epub."""
        self.book.set_identifier(f"wpd_{self.story['id']}")
        self.book.add_author(self.story["user"]["username"])

        self.book.set_title(self.story["title"])
        self.book.add_metadata("DC", "description", self.story["description"])
        self.book.add_metadata("DC", "date", self.story["createDate"])
        self.book.set_modified(self.story["modifyDate"])
        self.book.set_language("en")#self.story["language"]["name"])

        for tag in self.story["tags"]:
            self.book.add_metadata("DC", "subject", tag)
        self.book.add_metadata(
            "meta",
            "mature",
            str(int(self.story["mature"])),
        )
        self.book.add_metadata(
            "meta",
            "completed",
            str(int(self.story["completed"])),
        )

    def add_chapters(self):
        """Add chapters to epub, replacing references to image urls to static image paths if images are provided during initialization."""
        chapters = []

        for idx, (part, tree) in enumerate(zip(self.story["parts"], self.parts)):
            chapter = epub.EpubHtml(
                title=sub(r"[\x00-\x1F\x7F]", "", part["title"]),
                file_name=f"{idx}_{part['id']}.xhtml",  # Removes control characters from chapter title
            )

            if self.images:
                for img_idx, (img_data, img_tag) in enumerate(
                    zip(self.images[idx], tree.find_all("img"))
                ):
                    path = f"static/{idx}_{part['id']}/{img_idx}.jpeg"
                    img = epub.EpubImage(
                        media_type="image/jpeg", content=img_data, file_name=path
                    )
                    self.book.add_item(img)

                    img_tag["src"] = path

            chapter.set_content(str(tree))
            self.book.add_item(chapter)
            chapters.append(chapter)

    def compile(self):
        self.add_metadata()
        self.book.set_cover("cover.jpg", self.cover)
        self.add_chapters()
        self.book.enable_legacy_support(True)
        return True

    def dump(self) -> BytesIO:
        # Thanks https://stackoverflow.com/a/75398222
        buffer = BytesIO()
        epub.write_epub(buffer, self.book)

        buffer.seek(0)

        return buffer
