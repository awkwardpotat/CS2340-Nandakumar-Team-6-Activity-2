from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Restaurant, Review, ReviewReply
from accounts.models import Owner
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    search_term = request.GET.get('search')
    if search_term:
        restaurants = Restaurant.objects.filter(name__icontains=search_term)
    else:
        restaurants = Restaurant.objects.all()
    template_data = {}
    template_data['restaurants'] = restaurants
    return render(request, 'restaurants/index.html', {'template_data': template_data})

def show(request, id):
    restaurant = Restaurant.objects.get(id=id)
    reviews = Review.objects.filter(restaurant=restaurant)

    is_owner = False
    if request.user.is_authenticated and restaurant.owner:
        try:
            owner = Owner.objects.get(user=request.user)
            is_owner = (restaurant.owner == owner)
        except Owner.DoesNotExist:
            pass
    can_review = False
    is_favorite = False
    if request.user.is_authenticated:
        from accounts.models import Reviewer
        try:
            reviewer = Reviewer.objects.get(user=request.user)
            can_review = not Review.objects.filter(restaurant=restaurant, reviewer=reviewer).exists() and not is_owner
        except Reviewer.DoesNotExist:
            can_review = False
        is_favorite = request.user in restaurant.favorites.all()



    template_data = {}
    template_data['title'] = restaurant.name
    template_data['restaurant'] = restaurant
    template_data['reviews'] = reviews
    template_data['can_review'] = can_review
    template_data['is_favorite'] = is_favorite
    template_data['is_owner'] = is_owner
    return render(request, 'restaurants/show.html', {'template_data': template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '' and request.POST['rating'] != 0:
        restaurant = Restaurant.objects.get(id=id)
        from accounts.models import Reviewer
        try:
            reviewer = Reviewer.objects.get(user=request.user)
        except Reviewer.DoesNotExist:
            return redirect('restaurants.show', id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.rating = request.POST['rating']
        review.restaurant = restaurant
        review.reviewer = reviewer
        review.save()
        review.restaurant.update_average_rating()
        return redirect('restaurants.show', id=id)
    else:
        return redirect('restaurants.show', id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if not hasattr(review, 'reviewer') or review.reviewer is None or request.user != review.reviewer.user:
        return redirect('restaurants.show', id=id)

    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'restaurants/edit_review.html', {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '' and request.POST['rating'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.rating = request.POST['rating']
        review.save()
        review.restaurant.update_average_rating()
        return redirect('restaurants.show', id=id)
    else:
        return redirect('restaurants.show', id=id)

@login_required
def delete_review(request, id, review_id):
    from accounts.models import Reviewer
    try:
        reviewer = Reviewer.objects.get(user=request.user)
    except Reviewer.DoesNotExist:
        return redirect('restaurants.show', id=id)
    review = get_object_or_404(Review, id=review_id, reviewer=reviewer)
    restaurant = review.restaurant
    review.delete()
    restaurant.update_average_rating()
    return redirect('restaurants.show', id=id)

@login_required
def toggle_favorite(request, id):
    if request.method != 'POST':
        return redirect('restaurants.show', id=id)

    restaurant = get_object_or_404(Restaurant, id=id)
    if request.user in restaurant.favorites.all():
        restaurant.favorites.remove(request.user)
        is_favorite = False
    else:
        restaurant.favorites.add(request.user)
        is_favorite = True

    # If it's an AJAX request, return JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'is_favorite': is_favorite})

    # Otherwise redirect back to the restaurant page
    return redirect('restaurants.show', id=id)


@login_required
def create_reply(request, id, review_id):
    if request.method == 'POST':
        restaurant = get_object_or_404(Restaurant, id=id)
        review = get_object_or_404(Review, id=review_id, restaurant=restaurant)

        # Check if user is either the owner OR the reviewer
        is_owner = False
        is_reviewer = (review.reviewer.user == request.user)

        if restaurant.owner:
            try:
                owner = Owner.objects.get(user=request.user)
                is_owner = (restaurant.owner == owner)
            except Owner.DoesNotExist:
                pass

        if not (is_owner or is_reviewer):
            return redirect('restaurants.show', id=id)

        reply_text = request.POST.get('reply_text')
        if reply_text:
            ReviewReply.objects.create(
                review=review,
                author_user=request.user,
                reply_text=reply_text
            )

    return redirect('restaurants.show', id=id)

@login_required
def delete_reply(request, id, review_id, reply_id):
    if request.method == 'POST':
        restaurant = get_object_or_404(Restaurant, id=id)
        review = get_object_or_404(Review, id=review_id, restaurant=restaurant)
        reply = get_object_or_404(ReviewReply, id=reply_id, review=review)

        # Only the person who wrote the reply can delete it
        if reply.author_user == request.user:
            reply.delete()

    return redirect('restaurants.show', id=id)

@login_required
def toggle_claim(request, id):
    if request.method == 'POST':
        
        restaurant = get_object_or_404(Restaurant, id=id)
        # If restaurant has an owner and it's the current user -> unclaim
        if restaurant.owner is not None and restaurant.owner.user == request.user:
            restaurant.owner = None
        # If restaurant has no owner, try to assign the current user's Owner profile
        elif restaurant.owner is None:
            try:
                owner = Owner.objects.get(user=request.user)
                restaurant.owner = owner
            except Owner.DoesNotExist:
                # current user isn't an Owner; do nothing
                pass

        restaurant.save()
        return redirect('restaurants.show', id=id)