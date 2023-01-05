import plexapi
from plexapi.myplex import MyPlexAccount
import time
from dotenv import load_dotenv
import os

load_dotenv()

account = MyPlexAccount(f'{os.getenv("USER")}', f'{os.getenv("PASSWORD")}')
plex = account.resource(f'{os.getenv("SERVER")}').connect()

all_sections = {
    "show_sections":[],
    "movie_sections":[]
}

get_sections = plex.library.sections()
for index, section in enumerate(get_sections):
    if section.type.lower() == "show":
        all_sections['show_sections'].append(section.title)
    if section.type.lower() == "movie":
        all_sections['movie_sections'].append(section.title)

print(f"{len(all_sections['show_sections'])} Show Sections")
print(f"{len(all_sections['movie_sections'])} Movie Sections")

while True:
    watchlist = account.watchlist(filter='released', libtype='show')
    for item in watchlist:
        if item.type == "show":
            for section in all_sections['show_sections']:
                try:
                    result = plex.library.section(f"{section}").get(item.title)
                    update = plex.library.section(f"{section}").update(path=str(f"{result.locations[0]}"))
                    if update is not None:
                        print(f"Updating {item.title} on {section}")
                except plexapi.exceptions.NotFound:
                    pass
                except Exception as e:
                    print(e)
                    pass
    time.sleep(int(os.getenv("INTERVAL")))