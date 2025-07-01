from pyrogram import Client, filters
import re
import asyncio
import os
import glob
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client("video_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

VIDEO_LINK_REGEX = re.compile(
    r"(https?://(?:www\.)?(?:youtube\.com|youtu\.be|tiktok\.com|vm\.tiktok\.com|vt\.tiktok\.com|instagram\.com|twitter\.com|x\.com)/[^\s]+)"
)

@app.on_message(filters.regex(VIDEO_LINK_REGEX) & ~filters.private)
async def download_and_send_video(client, message):
    links = VIDEO_LINK_REGEX.findall(message.text)
    for link in links:
        status_message = await message.reply_text("Video İndiriliyor...")

        output_template = "temp_video"

        cmd = [
            "yt-dlp",
            "-f", "best",
            "-o", output_template + ".%(ext)s",
            link
        ]

        try:
            process = await asyncio.create_subprocess_exec(*cmd)
            await process.communicate()

            files = glob.glob(output_template + ".*")
            if files:
                video_file = files[0]
                if video_file.endswith(".mp4"):
                    await client.send_video(message.chat.id, video_file)
                else:
                    await status_message.edit("Video formatı mp4 değil, gönderilemiyor.")
                    os.remove(video_file)
                    continue
                os.remove(video_file)
                await status_message.delete()
            else:
                await status_message.edit("Video indirilemedi.")
        except Exception as e:
            await status_message.edit(f"Hata oluştu: {e}")

if __name__ == "__main__":
    print("Bot başlatılıyor...")
    app.run()
