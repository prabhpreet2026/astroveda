from django.shortcuts import render, redirect, get_object_or_404
from myapp.models import *
from django.contrib import messages
from django.utils.crypto import get_random_string
# Create your views here.

def index(request):
	return render(request,"index.html")

def about(request):
	return render(request,"about.html")


def four_zero_four(request):
	return render(request,"404.html")

def blog(request):
	return render(request,"blog.html")

def blog_details(request):
	return render(request,"blog-details.html")

def contact(request):
	return render(request,"contact.html")

def footer(request):
	return render(request,"footer.html")

def faq(request):
	return render(request,"faq.html")

def navbar(request):
	return render(request,"navbar.html")

def pricing(request):
    plans = PricingPlan.objects.filter(is_active=True).order_by("display_order")
    return render(request, "pricing.html", {"plans": plans})


def services(request):
    services = Service.objects.filter(is_active=True).order_by("display_order", "-created_at")
    return render(request, "services.html", {"services": services})


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    return render(request, "service-details.html", {"service": service})


def appointment(request):
    plan_slug = request.GET.get("plan")
    plan = PricingPlan.objects.filter(slug=plan_slug, is_active=True).first() if plan_slug else None

    if request.method == "POST":
        plan = get_object_or_404(PricingPlan, id=request.POST.get("plan"), is_active=True)

        request.session["appointment_data"] = {
            "plan_id": plan.id,
            "full_name": request.POST.get("full_name"),
            "phone": request.POST.get("phone"),
            "date_of_birth": request.POST.get("date_of_birth"),
            "time_of_birth": request.POST.get("time_of_birth"),
            "gender": request.POST.get("gender"),
            "birth_place": request.POST.get("birth_place"),
            "consultation_date": request.POST.get("consultation_date"),
            "language": request.POST.get("language"),
            "question": request.POST.get("question"),
        }

        return redirect("dummy_payment")

    if not plan:
        messages.error(request, "Please select a pricing plan first.")
        return redirect("pricing")

    return render(request, "appointment.html", {"plan": plan})

def dummy_payment(request):
    appointment_data = request.session.get("appointment_data")

    if not appointment_data or not appointment_data.get("plan_id"):
        messages.error(request, "Please select a pricing plan first.")
        return redirect("pricing")

    plan = get_object_or_404(PricingPlan, id=appointment_data["plan_id"], is_active=True)

    return render(request, "dummy_payment.html", {"plan": plan, "amount": plan.price, "appointment_data": appointment_data})


def dummy_payment_success(request):
    appointment_data = request.session.get("appointment_data")

    if not appointment_data or not appointment_data.get("plan_id"):
        messages.error(request, "Appointment information not found.")
        return redirect("pricing")

    plan = get_object_or_404(PricingPlan, id=appointment_data["plan_id"], is_active=True)
    transaction_id = "ASTRO" + get_random_string(10).upper()

    appointment = Appointment.objects.create(
        plan=plan,
        full_name=appointment_data["full_name"],
        phone=appointment_data["phone"],
        date_of_birth=appointment_data["date_of_birth"],
        time_of_birth=appointment_data["time_of_birth"],
        gender=appointment_data["gender"],
        birth_place=appointment_data["birth_place"],
        consultation_date=appointment_data["consultation_date"] or None,
        language=appointment_data["language"],
        question=appointment_data["question"],
        status="Confirmed",
    )

    payment = Payment.objects.create(appointment=appointment, amount=plan.price, transaction_id=transaction_id, status="Success")

    del request.session["appointment_data"]

    return render(request, "appointment_success.html", {"appointment": appointment, "payment": payment})

    
def dummy_payment_failed(request):
    request.session.pop("appointment_data", None)
    return render(request, "payment_failed.html")