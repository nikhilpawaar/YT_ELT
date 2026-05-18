import logging

logger = logging.getLogger(__name__)
table = "yt_api"

def insert_rows(cur, conn, schema, row):

    try:

        if schema == "staging":

            cur.execute(
                f"""
                INSERT INTO {schema}.{table}
                (
                    "video_id",
                    "video_title",
                    "Upload_date",
                    "Duration",
                    "video_views",
                    "Likes_count",
                    "Comments_count"
                )

                VALUES
                (
                    %(video_id)s,
                    %(title)s,
                    %(publishedAt)s,
                    %(duration)s,
                    %(viewCount)s,
                    %(likeCount)s,
                    %(commentCount)s
                );
                """,
                row
            )

        else:

            cur.execute(
                f"""
                INSERT INTO {schema}.{table}
                (
                    "video_id",
                    "video_title",
                    "Upload_date",
                    "Duration",
                    "video_views",
                    "Likes_count",
                    "Comments_count",
                    "Video_Type"
                )

                VALUES
                (
                    %(video_id)s,
                    %(title)s,
                    %(publishedAt)s,
                    %(duration)s,
                    %(viewCount)s,
                    %(likeCount)s,
                    %(commentCount)s,
                    %(video_Type)s
                );
                """,
                row
            )

        conn.commit()

        logger.info(f"Inserted row with video_id: {row['video_id']}")

    except Exception as e:

        logger.error(f"Error inserting row with video_id: {row['video_id']} - {e}")

        conn.rollback()

        raise e

def update_rows(cur, conn, schema, row):

    try:

        if schema == "staging":

            cur.execute(
                f"""
                UPDATE {schema}.{table}

                SET
                    "video_title" = %(title)s,
                    "Upload_date" = %(publishedAt)s,
                    "Duration" = %(duration)s,
                    "video_views" = %(viewCount)s,
                    "Likes_count" = %(likeCount)s,
                    "Comments_count" = %(commentCount)s

                WHERE "video_id" = %(video_id)s;
                """,
                row
            )

        else:

            cur.execute(
                f"""
                UPDATE {schema}.{table}

                SET
                    "video_title" = %(title)s,
                    "Upload_date" = %(publishedAt)s,
                    "Duration" = %(duration)s,
                    "video_views" = %(viewCount)s,
                    "Likes_count" = %(likeCount)s,
                    "Comments_count" = %(commentCount)s,
                    "Video_Type" = %(video_Type)s

                WHERE "video_id" = %(video_id)s;
                """,
                row
            )

        conn.commit()

        logger.info(f"Updated row with video_id: {row['video_id']}")

    except Exception as e:

        logger.error(f"Error updating row with video_id: {row['video_id']} - {e}")

        conn.rollback()

        raise e

def delete_rows(cur,conn,schema,ids_to_delete):

    try:
        ids_to_delete = f"""({','.join(f"'{id}'") for id in (ids_to_delete)})"""
        cur.execute (
            f"""
            DELETE FROM {schema}.{table}
            WHERE "video_id" IN {ids_to_delete};
            """
        )
        
        conn.commit()
        logger.info(f"deleted row with Video_IDs:{ids_to_delete}")
    except Exception as e:
        logger.error(f"Error deleting row with Video_IDs:{ids_to_delete} - {e}")
        raise e
