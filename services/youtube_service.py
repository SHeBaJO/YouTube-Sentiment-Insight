"""
YouTube API service for fetching comments and video metadata
"""
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import logging
from urllib.parse import urlparse, parse_qs

logger = logging.getLogger(__name__)


class YouTubeService:
    """Service for interacting with YouTube API"""
    
    def __init__(self, api_key: str):
        """
        Initialize YouTube API client
        
        Args:
            api_key: YouTube Data API v3 key
        """
        self.api_key = api_key
        self.youtube = build("youtube", "v3", developerKey=api_key)
    
    @staticmethod
    def extract_video_id(url: str) -> Optional[str]:
        """
        Extract video ID from YouTube URL
        
        Args:
            url: YouTube URL
            
        Returns:
            Video ID or None if invalid
        """
        try:
            parsed_url = urlparse(url)
            
            if parsed_url.hostname == "youtu.be":
                return parsed_url.path[1:]
            
            if parsed_url.hostname in ("www.youtube.com", "youtube.com"):
                try:
                    return parse_qs(parsed_url.query)["v"][0]
                except (KeyError, IndexError):
                    return None
            
            return None
        except Exception as e:
            logger.error(f"Error extracting video ID: {e}")
            return None
    
    def get_video_info(self, video_id: str) -> Dict:
        """
        Get video metadata
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            Dictionary with video information
        """
        try:
            request = self.youtube.videos().list(
                part="snippet,statistics",
                id=video_id
            )
            response = request.execute()
            
            if not response["items"]:
                return {}
            
            video = response["items"][0]
            snippet = video["snippet"]
            stats = video["statistics"]
            
            return {
                "video_id": video_id,
                "title": snippet.get("title", ""),
                "channel_name": snippet.get("channelTitle", ""),
                "channel_id": snippet.get("channelId", ""),
                "description": snippet.get("description", ""),
                "published_at": snippet.get("publishedAt", ""),
                "view_count": int(stats.get("viewCount", 0)),
                "like_count": int(stats.get("likeCount", 0)),
                "comment_count": int(stats.get("commentCount", 0))
            }
        except HttpError as e:
            logger.error(f"YouTube API error: {e}")
            return {}
        except Exception as e:
            logger.error(f"Error getting video info: {e}")
            return {}
    
    def get_comments(self, video_id: str, max_results: int = 100) -> List[Dict]:
        """
        Get comments from a YouTube video
        
        Args:
            video_id: YouTube video ID
            max_results: Maximum number of comments to retrieve
            
        Returns:
            List of comment dictionaries
        """
        comments = []
        try:
            request = self.youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=min(100, max_results),
                textFormat="plainText",
                order="relevance"
            )
            
            remaining = max_results
            while request and remaining > 0:
                response = request.execute()
                
                for item in response["items"]:
                    if remaining <= 0:
                        break
                    
                    comment = item["snippet"]["topLevelComment"]["snippet"]
                    comments.append({
                        "author": comment.get("authorDisplayName", ""),
                        "text": comment.get("textDisplay", ""),
                        "likes": comment.get("likeCount", 0),
                        "published_at": comment.get("publishedAt", ""),
                        "reply_count": comment.get("replyCount", 0)
                    })
                    remaining -= 1
                
                if "nextPageToken" in response and remaining > 0:
                    request = self.youtube.commentThreads().list(
                        part="snippet",
                        videoId=video_id,
                        pageToken=response["nextPageToken"],
                        maxResults=min(100, remaining),
                        textFormat="plainText",
                        order="relevance"
                    )
                else:
                    break
        
        except HttpError as e:
            logger.error(f"YouTube API error: {e}")
        except Exception as e:
            logger.error(f"Error fetching comments: {e}")
        
        return comments
    
    def get_channel_videos(self, channel_id: str, max_results: int = 10) -> List[Dict]:
        """
        Get recent videos from a channel
        
        Args:
            channel_id: YouTube channel ID
            max_results: Maximum number of videos to retrieve
            
        Returns:
            List of video information dictionaries
        """
        videos = []
        try:
            # Get channel uploads playlist ID
            channel_request = self.youtube.channels().list(
                part="contentDetails",
                id=channel_id
            )
            channel_response = channel_request.execute()
            
            if not channel_response["items"]:
                return videos
            
            uploads_playlist_id = channel_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
            
            # Get videos from uploads playlist
            request = self.youtube.playlistItems().list(
                part="snippet",
                playlistId=uploads_playlist_id,
                maxResults=min(50, max_results)
            )
            
            while request:
                response = request.execute()
                
                for item in response["items"]:
                    video_id = item["snippet"]["resourceId"]["videoId"]
                    video_info = self.get_video_info(video_id)
                    if video_info:
                        videos.append(video_info)
                
                if "nextPageToken" in response and len(videos) < max_results:
                    request = self.youtube.playlistItems().list(
                        part="snippet",
                        playlistId=uploads_playlist_id,
                        pageToken=response["nextPageToken"],
                        maxResults=min(50, max_results - len(videos))
                    )
                else:
                    break
        
        except HttpError as e:
            logger.error(f"YouTube API error: {e}")
        except Exception as e:
            logger.error(f"Error fetching channel videos: {e}")
        
        return videos[:max_results]
    
    def create_comments_dataframe(self, comments: List[Dict]) -> pd.DataFrame:
        """
        Create DataFrame from comments
        
        Args:
            comments: List of comment dictionaries
            
        Returns:
            DataFrame with comments
        """
        if not comments:
            return pd.DataFrame()
        
        df = pd.DataFrame(comments)
        df["published_at"] = pd.to_datetime(df["published_at"])
        return df
