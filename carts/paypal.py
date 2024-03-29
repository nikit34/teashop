import json

from django.conf import settings
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersCreateRequest


class PayPalClient:
    def __init__(self):
        self.client_id = getattr(settings, 'PAYPAL_CLIENT_ID', None)
        self.client_secret = getattr(settings, 'PAYPAL_CLIENT_SECRET', None)
        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        self.client = PayPalHttpClient(self.environment)

    def object_to_json(self, json_data):
        result = {}
        itr = json_data.__dict__.items()
        for key, value in itr:
            if not key.startswith("__"):
                if isinstance(value, list):
                    result[key] = self.array_to_json_array(value)
                elif not self.is_primittive(value):
                    result[key] = self.object_to_json(value)
                else:
                    result[key] = value
        return result

    def array_to_json_array(self, json_array):
        result =[]
        if isinstance(json_array, list):
            for item in json_array:
                if not self.is_primittive(item):
                    result.append(self.object_to_json(item))
                elif isinstance(item, list):
                    result.append(self.array_to_json_array(item))
                else:
                    result.append(item)
        return result

    def is_primittive(self, data):
        return isinstance(data, str) or isinstance(data, int)


class CreateOrder(PayPalClient):
    def __init__(self, order_obj, cart_obj):
        super(CreateOrder, self).__init__()
        _body = structurng_input(order_obj, cart_obj)
        self._res = self.create_order(_body)

    def create_order(self, body):
        request = OrdersCreateRequest()
        request.prefer('return=representation')
        request.request_body(body)
        response = self.client.execute(request)
        if settings.DEBUG:
            print('Status Code: ', response.status_code)
            print('Status: ', response.result.status)
            print('Order ID: ', response.result.id)
            print('Intent: ', response.result.intent)
            print('Links:')
            for link in response.result.links:
                print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
            print('Total Amount: {} {}' \
                .format(
                    response.result.purchase_units[0].amount.currency_code,
                    response.result.purchase_units[0].amount.value
                )
            )
        return response

    def get_response(self):
        return self._res


def structurng_input(order_obj, cart_obj):
    items = []
    for item in cart_obj.products.all():
        items.append({
            'name': item.title,
            'unit_amount': {
                'currency_code': 'USD',
                'value': str(item.price)
            },
            'quantity': '1',
            'category': 'PHYSICAL_GOODS' if item.delivery else 'DIGITAL_GOODS'
        })
    prepared_data_order = {
        'amount': {
            'currency_code': 'USD',
            'value': str(order_obj.total),
            'breakdown': {
                'item_total': {
                    'currency_code': 'USD',
                    'value': str(cart_obj.total)
                },
                'shipping': {
                    'currency_code': 'USD',
                    'value': str(order_obj.shipping_total)
                }
            }
        },
        'items': items,
        'shipping': {
            'address': {
                'address_line_1': order_obj.address.address_line_1,
                'address_line_2': order_obj.address.address_line_2,
                'admin_area_2': order_obj.address.city,
                'admin_area_1': order_obj.address.country,
                'postal_code': order_obj.address.postal_code,
                'country_code': 'PT',
            }
        }
    }
    return build_request_body(prepared_data_order)


def build_request_body(prepared_data_order):
    response_structure = {
        "intent": "CAPTURE",
        "application_context": {
            "brand_name": "TeaShop",
            "landing_page": "NO_PREFERENCE",
            "shipping_preference": "GET_FROM_FILE",
            "user_action": "PAY_NOW"
        },
        "purchase_units": [
            {
                "reference_id": "PUHF",
                "description": "PayPal deal",
                "custom_id": "CUST-HighFashions",
                "soft_descriptor": "HighFashions",
            },
        ]
    }
    response_structure['purchase_units'][0].update(prepared_data_order)

    if settings.DEBUG:
        print(json.dumps(response_structure, indent=4, sort_keys=True))

    return response_structure
