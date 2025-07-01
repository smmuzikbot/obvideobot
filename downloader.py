import yt_dlp
import os

async def download_and_send(client, message, url):
    await message.reply("🎬 Video indiriliyor...")

    ydl_opts = {
        'outtmpl': 'video.%(ext)s',
        'format': 'mp4',
        'quiet': True,
        'noplaylist': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            filename = filename.replace(".webm", ".mp4").replace(".mkv", ".mp4")

        await client.send_video(
            chat_id=message.chat.id,
            video=filename,
            caption=f"🔗 [{info.get('title', 'Video')}]({url})",
            parse_mode=None
        )
        os.remove(filename)

    except Exception as e:
        await message.reply(f"❌ Video indirilemedi: `{e}`", quote=True)
