
from datetime import timedelta, datetime

from sqlalchemy.engine import row


def parse_duration(duration_str):
    duration_str = duration_str.replace("P","").replace("T","")

    components = ['D','H','M','S']
    values = {'D':0,'H':0,'M':0,'S':0}
    for component in components:
        if component in duration_str:
            value,duration_str = duration_str.split(component)
            values[component] = int(value)

    total_duration = timedelta(
        days=values['D'],
        hours=values['H'],
        minutes=values['M'],
        seconds=values['S']
    )

    return total_duration

def transform_data(row):

    duration_td = parse_duration(row["Duration"])

    transformed_row = {

        "video_id": row["video_id"],

        "title": row["video_title"],

        "publishedAt": row["Upload_date"],

        "duration": (datetime.min + duration_td).time(),

        "viewCount": row["video_views"],

        "likeCount": row["Likes_count"],

        "commentCount": row["Comments_count"],

        "video_Type": "Shorts" if duration_td.total_seconds() <= 60 else "Normal"

    }

    return transformed_row
