from django.db import models
from django.contrib.auth.models import User


class Listing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    # Relationships
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")

    def __str__(self):
        return self.title


class Booking(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bookings")
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    check_in = models.DateField()
    check_out = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["listing", "guest", "check_in"], name="unique_booking_per_day")
        ]

    def __str__(self):
        return f"Booking for {self.listing.title} by {self.guest.username}"


class Review(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="reviews")
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField()  # 1–5
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("listing", "reviewer")

    def __str__(self):
        return f"Review {self.rating} for {self.listing.title}"
