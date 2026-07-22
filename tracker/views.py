from django.shortcuts import render, redirect
from .models import TrackerItem, Game
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .services import search_igdb_games
from django.http import JsonResponse
import json

# Create your views here.

def home(request):
    return render(request, "home.html")

@login_required
def tracker(request):
    # Fetch tracker items for the logged-in user
    tracker_items = TrackerItem.objects.filter(user=request.user)
    
    return render(request, "tracker.html", {"trackerItems": tracker_items })

@login_required
def search_games_ajax(request):
    query = request.GET.get("query", "").strip()
    results = []

    if query:
        results = search_igdb_games(query)

    data = []
    for game in results:
        cover = game.get("cover")
        cover_url = ""
        if cover and cover.get("url"):
            cover_url = "https:" + cover["url"].replace("t_thumb", "t_cover_big")

        data.append({
            "name" : game.get("name", "Unknown title"),
            "cover_image_url": cover_url
        })

    return JsonResponse({"results": data})

@login_required
def update_status(request, item_id):
    if request.method == "POST":
        body = json.loads(request.body)
        new_status = body.get("status")

        item = TrackerItem.objects.get(id=item_id, user=request.user)
        if new_status in dict(TrackerItem._meta.get_field('status').choices):
            item.status = new_status
            item.save()
            return JsonResponse({"status": "ok"})
        return JsonResponse({"status": "error", "message": "Invalid status"}, status=405)

@login_required
def add_game(request):
    if request.method == "POST":
        body = json.loads(request.body)
        title = body.get("title")
        cover_image_url = body.get("cover_image_url")

        game, created = Game.objects.get_or_create(
            title=title,
            defaults={"cover_image_url": cover_image_url}
        )
        TrackerItem.objects.get_or_create(user=request.user, game=game)

        return JsonResponse({"status":"ok"})
    return JsonResponse({"status":"error"}, status=405)
            
@login_required
def delete_game(request, item_id):
    if request.method == "POST":
        item = TrackerItem.objects.get(id=item_id, user=request.user)
        item.delete()
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"}, status=405)

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("tracker")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

@login_required
def get_notes(request, item_id):
    item = TrackerItem.objects.get(id=item_id, user=request.user)
    return JsonResponse({"notes": item.notes or ""})

@login_required
def save_notes(request, item_id):
    if request.method == "POST":
        body = json.loads(request.body)
        notes = body.get("notes", "")

        item = TrackerItem.objects.get(id=item_id, user=request.user)
        item.notes = notes
        item.save()

        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"}, status=405)