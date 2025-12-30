from datetime import datetime
import pytz

# Define the local timezone (replace with your desired timezone)
local_tz = pytz.timezone('Asia/Bishkek')


# Function to return the current local time
def local_now():
    # Make sure the datetime is timezone-aware
    return datetime.now(local_tz)
