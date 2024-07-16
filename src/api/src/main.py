from typing import Optional
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from ebooklib import epub
from create_book import (
    retrieve_story,
    set_cover,
    set_metadata,
    add_chapters,
    slugify,
    wp_get_cookies,
)
import tempfile
from io import BytesIO
from fastapi.staticfiles import StaticFiles
from urllib.request import urlopen, Request
from urllib import parse
from json import loads

app = FastAPI()
BUILD_PATH = Path(__file__).parent / "build"


@app.get("/")
def home():
    return FileResponse(BUILD_PATH / "index.html")


@app.get("/download/{story_id}")
async def download_book(
    story_id: int,
    download_images: bool = False,
    username: Optional[str] = None,
    password: Optional[str] = None,
):
    if username and not password or password and not username:
        return HTMLResponse(
            status_code=422,
            content='Include both the username <u>and</u> password, or neither. Support is available on the <a href="https://discord.gg/P9RHC4KCwd" target="_blank">Discord</a>',
        )

    if username and password:
        # username and password are URL-Encoded by the frontend. FastAPI automatically decodes them.
        try:
            cookies = await wp_get_cookies(username=username, password=password)
        except ValueError:
            return HTMLResponse(
                status_code=403,
                content='Incorrect Username and/or Password. Support is available on the <a href="https://discord.gg/P9RHC4KCwd" target="_blank">Discord</a>',
            )
    else:
        cookies = None

    data = await retrieve_story(story_id, cookies=cookies)
    book = epub.EpubBook()

    try:
        set_metadata(book, data)
    except KeyError:
        return HTMLResponse(
            status_code=404,
            content='Story not found. Check the ID - Support is available on the <a href="https://discord.gg/P9RHC4KCwd" target="_blank">Discord</a>',
        )

    await set_cover(book, data, cookies=cookies)
    # print("Metadata Downloaded")

    # Chapters are downloaded
    async for title in add_chapters(
        book, data, download_images=download_images, cookies=cookies
    ):
        # print(f"Part ({title}) downloaded")
        ...

    # Book is compiled
    temp_file = tempfile.NamedTemporaryFile(
        suffix=".epub", delete=True
    )  # Thanks https://stackoverflow.com/a/75398222

    # create epub file
    epub.write_epub(temp_file, book, {})

    temp_file.file.seek(0)
    book_data = temp_file.file.read()

    return StreamingResponse(
        BytesIO(book_data),
        media_type="application/epub+zip",
        headers={
            "Content-Disposition": f'attachment; filename="{slugify(data["title"])}_{story_id}_{"images" if download_images else ""}.epub"'  # Thanks https://stackoverflow.com/a/72729058
        },
    )


@app.get("/get_info/{story_id}/{endpoint}/{fields}")
def get_info(story_id: int, endpoint: str, fields: str):
    def get_url(url: str):
        req = Request(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        response = urlopen(req)
        return response.read()

    try:
        if endpoint == "v3stories":
            url = f"https://www.wattpad.com/api/v3/stories/{story_id}?fields={fields}"
        elif endpoint == "v3storyparts":
            url = (
                f"https://www.wattpad.com/api/v3/story_parts/{story_id}?fields={fields}"
            )
        elif endpoint == "getstoryurl":
            try:
                url = get_url(
                    f"https://www.wattpad.com/api/v3/story_parts/{story_id}?fields={fields}"
                )
                url = loads(url)
                url = parse.unquote(url["url"])
                content = str(get_url(url))
                content = content[
                    (content.find(':"https://www.wattpad.com/story/') + 32):
                ]
                content = content[: content.find("-")]
                return HTMLResponse(status_code=200, content=content)
            except Exception as error:
                return HTMLResponse(status_code=500, content=str(error))

        return HTMLResponse(status_code=200, content=get_url(url))
    except Exception as error:
        return HTMLResponse(status_code=500, content=str(error))


app.mount("/", StaticFiles(directory=BUILD_PATH), "static")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=80)
