from api_wrapper import GoogleAPIWrapper

# إنشاء نسخة من الكود مع مفتاح API
api = GoogleAPIWrapper("AIzaSyDCuWm5sKlxNeWGfdctfBRxvm5zuERVNIs")

# تحديد عنوان API والنقطة النهائية
base_url = "https://generativelanguage.googleapis.com/v1/models/"
endpoint = "gemini-pro:generateText"

# الحصول على الرابط الكامل مع مفتاح API
url = api.create_api_url(base_url, endpoint)

# إرسال طلب تجريبي
data = {
    "prompt": {"text": "مرحبا، كيف حالك؟"}
}

# طباعة الرابط للتحقق
print("الرابط الكامل:", url)

# إرسال الطلب والحصول على الرد
response = api.make_request(url, method="POST", data=data)
print("\nالرد من API:")
print(response)
