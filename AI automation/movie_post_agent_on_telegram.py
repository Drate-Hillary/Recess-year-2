import requests
from dotenv import load_dotenv
import os
from telegram import Bot
import asyncio
import logging

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

load_dotenv()

telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
tmdb_api_key = os.getenv("TMDB_API_KEY")

if not all([telegram_bot_token, telegram_chat_id, tmdb_api_key]):
    logger.error("Missing environment variables.")
else:
    try:
        bot = Bot(token=telegram_bot_token)
        
        # Get trending movies
        url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={tmdb_api_key}"
        response = requests.get(url)
        movies = []
        
        if response.status_code == 200:
            data = response.json()
            for movie in data['results'][:5]:
                title = movie['title']
                overview = movie['overview']
                poster_path = movie['poster_path']
                release_date = movie.get('release_date', 'N/A')
                vote_average = movie.get('vote_average', 'N/A')
                poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
                movies.append({
                    'title': title, 
                    'overview': overview, 
                    'poster_url': poster_url,
                    'release_date': release_date,
                    'vote_average': vote_average
                })
        else:
            logger.error(f"Failed to fetch movies from TMDB. Status code: {response.status_code}")
        
        # Post movies to Telegram
        if not movies:
            asyncio.run(bot.send_message(chat_id=telegram_chat_id, text="No trending movies found today."))
        else:
            async def _post_movies():
                for movie in movies:
                    try:
                        caption = (
                            f"🎬 <b>{movie['title']}</b>\n"
                            f"⭐ Rating: {movie['vote_average']}/10\n"
                            f"📅 Release Date: {movie['release_date']}\n\n"
                            f"{movie['overview'][:200]}..."
                        )
                        
                        if movie['poster_url']:
                            await bot.send_photo(
                                chat_id=telegram_chat_id,
                                photo=movie['poster_url'],
                                caption=caption,
                                parse_mode='HTML'
                            )
                        else:
                            await bot.send_message(
                                chat_id=telegram_chat_id,
                                text=caption,
                                parse_mode='HTML'
                            )
                        await asyncio.sleep(2)
                    except Exception as e:
                        logger.error(f"Error posting movie {movie['title']}: {e}")
            
            asyncio.run(_post_movies())
            logger.info("Successfully posted trending movies to Telegram.")
            
    except Exception as e:
        logger.error(f"An error occurred: {e}")