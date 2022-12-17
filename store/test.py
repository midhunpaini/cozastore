def sales_report_yearly(request):
    if 'admin_id' in request.session:

        some_day_last_week = datetime.date.today() - datetime.timedelta(days=365)

        order_today = OrderTable.objects.filter(date_delivered__gte=some_day_last_week,
                                                date_delivered__lte=datetime.date.today(), status='Delivered').order_by(
            'id')

        p = Paginator(order_today, 7)
        page_num = request.GET.get('page', 1)

        # print("NUMBER OF PAGES")
        # print(p.num_pages)
        try:

            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)
        # print(page)
        print(some_day_last_week)
        # OrderTable.objects.filter(date_delivered = datetime. date. today() )
        revenue = 0
        # print(order_today)
        for i in order_today:
            revenue = i.amount + revenue

        return render(request, 'admin/sales_report_yearly.html', {'order_today': order_today, 'revenue': revenue})
    else:
        return redirect(admin_login)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def export_csv_yearly(request):
    if 'admin_id' in request.session:
        some_day_last_week = datetime.date.today() - datetime.timedelta(days=365)

        orders = OrderTable.objects.filter(date_delivered__gte=some_day_last_week,
                                           date_delivered__lte=datetime.date.today(), status='Delivered').order_by('id')

        response = HttpResponse(content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename=Orders' + \
                                          str(datetime.datetime.now()) + '.csv'

        writer = csv.writer(response)

        writer.writerow(
            ['Order Id', 'Amount', 'Name', 'Phone number', "Payment method" 'Ordered date', 'Delivereed Date'])

        for order in orders:
            writer.writerow(
                [order.id, order.amount, order.name, order.phone_number, order.payment_method, order.created_at,
                 order.date_delivered])

        return response
    else:
        return redirect(admin_login)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def export_csv_weekly(request):
    if 'admin_id' in request.session:
        some_day_last_week = datetime.date.today() - datetime.timedelta(days=7)

        orders = OrderTable.objects.filter(date_delivered__gte=some_day_last_week,
                                           date_delivered__lte=datetime.date.today(), status='Delivered').order_by('id')

        response = HttpResponse(content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename=Orders' + \
                                          str(datetime.datetime.now()) + '.csv'

        writer = csv.writer(response)

        writer.writerow(
            ['Order Id', 'Amount', 'Name', 'Phone number', "Payment method" 'Ordered date', 'Delivereed Date'])

        for order in orders:
            writer.writerow(
                [order.id, order.amount, order.name, order.phone_number, order.payment_method, order.created_at,
                 order.date_delivered])

        return response
    else:
        return redirect(admin_login)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def export_csv_daily(request):
    if 'admin_id' in request.session:

        orders = OrderTable.objects.filter(date_delivered=datetime.date.today(), status='Delivered').order_by('id')

        response = HttpResponse(content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename=Orders' + \
                                          str(datetime.datetime.now()) + '.csv'

        writer = csv.writer(response)

        writer.writerow(
            ['Order Id', 'Amount', 'Name', 'Phone number', "Payment method" 'Ordered date', 'Delivereed Date'])

        for order in orders:
            writer.writerow(
                [order.id, order.amount, order.name, order.phone_number, order.payment_method, order.created_at,
                 order.date_delivered])

        return response
    else:
        return redirect(admin_login)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def export_csv_custom(request):
    if 'admin_id' in request.session:

        startdate = request.GET['startdate']

        enddate = request.GET['enddate']

        orders = OrderTable.objects.filter(date_delivered_gte=startdate, date_delivered_lte=enddate,
                                           status='Delivered').order_by('id')

        response = HttpResponse(content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename=Orders' + \
                                          str(datetime.datetime.now()) + '.csv'

        writer = csv.writer(response)

        writer.writerow(
            ['Order Id', 'Amount', 'Name', 'Phone number', "Payment method" 'Ordered date', 'Delivereed Date'])

        for order in orders:
            writer.writerow(
                [order.id, order.amount, order.name, order.phone_number, order.payment_method, order.created_at,
                 order.date_delivered])

        return response
    else:
        return redirect(admin_login)