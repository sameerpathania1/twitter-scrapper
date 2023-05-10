from datetime import datetime
from twspace_dl import Twspace, TwspaceDL


space = Twspace.from_space_url("https://twitter.com/i/spaces/1LyxBqBzMeyJN")
data = space.source["data"]["audioSpace"].get("metadata")
download = TwspaceDL(space, format_str=None)
download.download()
print(download.filename + ".m4a")