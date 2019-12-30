# Purpose:

1. Gathers image link posts from reddit.com/r/ptcgo.
2. Uses Google Cloud Vision API for OCR to extract pack codes from images.
3. Automatically redeems codes for packs in the Pokemon Trading Card Game Online client.

# Requirements:

View requirements.txt for full package list.

Requires Google Cloud Vision API access, which uses a json file and system environment variable for authentication.

First 1000 queries per month are free. Still unsure if this is per calendar month or every 30 days, etc.

Requires Reddit API access for the PRAW package.

Free, with rate limit of 30 per minute. Not an issue for this program using current delays.

# To-do list:

1. Maintain a timestamp for when the last most-recent post was created, in order to avoid reprocessing old posts on next Reddit API call.
2. Determine method of redeeming as many codes as possible.
  * Post-by-post? (most likely this, due to image processing adding delays)
  * Batches of 10 codes? (unlikely, too many delays added from processing a possible second image if the first image contains fewer than 10 codes)
