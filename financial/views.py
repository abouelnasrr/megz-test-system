from django.shortcuts import render, redirect
from .models import Expense
import json
from .forms import ExpenseForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import datetime
from django.utils.timezone import now, timedelta
from shop.models import History  # For receipts
from django.db.models.functions import TruncMonth


@login_required
def financial_page(request):
    expenses = Expense.objects.all()
    receipts = History.objects.all()

    # Get filter input
    date = request.GET.get("date")
    month = request.GET.get("month")
    days = request.GET.get("days")

    filtered_expenses = expenses
    filtered_receipts = receipts

    if date:
        filtered_expenses = expenses.filter(created_at__date=date)
        filtered_receipts = receipts.filter(created_at__date=date)

    elif month:
        year, month = map(int, month.split("-"))
        filtered_expenses = expenses.filter(created_at__year=year, created_at__month=month)
        filtered_receipts = receipts.filter(created_at__year=year, created_at__month=month)

    elif days:
        try:
            days_back = int(days)
            date_from = now() - timedelta(days=days_back)
            filtered_expenses = expenses.filter(created_at__gte=date_from)
            filtered_receipts = receipts.filter(created_at__gte=date_from)
        except:
            pass

    total_expenses = filtered_expenses.aggregate(Sum("amount"))["amount__sum"] or 0
    total_revenue = filtered_receipts.aggregate(Sum("total"))["total__sum"] or 0

    context = {
        "filtered_expenses": filtered_expenses,
        "filtered_receipts": filtered_receipts,
        "total_expenses": total_expenses,
        "total_revenue": total_revenue,
    }

    # Group and sum income & expenses by month
    monthly_income = (
        History.objects
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total_income=Sum("total"))
        .order_by("month")
    )

    monthly_expenses = (
        Expense.objects
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total_expense=Sum("amount"))
        .order_by("month")
    )

    # Merge them by month
    monthly_data = {}
    for entry in monthly_income:
        month = entry["month"].strftime("%Y-%m")
        monthly_data[month] = {"income": entry["total_income"], "expense": 0}

    for entry in monthly_expenses:
        month = entry["month"].strftime("%Y-%m")
        if month not in monthly_data:
            monthly_data[month] = {"income": 0, "expense": entry["total_expense"]}
        else:
            monthly_data[month]["expense"] = entry["total_expense"]

    # Add net profit
    for m in monthly_data:
        monthly_data[m]["net"] = float(monthly_data[m]["income"]) - float(monthly_data[m]["expense"])

    context["monthly_data"] = monthly_data
    # Convert to sorted list for consistent charting
    sorted_months = sorted(monthly_data.keys())

    sorted_months = sorted(monthly_data.keys())
    context["months"] = sorted_months
    context["income_data"] = [float(monthly_data[m]["income"]) for m in sorted_months]
    context["expense_data"] = [float(monthly_data[m]["expense"]) for m in sorted_months]
    context["net_data"] = [float(monthly_data[m]["net"]) for m in sorted_months]

    # ✅ Safe JSON for Chart.js
    context["months_json"] = json.dumps(context["months"])
    context["income_data_json"] = json.dumps(context["income_data"])
    context["expense_data_json"] = json.dumps(context["expense_data"])
    context["net_data_json"] = json.dumps(context["net_data"])
    return render(request, "financial/financial_dashboard.html", context)



@login_required
def expenses_page(request):
    form = ExpenseForm()

    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expenses_page')

    query = request.GET.get('q')
    if query:
        expenses = Expense.objects.filter(
            Q(name__icontains=query) |
            Q(expense_type__icontains=query) |
            Q(notes__icontains=query)
        ).order_by('-created_at')
    else:
        expenses = Expense.objects.all().order_by('-created_at')

    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'form': form,
        'expenses': page_obj,
        'query': query,
    }
    return render(request, 'financial/expenses.html', context)


