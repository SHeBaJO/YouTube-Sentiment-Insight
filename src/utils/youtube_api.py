"""
YouTube API utilities for fetching comments and video metadata
"""
import streamlit as st
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from typing import List, Dict, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class YouTubeCommentExtractor:
    """Extract comments and metadata from YouTube videos"""
    
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
        from urllib.parse import urlparse, parse_qs
        
        parsed_url = urlparse(url)
        
        if parsed_url.hostname == "youtu.be":
            return parsed_url.path[1:]
        
        if parsed_url.hostname in ("www.youtube.com", "youtube.com"):
            try:
                return parse_qs(parsed_url.query)["v"][0]
            except (KeyError, IndexError):
                return None
        
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
                "channel_id": snippet.get("channelId", ""),
                "channel_title": snippet.get("channelTitle", ""),
                "description": snippet.get("description", ""),
                "published_at": snippet.get("publishedAt", ""),
                "view_count": int(stats.get("viewCount", 0)),
                "like_count": int(stats.get("likeCount", 0)),
                "comment_count": int(stats.get("commentCount", 0)),
            }
        except HttpError as e:
            logger.error(f"Error fetching video info: {e}")
            return {}
    
    def fetch_comments(
        self,
        video_id: str,
        max_comments: int = 100,
        progress_callback=None
    ) -> List[Dict]:
        """
        Fetch comments with metadata from a YouTube video
        
        Args:
            video_id: YouTube video ID
            max_comments: Maximum number of comments to fetch
            progress_callback: Callback function for progress updates
            
        Returns:
            List of comment dictionaries with metadata
        """
        comments = []
        
        try:
            request = self.youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
                textFormat="plainText",
                order="relevance"
            )
            
            while request and len(comments) < max_comments:
                response = request.execute()
                
                for item in response["items"]:
                    if len(comments) >= max_comments:
                        break
                    
                    comment = item["snippet"]["topLevelComment"]["snippet"]
                    
                    comment_data = {
                        "comment_id": item["id"],
                        "text": comment["textDisplay"],
                        "author": comment["authorDisplayName"],
                        "likes": comment["likeCount"],
                        "published_at": comment["publishedAt"],
                        "reply_count": item["snippet"]["totalReplyCount"],
                    }
                    
                    comments.append(comment_data)
                    
                    if progress_callback:
                        progress = min(len(comments) / max_comments, 1.0)
                        progress_callback(progress)
                
                if "nextPageToken" in response and len(comments) < max_comments:
                    request = self.youtube.commentThreads().list(
                        part="snippet",
                        videoId=video_id,
                        pageToken=response["nextPageToken"],
                        maxResults=100,
                        textFormat="plainText",
                        order="relevance"
                    )
                else:
                    break
            
            return comments
        
        except HttpError as e:
            logger.error(f"Error fetching comments: {e}")
            return []
    
    def get_channel_videos(
        self,
        channel_id: str,
        max_results: int = 10
    ) -> List[Dict]:
        """
        Get list of videos from a channel
        
        Args:
            channel_id: YouTube channel ID
            max_results: Maximum number of videos to fetch
            
        Returns:
            List of video information dictionaries
        """
        videos = []
        
        try:
            # Get uploads playlist ID
            request = self.youtube.channels().list(
                part="contentDetails",
                id=channel_id
            )
            response = request.execute()
            
            if not response["items"]:
                return []
            
            uploads_playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
            
            # Get videos from uploads playlist
            request = self.youtube.playlistItems().list(
                part="snippet",
                playlistId=uploads_playlist_id,
                maxResults=min(max_results, 50)
            )
            
            while request and len(videos) < max_results:
                response = request.execute()
                
                for item in response["items"]:
                    video_data = {
                        "video_id": item["snippet"]["resourceId"]["videoId"],
                        "title": item["snippet"]["title"],
                        "description": item["snippet"]["description"],
                        "published_at": item["snippet"]["publishedAt"],
                    }
                    videos.append(video_data)
                
                if "nextPageToken" in response and len(videos) < max_results:
                    request = self.youtube.playlistItems().list(
                        part="snippet",
                        playlistId=uploads_playlist_id,
                        pageToken=response["nextPageToken"],
                        maxResults=min(max_results - len(videos), 50)
                    )
                else:
                    break
            
            return videos
        
        except HttpError as e:
            logger.error(f"Error fetching channel videos: {e}")
            return []


def create_comments_dataframe(comments: List[Dict]) -> pd.DataFrame:
    """
    Convert comments list to pandas DataFrame
    
    Args:
        comments: List of comment dictionaries
        
    Returns:
        DataFrame with comment data
    """
    if not comments:
        return pd.DataFrame()
    
    df = pd.DataFrame(comments)
    df["published_at"] = pd.to_datetime(df["published_at"])
    return df
