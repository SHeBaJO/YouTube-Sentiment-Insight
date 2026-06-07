"""
Download service for downloading YouTube videos and audio using yt-dlp
"""
import os
import logging
import yt_dlp

logger = logging.getLogger(__name__)


class DownloadService:
    """Service to download YouTube videos or audio using yt-dlp"""
    
    @staticmethod
    def download(url: str, format_type: str = "video", output_dir: str = "downloads") -> dict:
        """
        Download YouTube video or audio.
        
        Args:
            url: YouTube video URL or ID
            format_type: "video" (MP4 format, 720p or best progressive) or "audio" (M4A audio)
            output_dir: Directory to save the downloaded file
            
        Returns:
            Dictionary with download info (filepath, title, duration, success/error status)
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Progressive MP4 for video (no merge needed) or best M4A for audio (no transcode needed)
        if format_type == "audio":
            ydl_opts = {
                'format': 'bestaudio[ext=m4a]/bestaudio/best',
                'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
            }
        else:
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
            }
            
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filepath = ydl.prepare_filename(info)
                
                # Double-check if the file exists (sometimes yt-dlp might change extension)
                if not os.path.exists(filepath):
                    base_name = os.path.splitext(os.path.basename(filepath))[0]
                    for f in os.listdir(output_dir):
                        if f.startswith(base_name):
                            filepath = os.path.join(output_dir, f)
                            break
                            
                return {
                    "success": True,
                    "filepath": filepath,
                    "title": info.get("title", "Unknown Title"),
                    "duration": info.get("duration", 0),
                    "thumbnail": info.get("thumbnail", ""),
                    "size_bytes": os.path.getsize(filepath) if os.path.exists(filepath) else 0,
                }
        except Exception as e:
            logger.error(f"Error downloading YouTube video: {e}")
            return {
                "success": False,
                "error": str(e)
            }
