import base64
import os
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.utils import timezone
from django.db.models import Avg, Count, Sum, F
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from .forms import ImageUploadForm, CameraUploadForm, RatingForm
from .models import TobaccoImage, ClassificationResult, Rating
from .ml_models import (detect_tobacco, classify_tobacco_quality,
                       predict_tobacco_price, is_blurry)


def move_image_to_grade_folder(tobacco_image, grade):
    """
    Move the uploaded image to a grade‑specific subfolder inside MEDIA_ROOT/tobacco/<grade>/
    and update the image field accordingly.
    """
    old_path = tobacco_image.image.path
    grade_folder = os.path.join('tobacco', grade.replace(' ', '_'))
    new_filename = os.path.basename(old_path)
    new_relative = os.path.join(grade_folder, new_filename)
    new_full = os.path.join(settings.MEDIA_ROOT, new_relative)

    # Create the target directory if it doesn't exist
    os.makedirs(os.path.dirname(new_full), exist_ok=True)

    # Move the file on disk
    os.rename(old_path, new_full)

    # Update the model's image field to point to the new location
    tobacco_image.image.name = new_relative
    tobacco_image.save(update_fields=['image'])


def home(request):
    recent_results = ClassificationResult.objects.select_related('tobacco_image').order_by('-classified_at')[:5]
    return render(request, 'classifier/home.html', {'recent_results': recent_results})


@login_required
def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            grower_number = form.cleaned_data['grower_number']
            last_bale = TobaccoImage.objects.filter(grower_number=grower_number).order_by('-bale_number').first()
            if last_bale and last_bale.bale_number.isdigit():
                next_bale_number = str(int(last_bale.bale_number) + 1)
            else:
                next_bale_number = '1'

            tobacco_image = TobaccoImage(
                image=form.cleaned_data['image'],
                group=form.cleaned_data['group'],
                grower_number=grower_number,
                lot_number=form.cleaned_data['lot_number'],
                bale_number=next_bale_number,
                weight=form.cleaned_data['weight']
            )
            tobacco_image.save()

            image_path = tobacco_image.image.path

            # Blur check
            blur_score = is_blurry(image_path)
            tobacco_image.blur_score = blur_score

            # Tobacco detection
            is_tobacco, confidence = detect_tobacco(image_path)
            tobacco_image.is_tobacco = is_tobacco
            tobacco_image.save()

            if is_tobacco:
                grade, quality_confidence = classify_tobacco_quality(image_path)
                price = predict_tobacco_price(grade)

                ClassificationResult.objects.create(
                    tobacco_image=tobacco_image,
                    grade=grade,
                    confidence=quality_confidence,
                    price=price
                )

                # Move the image into a grade‑specific folder
                move_image_to_grade_folder(tobacco_image, grade)

            return redirect('classifier:result', image_id=tobacco_image.id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ImageUploadForm()

    return render(request, 'classifier/upload.html', {'form': form})


@login_required
def camera_upload(request):
    if request.method == 'POST':
        form = CameraUploadForm(request.POST)
        if form.is_valid():
            image_data = form.cleaned_data['image_data']
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr))

            grower_number = form.cleaned_data['grower_number']
            last_bale = TobaccoImage.objects.filter(grower_number=grower_number).order_by('-bale_number').first()
            if last_bale and last_bale.bale_number.isdigit():
                next_bale_number = str(int(last_bale.bale_number) + 1)
            else:
                next_bale_number = '1'

            tobacco_image = TobaccoImage(
                group=form.cleaned_data['group'],
                grower_number=grower_number,
                lot_number=form.cleaned_data['lot_number'],
                bale_number=next_bale_number,
                weight=form.cleaned_data['weight'],
            )
            tobacco_image.image.save(
                f'camera_img_{timezone.now().timestamp()}.{ext}', data, save=True
            )

            image_path = tobacco_image.image.path

            blur_score = is_blurry(image_path)
            tobacco_image.blur_score = blur_score

            is_tobacco, confidence = detect_tobacco(image_path)
            tobacco_image.is_tobacco = is_tobacco
            tobacco_image.save()

            if is_tobacco:
                grade, quality_confidence = classify_tobacco_quality(image_path)
                price = predict_tobacco_price(grade)

                ClassificationResult.objects.create(
                    tobacco_image=tobacco_image,
                    grade=grade,
                    confidence=quality_confidence,
                    price=price
                )

                move_image_to_grade_folder(tobacco_image, grade)

            return JsonResponse({
                'success': True,
                'redirect_url': f'/result/{tobacco_image.id}/'
            })
        else:
            errors = {field: [str(e) for e in msgs] for field, msgs in form.errors.items()}
            return JsonResponse({'success': False, 'errors': errors}, status=400)

    form = CameraUploadForm()
    return render(request, 'classifier/upload.html', {'camera': True, 'form': form})


def result(request, image_id):
    tobacco_image = get_object_or_404(TobaccoImage, id=image_id)
    ratings = Rating.objects.all().order_by('-created_at')
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.save()
            return redirect('classifier:result', image_id=image_id)
    else:
        form = RatingForm()

    context = {
        'tobacco_image': tobacco_image,
        'ratings': ratings,
        'form': form,
        'Rating': Rating,
    }

    if tobacco_image.is_tobacco:
        try:
            result = tobacco_image.result
            context['result'] = result
        except ClassificationResult.DoesNotExist:
            pass

    return render(request, 'classifier/result.html', context)


@login_required
def dashboard(request):
    total_processed = TobaccoImage.objects.count()
    total_tobacco = TobaccoImage.objects.filter(is_tobacco=True).count()
    total_non_tobacco = TobaccoImage.objects.filter(is_tobacco=False).count()

    latest_classifications = ClassificationResult.objects.select_related('tobacco_image').order_by('-classified_at')[:10]

    avg_price_by_grade = ClassificationResult.objects.values('grade').annotate(
        avg_price=Avg('price')
    ).order_by('-avg_price')

    farmer_summary = TobaccoImage.objects.filter(
        is_tobacco=True,
        grower_number__isnull=False
    ).values('grower_number').annotate(
        total_bales=Count('id'),
        total_weight=Sum('weight'),
        avg_price=Avg('result__price'),
        total_value=Sum(F('weight') * F('result__price'))
    ).order_by('-total_value')

    context = {
        'total_processed': total_processed,
        'total_tobacco': total_tobacco,
        'total_non_tobacco': total_non_tobacco,
        'latest_classifications': latest_classifications,
        'avg_price_by_grade': avg_price_by_grade,
        'farmer_summary': farmer_summary,
    }
    return render(request, 'classifier/dashboard.html', context)


@login_required
def search_farmer(request):
    grower_number = request.GET.get('grower_number', '')
    farmer_data = None

    if grower_number:
        farmer_data = TobaccoImage.objects.filter(
            is_tobacco=True,
            grower_number=grower_number
        ).values(
            'grower_number', 'lot_number', 'bale_number', 'weight',
            'result__grade', 'result__price', 'result__classified_at'
        ).order_by('-result__classified_at')

    context = {'grower_number': grower_number, 'farmer_data': farmer_data}
    return render(request, 'classifier/farmer_report.html', context)


@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_rating(request, rating_id):
    rating = get_object_or_404(Rating, id=rating_id)
    if request.method == 'POST':
        rating.delete()
        messages.success(request, 'Rating and comment deleted successfully.')
        return redirect('classifier:ratings_list')
    return render(request, 'classifier/delete_rating.html', {'rating': rating})


@login_required
def ratings_list(request):
    ratings = Rating.objects.all()
    average_rating = Rating.get_average_rating()
    total_ratings = ratings.count()
    context = {
        'ratings': ratings,
        'average_rating': average_rating,
        'total_ratings': total_ratings,
    }
    return render(request, 'classifier/ratings_list.html', context)