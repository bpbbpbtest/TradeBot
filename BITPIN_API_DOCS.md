# BitPin Exchange API - Complete DocumentationSource: https://docs.bitpin.ir/v1/ (mirrored from rendered pages)

======================================================================
# 1. Introduction
======================================================================


---

## Introduction bitpin-api-documentation

https://docs.bitpin.org/v1/docs/Introduction/bitpin-api-documentation

معرفیمستندات API بیت‌پین
Welcome to the Bitpin API documentation

اینجا جاییه که شما به عنوان یه توسعه‌دهنده، به تمامی ابزارها و اطلاعات لازم برای کار با API بیت‌پین دسترسی پیدا می‌کنید.
به کمک این API می‌تونید به داده‌های بازارها، قیمت‌ها و سایر عملیات‌های مالی دسترسی داشته باشید.

🌐 Base URL​

تمام درخواست‌های API باید به یکی از این آدرس‌ها ارسال بشه:

https://api.bitpin.ir — ⚠️ موقتاً در دسترس نیست
https://api.bitpin.org
اطلاعیه

توجه داشته باش که همیشه از آدرس درست استفاده کنی تا مطمئن بشی که اطلاعات صحیح و به‌روز دریافت می‌کنی.

⏱ Rate Limit​

حداکثر نرخ درخواست 300 درخواست در دقیقه به ازای هر IP است. این مقدار برای اکثر مسیرهای API صدق می‌کنه، ولی اگه جایی نرخ متفاوتی باشه، توی مستندات مربوط به اون بخش ذکر شده.

🔑 Authentication​

برای دسترسی به بخش‌هایی از API که نیاز به احراز هویت دارن، باید از توکن احراز هویت استفاده کنی.
توکن باید به این شکل در هدر درخواست HTTP قرار بگیره:

cURL
Python
curl -X GET "https://api.bitpin.org/api/v1/mkt/currencies/" \  
     -H "Authorization: Bearer YOUR_AUTH_TOKEN" \  
     -H "Content-Type: application/json"  

💬 Response​

پاسخ‌های API بیت‌پین همیشه به صورت JSON برمی‌گردن. یه نمونه از پاسخ موفق رو می‌بینی:

[  
  {  
    "currency": "IRT",  
    "name": "Toman",  
    "tradable": true,  
    "precision": "0"  
  },  
  {  
    "currency": "VTHO",  
    "name": "VeThor Token",  
    "tradable": true,  
    "precision": "0"  
  }  
]  

Additional Notes​
Errors: اگه خطایی پیش بیاد، API یه پیام خطا و کد HTTP برمی‌گردونه. برای اطلاعات بیشتر به بخش مدیریت خطا مراجعه کن.
Security: حتماً مطمئن شو که توکن احراز هویتت رو امن نگه داری و به شخص ثالثی فاش نکنی.
Versioning: همیشه از نسخه درست API استفاده کن. نسخه API تو مسیر درخواست مشخص میشه (مثال: /v1/).


---

## Introduction guide

https://docs.bitpin.org/v1/docs/Introduction/guide

معرفیراهنمای مطالعه
راهنمای مطالعه
🌐 نحوه استفاده از این داکیومنت​

اینجا جاییه که بهت یاد می‌دیم چطور با API بیت‌پین مثل یه حرفه‌ای کار کنی. هر چی لازم داری، از مبانی تا نکات پیشرفته، اینجا پیدا می‌کنی.

📝 ساختار داکیومنت​
Introduction: هر بخش یه مقدمه داره که توضیح می‌ده این API چه کارهایی برات انجام می‌ده.
Input Parameters: تمام پارامترهایی که باید به API بدی اینجا لیست شدن. فقط کافیه که مطمئن بشی پارامترها رو درست پر کردی.
Request Examples: نمونه درخواست‌هایی گذاشتیم که می‌تونی ازشون استفاده کنی تا سریع‌تر API رو به کار بگیری.
Responses: ساختار و نمونه‌های جواب‌هایی که از API می‌گیری رو هم برات توضیح دادیم تا راحت‌تر بتونی تحلیلشون کنی.
Important Tips: یه سری نکته و ترفند داریم که استفاده از API رو برات بهینه‌تر و امن‌تر می‌کنه.
اطلاعیه

🔗 Client Libraries
هنوز کتابخانه یا SDK رسمی نداریم، ولی برنامه داریم که به زودی برای زبان‌های مختلف کتابخانه‌هایی ارائه کنیم. به محض آماده شدن، لینک‌هاشون رو اینجا قرار می‌دیم.


---

## intro

https://docs.bitpin.org/v1/docs/intro

مقدمه

🌟 Welcome to the Bitpin API documentation! اینجا جاییه که شما به عنوان یه توسعه‌دهنده، به تمامی ابزارها و اطلاعات لازم برای کار با API بیت‌پین دسترسی پیدا می‌کنید.
به کمک این API می‌تونید به داده‌های بازارها، قیمت‌ها و سایر عملیات‌های مالی دسترسی داشته باشید.

🌐 Base URL​

تمام درخواست‌های API باید به یکی از این آدرس‌ها ارسال بشه:

https://api.bitpin.ir — ⚠️ موقتاً در دسترس نیست
https://api.bitpin.market
https://api.bitpin.org
اطلاعیه

توجه داشته باش که همیشه از آدرس درست استفاده کنی تا مطمئن بشی که اطلاعات صحیح و به‌روز دریافت می‌کنی.

⏱ Rate Limit​

حداکثر نرخ درخواست 300 درخواست در دقیقه به ازای هر IP است. این مقدار برای اکثر مسیرهای API صدق می‌کنه، ولی اگه جایی نرخ متفاوتی باشه، توی مستندات مربوط به اون بخش ذکر شده.

🔑 Authentication​

برای دسترسی به بخش‌هایی از API که نیاز به احراز هویت دارن، باید از توکن احراز هویت استفاده کنی.
توکن باید به این شکل در هدر درخواست HTTP قرار بگیره:

curl -X GET "https://api.bitpin.org/api/v1/mkt/currencies/" \  
     -H "Authorization: Bearer YOUR_AUTH_TOKEN" \  
     -H "Content-Type: application/json"  

🛠 Parameters​

تو این بخش، جدولی از پارامترهایی که ممکنه نیاز داشته باشی توی درخواست‌های API استفاده کنی رو داریم.

Parameter	Description	Required
Authorization	توکن احراز هویت که به صورت Bearer YOUR_AUTH_TOKEN ارسال می‌شود.	بله
Content-Type	نوع محتوای درخواست (معمولاً application/json).	بله
Accept	نوع محتوای قابل قبول در پاسخ (معمولاً application/json).	خیر
currency_id	شناسه ارز برای دریافت اطلاعات مربوط به آن (مثال: BTC).	خیر
💬 Response​

پاسخ‌های API بیت‌پین همیشه به صورت JSON برمی‌گردن. یه نمونه از پاسخ موفق رو می‌بینی:

{  
  "status": true,  
  "message": "Success",  
  "data": {  
    "currencies": [  
      {  
        "id": "btc",  
        "name": "Bitcoin",  
        "symbol": "BTC"  
      },  
      {  
        "id": "eth",  
        "name": "Ethereum",  
        "symbol": "ETH"  
      }  
    ]  
  }  
}  

status: نشان‌دهنده موفقیت یا شکست درخواست.
message: پیامی که وضعیت درخواست را توضیح می‌دهد.
data: داده‌های مربوط به درخواست، شامل لیست ارزها.
Additional Notes​
Errors: اگه خطایی پیش بیاد، API یه پیام خطا و کد HTTP برمی‌گردونه. برای اطلاعات بیشتر به بخش Handling API Errors مراجعه کن.
Security: حتماً مطمئن شو که توکن احراز هویتت رو امن نگه داری و به شخص ثالثی فاش نکنی.
Versioning: همیشه از نسخه درست API استفاده کن. نسخه API تو مسیر درخواست مشخص میشه (مثال: /v1/).


======================================================================
# 2. Basic Info
======================================================================


---

## Basic Info Request Rate Limit

https://docs.bitpin.org/v1/docs/Basic%20Info/Request_Rate_Limit

اطلاعات پایهمحدودیت نرخ درخواست
محدودیت نرخ درخواست
🚦 Request Rate Limit​

نرخ درخواست‌ها در API پابلیک بیت‌پین بصورت پیشفرض محدود به 300 درخواست در دقیقه برای هر IP هست. در API های پرایوت، ریت لیمیت ها بر اساس شناسه کاربر محدود میشوند.

📈 اقدام برای نرخ درخواست بیشتر​

اگه نیاز به نرخ درخواست بیشتری داری، می‌تونی درخواستت رو به تیم پشتیبانی بیت‌پین یا پشتیبانی VIP ارسال کنی. توی این درخواست، باید دلایل و نیازهای خودت رو برای افزایش نرخ درخواست توضیح بدی.
تیم پشتیبانی بعد از بررسی، تصمیم می‌گیره که آیا نرخ درخواستت باید افزایش پیدا کنه یا نه.

اطلاعیه

حتماً یادت باشه که درخواست افزایش نرخ فقط در صورتی ممکنه تأیید بشه که دلیل منطقی داشته باشی و منابع سیستم اجازه این افزایش رو بدن.

❌ Error Responses​
{
    "detail": "Request was throttled. Expected available in 86398 seconds."
}


---

## Basic Info Connection Method

https://docs.bitpin.org/v1/docs/Basic%20Info/Connection_Method

اطلاعات پایهروش اتصال
روش اتصال
🔐 Connection Method​

برای اتصال به API بیت‌پین، حتماً باید از پروتکل HTTPS استفاده کنی.
ارتباط از طریق HTTP امن نیست و پذیرفته نمی‌شه. فقط درخواست‌های امن از طریق HTTPS مجاز هستن.
بسته به Endpoint مورد نظر، درخواست‌ها باید به‌صورت POST یا GET ارسال بشن.

هشدار

یادت باشه که همیشه از HTTPS استفاده کنی تا از امنیت و رمزنگاری درخواست‌هات مطمئن بشی.

📚 Pager: Pagination​

Pagination روشی هست که برای مدیریت داده‌های حجیم توی API بیت‌پین استفاده می‌شه تا از ارسال حجم زیادی داده توی یک پاسخ جلوگیری بشه.
توی اکثر Endpointها، می‌تونی از پارامترهای offset و limit برای مشخص کردن آی‌دی شروع و تعداد آیتم‌های نمایش داده‌شده توی هر صفحه استفاده کنی.

🔄 Parameters​
offset: شناسه‌هایی که از این مقدار ست شده کمتر باشن.
limit: حداکثر تعداد آیتم‌های دریافتی (حداکثر: 100).
💡 Example​

برای دریافت سفارشات با استفاده از pagination، می‌تونی از درخواست زیر استفاده کنی:

GET /v1/odr/orders?offset=2&limit=10


======================================================================
# 3. Request & Responses
======================================================================


---

## Request & Responses Request

https://docs.bitpin.org/v1/docs/Request_&_Responses/Request

Request & ResponsesRequest
Request
👋 Introduction​

تو این بخش، توضیحات کلی درباره‌ی ساختار درخواست‌ها و نحوه‌ی ارسالشون به API بیت‌پین رو پیدا می‌کنی. درخواست‌ها معمولاً شامل URL Endpoint، پارامترهای ورودی و هدرهای احراز هویت هستن.

🛠 Request Structure​

پارامترها می‌تونن به دو روش ارسال بشن:

Query String: برای درخواست‌های GET
Request Body: برای درخواست‌های POST

پارامترها بسته به Endpoint متفاوت هستن و برای هر Endpoint به‌طور خاص توی مستندات اون بخش توضیح داده شدن. برای مثال:

💡 Example​

توی مثال زیر، یک درخواست POST برای ثبت سفارش جدید ارسال می‌شه.

POST /v1/odr/orders

cURL
Python
curl --location --request POST 'https://api.bitpin.org/api/v1/odr/orders' \  
--header 'Authorization: Bearer YOUR_AUTH_TOKEN' \  
--header 'Content-Type: application/json' \  
--data '{
    "symbol": "USDT_IRT",
    "type": "limit",
    "side": "buy",
    "price": 50000,
    "base_amount" : 100
}'

🛠 Request Params​
Parameter	Description	Required
symbol	نام بازار (مثل USDT_IRT)	بله
type	نوع سفارش (limit یا market)	بله
side	خرید یا فروش	بله
price	قیمت سفارش	بله
base_amount	مقدار ارز پایه برای سفارش	بله
نکته

برای هر Endpoint، ممکنه پارامترهای مختلفی استفاده بشه. همیشه به مستندات Endpoint مربوطه سر بزن.


---

## Request & Responses Success Response

https://docs.bitpin.org/v1/docs/Request_&_Responses/Success_Response

Request & ResponsesSuccess Response
Success Response
👋 Introduction​

پاسخ‌های موفق از API بیت‌پین معمولاً شامل کد وضعیت HTTP 200 یا 201 هستن و داده‌های مورد انتظار توی بدنه‌ی پاسخ قرار داره.

💡 Example​

توی مثال زیر، یک پاسخ موفق از API برای یک سفارش فروخته شده رو می‌بینیم:

{  
    "id": 535179385,  
    "symbol": "PIXFI_IRT",  
    "type": "market",  
    "side": "sell",  
    "price": "1956",  
    "stop_price": null,  
    "oco_target_price": null,  
    "base_amount": "63.0",  
    "quote_amount": "123228",  
    "identifier": null,  
    "state": "closed",  
    "closed_at": "2024-07-29T14:07:34.545604+03:30",  
    "created_at": "2024-07-29T14:07:34.176795+03:30",  
    "dealed_base_amount": "63",  
    "dealed_quote_amount": "123417",  
    "req_to_cancel": false,  
    "commission": "1000"  
}  

🛠 Request Params​
Parameter	Description	Required
id	شناسه سفارش	بله
symbol	نماد بازار	بله
type	نوع سفارش	بله
side	نوع عملیات (خرید/فروش)	بله
price	قیمت سفارش	بله
created_at	زمان ثبت سفارش	بله
state	وضعیت سفارش	بله
Additional Notes​

توی پاسخ‌های موفق، شما می‌تونید تمام اطلاعات لازم رو برای پیگیری و تحلیل سفارش‌هاتون دریافت کنید. حتماً به کدهای وضعیت HTTP و داده‌های برگردانده شده دقت کنین. این اطلاعات به شما کمک می‌کنه تا تجربه‌ای بهتر و بدون مشکل از API داشته باشین. 🚀


---

## Request & Responses Error Response

https://docs.bitpin.org/v1/docs/Request_&_Responses/Error_Response

Request & ResponsesError Response
Error Response
🚨 Handling Errors​

وقتی که مشکلی توی درخواست وجود داشته باشه یا API نتونه درخواست رو پردازش کنه، یه پاسخ خطا همراه با کد وضعیت HTTP مناسب برمی‌گرده. این کدهای خطا می‌تونن شامل 400، 401، 404، یا 500 باشن.

📦 Error Data Structure​

پاسخ‌های خطا معمولاً شامل یه پیام خطا و کد خطایی هست که برای توسعه‌دهنده‌ها قابل فهم باشه. این ساختار به شما کمک می‌کنه تا سریع‌تر مشکل رو پیدا و برطرف کنین.

{  
    "detail": "Given token not valid for any token type",  
    "code": "token_not_valid",  
    "messages": [  
        {  
            "token_class": "AccessToken",  
            "token_type": "access",  
            "message": "Token is invalid or expired"  
        }  
    ]  
}  

Additional Notes​
هشدار

توجه کنین که پیام‌های خطا می‌تونن کمک زیادی به رفع سریع مشکلات کنن. همیشه به کد وضعیت و پیام خطای ارائه شده دقت کنین تا بتونین به‌درستی مشکل رو برطرف کنین.

💡 Error Response​

خطاهای معمول: خطاهایی مثل 401 (Unauthorized) معمولاً به خاطر توکن نامعتبر یا منقضی شده هستن. مطمئن بشین که توکن‌هاتون درست ارسال شدن و منقضی نشدن.

404 (Not Found): این خطا معمولاً وقتی اتفاق می‌افته که مسیر درخواستی شما وجود نداشته باشه یا به اشتباه وارد شده باشه.

500 (Internal Server Error): این خطا به خاطر مشکلات سروره. اگه به‌طور مکرر با این خطا مواجه شدین، با تیم پشتیبانی تماس بگیرین.

429 (Rate Limit): این خطا به خاطر درخواست بیش از حده و درواقع شما به ریت لیمیت خوردی.


======================================================================
# 4. Authentication
======================================================================


---

## authentication intro

https://docs.bitpin.org/v1/docs/authentication/intro

احراز هویتدریافت توکن
دریافت توکن
👋 Introduction​

توی API بیت‌پین، برای دسترسی به بعضی از مسیرها، احراز هویت ضروریه.
این بخش کمکت می‌کنه تا نحوه‌ی احراز هویت و استفاده از API Key رو به‌درستی یاد بگیری.
احراز هویت توی بیت‌پین با استفاده از توکن‌هایی که از API Key و Secret Key به دست میان، انجام می‌شه.
در اینجا شما دو نوع توکن دریافت میکنی، Refresh Token و Access Token. از Access Token برای احراز هویت درخواست ها استفاده میشه و Refresh Token برای تازه سازی و دریافت Access Token جدید استفاده میشه.

🔑 Creating API Key​

برای شروع، به وب‌سایت یا اپلیکیشن بیت‌پین برو و بعد از ورود، به بخش API سر بزن.
توی این بخش می‌تونی یه جفت API Key و Secret Key بسازی.
همچنین باید لیستی از IP‌هایی که برای ارسال درخواست‌ها استفاده می‌کنی رو مشخص کنی.
هر API Key به یک لیست IP اختصاص داده می‌شه و درخواست‌ها فقط از این IP‌ها قابل انجامه.

هشدار

حتماً دقت کن که API Key و Secret Key رو امن نگه داری و از افشاشون جلوگیری کنی.

هشدار

حتماً دقت کن که Access Token بعد از 15 دقیقه و Refresh Token بعد از 30 روز اکسپایر میشن و تاریخ انقضاشون تموم میشه.

🔗 Endpoint​
POST /api/v1/usr/authenticate/

⏱ Rate Limit​
اطلاعیه

حداکثر تعداد درخواست‌های مجاز برای ایجاد توکن برابر با 200 درخواست در روز هست.

📨 Request​

برای استفاده از API بیت‌پین، باید Token رو توی هدر درخواست ارسال کنی.
نمونه‌ای از ساختار یه درخواست با استفاده از API Key برای دریافت توکن به صورت زیره:

cURL
Python
curl --location --request POST 'https://api.bitpin.org/api/v1/usr/authenticate/' \  
--header 'Content-Type: application/json' \   
--data '{  
   "api_key":"YOUR_API_KEY",  
   "secret_key":"YOUR_SECRET_KEY"  
}'  

💬 Success Response​
{
    "refresh": "eyJ0eXAiOiJKV....kIjoyLCJpcCI6IjE3Mi4xOC4wLjEifQ.LJd44M3...-0CiH2gokd_OWGBN3UnI",
    "access": "eyJ0eXAiOiJKV1Q....JqdGkiOiI3ZmM0YWY2ZjY1N2Y0MDU5YWRlNTY3...iNjMxZSI8UpTDxOS_utTTZW36W0KgU"
}


---

## authentication token

https://docs.bitpin.org/v1/docs/authentication/token

دریافت توکن‌ها

POST /api/v1/usr/authenticate/

با استفاده این مسیر می‌توانید با ارایه‌ی کلیدهای دریافت شده در مرحله قبل یک جفت Refresh Token و Access Token دریافت کنید.

شایان ذکر است این مسیر برای هر جفت کلید تنها از IP هایی که برای آن جفت کلید تنظیم شده قابل فراخوانی است. همچنین توکن‌های دریافت شده از این طریق نیز فقط برای همان IP ها قابل استفاده خواهند بود.

آنچه به عنوان توکن احراز هویت در فراخوانی‌ها مورد نیاز است همان Access Token می‌باشد.Refresh Token و Access Token با فرمت JWT و در قالب رشته‌ی Base64 هستند. برای آشنایی با این فرمت می‌توانید به این مطلب مراجعه کنید.

این توکن ها دارای زمان انقضای مشخصی هستند.Refresh Token دارای مدت اعتبار حدودا یک هفته است. این زمان برای Access Token حدود ۱۵ دقیقه است. با Base64 Decode کردن این توکن ها می‌توان زمان دقیق انقضای توکن را با استفاده از کلید exp در قسمت Payload به دست آورد، توصیه می‌شود با در نظر گرفتن یک حاشیه اطمینان پیش از انقضا اقدام به تازه‌سازی (Refresh) کنید. در صورت انقضای Refresh Token می‌بایست با فراخوانی مجدد مسیر فوق توکن‌های جدیدی دریافت کنید.

نرخ درخواست

200 در روز

درخواست​
cURL
Python
curl --location --request POST 'https://api.bitpin.org/api/v1/usr/authenticate/' \
--header 'Content-Type: application/json' \
--data '{
    "api_key":"JAIcxdBy53.34QA6CjM3p8dxDxY815PpobcgbrFnovOZU7hyYeV",
    "secret_key":"bAIscxdBy53.34QA6CjM3p8dxDxspobcgbrfdfnovOZU7hyYwe1hnh"
}' 

پاسخ موفق​
{
    "refresh": "eyJ0eXAiOiJKV....kIjoyLCJpcCI6IjE3Mi4xOC4wLjEifQ.LJd44M3...-0CiH2gokd_OWGBN3UnI",
    "access": "eyJ0eXAiOiJKV1Q....JqdGkiOiI3ZmM0YWY2ZjY1N2Y0MDU5YWRlNTY3...iNjMxZSI8UpTDxOS_utTTZW36W0KgU"
}

پاسخ ناموفق​
{
    "detail": "اطلاعات واد شده غلط است و یا آی پی شما اجازه دسترسی ندارد"
}


---

## authentication refresh token

https://docs.bitpin.org/v1/docs/authentication/refresh_token

احراز هویتتازه‌سازی توکن
تازه‌سازی توکن
👋 Introduction​

توکن‌های احراز هویت هم یه مدت عمر دارن! بعد از اینکه مدت اعتبار Access Token تموم شد، نیاز داری که یه توکن جدید بگیری. برای این کار از مسیر زیر استفاده کن:

🔗 Endpoint​
POST /api/v1/usr/refresh_token/

⏱ Rate Limit​
اطلاعیه

حداکثر تعداد درخواست‌های مجاز برای ایجاد توکن برابر با 200 درخواست در روز هست.

📨 Request​
cURL
Python
curl --location --request POST 'https://api.bitpin.org/api/v1/usr/refresh_token/' \
--header 'Content-Type: application/json' \
--data '{
    "refresh":"eyJ0eXAiOiJKV1QiLCJhbGciOiJI...PJ3zhAoHtt6ALi-ClC9cRh6ATRzUJ4bdbZxj0"
}'

💡 Success Response​

اگه درخواستت موفق باشه، یه Access Token جدید بهت برمی‌گرده:

{  
    "access": "NEW_ACCESS_TOKEN"  
}  

🛡️ Security Tips​

حتماً احراز هویت دو مرحله‌ای رو برای حساب کاربریت فعال کن تا امنیتت بالاتر بره.
API Key و Secret Key خودت رو جایی امن نگه دار و به هیچ عنوان با کسی به اشتراک نذار.
همچنین محدودیت IP رو هم درست تنظیم کن تا امنیت بیشتری داشته باشی.


======================================================================
# 5. Market Data
======================================================================


---

## market-data currencies

https://docs.bitpin.org/v1/docs/market-data/currencies

اطلاعات بازارلیست ارزها
لیست ارزها
👋Introduction​

توی این بخش، می‌تونید لیست کاملی از ارزهایی که در بیت‌پین پشتیبانی می‌شن رو دریافت کنید. اطلاعات شامل نماد ارز، نام ارز، قابلیت معامله و دقت اعشاری برای هر ارز هست. این اطلاعات بهتون کمک می‌کنه تا بهتر با ارزهای موجود و نحوه معامله اون‌ها آشنا بشید.

🔗 Endpoint​
GET /api/v1/mkt/currencies/

⏱ Rate Limit​
اطلاعیه
بدون توکن: 10,000 درخواست در روز
با توکن: 200 درخواست در دقیقه
📨 Request​

برای دریافت لیست ارزها، می‌تونید از درخواست زیر استفاده کنید:

cURL
Python
curl --location --request GET 'https://api.bitpin.org/api/v1/mkt/currencies/'  

💬 Success Response​

اگه درخواست موفق باشه، پاسخ به شکل زیر خواهد بود:

[  
  {  
    "currency": "IRT",  
    "name": "Toman",  
    "tradable": true,  
    "precision": "0"  
  },  
  {  
    "currency": "VTHO",  
    "name": "VeThor Token",  
    "tradable": true,  
    "precision": "0"  
  }  
]  

🛠️ Response Keys​

توضیح کلیدهای پاسخ:

currency: نماد ارز
name: نام ارز
tradable: آیا این ارز قابل معامله هست یا نه
precision: دقت اعشاری برای این ارز
Additional Notes​
این اطلاعات بهتون کمک می‌کنه که ارزهای قابل معامله رو بهتر بشناسید و برای معاملات خودتون برنامه‌ریزی کنید.
برای بروزرسانی‌های روزانه یا دریافت اطلاعات جدید، می‌تونید از این Endpoint در بازه‌های زمانی مشخص استفاده کنید.


---

## market-data markets

https://docs.bitpin.org/v1/docs/market-data/markets

اطلاعات بازارلیست بازارها
لیست بازارها
👋 Introduction​

تو این بخش، می‌تونید لیست کامل بازارهای معاملاتی پشتیبانی شده در بیت‌پین رو دریافت کنید. این اطلاعات شامل نماد بازار، نام بازار، ارز پایه و ارز مبادله‌ای هست که بهتون کمک می‌کنه بازارهای مختلف رو بهتر بشناسید.

🔗 Endpoint​
GET /api/v1/mkt/markets/

⏱ Rate Limit​
اطلاعیه
بدون توکن: 10,000 درخواست در روز
با توکن: 200 درخواست در دقیقه
📨 Request​

برای دریافت لیست بازارها، می‌تونید از درخواست زیر استفاده کنید:

cURL
Python
curl --location --request GET 'https://api.bitpin.org/api/v1/mkt/markets/'  

💬 Success Response​

اگه درخواست موفق باشه، پاسخ به شکل زیر خواهد بود:

  [  
    {  
      "symbol": "BTC_IRT",  
      "name": "Bitcoin/Toman",  
      "base": "BTC",  
      "quote": "IRT",  
      "tradable": true,  
      "price_precision": 0,  
      "base_amount_precision": 8,  
      "quote_amount_precision": 0  
    }  
  ]  

🛠 Response Keys​

توضیح کلیدهای پاسخ:

symbol: نماد بازار
name: نام بازار
base: ارز پایه
quote: ارز مبادله‌ای
tradable: آیا این بازار قابل معامله هست یا نه
price_precision: دقت قیمت
base_amount_precision: دقت اعشاری مقدار ارز پایه
quote_amount_precision: دقت اعشاری مقدار ارز مبادله‌ای
اطلاعیه

قیمت (price) باید مضربی از price_increment باشه.

Additional Notes​
این اطلاعات بهتون کمک می‌کنه که بازارهای موجود رو بهتر بشناسید و با آگاهی بیشتری در این بازارها معامله کنید.
برای بروزرسانی‌های مداوم می‌تونید به صورت روزانه از این Endpoint استفاده کنید تا لیست بازارها و اطلاعات جدید رو دریافت کنید.


---

## market-data networks

https://docs.bitpin.org/v1/docs/market-data/networks

اطلاعات بازارلیست شبکه‌ها
لیست شبکه‌ها
🌟 Introduction​

این بخش به شما امکان می‌دهد لیست تمام شبکه‌های بلاک‌چین فعال و پشتیبانی شده در پلتفرم بیت‌پین را دریافت کنید. این اطلاعات برای شناسایی شبکه‌های در دسترس جهت واریز و برداشت، و همچنین دسترسی به وضعیت نگهداری (Maintenance) شبکه‌ها برای هر ارز ضروری است.

📌 ۱. لیست شبکه‌ها​

لیستی از تمام شبکه‌های بلاک‌چین فعال و پشتیبانی شده توسط پلتفرم را برمی‌گرداند.

🔗 Endpoint​
GET /api/v1/mkt/networks/


⏱ سقف درخواست‌ها​
اطلاعیه
بدون توکن: 10,000 درخواست در روز
با توکن: 200 درخواست در دقیقه
📨 درخواست​
cURL
Python
curl --location --request GET 'https://api.bitpin.org/api/v1/mkt/networks/'

🧭 فیلترهای کوئری​
پارامتر	نوع	توضیحات
code	string	فیلتر بر اساس کد شبکه (مانند TRX, ETH).
can_deposit	boolean	فیلتر شبکه‌هایی که امکان واریز دارند.
can_withdraw	boolean	فیلتر شبکه‌هایی که امکان برداشت دارند.
💬 پاسخ (موفقیت‌آمیز)​
[
    {
        "id": 1,
        "code": "BTC",
        "title": "Bitcoin",
        "title_fa": "بیت‌کوین",
        "can_deposit": true,
        "can_withdraw": true,
        "address_pattern": "^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$"
    },
    {
        "id": 2,
        "code": "TRX",
        "title": "Tron (TRC20)",
        "title_fa": "ترون",
        "can_deposit": true,
        "can_withdraw": true,
        "address_pattern": "^T[a-zA-Z0-9]{33}$"
    }
]

📝 توضیح کلیدهای پاسخ​
id: شناسه یکتا برای شبکه.
code: کد یکتا برای شناسایی شبکه.
title: عنوان انگلیسی شبکه.
title_fa: عنوان فارسی شبکه.
can_deposit: مشخص می‌کند که آیا واریز برای این شبکه فعال است یا خیر.
can_withdraw: مشخص می‌کند که آیا برداشت برای این شبکه فعال است یا خیر.
address_pattern: الگوی Regex برای اعتبارسنجی آدرس‌ها در این شبکه.
📌 ۲. شبکه‌های اختصاصی ارز​

لیست شبکه‌های موجود برای یک ارز خاص، شامل وضعیت نگهداری (Maintenance) برای واریز و برداشت را برمی‌گرداند.

🔗 Endpoint​
GET /api/v2/wlt/networks/

⏱ سقف درخواست‌ها​
اطلاعیه

۶۰ درخواست در دقیقه

📨 درخواست​
cURL
Python
curl --location --request GET 'https://api.bitpin.org/api/v2/wlt/networks/?currency_code=USDT' \
--header 'Authorization: Bearer <token>'

🧭 پارامترهای کوئری​
پارامتر	نوع	اجباری	توضیحات
currency_code	string	بله	کد ارز مورد نظر (مانند BTC, USDT).
💬 پاسخ (موفقیت‌آمیز)​
[
    {
        "network": {
            "code": "TRX",
            "title": "Tron (TRC20)",
            "title_fa": "ترون",
            "can_deposit": true,
            "can_withdraw": true,
        },
        "deposit_under_maintenance": false,
        "withdraw_under_maintenance": false
    },
    {
        "network": {
            "code": "ETH",
            "title": "Ethereum (ERC20)",
            "title_fa": "اتریوم",
            "can_deposit": true,
            "can_withdraw": true,
        },
        "deposit_under_maintenance": false,
        "withdraw_under_maintenance": true
    }
]

📝 توضیح کلیدهای پاسخ​
network: جزئیات شبکه (به بخش لیست شبکه‌ها در بالا مراجعه کنید).
deposit_under_maintenance: اگر true باشد، واریز برای این ارز در این شبکه موقتاً غیرفعال است.
withdraw_under_maintenance: اگر true باشد، برداشت برای این ارز در این شبکه موقتاً غیرفعال است.
📝 خطاها​
406 Not Acceptable: پارامتر currency_code ارسال نشده است.
404 Not Found: ارزی با کد ارائه شده یافت نشد.


---

## market-data tickers

https://docs.bitpin.org/v1/docs/market-data/tickers

اطلاعات بازارلیست قیمت‌ها
لیست قیمت‌ها
👋 Introduction​

این بخش بهت کمک می‌کنه تا لیست قیمت‌های فعلی بازارهای بیت‌پین رو به‌دست بیاری.

🔗 Endpoint​
GET /api/v1/mkt/tickers/

⏱ Rate Limit​
اطلاعیه

80 درخواست در دقیقه

📨 Request​

برای دریافت لیست قیمت‌های فعلی بازارهای بیت‌پین، از این درخواست استفاده کن:

cURL
Python
curl --location --request GET 'https://api.bitpin.org/api/v1/mkt/tickers/'  

💬 Success Response​

اگه درخواست موفق باشه، پاسخ به این شکل خواهد بود:

[  
  {  
    "symbol": "BTC_IRT",  
    "price": "3145737420",  
    "daily_change_price": -15.58,  
    "low": "3035557311",  
    "high": "3745700550",   
    "timestamp": 1722860054.189  
  }  
]  

🛠 Response Keys​

توضیح کلیدهای پاسخ:

symbol: نماد بازار
price: قیمت فعلی بازار
daily_change_price: تغییر قیمت روزانه
low: کمترین قیمت روزانه
high: بیشترین قیمت روزانه
timestamp: زمان بروزرسانی
Additional Notes​
قیمت‌های این بخش بهت کمک می‌کنه که به‌روزترین قیمت‌ها رو مشاهده کنی و تصمیم‌های مالی هوشمندانه بگیری.
با استفاده از این درخواست، می‌تونی به‌صورت مداوم به بروزرسانی‌های بازار دسترسی داشته باشی.


---

## market-data orderbook

https://docs.bitpin.org/v1/docs/market-data/orderbook

اطلاعات بازاراوردر بوک
اوردر بوک
👋 Introduction​

اوردر بوک جاییه که می‌تونید سفارش‌های باز در هر یک از بازارهای بیت‌پین رو ببینید.
این سفارشات شامل لیست سفارش‌های خرید (bids) و فروش (asks) هست.

🔗 Endpoint​
GET /api/v1/mth/orderbook/{symbol}/

⏱ Rate Limit​
اطلاعیه

60 درخواست در دقیقه

📨 Request​

برای دریافت سفارش‌های باز در هر یک از بازارهای بیت‌پین می‌تونید از این مسیر استفاده کنید. اوردر بوک شامل لیست سفارش‌های خرید (bids) و فروش (asks) است:

cURL
Python
curl --location --request GET 'https://api.bitpin.org/api/v1/mth/orderbook/{symbol}/'  

💬 Success Response​

اگه درخواست موفق باشه، پاسخ به شکل زیر خواهد بود:

{  
  "asks": [  
    ["51000", "2000.00000000"],  
    ["52000", "2000.00000000"],  
    ["52500", "1000.00000000"]  
  ],  
  "bids": [  
    ["50000", "1000.00000000"],  
    ["49500", "1000.00000000"],  
    ["49000", "1000.00000000"]  
  ]  
}  

هشدار

در هر درخواست تنها 20 ردیف از اوردر بوک پاسخ داده میشود.

🛠 Response Keys​

توضیح کلیدهای پاسخ:

asks: لیست سفارش‌های فروش
bids: لیست سفارش‌های خرید
Additional Notes​
استفاده از این مسیر بهتون کمک می‌کنه تا به‌روزترین اطلاعات سفارش‌های باز بازارها رو داشته باشید و بهترین تصمیم‌ها رو بگیرید.
با این درخواست، می‌تونید به‌طور مداوم اطلاعات دفتر سفارشات رو رصد کنید.


---

## market-data matches

https://docs.bitpin.org/v1/docs/market-data/matches

اطلاعات بازارلیست معاملات
لیست معاملات
👋 Introduction​

در این بخش می‌تونید آخرین معاملات انجام‌شده در هر بازار رو دریافت کنید.
اطلاعات شامل جزئیات قیمتی، مقدار معامله‌شده و نوع معامله (خرید یا فروش) است.

🔗 Endpoint​
GET /api/v1/mth/matches/{symbol}/

⏱ Rate Limit​
اطلاعیه

60 درخواست در دقیقه

📨 Request​

برای دریافت آخرین معاملات انجام‌شده در هر بازار، می‌تونید از این مسیر استفاده کنید. این اطلاعات شامل جزئیات قیمتی، مقدار معامله‌شده و نوع معامله (خرید یا فروش) است:

cURL
Python
curl --location --request GET 'https://api.bitpin.org/api/v1/mth/matches/{symbol}/'  

💬 Success Response​

اگه درخواست موفق باشه، پاسخ به شکل زیر خواهد بود:

[  
  {  
    "id": "73802972_73807087",  
    "price": "1019000000",  
    "base_amount": "0.01086870",  
    "quote_amount": "11075213",  
    "side": "sell"  
  },  
  {  
    "id": "73802711_73807087",  
    "price": "1019000000",  
    "base_amount": "0.00575072",  
    "quote_amount": "5859993",  
    "side": "buy"  
  }  
]  

🛠 Response Keys​

توضیح کلیدهای پاسخ:

id: شناسه معامله
price: قیمت معامله
base_amount: مقدار رمزارز پایه معامله‌شده
quote_amount: مقدار ارز مبادله‌ای معامله‌شده (USDT or IRT)
side: نوع معامله (خرید یا فروش)
Additional Notes​
با استفاده از این درخواست، می‌تونید آخرین تغییرات معاملات در بازار رو مشاهده کنید و توی معاملاتتون از اطلاعات دقیق استفاده کنید.


---

## market-data candles

https://docs.bitpin.org/v1/docs/market-data/candles

اطلاعات بازارکندل‌ها
کندل‌ها
👋 Introduction​

با استفاده از این API می‌توانید تاریخچه کندل‌های (OHLCV) هر بازار بیت‌پین را در بازه زمانی و تایم‌فریم دلخواه دریافت کنید.

این مسیر عمومی است و نیازی به توکن احراز هویت ندارد.

برای دریافت کندل‌های لحظه‌ای، به‌جای درخواست پی‌درپی به این مسیر، روی رویداد candle_update در کانال بازار وب‌سوکت Subscribe کنید.

🔗 Endpoint​
GET /api/v1/mkt/candles/

⏱ Rate Limit​
اطلاعیه

این مسیر محدودیت اختصاصی ندارد و محدودیت پیش‌فرض API عمومی روی آن اعمال می‌شود: ۳۰۰ درخواست در دقیقه به ازای هر IP. برای جزئیات بیشتر محدودیت نرخ درخواست را ببینید.

⏳ Time Format​
اطلاعیه

تمامی مقادیر زمانی در درخواست، به‌صورت Unix timestamp بر حسب ثانیه ارسال می‌شوند. در پاسخ نیز ts بر حسب ثانیه و time بر حسب میلی‌ثانیه است.

📨 Request​

برای دریافت کندل‌های یک بازار، از این درخواست استفاده کن:

cURL
Python
curl --location --request GET 'https://api.bitpin.org/api/v1/mkt/candles/?symbol=BTC_IRT&from=1735689600&to=1735776000&res=1h'

🛠 Request Params​
Parameter	Description	Type	Required	Example
symbol	نام بازار (مانند BTC_USDT یا BTC_IRT)	String	بله	BTC_IRT
from	ابتدای بازه زمانی؛ کندل‌های این زمان به بعد بازگردانده می‌شوند	Integer	بله	1735689600
to	انتهای بازه زمانی؛ کندل‌ها تا این زمان (شامل خودش) بازگردانده می‌شوند	Integer	بله	1735776000
res	تایم‌فریم کندل (پیش‌فرض: 30m)	String	خیر	1h
📊 Resolutions​

مقدار res باید یکی از موارد زیر باشد:

Value	تایم‌فریم	Value	تایم‌فریم
1m	۱ دقیقه	4h	۴ ساعت
5m	۵ دقیقه	6h	۶ ساعت
15m	۱۵ دقیقه	1d	۱ روز
30m	۳۰ دقیقه	1w	۱ هفته
1h	۱ ساعت	1M	۱ ماه
3h	۳ ساعت		
اطلاعیه

مقدار 1m با حرف کوچک به معنی یک دقیقه و مقدار 1M با حرف بزرگ به معنی یک ماه است. به بزرگ و کوچک بودن حرف دقت کنید.

هشدار

اگر مقداری خارج از جدول بالا ارسال کنید، خطایی دریافت نمی‌کنید؛ درخواست بدون اطلاع‌رسانی با تایم‌فریم پیش‌فرض 30m پاسخ داده می‌شود. بنابراین همیشه مقدار کلید resolution را در پاسخ بررسی کنید.

مقادیر عددی به سبک TradingView نیز پذیرفته می‌شوند و به مقادیر بالا تبدیل می‌گردند: عدد کوچک‌تر از ۶۰ به‌عنوان دقیقه (15 → 15m) و عدد ۶۰ یا بزرگ‌تر به‌عنوان ساعت کامل (60 → 1h و 240 → 4h) در نظر گرفته می‌شود. عددی که به یک تایم‌فریم پشتیبانی‌شده تبدیل نشود (مثلاً 120 → 2h) به 30m بازمی‌گردد.

📏 Range Limit​
اطلاعیه

در هر درخواست حداکثر ۱۰٬۰۰۰ کندل قابل دریافت است. این تعداد از روی طول بازه و تایم‌فریم تخمین زده می‌شود؛ پس برای بازه‌های طولانی‌تر باید res بزرگ‌تری انتخاب کنید. برای نمونه 1m حدود ۷ روز و 1h حدود ۴۱۶ روز را پوشش می‌دهد.

💬 Success Response​

اگر درخواست موفق باشد، پاسخ به شکل زیر خواهد بود:

[
  {
    "open": 1019000000.0,
    "close": 1020000000.0,
    "low": "1017500000",
    "high": "1023000000",
    "volume": "1.48520000",
    "ts": 1735689600.0,
    "resolution": "1h",
    "time": 1735689600000
  },
  {
    "open": 1020000000.0,
    "close": 1021500000.0,
    "low": "1019000000",
    "high": "1024000000",
    "volume": "0.93110000",
    "ts": 1735693200.0,
    "resolution": "1h",
    "time": 1735693200000
  }
]

📝 Response Keys​

کندل‌ها به ترتیب از قدیمی‌ترین به جدیدترین بازگردانده می‌شوند.

open: قیمت باز شدن کندل (عدد)
close: قیمت بسته شدن کندل (عدد)
low: کمترین قیمت کندل (رشته)
high: بیشترین قیمت کندل (رشته)
volume: حجم معامله‌شده رمزارز پایه در طول کندل (رشته)
ts: زمان باز شدن کندل، Unix timestamp بر حسب ثانیه
resolution: تایم‌فریمی که کندل واقعاً با آن ساخته شده است
time: زمان مخصوص ابزارهای نمودار، بر حسب میلی‌ثانیه. برای تایم‌فریم‌های 1m تا 6h برابر زمان باز شدن کندل است (ts × ۱۰۰۰) و برای 1d، 1w و 1M به انتهای بازه منتقل می‌شود؛ همان چیزی که کتابخانه‌های نموداری انتظار دارند.
اطلاعیه

مقادیر open و close به‌صورت عدد و مقادیر low، high و volume به‌صورت رشته بازگردانده می‌شوند. پیش از هر محاسبه‌ای، در سمت کلاینت آن‌ها را تبدیل نوع کنید.

❌ Error Responses​

درخواست بیش از ۱۰٬۰۰۰ کندل، پاسخ 400 دریافت می‌کند:

{
  "detail": "Requested 43201 candles exceeds maximum limit of 10000"
}

Additional Notes​
📭 بازار ناشناخته، بازه‌ای که کندلی برای آن ذخیره نشده، و بازاری که موقتاً معلق شده باشد، همگی به‌جای خطا یک لیست خالی [] برمی‌گردانند.
🕒 پاسخ این مسیر تا ۵ ثانیه کش می‌شود؛ بنابراین ممکن است آخرین کندل با تأخیری کوتاه نسبت به بازار به‌روزرسانی شود.


---

## market-data commissions

https://docs.bitpin.org/v1/docs/market-data/commissions

اطلاعات بازارلیست کارمزد‌ها
لیست کارمزد‌ها

نیازمند احراز هویت

👋 Introduction​

در این بخش می‌تونید لیست کارمزد‌ها برای هربازار را دریافت کنید. اطلاعات شامل کارمزد میکر و تیکر است.

🔗 Endpoint​
GET /api/v1/mkt/commissions/

⏱ Rate Limit​
اطلاعیه

1000 درخواست در روز

📨 Request​

این مسیر، کارمزد معاملات تمام بازارها را برمی‌گرداند. هر دو نوع کارمزد میکر (Maker) و تیکر (Taker) در خروجی موجود است.

cURL
Python
curl --location --request GET 'https://bitpin.org/api/v1/mkt/commissions/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1LCJhbGciOiJIUz...r0vtVKSN0sDvVhgW4rmIl8yudcqveCGM'

💬 Success Response​

اگه درخواست موفق باشه، پاسخ به شکل زیر خواهد بود:

[
  {
    "market": 1,
    "symbol": "BTC_IRT",
    "maker": 0.3,
    "taker": 0.4
  },
  {
    "market": 2,
    "symbol": "BTC_USDT",
    "maker": 0.25,
    "taker": 0.35
  }
]

🛠 Response Keys​

توضیح کلیدهای موجود در پاسخ:

market: شناسه بازار
symbol: نماد بازار
maker: کمیسیون میکر (Maker)
taker: کمیسیون تیکر (Taker)


======================================================================
# 6. Wallet
======================================================================


---

## wallet 

https://docs.bitpin.org/v1/docs/wallet/

کیف پولکیف پول
مدیریت دارایی
کیف پول

این بخش از مستندات بهت اجازه می‌ده تا میزان موجودی کیف پول خودت رو برای ارزهای مختلف مشاهده کنی.
با استفاده از این API می‌تونی موجودی ارزها رو به تفکیک مشاهده کنی و بر اساس نیازت فیلترشون کنی.

🔗 Endpoint​
GET /api/v1/wlt/wallets/

⏱ Rate Limit​
اطلاعیه

60 درخواست در دقیقه

📨 Request​

با استفاده از این درخواست و احراز هویت، موجودی کیف پول‌های خودت رو برای ارزهای مختلف بررسی کن:

cURL
Python
curl --location --request GET 'https://api.bitpin.org/api/v1/wlt/wallets/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOi...'

🛠 Request Params​

برای فیلتر کردن نتایج می‌تونی از پارامترهای زیر استفاده کنی:

Parameter	Description	Type	Required
assets	نام دارایی مثل: BTC, IRT, USDT	String	خیر
service	نام سرویس دارایی مثل: main	String	خیر
offset	شناسه‌هایی که از این مقدار کمتر باشه	Integer	خیر
limit	حداکثر تعداد شناسه‌های دریافتی (حداکثر 200)	Integer	خیر
💬 Success Response​

اگه درخواست موفقیت‌آمیز باشه، پاسخ به شکل زیر خواهد بود:

[  
   {  
     "id": 3108164,  
     "asset": "RIAL",  
     "balance": "1671.6",  
     "frozen": "0.0",  
     "service": "main"  
   },  
   {  
     "id": 3108166,  
     "asset": "CELR",  
     "balance": "5631.6",  
     "frozen": "0.0",  
     "service": "main"  
   }  
]  

📝 Response Keys​

توضیح کلیدهای پاسخ:

id: شناسه دارایی
asset: نام دارایی (رمزارز)
balance: موجودی قابل استفاده دارایی (حاصل تفاضل مقدار مسدودی از کل دارایی)
frozen: موجودی مسدود شده (درگیر در سفارشات یا تراکنش‌های تایید نشده)
service: نام سرویس (مثلاً main)
Additional Notes​
با استفاده از این API می‌تونی به‌راحتی موجودی کیف پول‌های مختلف خودت رو بررسی کنی و وضعیت مالی خودت رو به‌صورت دقیق کنترل کنی.


---

## wallet deposit

https://docs.bitpin.org/v1/docs/wallet/deposit

کیف پولواریزها
مدیریت واریز ها
👋 مقدمه​

این بخش به شما امکان می‌دهد آدرس‌های واریز خود را برای دارایی‌های دیجیتال دریافت کرده و تاریخچه واریزهای خود را مشاهده کنید. اطمینان از استفاده از شبکه صحیح و وارد کردن ممو/تگ‌های مورد نیاز برای موفقیت آمیز بودن واریزها ضروری است.

📌 ۱. دریافت آدرس واریز​

از این اندپوینت برای دریافت آدرس واریز یک ارز دیجیتال خاص در یک شبکه بلاک‌چین مشخص استفاده کنید.

🔗 Endpoint​
POST /api/v2/wlt/address/

⏱ سقف درخواست‌ها​
اطلاعیه

۶۰ درخواست در دقیقه

🧰 دسترسی‌ها​
نیازمند احراز هویت JWT
حساب کاربری باید حداقل در سطح ۱ احراز هویت شده باشد
📨 درخواست​
cURL
Python
curl --request POST 'https://api.bitpin.org/api/v2/wlt/address/' \
--header 'Authorization: Bearer <token>' \
--header 'Content-Type: application/json' \
--data-raw '{
"currency": "USDT",
"network": "ETH"
}'

📦 Body درخواست​
پارامتر	نوع	اجباری	توضیحات
currency	string	بله	کد ارز (مانند BTC, USDT).
network	string	بله	کد شبکه
💬 پاسخ (موفقیت‌آمیز)​
{
  "currency": "USDT",
  "network": 2,
  "address": "TXyz1234567890abcdefghijklmnop",
  "memo": "",
  "is_multi_format_address": false,
  "address2": ""
}

📝 توضیح کلیدهای پاسخ​
currency: کد ارز (رشته)
network: شناسه شبکه
address: آدرس اختصاصی واریز شما در این شبکه
memo: ممو/تگ (الزامی برای شبکه‌هایی مثل XRP, XLM, EOS و غیره)
is_multi_format_address: true اگر آدرس دارای چندین فرمت باشد (مثلاً legacy در مقابل segwit)
address2: فرمت آدرس جایگزین (در صورت وجود)
📌 ۲. لیست واریزها​

تاریخچه‌ای از تمام واریزهای خود، شامل دارایی‌های تومانی و رمزارزی را مشاهده کنید.

🔗 Endpoint​
GET /api/v2/wlt/deposits/

⏱ سقف درخواست‌ها​
اطلاعیه

60 درخواست در دقیقه

📨 درخواست​
cURL
Python
curl --request GET 'https://api.bitpin.org/api/v2/wlt/deposits/?currency=USDT&is_crypto=true' \
--header 'Authorization: Bearer <token>'

🧭 فیلترهای کوئری​
پارامتر	نوع	توضیحات
currency	string	فیلتر بر اساس کد ارز (حساس نبودن به حروف بزرگ/کوچک).
network	string	فیلتر بر اساس کد شبکه.
state	string	فیلتر بر اساس وضعیت واریز (مانند completed).
start	date-time	فیلتر واریزهای ایجاد شده از این تاریخ به بعد.
end	date-time	فیلتر واریزهای ایجاد شده قبل از این تاریخ.
is_crypto	boolean	اگر true باشد، فقط واریزهای رمزارزی را برمی‌گرداند.
has_network	boolean	اگر true باشد، فقط واریزهای دارای شبکه را نشان می‌دهد.
wallet_transfer	boolean	اگر true باشد، فقط انتقال های ولت را نشان می‌دهد.
identifier	string	فیلتر بر اساس شناسه یکتای واریز.

این API از پارامتر های Offset و Limit برای pagination پاسخ استفاده میکند.

💬 پاسخ (موفقیت‌آمیز)​
[
    {
      "id": 23744533,
      "has_reward": false,
      "cause": "service transfer",
      "amount": "200.00",
      "state": "succeed",
      "service": "stake",
      "wallet_transfer": true,
      "account_number": null,
      "referrer_id": "",
      "tx_hash": "",
      "tx_url": "",
      "created_at": "2026-01-03T18:02:40.151987+03:30",
      "network": null,
      "internal": true,
      "cause_fa": "انتقال بیت‌پین",
      "description": "برداشت از کیف پول اصلی بابت مشارکت در طرح کسب درآمد",
      "short_description": null,
      "deposit_method": "internal",
      "currency": "USDT"
    },
    {
      "id": 23744529,
      "has_reward": false,
      "cause": "service transfer",
      "amount": "550.00",
      "state": "succeed",
      "service": "stake",
      "wallet_transfer": true,
      "account_number": null,
      "referrer_id": "",
      "tx_hash": "",
      "tx_url": "",
      "created_at": "2026-01-03T18:02:32.990245+03:30",
      "network": null,
      "internal": true,
      "cause_fa": "انتقال بیت‌پین",
      "description": "برداشت از کیف پول اصلی بابت مشارکت در طرح کسب درآمد",
      "short_description": null,
      "deposit_method": "internal",
      "currency": "USDT"
    }
]

📝 توضیح کلیدهای پاسخ​
id: شناسه عددی داخلی.
currency: کد ارز واریز شده.
amount: مقدار خالص واریز شده.
state: وضعیت فعلی (مانند completed, pending).
network: جزئیات شبکه برای واریزهای رمزارزی.
tx_hash: هش تراکنش در شبکه بلاک‌چین.
tx_url: لینک مشاهده تراکنش در مرورگر بلاک‌چین.
created_at: زمان ثبت واریز.
⚠️ نکات مهم​
💡 ممو/تگ (Memo/Tag): همیشه برای دارایی‌هایی مثل XRP, XLM یا EOS ممو را وارد کنید. کوتاهی در این مورد می‌تواند منجر به از دست رفتن دائمی وجه شود.
💡 انتخاب شبکه: اطمینان حاصل کنید که شبکه ارسال‌کننده با شبکه آدرس واریز مطابقت داشته باشد.
💡 احراز هویت (KYC): واریزها فقط برای حساب‌هایی که مراحل اولیه احراز هویت را انجام داده‌اند پردازش می‌شوند.


---

## wallet withdraw

https://docs.bitpin.org/v1/docs/wallet/withdraw

کیف پولبرداشت‌ها
مدیریت درخواست‌های برداشت
👋 مقدمه​

این بخش به شما امکان می‌دهد درخواست‌های برداشت خود را برای دارایی‌های تومانی یا رمزارزی ایجاد کنید، تاریخچه برداشت‌های خود را مشاهده کرده و درخواست‌ها را با استفاده از رمز یک‌بارمصرف (OTP) تأیید کنید. بیت‌پین از هر دو نوع برداشت خارجی (به کیف‌پول‌های بلاک‌چین یا حساب‌های بانکی) و انتقال داخلی بین کاربران پشتیبانی می‌کند.

📌 ۱. لیست و ایجاد برداشت​

این بخش امکان پیگیری وضعیت برداشت‌های قبلی یا ایجاد درخواست جدید با استفاده از کد ارز را فراهم می‌کند.

🔗 Endpoints​
GET /api/v2/wlt/withdraws/
POST /api/v2/wlt/withdraws/

⏱ سقف درخواست‌ها​
اطلاعیه

۱۰,۰۰۰ درخواست در روز

🧰 دسترسی‌ها​
نیازمند احراز هویت JWT
حساب کاربری باید وضعیت «تأیید شده» (Accepted) داشته باشد
📥 GET - تاریخچه برداشت‌ها​

از این اندپوینت برای دریافت تاریخچه برداشت‌های خودتون استفاده کنید. پاسخ این API با offset و limit paginate میشه.

🧭 فیلترهای کوئری​
پارامتر	نوع	توضیحات
currency	string	فیلتر بر اساس کد ارز (حساس نبودن به حروف بزرگ/کوچک).
address	string	فیلتر بر اساس آدرس مقصد.
state	string	فیلتر بر اساس وضعیت (می‌تواند لیستی جدا شده با کاما باشد).
start	datetime	فیلتر برداشت‌هایی که از تاریخ مشخص‌شده یا پس از آن ایجاد شده‌اند (YYYY-MM-DD)
end	date-time	فیلتر برداشت‌هایی که تا تاریخ مشخص‌شده یا پیش از آن ایجاد شده‌اند (YYYY-MM-DD)
service	string	فیلتر بر اساس نام سرویس (مانند main، staking و غیره)
network	string	فیلتر بر اساس کد شبکه.
identifier	string	فیلتر بر اساس شناسه یکتای برداشت.
📨 نمونه درخواست​
cURL
Python
curl --request GET 'https://api.bitpin.org/api/v2/wlt/withdraws/?currency=USDT' \
--header 'Authorization: Bearer <token>'

💬 پاسخ (موفقیت‌آمیز)​
[
  {
    "identifier": "05928b2cfd8944a2a983fb5243e6b52b",
    "id": 123456789,
    "currency": "IRT",
    "amount": "9999999",
    "commission": "2000",
    "user_gain": "3706923",
    "service": "main",
    "state": "succeed",
    "destination": {
      "iban": "xxxx",
      "card": ""
    },
    "description": null,
    "short_description": null,
    "created_at": "2025-12-18T12:35:21.278411+03:30",
    "closed_at": "2025-12-18T12:38:01.141543+03:30",
    "is_partially_successful": false
  },
  {
    "identifier": "7a1fc0276dd340689ce8099bb373df8e",
    "id": 16231370,
    "currency": "BTC",
    "amount": "0.1",
    "commission": "0.0001",
    "user_gain": "0.0999",
    "service": "main",
    "state": "succeed",
    "crypto_details": {
      "address": "xxxx",
      "network": "BTC",
      "tx_hash": "",
      "tx_url": ""
    },
    "description": "withdraw on ",
    "short_description": "withdraw",
    "created_at": "2025-12-14T18:45:53.337691+03:30",
    "closed_at": "2025-12-14T18:49:02.424466+03:30",
    "is_partially_successful": false
  }
]



📝 توضیح کلیدهای پاسخ​
کلید	نوع	توضیحات
identifier	uuid	شناسه عمومی و یکتا برای برداشت
id	integer	شناسه داخلی یکتا
currency	string	کد ارز
state	string	وضعیت فعلی برداشت
amount	decimal	مقدار برداشت
commission	decimal	کارمزد کسر شده برای برداشت.
user_gain	decimal	مبلغ خالص دریافتی کاربر پس از کسر کارمزد.
created_at	date-time	زمان ثبت درخواست.
crypto_details	object (Optional)	جزئیات برداشت رمزارزی
destination	object (Optional)	جزئیات برداشت ریالی
internal	boolean	اگر true باشد، این یک انتقال داخلی است.

برای برداشت های رمزارزی، ابجکت crypto_details وجود داره که اطلاعات زیر داخلش هست:

کلید	نوع	توضیحات
network	string	کد شبکه
address	string	آدرس مقصد (کریپتو) یا شبا/کارت (تومان)
tx_hash	string	هش تراکنش (در صورت نهایی شدن)
tx_url	string	لینک تراکنش (در صورت نهایی شدن)

برای برداشت های ریالی، ابجکت destination فرستاده میشه که اطلاعات زیر رو ارائه میده:

کلید	نوع	توضیحات
iban	string	شماره شبای مقصد
card	string	شماره کارت مقصد
💸 ایجاد درخواست برداشت​

این endpoint به کاربران احراز هویت‌شده امکان می‌دهد درخواست‌های برداشت برای تومان (IRT) و ارزهای دیجیتال ایجاد کنند.

🔗 endpoint​

POST /api/v2/wlt/withdraws/

⏱ سقف درخواست‌ها​
اطلاعیه

10000 درخواست در روز

📨 درخواست​

از این endpoint برای ثبت درخواست برداشت استفاده کنید. درخواست برای برداشت تومان و ارزهای دیجیتال متفاوت است.

انتقال داخلی​

برای انتقال دارایی‌های شما (فقط رمزارز) به حساب کاربری دیگر در صرافی بیت‌پین استفاده می‌شود.

📦 نمونه درخواست​
cURL
Python
curl --request POST 'https://api.bitpin.org/api/v2/wlt/withdraws/' \
--header 'Authorization: Bearer <token>' \
--header 'Content-Type: application/json' \
--data-raw '{
"currency": "BTC",         // کد ارز مورد نظر
"amount": 0.001,
"alternative_address": "0935*****"  // شماره موبایل یا ایمیل کاربر مقصد در بیت‌پین
}'

برداشت تومان​

برای برداشت تومان به حساب بانکی یا درگاه‌های داخلی استفاده می‌شود. برای دریافت آی‌دی شماره حساب های ثبت شده خود بخش شماره حساب را مطالعه کنید.

📦 نمونه درخواست​
cURL
Python
curl --request POST 'https://api.bitpin.org/api/v2/wlt/withdraws/' \
--header 'Authorization: Bearer <token>' \
--header 'Content-Type: application/json' \
--data-raw '{
"currency": "IRT", // کد ارز تومان
"amount": 10000, // به تومان
"account_number": 123 // آی‌دی شماره حساب مقصد
}'

برداشت ارز دیجیتال​

برای برداشت ارزهای دیجیتال (مانند USDT، BTC و غیره) به کیف‌پول‌های خارجی یا آدرس‌های جایگزین استفاده می‌شود.

📦 نمونه درخواست​
cURL
Python
curl --request POST 'https://api.bitpin.org/api/v2/wlt/withdraws/' \
--header 'Authorization: Bearer <token>' \
--header 'Content-Type: application/json' \
--data-raw '{
"currency": "BTC",
"amount": 0.1,
"network": "BTC",
"address": "0x769426***"
}'

💬 پاسخ (موفقیت‌آمیز)​

اگر درخواست با موفقیت انجام شود، پاسخ به شکل زیر خواهد بود:

  {
    "identifier": "7a1fc0276dd340689ce8099bb373df8e",
    "id": 16231370,
    "currency": "BTC",
    "amount": "0.1",
    "commission": "0.0001",
    "user_gain": "0.0999",
    "service": "main",
    "state": "initial",
    "crypto_details": {
      "address": "xxxx",
      "network": "BTC",
      "tx_hash": "",
      "tx_url": ""
    },
    "description": "withdraw on ",
    "short_description": "withdraw",
    "created_at": "2025-12-14T18:45:53.337691+03:30",
    "closed_at": "2025-12-14T18:49:02.424466+03:30",
    "is_partially_successful": false,
    "is_single_otp": true
  }

📝 توضیح کلیدهای پاسخ​

پاسخ مشابه درخواست GET است، تنها کلید زیر در آن اضافه وجود دارد:

🔑 کلید	📋 توضیحات
is_single_otp	نیاز به تنها یک رمز یک‌بارمصرف برای تأیید (در صورت true بودن)
📌 ۲. تأیید با رمز یک‌بارمصرف (OTP)​

پس از ایجاد، برداشت‌ها باید با رمز یک‌بارمصرف تأیید شوند. در صورتی که بعد از ثبت درخواست برداشت، مقدار کلید is_single_otp برابر true بود، تنها نیاز به تأیید OTP اول وجود دارد. در غیر این‌صورت باید تأیید را در دو مرحله انجام دهید.

🔗 Endpoint​

POST /api/v1/wlt/withdraws/verify/otp/{id}/

⏱ سقف درخواست‌ها​
اطلاعیه

۱۰,۰۰۰ درخواست در روز

🔐 مراحل​
تأیید رمز اول (OTP1): کد شش‌رقمی برنامه Authenticator (مانند Google Authenticator) که روی حساب شما فعال است.
تأیید رمز دوم (OTP2): رمز دومی که برای شما ارسال می‌شود (در صورت نیاز با ارسال is_second_otp: true).
غیرفعال‌کردن رمز دوم

برای حذف مرحله دوم، آدرس مقصد را در دفترچه آدرس ثبت کنید و گزینه آدرس مورد اعتماد را برای آن تیک بزنید. پس از آن، برداشت‌های ارسالی به آن آدرس با is_single_otp: true ایجاد می‌شوند و تنها با تأیید OTP اول (کد Authenticator) نهایی می‌شوند.

📨 نمونه درخواست​
cURL
Python
curl --request POST 'https://api.bitpin.org/api/v1/wlt/withdraws/verify/otp/1234/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <token>' \
--data-raw '{
"otp": "123456",
"is_second_otp": false
}'

💬 پاسخ (موفقیت‌آمیز)​
{"detail": "success"}

📝 خطاهای تأیید​
کد HTTP	کد خطا	توضیحات
400	invalid_otp	رمز وارد شده اشتباه است.
400	otp1_already_verified	مرحله اول تأیید قبلاً انجام شده است.
400	extra_try	تلاش‌های ناموفق بیش از حد؛ برداشت لغو شد.
404	-	برداشت یافت نشد.
💡 نکات تکمیلی​
💡 انتقال داخلی: استفاده از alternative_address (موبایل/ایمیل) امکان انتقال آنی و بدون کارمزد را در داخل بیت‌پین فراهم می‌کند.
💡 تک مرحله‌ای: اگر is_single_otp در پاسخ ایجاد برداشت true باشد، تنها یک فراخوانی برای تأیید نیاز است. این حالت زمانی رخ می‌دهد که آدرس مقصد در دفترچه آدرس به‌عنوان آدرس مورد اعتماد ثبت شده باشد.


---

## wallet account number

https://docs.bitpin.org/v1/docs/wallet/account_number

کیف پولشماره حساب‌ها
شماره حساب‌ها

این بخش از مستندات بهت اجازه می‌ده تا شماره حساب های ثبت شدت رو مشاهده کنی و ازشون برای درخواست برداشت استفاده کنی.

🔗 Endpoint​
GET /api/v1/wlt/account_numbers/

⏱ Rate Limit​
اطلاعیه

60 درخواست در دقیقه

📨 Request​

با استفاده از این درخواست و احراز هویت، شماره حساب های خودت رو دریافت کن

cURL
Python
curl --location --request GET 'https://api.bitpin.org/api/v1/wlt/account_numbers/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOi...'

🛠 Request Params​

این API هم از پارامتر های Offset و Limit برای pagination استفاده میکنه.

💬 Success Response​

اگه درخواست موفقیت‌آمیز باشه، پاسخ به شکل زیر خواهد بود:

[
    {
      "id": 123,
      "currency": {
        "currency": "IRT",
        "name": "Toman",
        "tradable": true,
        "precision": "2"
      },
      "iban": "IR89370400440532013000",
      "card": "411111******1111",
      "value": "",
      "state": "verified"
    },
    {
      "id": 124,
      "currency": {
        "currency": "IRT",
        "name": "Toman",
        "tradable": true,
        "precision": "2"
      },
      "iban": "IR12345678901234567890",
      "card": "555555******4444",
      "value": "",
      "state": "initial"
    }
]

📝 Response Keys​

توضیح کلیدهای پاسخ:

id: شناسه شماره حساب
currency: اطلاعات مربوط به ارز
iban: شماره شبا
card: شماره کارت
state: وضعیت (initial, verified, rejected)


======================================================================
# 7. Orders
======================================================================


---

## order overview

https://docs.bitpin.org/v1/docs/order/overview

سفارشتوضیحات کلی
توضیحات کلی
👋 Introduction​

تو این بخش از مستندات، به بررسی انواع سفارشات و نحوه کار با اونا می‌پردازیم.
سفارشات می‌تونن به‌صورت خرید یا فروش و با انواع مختلفی مثل Limit، Market، Stop-Limit و OCO ثبت بشن.
این API بهت امکان مشاهده و مدیریت سفارشات خودت رو می‌ده.

اطلاعیه

با استفاده از این نوع سفارشات، می‌تونی استراتژی‌های مختلف برای مدیریت سرمایه‌گذاری و معاملات خودت پیاده کنی.
هر سفارش با توجه به نیازت و شرایط بازار انتخاب می‌شه.

انواع سفارشات​
Limit Order:
تو این نوع سفارش، قیمت خرید یا قیمت فروش رو تعیین می‌کنی.
اطلاعیه

این سفارش برای زمانی که نمی‌خوای معامله خودت رو در قیمت‌های غیرمطلوب انجام بدی مناسبه.

Market Order:
تو سفارش مارکت، قیمت محدود برای سفارش تعیین نمی‌شه و سفارش با بهترین قیمت بازار اجرا می‌شه.
اطلاعیه

سفارشات مارکت زمانی استفاده می‌شن که سرعت اجرای معامله از دقت قیمت مهم‌تره.

Stop-Limit Order:
مشخص می‌کنی که اگه قیمت بازار به یک مقدار مشخص رسید، یک سفارش Limit فعال بشه.
اطلاعیه

این نوع سفارش‌ها معمولاً برای محدود کردن زیان یا حفاظت از سود استفاده می‌شن.

OCO Order:
این سفارش ترکیبی از Limit و Stop-Limit هست و به گونه‌ای طراحی شده که یک سفارش Limit ثبت می‌شه و اگه اجرا نشد و قیمت بازار به حد تعیین‌شده رسید، سفارش اولیه لغو شده و یک سفارش جدید با قیمت ثانویه فعال می‌شه.
هشدار

OCO یک ابزار پیچیدست که نیاز به تجربه و دقت بالا در تنظیم اون داره.
استفاده صحیح ازش می‌تونه تو شرایط بازار متغیر مفید باشه.

Additional Notes​

با انتخاب درست نوع سفارشات، می‌تونی ریسک معاملات خودت رو کاهش بدی و استراتژی‌هات رو بهینه‌سازی کنی.
برای برنامه‌ریزی بهتر معاملات، به جزئیات و شرایط هر نوع سفارش توجه کن و از ابزارهای پیشرفته مثل OCO استفاده کن.


---

## order place-order intro

https://docs.bitpin.org/v1/docs/order/place-order/intro

مقدمه

در این قسمت جزییات ثبت سفارش جدید،‌ مشاهده‌ی وضعیت، لغو سفارش‌های فعال و مشاهده‌ی معاملات کاربر توضیح داده شده است. تمام فراخوانی‌های این بخش نیازمند ارایه توکن احراز هویت هستند.

تمامی درخواست های این بخش باید همراه با توکن احراز هویت باشد.

Authenticated

نرخ درخواست

18000 در ساعت

پارامترهای ورودی​
پارامتر	محتوا	نوعت داده	اجباری	مثال
symbol	نام بازار	string	بله	BTC_IRT
type	limit یا market یا stop_limit یا oco	string	بله	stop_limit
side	buy یا sell	string	بله	buy
base_amount	ارزش معامله بر اساس ارز موردمعامله	float	no	"0.0002"
quote_amount	ارزش معامله بر اساس ارز پایه موردمعامله	float	no	"100000"
price	قیمت هدف معامله	string	no	"60000.45"
stop_price	قیمت شروع معامله	string	no	"61000.45"
price_limit_oco	حد قیمت سفارش محدود ثانویه	string	no	"59000.45"
identifier	شناسه خاص دریافتی از کاربر برای تسهیل پیگیری سفارش	string	no	"myidentifier-4"
نمونه پاسخ​
{
    "id": 535179385,
    "symbol": "PIXFI_IRT",
    "type": "market",
    "side": "sell",
    "price": "1956",
    "stop_price": null,
    "price_limit_oco": null,
    "base_amount": "63.0",
    "quote_amount": "123228",
    "identifier": null,
    "state": "closed",
    "closed_at": "2024-07-29T14:07:34.545604+03:30",
    "created_at": "2024-07-29T14:07:34.176795+03:30",
    "dealed_base_amount": "63",
    "dealed_quote_amount": "123417",
    "req_to_cancel": false,
    "commission": "1000"
}


---

## order place order

https://docs.bitpin.org/v1/docs/order/place_order

سفارشثبت سفارش
ثبت سفارش
👋 Introduction​

با استفاده از این API، می‌تونی یه سفارش جدید ثبت کنی. این سفارش می‌تونه یکی از انواع سفارش‌های limit، market، stop_limit یا oco باشه.
همه‌ی درخواست‌های این بخش نیازمند ارایه توکن احراز هویت هستن. بنابراین، حتماً مطمئن شو که توکن احراز هویتت به‌درستی توی هدر درخواست قرار گرفته باشه. 🎫

🔗 Endpoint​
POST /api/v1/odr/orders/

⏱ Rate Limit​
اطلاعیه

حداکثر تعداد درخواست‌های مجاز برای ثبت سفارش برابر با 5400 درخواست در ساعت هست.

📨 Request​
cURL
Python
curl --location --request POST 'https://api.bitpin.org/api/v1/odr/orders/' \  
--header 'Authorization: Bearer YOUR_ACCESS_TOKEN' \  
--header 'Content-Type: application/json' \  
--data '{  
    "symbol": "BTC_IRT",  
    "type": "limit",  
    "side": "buy",  
    "base_amount": "0.01",  
    "quote_amount": "1000000",  
    "price": "100000000",  
    "stop_price": null,  
    "oco_target_price": null,  
    "identifier": "unique_order_id"  
}'  

💬 Success Response​
{  
    "id": 535179385,  
    "symbol": "PIXFI_IRT",  
    "type": "limit",  
    "side": "sell",  
    "price": "1956",  
    "stop_price": null,  
    "oco_target_price": null,  
    "base_amount": "63.0",  
    "quote_amount": "123228",  
    "identifier": null,  
    "state": "active",  
    "closed_at": null,  
    "created_at": "2024-07-29T14:07:34.176795+03:30",  
    "dealed_base_amount": "0",  
    "dealed_quote_amount": "0",  
    "req_to_cancel": false,  
    "commission": "1000"  
}  

🛠 Request Params​
Parameter	Description	Type	Required
symbol	نام بازار (مثل BTC_IRT)	String	بله
type	نوع سفارش (limit، market، stop_limit، oco)	String	بله
side	ساید سفارش (buy یا sell)	String	بله
base_amount	مقدار معامله بر اساس ارز پایه	Decimal	بله
quote_amount	مقدار معامله بر اساس ارز مبادله‌ای	Decimal	خیر
price	قیمت هدف معامله (فقط برای سفارش‌های limit و oco)	Decimal	خیر
stop_price	قیمت شرط شروع معامله (فقط برای سفارش‌های stop_limit و oco)	Decimal	خیر
oco_target_price	قیمت هدف در سفارش‌های oco.	Decimal	خیر
identifier	شناسه خاص سفارش برای پیگیری و جلوگیری از ثبت تکراری	String	خیر
Additional Notes​
حتماً مطمئن شو که symbol و type رو به‌درستی تنظیم کردی، چون این دو پارامتر نقش مهمی تو نوع سفارش و بازار معاملاتی دارن.
اگه از سفارش‌های oco استفاده می‌کنی، باید پارامترهای price و stop_price و oco_target_price رو دقیق تنظیم کنی تا سفارش به‌درستی اجرا بشه.
identifier یه شناسه خاصه که می‌تونی برای جلوگیری از ثبت سفارش‌های تکراری و پیگیریشون استفاده کنی. این پارامتر به‌ویژه زمانی که سیستم‌های خودکار برای ثبت سفارش استفاده می‌شن، خیلی مفیده.


---

## order place-order limit

https://docs.bitpin.org/v1/docs/order/place-order/limit

محدود

POST /api/v1/odr/orders/

درخواست​
cURL
Python
curl --location --request POST 'https/api.bitpin.org/api/v1/odr/orders/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1..N0sDvVhgW4rmIl8yudcqv2IeCGM' \
--header 'Content-Type: application/json' \
--data '{
    "symbol": "USDT_IRT",
    "type": "limit",
    "side": "buy",
    "price": 50000,
    "base_amount" : 100
}'


---

## order place-order market

https://docs.bitpin.org/v1/docs/order/place-order/market

فوری

POST /api/v1/odr/orders/

در این سفارش میتوانید هم از base_amount و هم از quote_amount استفاده کنید.

درخواست​
cURL
Python
curl --location --request POST 'https:/bitpin.org/api/v1/odr/orders/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI...9B3NcH2F_fFKn45njGgoStttMsL4' \
--header 'Content-Type: application/json' \
--data '{
    "symbol": "USDT_IRT",
    "type": "market",
    "side": "buy",
    "base_amount" : 100
}'


---

## order place-order oco

https://docs.bitpin.org/v1/docs/order/place-order/oco

OCO

POST /api/v1/odr/orders/

درخواست​
cURL
Python
curl --location --request POST 'https:/bitpin.org/api/v1/odr/orders/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI...9B3NcH2F_fFKn45njGgoStttMsL4' \
--header 'Content-Type: application/json' \
--data '{
    "symbol": "USDT_IRT",
    "type": "oco",
    "side": "buy",
    "base_amount": 100,
    "stop_price": 5000,
    "price": 49000,
    "price_limit_oco": 51000
}'


---

## order place-order stop limit

https://docs.bitpin.org/v1/docs/order/place-order/stop_limit

با حد ضرر/سود

POST /api/v1/odr/orders/

درخواست​
cURL
Python
curl --location --request POST 'https:/bitpin.org/api/v1/odr/orders/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI...9B3NcH2F_fFKn45njGgoStttMsL4' \
--header 'Content-Type: application/json' \
--data '{
    "symbol": "USDT_IRT",
    "type": "stop_limit",
    "side": "buy",
    "base_amount": 100,
    "stop_price": 5000,
    "price": 49000
}'


---

## order Order Types limit order

https://docs.bitpin.org/v1/docs/order/Order%20Types/limit_order

سفارشانواع سفارشسفارش لیمیت
سفارش لیمیت (Limit Order)
👋 Introduction​

سفارش لیمیت این امکان رو بهت می‌ده که خرید یا فروش ارز دیجیتال خودت رو با قیمتی که خودت تعیین می‌کنی انجام بدی.
این نوع سفارش فقط وقتی اجرا می‌شه که قیمت بازار به قیمت تعیین‌شده توسط تو برسه.

مثلا فرض کن می‌خوای 100 واحد تتر (USDT) رو با قیمت 62000 تومان بخری. برای این کار از سفارش لیمیت استفاده می‌کنی.

🔗 Endpoint​
POST /api/v1/odr/orders/

⏱ Rate Limit​
اطلاعیه

حداکثر تعداد درخواست‌های مجاز برای ثبت سفارش برابر با 5400 درخواست در ساعت هست.

📨 Request​
cURL
Python
curl --location --request POST 'https://api.bitpin.org/api/v1/odr/orders/' \  
--header 'Authorization: Bearer YOUR_ACCESS_TOKEN' \  
--header 'Content-Type: application/json' \  
--data '{
    "symbol": "USDT_IRT",
    "type": "limit",
    "side": "buy",
    "price": 62000,
    "base_amount": 100
}'

🛠 Request Params​
Parameter	Description	Type	Required	Example
symbol	نام بازار (مثل USDT_IRT)	String	بله	USDT_IRT
type	نوع سفارش (limit)	String	بله	limit
side	ساید سفارش (buy یا sell)	String	بله	buy
price	قیمت پیشنهادی برای خرید یا فروش	Integer	بله	62000
base_amount	مقدار رمزارز برای خرید یا فروش	Integer	بله	100
💬 Success Response​
{
        "symbol": "USDT_IRT",  
        "type": "limit",  
        "side": "buy",  
        "base_amount": "100",  
        "quote_amount": "6200000",  
        "price": "62000",  
        "stop_price": null,  
        "oco_target_price": null,  
        "identifier": "716848bc-3f15-4b28-b113-0ce8dc621eff",  
        "state": "active",  
        "created_at": "2024-06-15T10:00:00.000000+03:30",  
        "closed_at": null,  
        "dealed_base_amount": "0",  
        "dealed_quote_amount": "0",  
        "req_to_cancel": false,  
        "commission": "0.5"  
}

Additional Notes​
حتماً مطمئن شو که symbol و type رو درست انتخاب کردی، چون اینا تعیین می‌کنن که سفارش‌ت تو کدوم بازار و به چه نوعی ثبت بشه.
identifier خیلی مفیده اگه بخوای سفارش‌هات رو پیگیری کنی یا از ثبت سفارش‌های تکراری جلوگیری کنی.
اگه قیمت بازار به حد تعیین‌شده نرسه، سفارش‌ت فعال باقی می‌مونه تا وقتی که یا قیمت به حد برسه یا خودت سفارش رو لغو کنی.


---

## order Order Types market

https://docs.bitpin.org/v1/docs/order/Order%20Types/market

سفارشانواع سفارشسفارش مارکت
سفارش مارکت (Market Order)
👋 Introduction​

سفارش مارکت بهت این امکان رو می‌ده تا بلافاصله و با بهترین قیمت موجود در بازار، خرید یا فروش خودت رو انجام بدی.
این نوع سفارش بهت اجازه می‌ده که از تغییرات سریع بازار بهره‌برداری کنی، چون سفارش‌ت فوراً با بهترین قیمت فعلی بازار تکمیل می‌شه.

مثال کاربردی:​

فرض کن می‌خوای 100 واحد از رمزارز تتر (USDT) رو به قیمت بازار بخری. تو این نوع سفارش نیازی به تعیین قیمت نداری و سفارش‌ت به‌سرعت و با بهترین قیمت موجود در بازار تکمیل می‌شه.

🔗 Endpoint​
POST /api/v1/odr/orders/

⏱ Rate Limit​
اطلاعیه

حداکثر تعداد درخواست‌های مجاز برای ثبت سفارش برابر با 5400 درخواست در ساعت هست.

📨 Request​
cURL
Python
curl --location --request POST 'https://api.bitpin.org/api/v1/odr/orders/' \  
--header 'Authorization: Bearer YOUR_ACCESS_TOKEN' \  
--header 'Content-Type: application/json' \  
--data '{
    "symbol": "USDT_IRT",
    "type": "market",
    "side": "buy",
    "base_amount": 100
}'

🛠 Request Params​
Parameter	Description	Type	Required	Example
symbol	نام بازار (مثل USDT_IRT)	String	بله	USDT_IRT
type	نوع سفارش (market)	String	بله	market
side	ساید سفارش (buy یا sell)	String	بله	buy
base_amount	مقدار رمزارز برای خرید یا فروش	Integer	خیر	100
quote_amount	مقدار تومانی یا تتری برای خرید یا فروش	Integer	خیر	100
هشدار

در سفارش مارکت میتونی base_amount و یا quote_amount رو وارد کنی. ولی دقت کن که فقط یکیشو میتونی بفرستی. اگر هر دو رو بفرستی، بصورت پیشفرض base_amount مورد قبول سیستم قرار میگیره.

Additional Notes​
تو سفارش مارکت می‌تونی به جای تعیین مقدار ارز پایه (base_amount)، مقدار ارز مرجع (quote_amount) رو هم تعیین کنی تا بر اساس اون معامله انجام بشه.
سفارش بازار برای کسایی مناسبه که می‌خوان سریع معامله کنن و از نوسانات بازار بهره‌برداری کنن.


---

## order Order Types oco

https://docs.bitpin.org/v1/docs/order/Order%20Types/oco

سفارشانواع سفارشسفارش OCO
سفارش OCO
👋 Introduction​

فرض کن می‌خوای یه سفارش OCO ثبت کنی. این سفارش ترکیبی از سفارش لیمیت و استاپ لیمیت هست.
تو این نوع سفارش، دو سفارش به‌طور همزمان تو بازار قرار می‌گیرن؛ اگه یکی از اونا انجام بشه، اون یکی به‌صورت خودکار لغو می‌شه. این نوع سفارش برای مدیریت همزمان خرید و فروش تو بازار خیلی مفیده.

مثال کاربردی:​

فرض کن 1 بیت کوین داری و میخوایی وقتی رسید به قیمت 70000 دلار بفروشی. ولی اگر قیمت ریخت تا 58000 دلار، برای جلوگیری از ضرر بیشتر روی قیمت 57990 بیت کوین ها رو بفروش.

🔗 Endpoint​
POST /api/v1/odr/orders/

⏱ Rate Limit​
اطلاعیه

حداکثر تعداد درخواست‌های مجاز برای ثبت سفارش برابر با 5400 درخواست در ساعت هست.

📨 Request​
cURL
Python
curl --location --request POST 'https://api.bitpin.org/api/v1/odr/orders/' \  
--header 'Authorization: Bearer YOUR_ACCESS_TOKEN' \  
--header 'Content-Type: application/json' \  
--data '{
    "symbol": "BTC_USDT",
    "type": "oco",
    "side": "sell",
    "base_amount": 1,
    "oco_target_price": 70000
    "stop_price": 58000,
    "price": 57990,
}'

🛠 Request Params​
Parameter	Description	Type	Required	Example
symbol	نام بازار (مثل USDT_IRT)	String	بله	USDT_IRT
type	نوع سفارش (oco)	String	بله	oco
side	ساید سفارش (buy یا sell)	String	بله	buy
oco_target_price	قیمت هدف	Integer	بله	70000
stop_price	قیمت استاپ	Integer	بله	58000
price	قیمت سفارش لیمیت اولیه	Integer	بله	57990
base_amount	مقدار رمزارز برای خرید یا فروش	Integer	بله	100
Additional Notes​
سفارش OCO بهت این امکان رو می‌ده که دو هدف رو همزمان دنبال کنی؛ اگه یکی از سفارش‌ها فعال بشه، دیگری به‌صورت خودکار لغو می‌شه.
قیمت استاپ و قیمت سفارش لیمیت باید به دقت تنظیم بشن تا سفارش‌های شما به‌درستی اجرا بشن.


---

## order Order Types stop limit order

https://docs.bitpin.org/v1/docs/order/Order%20Types/stop_limit_order

سفارشانواع سفارشسفارش استاپ لیمیت
سفارش استاپ لیمیت (Stop Limit Order)
👋 Introduction​

سفارش استاپ لیمیت یک ترکیب از سفارش استاپ و سفارش لیمیت است. در این نوع سفارش، شما قیمتی رو به‌عنوان "قیمت توقف" تعیین می‌کنی که با رسیدن قیمت بازار به اون، سفارش لیمیت فعال می‌شه.
این سفارش برای محافظت از ضررهای احتمالی یا کسب سود از نوسانات بازار بسیار مفیده.

مثال کاربردی:​

فرض کن می‌خوای 100 واحد از رمزارز تتر (USDT) رو زمانی خریداری کنی که قیمت اون از 62000 تومان عبور کنه و با قیمت 61900 تومان خریداری بشه.

🔗 Endpoint​
POST /api/v1/odr/orders/

⏱ Rate Limit​
اطلاعیه

حداکثر تعداد درخواست‌های مجاز برای ثبت سفارش برابر با 5400 درخواست در ساعت هست.

📨 Request​
cURL
Python
curl --location --request POST 'https://api.bitpin.org/api/v1/odr/orders/' \  
--header 'Authorization: Bearer YOUR_ACCESS_TOKEN' \  
--header 'Content-Type: application/json' \  
--data '{
    "symbol": "USDT_IRT",
    "type": "stop_limit",
    "side": "buy",
    "base_amount": 100,
    "stop_price": 62000,
    "price": 61900
}'

🛠 Request Params​
Parameter	Description	Type	Required	Example
symbol	نام بازار (مثل USDT_IRT)	String	بله	USDT_IRT
type	نوع سفارش (stop_limit)	String	بله	stop_limit
side	ساید سفارش (buy یا sell)	String	بله	buy
stop_price	قیمت استاپ	Integer	بله	62000
price	قیمت سفارش پس از فعال شدن	Integer	بله	61900
base_amount	مقدار رمزارز برای خرید یا فروش	Integer	بله	100
Additional Notes​
سفارش استاپ لیمیت برای محافظت از سرمایه در بازارهای ناپایدار بسیار مفیده.
قیمت استاپ باید به‌گونه‌ای تعیین بشه که با رسیدن بازار به اون، سفارش شما فعال شده و با قیمت لیمیت تعیین‌شده تکمیل بشه.


---

## order cancel

https://docs.bitpin.org/v1/docs/order/cancel

سفارشلغو سفارش با شناسه
لغو سفارش با شناسه
👋 Introduction​

با فراخوانی این مسیر می‌تونی یه سفارش خاص خودت رو با استفاده از شناسه‌اش لغو کنی.

🔗 Endpoint​
DELETE /api/v1/odr/orders/{order_id}/

⏱ Rate Limit​
اطلاعیه

حداکثر تعداد درخواست‌های مجاز برای لغو سفارش برابر با 5400 درخواست در ساعت هست.

📨 Request Example​
cURL
Python
curl --location --request DELETE 'https://api.bitpin.org/api/v1/odr/orders/{order_id}/' \  
--header 'Authorization: Bearer YOUR_ACCESS_TOKEN'

اطلاعیه

حتماً مطمئن شو که شناسه‌ی سفارش (order_id) رو به درستی وارد کردی. این شناسه باید به سفارشی که می‌خوای لغو کنی، اختصاص داشته باشه.

💬 Responses​
اگه درخواست موفق باشه، کد 204 No Content برگردونده می‌شه که به معنی لغو موفقیت‌آمیز سفارشه.
اگه درخواست ناموفق باشه، کد 406 Not Acceptable برگردونده می‌شه که نشون می‌ده درخواست لغو با مشکل مواجه شده.
❌ Error Responses​
{
    "detail": "not allowed"
}

اخطار
کد 406: درخواست غیر قابل قبول.


---

## order cancel-identifier

https://docs.bitpin.org/v1/docs/order/cancel-identifier

سفارشلغو سفارش با شناسه خاص
لغو سفارش با شناسه خاص
👋 Introduction​

با فراخوانی این مسیر می‌تونی یه سفارش خودت رو با استفاده از شناسه‌ای که خودت برامون فرستادی لغو کنی.

🔗 Endpoint​
DELETE /api/v1/odr/orders/identifier/{order_identifier}/

⏱ Rate Limit​
اطلاعیه

حداکثر تعداد درخواست‌های مجاز برای لغو سفارش برابر با 18000 درخواست در ساعت هست.

📨 Request Example​
cURL
Python
curl --location --request DELETE 'https://api.bitpin.org/api/v1/odr/orders/identifier/{order_identifier}/' \  
--header 'Authorization: Bearer YOUR_ACCESS_TOKEN'

اطلاعیه

حتماً مطمئن شو که شناسه‌ی سفارش (order_identifier) رو به درستی وارد کردی. این شناسه باید به سفارشی که می‌خوای لغو کنی، اختصاص داشته باشه.

💬 Responses​
اگه درخواست موفق باشه، کد 204 No Content برگردونده می‌شه که به معنی لغو موفقیت‌آمیز سفارشه.
اگه درخواست ناموفق باشه، کد 406 Not Acceptable برگردونده می‌شه که نشون می‌ده درخواست لغو با مشکل مواجه شده.
❌ Error Responses​
{
    "detail": "not allowed"
}

اخطار
کد 406: درخواست غیر قابل قبول.


---

## order get order list

https://docs.bitpin.org/v1/docs/order/get_order_list

سفارشدریافت لیست سفارشات
دریافت لیست سفارشات

با استفاده از این API، می‌تونی لیست سفارشات خودت رو دریافت و بررسی کنی.

نگهداری سفارش‌ها

این API تنها موارد زیر را بازمی‌گرداند:

تمامی سفارش‌های Active
تمامی سفارش‌های Closed مربوط به ۷ روز اخیر، شامل سفارش‌های پرشده، نیمه‌پرشده و کاملاً کنسل‌شده

سفارش‌های Closed پس از گذشت ۷ روز از این API حذف می‌شوند. سفارش‌هایی که حداقل یک Match داشته باشند به API دریافت تاریخچه سفارشات منتقل می‌شوند. سفارش‌هایی که بدون هیچ Match به‌صورت کامل Cancel شده‌اند به تاریخچه منتقل نمی‌شوند و پس از ۷ روز به‌طور کامل حذف می‌شوند.

این API همچنان منبع Real-time سفارش‌های کاربر است؛ بنابراین برای پیگیری سفارش‌های Active و تمامی سفارش‌های Closed تا ۷ روز پس از بسته شدن، می‌توانید از همین API استفاده کنید.

سفارشی که حداقل یک Match داشته باشد و کمتر از ۷ روز از بسته شدن آن گذشته باشد، در این بازه از هر دو API قابل دریافت است. پس از ۷ روز، تنها از طریق دریافت تاریخچه سفارشات قابل دریافت خواهد بود.

🔗 Endpoint​
GET /api/v1/odr/orders/

⏱ Rate Limit​
اطلاعیه

حداکثر تعداد درخواست‌های مجاز برای دریافت لیست سفارش برابر با 80 درخواست در دقیقه هست.

📨 Request​
cURL
Python
curl --location --request GET 'https://api.bitpin.org/api/v1/odr/orders/' \  
--header 'Authorization: Bearer eyJ0eXAiOiJ...M9B3NcH2F_fFKn45njGgoStttMsL4'  

🛠 Request Params​
Parameter	Description	Type	Required	Example
symbol	نام بازار (مثل BTC_IRT)	String	خیر	BTC_IRT
side	نوع سفارش (خرید: buy یا فروش: sell)	Array[String]	خیر	buy,sell
state	وضعیت سفارش (initial، active، closed)	Array[String]	خیر	active,closed
type	نوع سفارش (limit، market، stop_limit، oco)	Array[String]	خیر	limit،market
identifier	شناسه خاص سفارش برای پیگیری یا جلوگیری از ثبت تکراری	String	خیر	abc123
start	سفارش‌هایی که بعد از این زمان ساخته شده‌اند رو نمایش می‌ده	Date	خیر	2024-07-15
end	سفارش‌هایی که قبل از این زمان ساخته شده‌اند رو نمایش می‌ده	Date	خیر	2024-07-15
ids_in	لیستی از شناسه‌های سفارش‌ها که می‌خوای نمایش داده بشن	Array[String]	خیر	1,2,3
identifiers_in	لیستی از شناسه‌های خاص سفارش‌ها برای فیلتر کردن نتایج	Array[String]	خیر	xyz1,xyz2
offset	سفارش‌هایی که شناسه‌شون کمتر از این مقداره رو نمایش بده	Integer	خیر	608612655
limit	حداکثر تعداد سفارش‌های دریافتی (حداکثر: 100)	Integer	خیر	50
💬 Success Response​
[  
    {  
        "id": 1,  
        "symbol": "USDT_IRT",  
        "type": "limit",  
        "side": "buy",  
        "base_amount": "0.02",  
        "quote_amount": "1000",  
        "price": "50000",  
        "stop_price": null,  
        "oco_target_price": null,  
        "identifier": "716848bc-3f15-4b28-b113-0ce8dc621eff",  
        "state": "active",  
        "created_at": "2024-06-15T10:00:00.000000+03:30",  
        "closed_at": null,  
        "dealed_base_amount": "0",  
        "dealed_quote_amount": "0",  
        "req_to_cancel": false,  
        "commission": "0.5"  
    }  
]  

📝 Response Keys​
symbol: نام بازار که با _ جدا شده (مثل BTC_IRT).
type: نوع سفارش که شامل یکی از موارد limit، market، stop_limit، oco می‌شه.
side: نوع عملیات سفارش: buy برای خرید و sell برای فروش.
base_amount: مقدار رمزارز پایه معامله شده (cryptocurrency) مثلاً در بازار بیت‌کوین به تومان، اگه 0.001 بیت‌کوین خریداری کردی، این مقدار برابر "0.001" می‌شه.
quote_amount: مقدار ارز مبادله‌ای معامله شده (USDT or IRT) مثلاً در بازار بیت‌کوین به تومان، اگه سفارشی به ارزش یک میلیارد تومان داشته باشی، این مقدار برابر "1000000000" می‌شه.
price: قیمت سفارش. در سفارش‌های limit و stop_limit و oco.
stop_price: قیمت فعال‌سازی سفارش در سفارش‌های stop_limit و oco.
oco_target_price: قیمت هدف در سفارش‌های oco.
identifier: شناسه خاص سفارش که برای جلوگیری از ثبت سفارش‌های تکراری و پیگیری استفاده می‌شه.
state: وضعیت سفارش که می‌تونه یکی از حالت‌های initial، active، closed باشه.
req_to_cancel: اگه کاربر درخواست لغو سفارش رو ثبت کرده باشه، این مقدار true می‌شه.
created_at: زمان ثبت سفارش به صورت timezone aware.
closed_at: زمان بسته شدن سفارش به صورت timezone aware.
dealed_base_amount: مقدار رمزارز پایه معامله شده در طول سفارش. این مقدار با تکمیل سفارش افزایش پیدا می‌کنه.
dealed_quote_amount: مقدار ارز مبادله‌ای معامله شده در طول سفارش.
commission: مقدار کارمزدی که در طول اجرای سفارش پرداخت شده.
Additional Notes​

🌍 با استفاده از این API، می‌تونی به سادگی تمام سفارشاتت رو مدیریت کنی و به تفصیل بررسی کنی. این امر بهت امکان می‌ده تا به راحتی تاریخچه سفارشاتت رو مرور و آنالیز کنی و بر اساس داده‌ها، تصمیمات بهتری بگیری.


---

## order get order by id

https://docs.bitpin.org/v1/docs/order/get_order_by_id

سفارشدریافت سفارش با شناسه
دریافت سفارش با شناسه

با استفاده از این API، می‌تونی یه سفارش خاص ثبت‌شده رو بر اساس شناسه سفارش ببینی.

اطلاعیه

برای استفاده از این API، حتماً باید شناسه سفارش (order ID) ثبت‌شده برای سفارش رو توی درخواستت ارسال کنی.

اطلاعیه

برای دریافت چند سفارش با شناسه سفارش (order ID) یا شناسه خاص (identifier) ثبت‌شده می‌تونی از پارامتر ids_in و identifiers_in در لیست سفارشات استفاده کنی

🔗 Endpoint​
GET /api/v1/odr/orders/{order_id}/

⏱ Rate Limit​
اطلاعیه

حداکثر تعداد درخواست‌های مجاز برای دریافت یک سفارش برابر با 80 درخواست در دقیقه هست.

هشدار

مجموع درخواست های دریافت لیست سفارش و یا دریافت یک سفارش، در مجموع برابر با 80 درخواست در دقیقه هست.

📨 Request​
cURL
Python
curl --location --request GET 'https://api.bitpin.org/api/v1/odr/orders/12345/' \  
--header 'Authorization: Bearer eyJ0eXAiOiJ...M9B3NcH2F_fFKn45njGgoStttMsL4'  

💬 Success Response​
{  
    "id": 12345,  
    "symbol": "USDT_IRT",  
    "type": "limit",  
    "side": "buy",  
    "base_amount": "0.02",  
    "quote_amount": "1000",  
    "price": "50000",  
    "stop_price": null,  
    "oco_target_price": null,  
    "identifier": "716848bc-3f15-4b28-b113-0ce8dc621eff",  
    "state": "active",  
    "created_at": "2024-06-15T10:00:00.000000+03:30",  
    "closed_at": null,  
    "dealed_base_amount": "0",  
    "dealed_quote_amount": "0",  
    "req_to_cancel": false,  
    "commission": "0.5"  
}  

📝 Response Keys​
symbol: نام بازار که با _ جدا شده (مثل BTC_IRT).
type: نوع سفارش که شامل یکی از موارد limit، market، stop_limit، oco می‌شه.
side: نوع عملیات سفارش: buy برای خرید و sell برای فروش.
base_amount: مقدار رمزارز پایه معامله شده (cryptocurrency) مثلاً در بازار بیت‌کوین به تومان، اگه 0.001 بیت‌کوین خریداری کردی، این مقدار برابر "0.001" می‌شه.
quote_amount: مقدار ارز مبادله‌ای معامله شده (USDT or IRT) مثلاً در بازار بیت‌کوین به تومان، اگه سفارشی به ارزش یک میلیارد تومان داشته باشی، این مقدار برابر "1000000000" می‌شه.
price: قیمت سفارش. در سفارش‌های limit و stop_limit و oco.
stop_price: قیمت فعال‌سازی سفارش در سفارش‌های stop_limit و oco.
oco_target_price: قیمت هدف در سفارش‌های oco.
identifier: شناسه خاص سفارش که برای جلوگیری از ثبت سفارش‌های تکراری و پیگیری استفاده می‌شه.
state: وضعیت سفارش که می‌تونه یکی از حالت‌های initial، active، closed باشه.
req_to_cancel: اگه کاربر درخواست لغو سفارش رو ثبت کرده باشه، این مقدار true می‌شه.
created_at: زمان ثبت سفارش به صورت timezone aware.
closed_at: زمان بسته شدن سفارش به صورت timezone aware.
dealed_base_amount: مقدار رمزارز پایه معامله شده در طول سفارش. این مقدار با تکمیل سفارش افزایش پیدا می‌کنه.
dealed_quote_amount: مقدار ارز مبادله‌ای معامله شده در طول سفارش.
commission: مقدار کارمزدی که در طول اجرای سفارش پرداخت شده.


---

## order order history

https://docs.bitpin.org/v1/docs/order/order_history

سفارشدریافت تاریخچه سفارشات
دریافت تاریخچه سفارشات
👋 Introduction​

با استفاده از این API می‌توانید تاریخچه سفارش‌های بسته‌شده (Closed) خود را به ترتیب از جدیدترین به قدیمی‌ترین دریافت کنید.

تنها سفارش‌هایی در این تاریخچه نگهداری می‌شوند که حداقل یک Match داشته باشند. سفارش‌هایی که بدون هیچ Match به‌صورت کامل Cancel شده‌اند به این API منتقل نمی‌شوند؛ این سفارش‌ها تا ۷ روز پس از بسته شدن در لیست سفارشات در دسترس هستند و پس از آن به‌طور کامل حذف می‌شوند.

انتقال سفارش‌ها به این API به‌صورت Asynchronous انجام می‌شود؛ بنابراین ممکن است یک سفارش با تأخیری کوتاه پس از بسته شدن در این مسیر قابل مشاهده باشد.

تمامی درخواست‌های این بخش نیازمند ارائه توکن احراز هویت هستند؛ بنابراین اطمینان حاصل کنید که توکن احراز هویت به‌درستی در هدر درخواست قرار گرفته باشد. 🎫

🔗 Endpoint​
GET /api/v1/odr/order_history/

⏱ Rate Limit​
اطلاعیه

حداکثر تعداد درخواست‌های مجاز برای دریافت تاریخچه سفارشات برابر با ۵ درخواست در ثانیه به ازای هر کاربر است. در صورت عبور از این حد، پاسخ 429 دریافت خواهید کرد.

⏳ Time Format​
اطلاعیه

تمامی مقادیر زمانی در این API، هم در درخواست و هم در پاسخ، به‌صورت Unix timestamp بر حسب میلی‌ثانیه ارائه می‌شوند و برخلاف سایر API‌های سفارش، به‌صورت timezone aware نیستند.

📨 Request​
curl --location --request GET 'https://api.bitpin.org/api/v1/odr/order_history/?symbol=USDT_IRT&side=sell&limit=50' \  
--header 'Authorization: Bearer YOUR_ACCESS_TOKEN'

🛠 Request Params​
Parameter	Description	Type	Required	Example
start	سفارش‌هایی که از این زمان به بعد ایجاد شده‌اند را نمایش می‌دهد (پیش‌فرض: یک ماه پیش از end)	Integer	خیر	1785159993973
end	سفارش‌هایی که پیش از این زمان ایجاد شده‌اند را نمایش می‌دهد (پیش‌فرض: زمان حال)	Integer	خیر	1785159994620
limit	حداکثر تعداد سفارش‌های دریافتی در هر صفحه (بین ۱ تا ۲۰۰، پیش‌فرض: ۵۰)	Integer	خیر	50
cursor	مقدار next_cursor دریافت‌شده از پاسخ قبلی. با ارسال این پارامتر، مقادیر start و end نادیده گرفته می‌شوند	String	خیر	eyJzIjoxNzY3...
symbol	نام بازار (مانند BTC_USDT یا BTC_IRT)	String	خیر	BTC_IRT
side	نوع سفارش (خرید: buy یا فروش: sell)	String	خیر	sell
order_type	نوع سفارش (limit، market، stop_limit، oco)	String	خیر	limit
اطلاعیه

بازه زمانی درخواستی نمی‌تواند بیش از ۳ ماه باشد و مقدار start باید پیش از end باشد؛ در غیر این صورت پاسخ 400 دریافت خواهید کرد.

اطلاعیه

فیلترها در cursor ذخیره نمی‌شوند. هنگام درخواست صفحه بعد، پارامترهای symbol، side، order_type و limit را مجدداً به همراه cursor ارسال کنید؛ در غیر این صورت صفحه بعد بدون اعمال فیلتر بازگردانده می‌شود.
مقادیر خالی مانند side= یا symbol= نیز به‌منزله ارسال‌نشدن پارامتر در نظر گرفته می‌شوند.

📄 Pagination​

این API به‌جای شماره صفحه، از روش cursor based برای صفحه‌بندی استفاده می‌کند.

۱. درخواست نخست را به همراه فیلترهای موردنظر و در صورت نیاز پارامترهای start و end ارسال کنید.
۲. تا زمانی که مقدار has_next برابر true است، درخواست بعدی را با مقدار next_cursor در پارامتر cursor و به همراه همان فیلترها ارسال کنید.
۳. این روند را تا زمانی که مقدار has_next برابر false شود ادامه دهید.

curl --location --request GET 'https://api.bitpin.org/api/v1/odr/order_history/?cursor=eyJzIjoxNzY3MjI1NjAwMDAwLCJ...&symbol=USDT_IRT&side=sell&limit=50' \  
--header 'Authorization: Bearer YOUR_ACCESS_TOKEN'

💬 Success Response​
{
    "results": [
        {
            "id": 2554860873,
            "wallet_group_id": null,
            "service": "main",
            "market_id": 5,
            "symbol": "USDT_IRT",
            "base_currency": "USDT",
            "quote_currency": "IRT",
            "identifier": null,
            "side": "sell",
            "type": "market",
            "base_amount": "1.00",
            "quote_amount": "190989",
            "dealed_base_amount": "1.00",
            "dealed_quote_amount": "190951",
            "commission": "0.0000",
            "price": "0",
            "stop_price": null,
            "oco_target_price": null,
            "activation_price": "0",
            "average_price": "190951",
            "fulfilled": 1.0,
            "activated_oco_type": "",
            "created_at": 1785159993973,
            "activated_at": 1785159993924,
            "req_to_cancel_at": null,
            "closed_at": 1785159994620
        }
    ],
    "next_cursor": "eyJzIjoxNzY3MjI1NjAwMDAwLCJlIjoxNzY5OTA0MDAwMDAwLCJjIjoiMjAyNi0wMS0wNVQwMDowMDowMCswMDowMCIsImkiOjJ9",
    "has_next": true
}

📝 Response Keys​
results: فهرست سفارش‌های این صفحه، به ترتیب از جدیدترین به قدیمی‌ترین.
next_cursor: مقداری که برای دریافت صفحه بعد باید در پارامتر cursor ارسال شود.
has_next: مشخص می‌کند صفحه بعدی وجود دارد یا خیر (true یا false).
آبجکت سفارش​
id: شناسه سفارش.
wallet_group_id: گروه کیف پول مرتبط با سفارش، در صورت وجود.
service: سرویسی که سفارش از طریق آن ثبت شده است (مانند main).
market_id: شناسه عددی بازار.
symbol: نام بازار که با _ جدا شده است (مانند USDT_IRT).
base_currency: ارز پایه بازار (مانند USDT).
quote_currency: ارز مبادله‌ای بازار (مانند IRT).
identifier: شناسه خاص سفارش که هنگام ثبت سفارش تعیین شده است، در صورت وجود.
side: نوع عملیات سفارش: buy برای خرید و sell برای فروش.
type: نوع سفارش که شامل یکی از موارد limit، market، stop_limit یا oco می‌شود.
base_amount: مقدار درخواست‌شده از رمزارز پایه.
quote_amount: مقدار درخواست‌شده از ارز مبادله‌ای.
dealed_base_amount: مقدار رمزارز پایه معامله‌شده در طول سفارش.
dealed_quote_amount: مقدار ارز مبادله‌ای معامله‌شده در طول سفارش.
commission: مقدار کارمزد پرداخت‌شده در طول اجرای سفارش.
price: قیمت سفارش، که در سفارش‌های limit، stop_limit و oco تعیین می‌شود.
stop_price: قیمت فعال‌سازی سفارش در سفارش‌های stop_limit و oco.
oco_target_price: قیمت هدف در سفارش‌های oco.
activation_price: قیمتی که سفارش در آن فعال شده است.
average_price: میانگین قیمت اجرای سفارش در تمامی Match‌های آن.
fulfilled: میزان اجرای سفارش، عددی بین 0 و 1 که مقدار 1.0 به معنای تکمیل کامل سفارش است.
activated_oco_type: در سفارش‌های oco مشخص می‌کند کدام سمت فعال شده است. برای سایر انواع سفارش، مقدار آن رشته خالی است.
created_at: زمان ثبت سفارش، به‌صورت Unix timestamp بر حسب میلی‌ثانیه.
activated_at: زمان فعال شدن سفارش، به‌صورت Unix timestamp بر حسب میلی‌ثانیه.
req_to_cancel_at: زمان ثبت درخواست لغو توسط کاربر، به‌صورت Unix timestamp بر حسب میلی‌ثانیه. در صورتی که درخواست لغوی ثبت نشده باشد، مقدار آن null است.
closed_at: زمان بسته شدن سفارش، به‌صورت Unix timestamp بر حسب میلی‌ثانیه.
⚠️ Error Responses​
Status	توضیحات
400	بازه زمانی درخواستی بیش از ۳ ماه است، یا مقدار start پیش از end نیست.
429	تعداد درخواست‌ها از حد مجاز ۵ درخواست در ثانیه بیشتر شده است.
Additional Notes​

🌍 با استفاده از این API می‌توانید فعالیت‌های معاملاتی قدیمی‌تر خود را بررسی و برای گزارش‌گیری استفاده کنید.
🔄 سفارشی که حداقل یک Match داشته باشد و کمتر از ۷ روز از بسته شدن آن گذشته باشد، هم از این API و هم از لیست سفارشات قابل دریافت است؛ بنابراین در صورت استفاده از هر دو مسیر، داده‌های تکراری را بر اساس id حذف کنید.
⚡ این API بلادرنگ (Real-time) نیست. برای پیگیری سفارش‌های Active و سفارش‌های تازه بسته‌شده، از لیست سفارشات یا وب‌سوکت وضعیت سفارشات استفاده کنید.


---

## order get fills list

https://docs.bitpin.org/v1/docs/order/get_fills_list

سفارشدریافت لیست معاملات انجام شده
دریافت لیست معاملات انجام شده
👋 Introduction​

با استفاده از این API می‌تونی جزییات معاملات انجام‌شده خودت رو ببینی. این قابلیت بهت این امکان رو می‌ده که تاریخچه معاملاتت رو بررسی کنی و اطلاعات مربوط به هر معامله مثل مقدار، قیمت، و هزینه کارمزد رو مشاهده کنی.

🔗 Endpoint​
GET /api/v1/odr/fills/

⏱ Rate Limit​
اطلاعیه

حداکثر تعداد درخواست‌های مجاز برای دریافت لیست معاملات برابر با 80 درخواست در دقیقه هست.

📨 Request Example​
cURL
Python
curl --location --request GET 'https://api.bitpin.org/api/v1/odr/fills/' \  
--header 'Authorization: Bearer YOUR_ACCESS_TOKEN'

🛠 Request Params​
Parameter	Description	Type	Required	Example
symbol	نام بازار که معامله در آن صورت گرفته	String	خیر	BTC_IRT
side	سمت معامله (مثلاً خرید یا فروش)	String	خیر	buy
offset	شناسه معاملاتی که باید کمتر از این مقدار باشد	Integer	خیر	65375307
limit	حداکثر تعداد معاملات دریافتی (حداکثر: 100)	Integer	خیر	100
💬 Success Response​
[
    {
        "id": 65375307,
        "symbol": "PIXFI_IRT",
        "base_amount": "63.0",
        "quote_amount": "123417",
        "price": "1959",
        "created_at": "2024-07-29T14:07:34.534824+03:30",
        "commission": "0",
        "side": "sell",
        "commission_currency": "IRT",
        "order_id": 535179385
    },
    {
        "id": 65375268,
        "symbol": "PIXFI_IRT",
        "base_amount": "63.0",
        "quote_amount": "123228",
        "price": "1956",
        "created_at": "2024-07-29T14:06:56.095051+03:30",
        "commission": "0.0",
        "side": "buy",
        "commission_currency": "PIXFI",
        "order_id": 535178666
    }
]

🗝️ Response Keys - کلیدهای پاسخ​
id: شناسه معامله.
symbol: نام بازاری که معامله توش انجام شده.
base_amount: مقدار ارز پایه که در معامله جابجا شده.
quote_amount: مقدار ارز مبادله‌ای که در معامله جابجا شده.
price: قیمت هر واحد ارز پایه در زمان معامله.
created_at: زمان ایجاد معامله، با توجه به منطقه زمانی.
commission: هزینه کارمزد معامله.
side: سمت معامله (خرید یا فروش).
commission_currency: واحد پول کارمزد.
order_id: شناسه سفارش مرتبط با این معامله.


---

## order bulk

https://docs.bitpin.org/v1/docs/order/bulk

ثبت چندین سفارش

Authenticated

POST /api/v1/odr/orders/bulk/

با این درخواست میتوانید چندین سفارش مختلف را تنها با یک درخواست ثبت کنید.

اطلاعات موردنظر برای هر سفارش مانند قرار دادن تک سفارش میباشد.

حداکثر 10 سفارش همزمان میتوانید در یک درخواست قرار دهید.

تنها میتوانید بر روی یک بازار چندین سفارش قرار دهید.

درخواست​
cURL
Python
curl --location --request POST 'https/api.bitpin.org/api/v1/odr/orders/bulk' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1..N0sDvVhgW4rmIl8yudcqv2IeCGM' \
--header 'Content-Type: application/json' \
--data '[
"orders": {
  "symbol": "USDT_IRT",
  "base_amount": 100,
  "price": 50000,
  "side": "buy",
  "type": "limit"
},
{
  "symbol": "USDT_IRT",
  "base_amount": 50,
  "price": 51000,
  "side": "buy",
  "type": "limit"
}]'

پاسخ موفق​
[
    "orders" : [
    {
        "id": 1,
        "symbol": "USDT_IRT",
        "type": "limit",
        "side": "buy",
        "base_amount": "100.00",
        "quote_amount": "5000000.00",
        "price": "50000",
        "stop_price": null,
        "price_limit_oco": null,
        "identifier": "716848bc-3f15-4b28-b113-0ce8dc621eff",
        "state": "active",
        "created_at": "2024-06-15T10:00:00.000000+03:30",
        "closed_at": null,
        "dealed_base_amount": "0",
        "dealed_quote_amount": "0",
        "req_to_cancel": false,
        "commission": "20.0"
    },
    {
        "id": 2,
        "symbol": "USDT_IRT",
        "type": "limit",
        "side": "buy",
        "base_amount": "50.00",
        "quote_amount": "2500000.00",
        "price": "50000",
        "stop_price": null,
        "price_limit_oco": null,
        "identifier": "716848bc-3f15-4b28-b113-0ce8dc621eff",
        "state": "active",
        "created_at": "2024-06-15T10:00:00.000000+03:30",
        "closed_at": null,
        "dealed_base_amount": "0",
        "dealed_quote_amount": "0",
        "req_to_cancel": false,
        "commission": "20.0"
    }
    ]
]


---

## order Bulk Orders Place Bulk Orders

https://docs.bitpin.org/v1/docs/order/Bulk%20Orders/Place_Bulk_Orders

سفارشBulk Ordersثبت چندین سفارش همزمان
Place Bulk Orders
👋 Introduction​

با استفاده از این قابلیت، می‌تونی چندین سفارش مختلف رو تنها با یک درخواست ثبت کنی.
این قابلیت برای زمانی که نیاز به ثبت چندین سفارش در یک بازار داری، خیلی کارآمده.

⚠️ Limitations​
توجه
حداکثر می‌تونی ۱۰ سفارش رو تو یک درخواست ثبت کنی.
🔗 Endpoint​
POST /api/v1/odr/orders/bulk

⏱ Rate Limit​
اطلاعیه

حداکثر تعداد درخواست‌های مجاز برای ثبت سفارش برابر با 1800 درخواست در ساعت هست.

📨 Request Example​
cURL
Python
curl --location --request POST 'https://api.bitpin.org/api/v1/odr/orders/bulk' \  
--header 'Authorization: Bearer YOUR_ACCESS_TOKEN' \  
--header 'Content-Type: application/json' \  
--data '[
    {
        "symbol": "USDT_IRT",
        "base_amount": 100,
        "price": 50000,
        "side": "buy",
        "type": "limit"
    },
    {
        "symbol": "USDT_IRT",
        "base_amount": 50,
        "price": 51000,
        "side": "buy",
        "type": "limit"
    }
]'

💬 Success Response​
{
    "orders":[
        {  
            "id": 535179385,  
            "symbol": "PIXFI_IRT",  
            "type": "limit",  
            "side": "sell",  
            "price": "1956",  
            "stop_price": null,  
            "oco_target_price": null,  
            "base_amount": "63.0",  
            "quote_amount": "123228",  
            "identifier": null,  
            "state": "active",  
            "closed_at": null,  
            "created_at": "2024-07-29T14:07:34.176795+03:30",  
            "dealed_base_amount": "0",  
            "dealed_quote_amount": "0",  
            "req_to_cancel": false,  
            "commission": "1000"  
        },
        {  
            "id": 535179255,  
            "symbol": "PIXFI_IRT",  
            "type": "limit",  
            "side": "sell",  
            "price": "2000",  
            "stop_price": null,  
            "oco_target_price": null,  
            "base_amount": "80.0",  
            "quote_amount": "160000",  
            "identifier": null,  
            "state": "active",  
            "closed_at": null,  
            "created_at": "2024-07-29T14:07:34.176795+03:30",  
            "dealed_base_amount": "0",  
            "dealed_quote_amount": "0",  
            "req_to_cancel": false,  
            "commission": "1000"  
        }
    ]
}

اخطار

اگر یک یا چند سفارش در درخواست ناموفق باشند، کل درخواست با خطا مواجه شود. بنابراین، حتماً پارامترهای مربوط به هر سفارش را به دقت بررسی کنید.


---

## order Bulk Orders Cancel Bulk Orders

https://docs.bitpin.org/v1/docs/order/Bulk%20Orders/Cancel_Bulk_Orders

سفارشBulk Ordersلغو چندین سفارش همزمان
لغو چندین سفارش همزمان
👋 Introduction​

با این درخواست می‌تونی چندین سفارش فعال خودت رو به‌صورت همزمان لغو کنی. این قابلیت وقتی کاربرد داره که نیاز به لغو سریع و همزمان چند سفارش داشته باشی.

⚠️ Important Note​
هشدار

فراخوانی موفق این مسیر به معنای دریافت درخواست لغو توسط هسته‌ی معاملاتیه. پردازش و بسته شدن سفارش‌ها بعد از مدت کوتاهی انجام می‌شه.

🔗 Endpoint​
DELETE /api/v1/odr/orders/bulk/

📨 لغو با شناسه‌های سفارش​
cURL
Python
curl --location --request DELETE 'https://bitpin.org/api/v1/odr/orders/bulk/' \  
--header 'Authorization: Bearer YOUR_ACCESS_TOKEN' \  
--data '{
  "ids": ["1", "2"]
}'

📨 لغو با شناسه‌های خاص​
cURL
Python
curl --location --request DELETE 'https://bitpin.org/api/v1/odr/orders/bulk/' \  
--header 'Authorization: Bearer YOUR_ACCESS_TOKEN' \  
--data '{
  "identifiers": ["abcd1", "abcd2"]
}'

💬 Success Response​
{
    "canceled_orders": ["abcd1", "abcd2"],
    "not_canceled_orders": []
}

❌ Error Responses​
اخطار
کد 406: درخواست غیر قابل پردازش.


---

## order bulk-cancel

https://docs.bitpin.org/v1/docs/order/bulk-cancel

لفو چندین سفارش

Authenticated

DELETE /api/v1/odr/bulk/

با فراخوانی این مسیر می‌توانید چندین سفارش خود را لغو کنید. فراخوانی موفق این مسیر به معنای دریافت درخواست لغو شما توسط هسته‌ي معاملاتی است. پردازش این درخواست و بسته شدن سفارش ها پس از زمان بسیار کوتاهی انجام خواهد شد. پاسخ موفق این درخواست کد 204 است. درخواست تکراری یا غیر قابل پردازش با کد 406 پاسخ داده می‌شود. ‍‍

لغو با شناسه​
cURL
Python
curl --location --request DELETE 'https:/bitpin.org/api/v1/odr/orders/bulk/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUz...r0vtVKSN0sDvVhgW4rmIl8yudcqv2IeCGM' \
--data '{
  "ids": ["1", "2"]
}'

پاسخ موفق​
{
    "canceled_orders": [1, 2],
    "not_canceled_orders": []
}

لغو با شناسه خاص​
cURL
Python
curl --location --request DELETE 'https:/bitpin.org/api/v1/odr/orders/bulk/' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUz...r0vtVKSN0sDvVhgW4rmIl8yudcqv2IeCGM' \
--data '{
  "identifiers": ["abcd1", "abcd2"]
}'

پاسخ موفق​
{
    "canceled_orders": ["abcd1", "abcd2"],
    "not_canceled_orders": []
}


======================================================================
# 8. WebSocket
======================================================================


---

## websocket intro

https://docs.bitpin.org/v1/docs/websocket/intro

وب سوکتمعرفی
معرفی
👋 مقدمه​

با استفاده از وب‌سوکت بیت‌پین می‌توانید داده‌های زنده (real-time) مربوط به بازار، دفتر سفارش‌ها و سفارش‌های کاربر را بدون نیاز به درخواست‌های مکرر از REST API دریافت کنید.

وب‌سوکت فقط در صورت تغییر داده، آپدیت‌ها را ارسال می‌کند.
بنابراین می‌توانید وضعیت اولیه را از REST API بگیرید و سپس تغییرات را از وب‌سوکت دنبال کنید.

🔗 Base URL​
wss://centrifugo.bitpin.org/connection/websocket

اطلاعیه

تمام پیام‌ها شامل کلید event هستند که نوع پیام را مشخص می‌کند.

نیازی به ایجاد اتصال جداگانه برای هر نوع داده نیست.

در صورت استفاده غیرمتعارف، اتصال محدود خواهد شد.

از wss برای ارتباط امن استفاده کنید.

🛠️ SDKهای پیشنهادی​
ماژول	کاربرد
centrifuge-js	مرورگر، NodeJS، ReactNative
centrifuge-python	پایتون (asyncio)
centrifuge-java	Java و Android
centrifuge-go	Golang
centrifuge-swift	iOS
centrifuge-dart	Flutter و Dart
📚 منابع بیشتر​
Centrifuge Documentation


---

## websocket quick start

https://docs.bitpin.org/v1/docs/websocket/quick_start

وب سوکتشروع سریع
شروع سریع
👋 مقدمه​

برای دریافت داده‌های لحظه‌ای از بازار و سفارش‌های خود، کافی است با استفاده از Centrifuge به وب‌سوکت بیت‌پین متصل شوید و در کانال‌های مورد نظر عضو شوید.

🔀 انواع کانال‌ها​
🔹 کانال‌های عمومی (Public Channels)​
کانال	توضیح
matches:SYMBOL	دریافت معاملات انجام‌شده در بازار
orderbook:SYMBOL	دریافت تغییرات دفتر سفارش‌ها
market:SYMBOL	دریافت تغییرات بازار (کندل و قیمت)
اطلاعیه

به جای SYMBOL باید نماد بازار مورد نظر را قرار دهید.
مثلاً: matches:USDT_IRT

🔹 کانال‌های خصوصی (User Channels)​
کانال	توضیح
user:order_info#USER_IDENTIFIER	دریافت آپدیت‌های سفارش‌ها و معاملات کاربر
اطلاعیه

برای اتصال به این کانال‌ها باید user_identifier و ws-token را از API مربوطه دریافت کنید.
این مقادیر برای احراز هویت کاربر در اتصال وب‌سوکت الزامی هستند.

نحوه دریافت توکن وب‌سوکت و شناسه کاربر

📘 مثال استفاده با JavaScript​
۱. نصب کتابخانه​
npm install centrifuge

۲. اتصال به کانال معاملات یک بازار​
import { Centrifuge } from "centrifuge";

const centrifuge = new Centrifuge("wss://centrifugo.bitpin.org/connection/websocket");

// رویدادهای اتصال
centrifuge.on("connected", () => console.log("Connected"));
centrifuge.on("disconnected", () => console.log("Disconnected"));
centrifuge.on("error", (ctx) => console.error("Error:", ctx));

// عضویت در کانال معاملات BTC/IRT
const sub = centrifuge.newSubscription("matches:BTC_IRT");
sub.on("publication", (ctx) => console.log("New match:", ctx.data));
sub.subscribe();

centrifuge.connect();

۳. اتصال با توکن JWT​

اگر قصد دارید به کانال‌های کاربری خصوصی متصل شوید، باید از توکن وب‌سوکت استفاده کنید:

const centrifuge = new Centrifuge("wss://centrifugo.bitpin.org/connection/websocket", {
  token: "your-ws-jwt-token"
});

centrifuge.connect();

اطلاعیه

در صورت تغییر توکن یا انقضای آن، لازم است اتصال مجدداً برقرار شود.

اتصال هم‌زمان از چند کلاینت پشتیبانی می‌شود.


---

## websocket ws info

https://docs.bitpin.org/v1/docs/websocket/ws_info

وب سوکتدریافت اطلاعات وب سوکت
دریافت اطلاعات وب سوکت
دریافت اطلاعات وب‌سوکت
👋 مقدمه​

این API جهت صدور توکن اتصال وب‌سوکت و ارائه‌ی شناسه‌ی اختصاصی کاربر طراحی شده است. برای استفاده از آن، باید کلیدهای معتبر api_key و secret_key را در بدنه‌ی درخواست ارسال کنید.

🔗 مسیر API​
POST /api/v1/usr/ws-info/

اطلاعیه

ارسال api_key و secret_key در بدنه‌ی درخواست لازم است.

⏱ محدودیت تعداد درخواست‌ها​

حداکثر ۱۰ درخواست در دقیقه برای هر کاربر مجاز است.

📨 نمونه درخواست​
curl --location --request POST 'https://api.bitpin.org/api/v1/usr/ws-info/' \
--header 'Content-Type: application/json' \
--data '{
  "api_key": "YOUR_API_KEY",
  "secret_key": "YOUR_SECRET_KEY"
}'

💬 پاسخ موفقیت‌آمیز​
{
  "user_identifier": "ZMQE74O6",
  "ws_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJ..."
}

📘 توضیحات فیلدها​
فیلد	نوع	توضیح
user_identifier	string	شناسه‌ی کوتاه و اختصاصی کاربر که برای نام‌گذاری کانال‌های خصوصی وب‌سوکت استفاده می‌شود (مثلاً: user:order_info#<user_identifier>).
ws_token	string	توکن احراز هویت وب‌سوکت که باید هنگام اتصال به سرور وب‌سوکت ارسال شود.


---

## websocket market

https://docs.bitpin.org/v1/docs/websocket/market

وب سوکتاطلاعات بازار (Market)
اطلاعات بازار (Market)
👋 مقدمه​

برای دریافت اطلاعات بازار شامل کندل و قیمت در یک بازار خاص، در کانال زیر عضو شوید:

market:SYMBOL

اطلاعیه

به جای SYMBOL نماد بازار مورد نظر را قرار دهید.
مثلاً: market:USDT_IRT

🔔 زمان ارسال پیام‌ها​

با انجام هر معامله جدید در بازار، یک پیام آپدیت قیمت به این کانال ارسال می‌شود

و هر ۱۰ ثانیه ,دو کندل آخر به ازای هر تایم فریم ارسال می‌شود.

📡 نحوه درخواست عضویت​
{
  "method": "subscribe",
  "params": {
    "channel": "market:BTC_IRT"
  }
}

📨 ساختار پیام دریافتی​
۱. آپدیت کندل (candle_update)​
{
  "candles": [
    {
      "open": "<decimal>",
      "close": "<decimal>",
      "low": "<decimal>",
      "high": "<decimal>",
      "volume": "<decimal>",
      "ts": "<float>",
      "resolution": "<string>"
    }
  ],
  "symbol": "<string>",
  "event_time": "%Y-%m-%dT%H:%M:%S.%fZ",
  "event": "candle_update"
}


۲. آپدیت قیمت (currency_price_update)​
{
  "price": "<decimal>",
  "change": "<decimal>",
  "min": "<decimal>",
  "max": "<decimal>",
  "mean": "<decimal>",
  "value": "<decimal>",
  "amount": "<decimal>",
  "time": "<float>",
  "symbol": "<string>",
  "event_time": "%Y-%m-%dT%H:%M:%S.%fZ",
  "event": "currency_price_update"
}

📘 مثال پیام دریافتی​
۱. آپدیت کندل (candle_update)​
{
  "candles": [
    {
      "open": "1019000000",
      "close": "1020000000",
      "low": "1017000000",
      "high": "1025000000",
      "volume": "0.01086870",
      "ts": "1760873797.0",
      "resolution": "1m"
    },
    {
      "open": "1020000000",
      "close": "1025000000",
      "low": "1019000000",
      "high": "1028000000",
      "volume": "0.01120140",
      "ts": "1760873857.0",
      "resolution": "1m"
    }
  ],
  "symbol": "BTC_IRT",
  "event_time": "2025-10-19T11:38:27.929164Z",
  "event": "candle_update"
}


۲. آپدیت قیمت (currency_price_update)​
{
  "price": "1020000000",
  "change": "0.0258",
  "min": "1012000000",
  "max": "1025000000",
  "mean": "1019100000",
  "value": "2050105000",
  "amount": "2.01119821",
  "time": "1760873857000",
  "symbol": "BTC_IRT",
  "event_time": "2025-10-19T11:38:27.929164Z",
  "event": "currency_price_update"
}


🧾 توضیحات فیلدها​
۱. آپدیت کندل (candle_update)​
فیلد	نوع	توضیح
open	Decimal	قیمت باز شدن
close	Decimal	قیمت بسته شدن
low	Decimal	پایین‌ترین قیمت
high	Decimal	بیشترین قیمت
volume	Decimal	حجم معاملات
ts	Float	زمان شروع کندل به‌صورت timestamp (ثانیه)
resolution	String	تایم فریم: 1m,5m,15m,30m,1h,3h,4h,6h,1d,1w,1M
symbol	String	نماد بازار (مثلاً BTC_IRT)
event_time	String (UTC ISO 8601)	زمان ثبت رویداد
event	String	نوع پیام (candle_update)
۲. آپدیت قیمت (currency_price_update)​
فیلد	نوع	توضیح
price	Decimal	قیمت بازار
change	Decimal	تغییرات قیمت نسبت به ۲۴ ساعت اخیر
min	Decimal	پایین‌ترین قیمت ۲۴ ساعت اخیر
max	Decimal	بیشترین قیمت ۲۴ ساعت اخیر
mean	Decimal	متوسط قیمت ۲۴ ساعت اخیر
value	Decimal	حجم بازار در ۲۴ ساعت اخیر
amount	Decimal	حجم بازار در ۲۴ ساعت اخیر بر اساس ارز مبادله
time	Float	زمان اپدیت قیمت
symbol	String	نماد بازار (مثلاً BTC_IRT)
event_time	String (UTC ISO 8601)	زمان ثبت رویداد
event	String	نوع پیام (currency_price_update)


---

## websocket orderbook

https://docs.bitpin.org/v1/docs/websocket/orderbook

وب سوکتدفتر سفارش‌ها (Orderbook)
دفتر سفارش‌ها (Orderbook)
👋 مقدمه​

برای دریافت داده‌های لحظه‌ای از دفتر سفارش‌ها، در کانال زیر عضو شوید:

orderbook:SYMBOL

اطلاعیه

به‌جای SYMBOL باید نماد بازار موردنظر را قرار دهید.
مثلاً: orderbook:USDT_IRT

🔔 زمان ارسال پیام‌ها​

هنگامی که سفارش جدیدی به دفتر سفارش‌ها اضافه شود یا تغییری در سفارش‌های موجود رخ دهد.

📡 نمونه درخواست عضویت​
{
  "method": "subscribe",
  "params": {
    "channel": "orderbook:BTC_IRT"
  }
}

📨 ساختار پیام دریافتی​
{
  "asks": [["<price>", "<amount>"]],
  "bids": [["<price>", "<amount>"]],
  "volume_ask": "<decimal>",
  "volume_bid": "<decimal>",
  "price": "<decimal>",
  "symbol": "<string>",
  "event": "market_data",
  "event_time": "%Y-%m-%dT%H:%M:%S.%fZ"
}


📘 مثال پیام دریافتی​
{
  "asks": [["51000", "2000.00000000"]],
  "bids": [["50000", "1000.00000000"]],
  "volume_ask": "2000.0",
  "volume_bid": "1000.0",
  "price": "50000.0",
  "symbol": "BTC_IRT",
  "event_time": "2024-08-14T14:37:54.487062Z",
  "event": "market_data"
}

🧾 توضیحات فیلدها​
فیلد	نوع	توضیح
asks	Array[[قیمت، حجم]]	لیست سفارش‌های فروش
bids	Array[[قیمت، حجم]]	لیست سفارش‌های خرید
volume_ask	Decimal	مجموع حجم سفارش‌های فروش
volume_bid	Decimal	مجموع حجم سفارش‌های خرید
price	Decimal	آخرین قیمت معامله‌شده
symbol	String	نماد بازار (مثلاً BTC_IRT)
event_time	String (UTC ISO 8601)	زمان ثبت رویداد
event	String	نوع پیام (در اینجا market_data)
اطلاعیه

ترتیب asks و bids از کم به زیاد بر اساس قیمت مرتب شده است.

برای دریافت تغییرات لحظه‌ای کافی است پس از عضویت در کانال، پیام‌های publication را گوش کنید.


---

## websocket matches

https://docs.bitpin.org/v1/docs/websocket/matches

وب سوکتمعاملات بازار (Match)
معاملات بازار (Match)
👋 مقدمه​

برای دریافت معاملات انجام‌شده در یک بازار خاص، در کانال زیر عضو شوید:

matches:SYMBOL

اطلاعیه

به جای SYMBOL نماد بازار مورد نظر را قرار دهید.
مثلاً: matches:USDT_IRT

🔔 زمان ارسال پیام‌ها​

با انجام هر معامله جدید در بازار، یک پیام به این کانال ارسال می‌شود.

📡 نحوه درخواست عضویت​
{
  "method": "subscribe",
  "params": {
    "channel": "matches:BTC_IRT"
  }
}

📨 ساختار پیام دریافتی​
{
  "matches": [
    {
      "id": "<string>",
      "price": "<decimal>",
      "base_amount": "<decimal>",
      "quote_amount": "<decimal>",
      "side": "<string>",
      "time": <float>
    }
  ],
  "symbol": "<string>",
  "event_time": "%Y-%m-%dT%H:%M:%S.%fZ",
  "event": "matches_update"
}


📘 مثال پیام دریافتی​
{
  "matches": [
    {
      "id": "73802972_73807087",
      "price": "1019000000",
      "base_amount": "0.01086870",
      "quote_amount": "11075213",
      "side": "sell",
      "time": 1760873797.149016
    }
  ],
  "symbol": "BTC_IRT",
  "event_time": "2025-10-19T11:38:27.929164Z",
  "event": "matches_update"
}


🧾 توضیحات فیلدها​
فیلد	نوع	توضیح
id	String	شناسه یکتای معامله
price	Decimal	قیمت انجام معامله
base_amount	Decimal	مقدار ارز پایه معامله‌شده
quote_amount	Decimal	مقدار ارز مقابل معامله‌شده
side	String	جهت معامله از دید taker (buy یا sell)
time	Float	زمان انجام معامله به‌صورت timestamp (ثانیه)
symbol	String	نماد بازار (مثلاً BTC_IRT)
event_time	String (UTC ISO 8601)	زمان ثبت رویداد
event	String	نوع پیام (matches_update)


---

## websocket user orders

https://docs.bitpin.org/v1/docs/websocket/user_orders

وب سوکتوضعیت سفارش‌های کاربر
وضعیت سفارش‌های کاربر
👋 مقدمه​

برای دریافت آپدیت‌های سفارش‌های خود، در کانال زیر عضو شوید:

user:order_info#<user_identifier>

اطلاعیه

این کانال نیاز به توکن JWT معتبر هنگام اتصال دارد.

نحوه دریافت user_identifier و توکن وب‌سوکت

🔔 زمان ارسال پیام‌ها​
پس از ایجاد سفارش جدید
پس از هر معامله
پس از لغو یا تکمیل سفارش
📡 نحوه درخواست عضویت​
{
  "method": "subscribe",
  "params": {
    "channel": "user:order_info#V33EQ5LV"
  }
}

📨 ساختار پیام دریافتی​
۱. آپدیت سفارش (user_order_update)​
{
  "id": <int>,
  "market": <int>,
  "symbol": "<string>",
  "type": "<string>",
  "side": "<string>",
  "price": "<decimal>",
  "stop_price": "<decimal> | null",
  "oco_target_price": "<decimal> | null",
  "base_amount": "<decimal>",
  "quote_amount": "<decimal>",
  "identifier": "<string> | null",
  "state": "<string>",
  "closed_at": "%Y-%m-%dT%H:%M:%S.%f+04:30",
  "created_at": "%Y-%m-%dT%H:%M:%S.%f+04:30",
  "dealed_base_amount": "<decimal>",
  "dealed_quote_amount": "<decimal>",
  "req_to_cancel": <bool>,
  "commission": "<decimal>",
  "gain_currency_code": "<string>",
  "resource_currency_code": "<string>",
  "fulfilled": "<decimal>",
  "event": "user_order_update",
  "event_time": "%Y-%m-%dT%H:%M:%S.%fZ"
}


۲. معامله جدید (user_match_update)​
{
  "id": <int>,
  "symbol": "<string>",
  "base_amount": "<decimal>",
  "quote_amount": "<decimal>",
  "price": "<decimal>",
  "created_at": "%Y-%m-%dT%H:%M:%S.%f+04:30",
  "commission": "<decimal>",
  "side": "<string>",
  "commission_currency": "<string>",
  "order_id": <int>,
  "identifier": "<string> | null",
  "event": "user_match_update",
  "event_time": "%Y-%m-%dT%H:%M:%S.%fZ"
}

📘 مثال پیام دریافتی​
۱. آپدیت سفارش (user_order_update)​
{
  "id": 123,
  "market": 1,
  "symbol": "PAXG_IRT",
  "type": "market",
  "side": "sell",
  "price": "464414599",
  "stop_price": null,
  "oco_target_price": null,
  "base_amount": "0.0012",
  "quote_amount": "557297",
  "identifier": null,
  "state": "closed",
  "closed_at": "2025-10-19T15:33:47.482954+03:30",
  "created_at": "2025-10-19T15:33:45.595667+03:30",
  "dealed_base_amount": "0.0012",
  "dealed_quote_amount": "559447",
  "req_to_cancel": false,
  "commission": "0.0000",
  "gain_currency_code": "IRT",
  "resource_currency_code": "PAXG",
  "fulfilled": "1.00",
  "event": "user_order_update",
  "event_time": "2025-10-19T12:03:47.620634Z"
}

۲. معامله جدید (user_match_update)​
{
  "id": 1234,
  "symbol": "PAXG_IRT",
  "base_amount": "0.0004",
  "quote_amount": "185725",
  "price": "464314617",
  "created_at": "2025-10-19T15:33:47.365130+03:30",
  "commission": "0",
  "side": "sell",
  "commission_currency": "IRT",
  "order_id": 123,
  "identifier": null,
  "event": "user_match_update",
  "event_time": "2025-10-19T12:03:47.651296Z"
}

🧾 توضیحات فیلدها​

تمام فیلدها مشابه REST API هستند:

فیلد	نوع	توضیح
تمام فیلدهای user_order_update	—	توضیحات فیلد سفارش
تمام فیلدهای user_match_update	—	توضیحات فیلد معامله


======================================================================
# 9. Error Handling
======================================================================


---

## Error Handling best practices

https://docs.bitpin.org/v1/docs/Error%20Handling/best_practices

مدیریت خطاراهکارهای بهینه برای مدیریت خطاها
راهکارهای بهینه برای مدیریت خطاها
🔍 بررسی کد وضعیت (HTTP Status Code)​

هر پاسخ API شامل یک کد وضعیت HTTP است که وضعیت درخواست شما را نشان می‌دهد. باید این کدها را به دقت بررسی کنید و بر اساس آن‌ها عمل کنید. برای مثال:

2xx: موفقیت (Success) - درخواست شما به درستی پردازش شده است.
4xx: خطای کاربر (Client Error) - مشکلی در درخواست شما وجود دارد.
5xx: خطای سرور (Server Error) - مشکلی در سمت سرور رخ داده است.
🛠 مدیریت خطاهای بازگشتی از API​

هر زمان که خطایی رخ دهد، به جز کد وضعیت HTTP، پیام خطای مربوطه نیز در پاسخ API ارائه می‌شود. به پیام خطا توجه کنید و بر اساس محتوای آن تصمیم‌گیری کنید. برای مثال:

اگر توکن شما منقضی شده است، باید فرآیند تمدید توکن (Token Refresh) را اجرا کنید.
اگر درخواست شما به درستی فرمت نشده باشد، پیام خطا به شما اطلاعات دقیقی در مورد پارامترهای اشتباه می‌دهد.
🔄 راه‌اندازی Retry برای خطاهای موقت​

در برخی موارد ممکن است خطاهای موقتی به دلیل مشکلات شبکه یا بار زیاد سرور رخ دهند. برای خطاهایی که دارای کد 5xx هستند، می‌توانید با تأخیر مجدد (Retry) درخواست خود را اجرا کنید. بهتر است از الگوریتم‌های Exponential Backoff استفاده کنید تا بار زیادی روی سرور ایجاد نشود.

📝 لاگ کردن خطاها​

همیشه خطاهای رخ داده در اپلیکیشن خود را لاگ کنید. این کار به شما کمک می‌کند تا سریع‌تر مشکلات را شناسایی کنید و در صورت نیاز آن‌ها را برطرف کنید. در لاگ‌ها حتماً کد وضعیت HTTP، پیام خطا و زمان وقوع خطا را ثبت کنید.

🛡 استفاده از کدهای خطای خاص​

هر API کدهای خطای خاص خود را داشته باشد. برای مثال، در بیت‌پین خطاهایی مانند "عدم احراز هویت" یا "محدودیت درخواست" بازگردانده شوند. بر اساس نوع خطا باید اقدامات خاصی مانند درخواست توکن جدید یا کاهش تعداد درخواست‌ها انجام شود.

⏳ مدیریت Timeout​

زمانی که یک درخواست به سرور ارسال می‌شود، ممکن است به دلیل مشکلات شبکه یا تاخیر در پردازش درخواست‌ها، پاسخ دیرتر از حد معمول برگردد. در این مواقع باید درخواست را مجدداً پس از مدت معقولی ارسال کنید. همچنین تنظیم زمان‌سنجی (Timeout) مناسب در کتابخانه HTTP خود برای جلوگیری از منتظر ماندن بی‌پایان بسیار مهم است.


---

## Error Handling common error codes

https://docs.bitpin.org/v1/docs/Error%20Handling/common_error_codes

مدیریت خطاکدهای خطای رایج
کدهای خطای رایج

در این بخش کدهای خطای رایج در API بیت‌پین آورده شده‌اند. این خطاها باید به درستی مدیریت شوند تا عملکرد اپلیکیشن پایدار باقی بماند.

400 Bad Request:​

توضیحات: درخواست شما دارای پارامترهای اشتباه یا ناقص است. راهکار: پارامترهای درخواست را بررسی کنید و مطمئن شوید که همه پارامترهای مورد نیاز به درستی ارسال شده‌اند.

401 Unauthorized:​

توضیحات: شما برای دسترسی به این API احراز هویت نشده‌اید یا توکن شما منقضی شده است. راهکار: مطمئن شوید که توکن صحیح در درخواست استفاده شده است. در صورت نیاز، فرآیند تمدید توکن را اجرا کنید.

403 Forbidden:​

توضیحات: شما مجوز لازم برای دسترسی به این API را ندارید. راهکار: بررسی کنید که آیا دسترسی لازم برای این API را دارید یا خیر. ممکن است دسترسی شما محدود شده باشد.

404 Not Found:​

توضیحات: مسیر یا منبع موردنظر پیدا نشد. راهکار: آدرس URL و پارامترهای ارسالی را بررسی کنید و اطمینان حاصل کنید که مسیر مورد نظر صحیح است.

429 Too Many Requests:​

توضیحات: شما از حد مجاز درخواست‌ها عبور کرده‌اید. راهکار: باید درخواست‌های خود را کاهش دهید و منتظر بمانید تا محدودیت زمانی پایان یابد.

500 Internal Server Error:​

توضیحات: خطایی در سمت سرور رخ داده است. راهکار: منتظر بمانید و پس از چند لحظه مجدداً تلاش کنید. در صورت تداوم مشکل، با تیم پشتیبانی تماس بگیرید.

503 Service Unavailable:​

توضیحات: سرور موقتاً در دسترس نیست یا به دلیل بار زیاد قادر به پاسخگویی نیست. راهکار: درخواست خود را پس از تأخیر مجدداً ارسال کنید. بهتر است از الگوریتم‌های Exponential Backoff برای مدیریت درخواست‌های مکرر استفاده کنید.


---

## deprecations

https://docs.bitpin.org/v1/docs/deprecations

مدیریت خطااطلاعیه منسوخ شدن APIها
اطلاعیه منسوخ شدن APIها

⚠️ در نسخه‌های جدید API بیت‌پین، برخی از مسیرهای نسخه v1 منسوخ (Deprecated) شده‌اند و به نسخه جدید منتقل شده‌اند.

هشدار

لطفاً قبل از 31 مرداد 1405 کدهای خود را به نسخه جدید مهاجرت دهید.

APIهای جایگزین شده​
برداشت‌ها (Withdraws)​

❌ مسیرهای قدیمی:

/api/v1/wlt/withdraws/
/api/v1/wlt/withdraws/by-currency-code/

✅ مسیر جدید:

/api/v2/wlt/withdraws/
شبکه‌ها (Networks)​

❌ مسیر قدیمی:

/api/v1/wlt/networks/

✅ مسیر جدید:

/api/v2/wlt/networks/
آدرس‌ها (Address)​

❌ مسیر قدیمی:

/api/v1/wlt/address/

✅ مسیر جدید:

/api/v2/wlt/address/
واریزها (Deposits)​

❌ مسیر قدیمی:

/api/v1/wlt/deposits/

✅ مسیر جدید:

/api/v2/wlt/deposits/
