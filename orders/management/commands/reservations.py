from collections import Counter
from datetime import datetime, time

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from carts.models import Cart
from chats.models import ContactMessage, DoorHit, WaitlistSignup
from orders.models import Order


class Command(BaseCommand):
    help = "List reserved orders and contact messages, then a per-source funnel: the signals the demand check counts"

    def add_arguments(self, parser):
        parser.add_argument('--since', help='count only records from this date on, YYYY-MM-DD')

    def handle(self, *args, **options):
        since = None
        if options.get('since'):
            try:
                day = datetime.strptime(options['since'], '%Y-%m-%d').date()
            except ValueError:
                raise CommandError('--since expects YYYY-MM-DD')
            since = timezone.make_aware(datetime.combine(day, time.min))

        orders = Order.objects.filter(status='reserved').select_related('billing_profile', 'cart').order_by('-timestamp')
        contact_messages = ContactMessage.objects.all()
        carts = Cart.objects.all()
        signups = WaitlistSignup.objects.all()
        door_hits = DoorHit.objects.all()
        if since:
            door_hits = door_hits.filter(timestamp__gte=since)
            signups = signups.filter(timestamp__gte=since)
            orders = orders.filter(timestamp__gte=since)
            contact_messages = contact_messages.filter(timestamp__gte=since)
            carts = carts.filter(timestamp__gte=since)

        self.stdout.write("Reserved orders: {count}".format(count=orders.count()))
        for order in orders:
            items = ', '.join(
                '{qty} x {title}'.format(qty=item.quantity, title=item.product.title_primary)
                for item in order.cart.cart_items.all()
            )
            self.stdout.write('{ts:%Y-%m-%d %H:%M}  {order_id}  {total} EUR  {email}  {phone}  |  {items}  |  src={source}{company}'.format(
                ts=order.timestamp,
                order_id=order.order_id,
                total=order.total,
                email=order.billing_profile.email if order.billing_profile else '-',
                phone=order.phone or '-',
                items=items,
                source=order.source or '-',
                company='  |  {company} NIF {nif}'.format(company=order.company or '-', nif=order.nif or '-') if (order.company or order.nif) else '',
            ))

        self.stdout.write("")
        self.stdout.write("Contact messages: {count}".format(count=contact_messages.count()))
        for message in contact_messages:
            self.stdout.write('{ts:%Y-%m-%d %H:%M}  {name}  {email}  src={source}  |  {content}'.format(
                ts=message.timestamp,
                name=message.full_name,
                email=message.email,
                source=message.source or '-',
                content=' '.join(message.content.split()),
            ))

        self.stdout.write("")
        self.stdout.write("Checkout clicks (fake door): {count}".format(count=door_hits.count()))
        for hit in door_hits:
            self.stdout.write('{ts:%Y-%m-%d %H:%M}  {total} EUR  src={source}  |  {items}'.format(
                ts=hit.timestamp, total=hit.total, source=hit.source or '-', items=hit.items or '-'))

        self.stdout.write("")
        self.stdout.write("Waitlist signups: {count}".format(count=signups.count()))
        for signup in signups:
            self.stdout.write('{ts:%Y-%m-%d %H:%M}  {email}  {occasion}  {company}{boxes}  {total} EUR  src={source}  |  {items}'.format(
                ts=signup.timestamp,
                email=signup.email,
                occasion=signup.occasion or '-',
                company=signup.company or '-',
                boxes=' x{n}'.format(n=signup.boxes) if signup.boxes else '',
                total=signup.total,
                source=signup.source or '-',
                items=signup.items or '-',
            ))

        visits = Counter(carts.values_list('source', flat=True))
        with_items = Counter(carts.filter(cart_items__isnull=False).distinct().values_list('source', flat=True))
        reserved = Counter(orders.values_list('source', flat=True))
        messages = Counter(contact_messages.values_list('source', flat=True))
        waitlist = Counter(signups.values_list('source', flat=True))
        doors = Counter(door_hits.values_list('source', flat=True))
        self.stdout.write("")
        self.stdout.write("By source: carts / carts with items / checkout clicks / signups / reservations / messages")
        for source in sorted(set(visits) | set(reserved) | set(messages) | set(waitlist) | set(doors), key=lambda s: (-visits[s], s)):
            self.stdout.write('{source:<28} {visits:>6} {items:>6} {doors:>6} {signups:>6} {reserved:>6} {messages:>6}'.format(
                source=source or '-',
                visits=visits[source],
                items=with_items[source],
                doors=doors[source],
                signups=waitlist[source],
                reserved=reserved[source],
                messages=messages[source],
            ))
