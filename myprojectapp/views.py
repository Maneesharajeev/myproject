from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.db import connection
from django.db.models import Count



from django.shortcuts import render, redirect, get_object_or_404
from .models import *

def get_data(request):
    return HttpResponse("Working")

def home(request):
    return render(request, 'home.html')

def index(request):
    return render(request, 'index.html')


def preorder(request):
   return render(request, 'preorder.html')

from django.shortcuts import render
from django.http import HttpResponse


def preorderaction(request):

    cursor = connection.cursor()

    na = request.POST['name']
    ph = request.POST['phone']
    em = request.POST['email']
    ad = request.POST['address']
    sa = request.POST['saree']
    co = request.POST['color']
    qu = request.POST['quantity']
    de = request.POST['delivery_date']
    pi = request.POST['priority']

    sql = "insert into myprojectapp_customer(name,phone,email,address,saree,color,quantity,delivery_date,priority) values('%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (na, ph, em, ad, sa, co, qu, de,pi)

    cursor.execute(sql)

    msg = "<script>alert('Order Placed Successfully');window.location='/preorder/';</script>"

    return HttpResponse(msg)


def preorders(request):

    data = customer.objects.all()

    return render(request, 'preorders.html', {'data': data})



def admin_dashboard(request):
    orders = customer.objects.all()

    return render(request, 'admin_dashboard.html', {'orders': orders})


def assign_woker(request):
    worker = Worker.objects.all()

    return render(request, 'assign_worker.html', {'worker': worker})


# Assign Worker

def assign_workeraction(request):

    cursor = connection.cursor()

    na = request.POST['name']
    ph = request.POST['phone']
    ad = request.POST['address']
    wo = request.POST['work_type']
    pe = request.POST['personal_id']
    sa = request.POST['salary']
    
    sql = "insert into myprojectapp_worker(name,phone,address,work_type,personal_id,salary) values('%s','%s','%s','%s','%s','%s')" % (na, ph, ad, wo, pe, sa)

    cursor.execute(sql)

    msg = "<script>alert('woker assigned Successfully');window.location='/assign_worker/';</script>"

    return HttpResponse(msg)

def worker(request):

    data = Worker.objects.all()

    return render(request, 'workers.html', {'data': data})


def workers(request, id):

    preorder = customer.objects.get(id=id)

    data = Worker.objects.all()

    cursor = connection.cursor()

    sql = """
    SELECT
        w.id,
        w.name,
        w.phone,
        COALESCE(COUNT(DISTINCT a.preorder_id), 0) AS current_orders

    FROM myprojectapp_worker w

    LEFT JOIN myprojectapp_assigned_work a
    ON w.id = a.worker_id

    GROUP BY
        w.id,
        w.name,
        w.phone

    ORDER BY current_orders ASC
    """

    cursor.execute(sql)

    workers = cursor.fetchall()

    data = []

    for i in workers:

        row = {
            'id': i[0],
            'name': i[1],
            'phone': i[2],
            'current_orders': i[3] if i[3] else 0
        }

        data.append(row)

    return render(request, 'selectwoker.html', {
        'preorder': preorder,
        'data': data
    })

from django.shortcuts import redirect

from .models import customer, Worker, Assigned_Work

def assign(request):
    data=Assigned_Work.objects.all()
    return render(request, 'selectwoker.html', {'data': data})





from django.db import connection



# SHOW SELECT WORKER PAGE

def select_worker(request, id):

    # Get preorder/customer details
    preorder = get_object_or_404(customer, id=id)

    cursor = connection.cursor()

    sql = """
    SELECT
        w.id,
        w.name,
        w.phone,

        COALESCE(COUNT(DISTINCT a.preorder_id), 0) AS current_orders
    FROM myprojectapp_worker w

    LEFT JOIN myprojectapp_assigned_work a
    ON w.id = a.worker_id

    GROUP BY
        w.id,
        w.name,
        w.phone

    ORDER BY current_orders ASC
    """

    cursor.execute(sql)

    workers = cursor.fetchall()

    data = []

    for i in workers:

        row = {
            'id': i[0],
            'name': i[1],
            'phone': i[2],
            'current_orders': i[3] if i[3] else 0
        }

        data.append(row)

    context = {
        'preorder': preorder,
        'data': data
    }

    return render(request, 'selectwoker.html', context)


# ASSIGN ORDER TO WORKER

def assign_order(request, customer_id, worker_id):

    preorder = get_object_or_404(customer, id=customer_id)

    worker = get_object_or_404(Worker, id=worker_id)

    # prevent duplicate assignment
    already_exists = Assigned_Work.objects.filter(
        preorder_id=customer_id,
        worker_id=worker_id
    ).exists()

    if not already_exists:

        Assigned_Work.objects.create(
            preorder_id=customer_id,
            worker_id=worker_id,
            worker_name=worker.name
            
        )

    return redirect(f'/select_worker/{customer_id}/')





def loginaction(request):

    if request.method == 'POST':

        personal_id = request.POST['personal_id']

        name = request.POST.get('x_user_784')

        # ADMIN LOGIN

        if name == "admin@gmail.com" and personal_id == "admin":

            request.session['admin'] = True

            return redirect('/admin_dashboard/')

        # WORKER LOGIN

        cursor = connection.cursor()

        sql = """
        SELECT *
        FROM myprojectapp_worker
        WHERE personal_id = %s
        AND name = %s
        """

        cursor.execute(sql, [personal_id, name])

        worker = cursor.fetchone()

        if worker:

            request.session['worker_id'] = worker[0]

            return redirect('/worker_dashboard/')

        else:

            return render(
                request,
                'home.html',
                {
                    'error': 'Invalid Username or Personal ID'
                }
            )

    return render(request, 'home.html')

def worker_dashboard(request):

    worker_id = request.session.get('worker_id')

    data = Assigned_Work.objects.filter(
        worker_id=worker_id,
        work_status='In Progress'
    )

    return render(
        request,
        'worker_dashboard.html',
        {
            'data': data
        }
    )

from .models import Assigned_Work


def neworders(request):

    worker_id = request.session.get('worker_id')

    data = Assigned_Work.objects.filter(
        worker_id=worker_id,
        work_status='Pending'
    )

    return render(
        request,
        'neworders.html',
        {
            'data': data
        }
    )

from django.shortcuts import redirect, get_object_or_404

def accept_order(request, id):

    work = get_object_or_404(Assigned_Work, id=id)

    work.work_status = 'In Progress'

    work.save()

    return redirect('/worker_dashboard/')

def completed_order(request, id):

    work = Assigned_Work.objects.get(id=id)

    work.work_status = 'Completed'

    work.save()

    return redirect('/worker_dashboard/')

def completedorders(request):

    worker_id = request.session.get('worker_id')

    data = Assigned_Work.objects.filter(
        worker_id=worker_id,
        work_status='Completed'
    )

    return render(
        request,
        'completedorders.html',
        {
            'data': data
        }
    )



def trackorder(request):

    workers = Worker.objects.all()

    for worker in workers:

        # TOTAL ASSIGNED ORDERS

        total_orders = Assigned_Work.objects.filter(
            worker=worker
        ).count()

        # CURRENT ORDERS

        current_orders = Assigned_Work.objects.filter(
            worker=worker,
            work_status='In Progress'
        ).count()

        # COMPLETED ORDERS

        completed_orders = Assigned_Work.objects.filter(
            worker=worker,
            work_status='Completed'
        ).count()

        # STORE VALUES

        worker.total_count = total_orders

        worker.current_count = current_orders

        worker.completed_count = completed_orders

    return render(
        request,
        'trackorder.html',
        {
            'workers': workers
        }
    )

def worker_order(request, worker_id):

    worker = get_object_or_404(Worker, id=worker_id)

    orders = Assigned_Work.objects.filter(
        worker=worker
    )

    return render(
        request,
        'worker_order.html',
        {
            'worker': worker,
            'orders': orders
        }
    )

def current_order(request, id):

    worker = get_object_or_404(Worker, id=id)

    orders = Assigned_Work.objects.filter(
        worker=worker,
        work_status='In Progress'
    )

    return render(
        request,
        'current_order.html',
        {
            'worker': worker,
            'orders': orders
        }
    )


def completed_order(request, id):

    worker = get_object_or_404(Worker, id=id)

    orders = Assigned_Work.objects.filter(
        worker=worker,
        work_status='Completed'
    )

    return render(
        request,
        'completed_order.html',
        {
            'worker': worker,
            'orders': orders
        }
    )


def completed_ordert(request, id):

    work = Assigned_Work.objects.get(id=id)

    work.work_status = 'Completed'

    work.save()

    return redirect('/completedorders/')

def editworker(request, id):

    worker = Worker.objects.get(id=id)
    return render(request, 'editworker.html', {'worker': worker})

def update_worker(request, id):
    worker = Worker.objects.get(id=id)

    worker.name = request.POST['name']
    worker.phone = request.POST['phone']
    worker.address = request.POST['address']
    worker.work_type = request.POST['work_type']
    worker.personal_id = request.POST['personal_id']
    worker.salary = request.POST['salary']

    worker.save()

    return redirect('/workers/')

def delete_worker(request, id):
    Worker.objects.get(id=id).delete()
    return redirect('/workers/')