from pytz import timezone, UTC
import jdatetime

def jalali_to_gregorian(j_input):
    '''
    "1404-06-12 00:15"
    "1402-02-11 22:18"
    '''
    jd = jdatetime.datetime.strptime(j_input, "%Y-%m-%d %H:%M")
    greg = jd.togregorian()  # تبدیل به میلادی

    tehran_tz = timezone("Asia/Tehran")
    greg_tehran = tehran_tz.localize(greg)  # زمان تهران
    greg_utc = greg_tehran.astimezone(UTC)  # تبدیل به UTC

    return greg_utc
