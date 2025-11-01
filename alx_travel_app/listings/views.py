from rest_framework import viewsets
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .tasks import send_booking_mail

class ListingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows listings to be viewed or edited.
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)


class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows bookings to be viewed or edited.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        listing = Listing.objects.all().first()
        booking = serializer.save(guest=self.request.user, listing=listing)
        send_booking_mail.delay(self.request.user.username)

