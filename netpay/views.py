import base64
from Crypto.Cipher import AES
import datetime
from django.http import Http404
from django.utils.translation import ugettext as _
import hashlib
from urllib.parse import quote
from django.shortcuts import render_to_response, render, 
from django.template import RequestContext

from .forms import NetpayForm
from .models import Invoice_Netpay

def render_to(tmpl):
    def renderer(func):
        def wrapper(request, *args, **kw):
            output = func(request, *args, **kw)
            if not isinstance(output, dict):
                return output
#            return render_to_response(tmpl, output)
#                   #context_instance=RequestContext(request))
            return render(request, tmpl, output)
        return wrapper
    return renderer


API_KEY = "oikcsbf9fqvp2scvoe28iki4si"
AuthSign = '2750'
url_net2pay_pay = 'https://my.net2pay.ru/billingService/paypage/'
SUCCESS_URL = 'http://example.com/'
FAIL_URL = 'http://example.com/'

def md5_base64(text):
	# функция для кодирования текста в md5 с последующим base64
    m = hashlib.md5()
    m.update(text.encode())
    r = m.digest()
    return base64.b64encode(r).decode().strip()

def crypt_param(val, key):
	#Функция для шифрования параметров AES
    BLOCK_SIZE = 16
    PADDING = chr(BLOCK_SIZE - len(val) % BLOCK_SIZE)
    pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
    EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
    cipher = AES.new(key)
    encoded = EncodeAES(cipher, val)
    # print 'Encrypted string:', encoded
    return encoded

@render_to("netpay_payment.html")
def payment_netpay(request):
    "Отображает интерфейс для оплаты по банковским картам NETPAY"
    context = {}
    form = NetpayForm()
    if request.POST:
        form = NetpayForm(request.POST)
        if form.is_valid(): #Если форма валидна, то создаем запись в базе с определенным id
            inv = Invoice_Netpay()
            inv.amount = form.cleaned_data['money']
            inv.desc = _("Пополнение счета через Netpay")
            inv.login = 'Username'
            inv.currency = 'RUB'
            inv.save()
			
			#Создаем нужные ключи для шифрования
            md5_api_key = md5_base64(API_KEY)
            order_date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%dV%H:%M:%S")
            # order_date = '2014-06-28V13:39:49'
            crypt_key = md5_base64(md5_api_key + order_date)[:16]
			
			# Формируем параметры
            params = {}
            params['description'] = 'ORDER %s' % inv.id
            params['amount'] = inv.amount
            params['currency'] = 'RUB'
            params['orderID'] = inv.id
            params['cardHolderCity'] = ""
            params['cardHolderCountry'] = ""
            params['cardHolderPostal'] = ""
            params['cardHolderRegion'] = ""
            params['successUrl'] = SUCCESS_URL
            params['failUrl'] = FAIL_URL
			
			# Шифруем параметры
            params_crypted = []
            for k, v in params.items():
                r = crypt_param('%s=%s' % (k, v), crypt_key).decode()
                params_crypted.append(r)
            data = quote('&'.join(params_crypted))
			
			#данные формы для отправки на Netpay
            context["action"] = url_net2pay_pay
            context["data"] = data
            context["auth"] = AuthSign
            context["order_date"] = quote(order_date)
            return context

        else:
            context['form'] = form
            return context
    else:
        context['form'] = form
    return context
