# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .forms import TransferSearchForm
from .models import Location, CartShip, Listing
from django.contrib import messages

def search_transfer(request):
    locations = Location.objects.all()
    if request.method == 'POST':
        form = TransferSearchForm(request.POST)
        if form.is_valid():
            pickup_location = form.cleaned_data['pickup_location']
            dropoff_location = form.cleaned_data['dropoff_location']
            num_people = form.cleaned_data['num_people']

            # Fetch the data from Listing based on search criteria
            options = Listing.objects.filter(
                pickup_location__iexact=pickup_location,
                dropoff_location__iexact=dropoff_location,
                capacity__gte=num_people
            )

            # Pass the filtered results to the template
            return render(request, 'cart/transfer_results.html', {
                'options': options, 
                'pickup_location': pickup_location, 
                'dropoff_location': dropoff_location, 
                'num_people': num_people
            })
    else:
        form = TransferSearchForm()

    return render(request, 'cart/search_transfer.html', {'form': form, 'locations': locations})
def add_to_cart(request, option_id):
    listing_option = get_object_or_404(Listing, pk=option_id)
    cart_item, created = CartShip.objects.get_or_create(listing_option=listing_option)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    messages.success(request, 'Item added to cart successfully!')
    return redirect('view_cart')

def view_cart(request):
    cart_items = CartShip.objects.all()
    for item in cart_items:
        item.total_price = item.quantity * item.listing_option.price
    return render(request, 'cart/view_cart.html', {'cart_items': cart_items})

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartShip, pk=item_id)
    cart_item.delete()
    messages.success(request, 'Item removed from cart successfully!')
    return redirect('view_cart')