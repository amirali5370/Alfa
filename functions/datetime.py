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


def gregorian_to_jalali(utc_dt):
    """
    تبدیل datetime جهانی (UTC) به تاریخ شمسی با ساعت تهران
    utc_dt: datetime با tzinfo=UTC
    خروجی: jdatetime.datetime با تاریخ شمسی و ساعت تهران
    """
    if utc_dt.tzinfo is None:
        # اگر ورودی naive باشه فرض می‌کنیم UTC است
        utc_dt = utc_dt.replace(tzinfo=UTC)
    
    # تبدیل به ساعت تهران
    tehran_tz = timezone("Asia/Tehran")
    tehran_dt = utc_dt.astimezone(tehran_tz)
    
    # تبدیل به تاریخ شمسی
    jalali_dt = jdatetime.datetime.fromgregorian(
        year=tehran_dt.year,
        month=tehran_dt.month,
        day=tehran_dt.day,
        hour=tehran_dt.hour,
        minute=tehran_dt.minute,
        second=tehran_dt.second
    )
    
    return jalali_dt.strftime("%Y/%m/%d %H:%M")