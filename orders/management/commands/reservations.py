from django.core.management.base import BaseCommand

from chats.models import ContactMessage
from orders.models import Order


class Command(BaseCommand):
    help = "List reserved orders and contact messages: the signals the demand check counts"

    def handle(self, *args, **options):
        orders = Order.objects.filter(status='reserved').select_related('billing_profile', 'cart').order_by('-timestamp')
        self.stdout.write("Reserved orders: {count}".format(count=orders.count()))
        for order in orders:
            items = ', '.join(
                '{qty} x {title}'.format(qty=item.quantity, title=item.product.title_primary)
                for item in order.cart.cart_items.all()
            )
            self.stdout.write('{ts:%Y-%m-%d %H:%M}  {order_id}  {total} EUR  {email}  {phone}  |  {items}'.format(
                ts=order.timestamp,
                order_id=order.order_id,
                total=order.total,
                email=order.billing_profile.email if order.billing_profile else '-',
                phone=order.phone or '-',
                items=items,
            ))

        contact_messages = ContactMessage.objects.all()
        self.stdout.write("")
        self.stdout.write("Contact messages: {count}".format(count=contact_messages.count()))
        for message in contact_messages:
            self.stdout.write('{ts:%Y-%m-%d %H:%M}  {name}  {email}  |  {content}'.format(
                ts=message.timestamp,
                name=message.full_name,
                email=message.email,
                content=' '.join(message.content.split()),
            ))
