from sqlalchemy.orm import Session
from sqlalchemy import func, not_
from app.models.work_order import WorkOrder
from app.models.machine import Machine

def get_dashboard_stats(db: Session) -> dict:
    open_count = db.query(WorkOrder).filter(WorkOrder.status != 'closed').count()
    total_count = db.query(WorkOrder).count()

    closed_wos = db.query(WorkOrder).filter(WorkOrder.status == 'closed', WorkOrder.opened_at.isnot(None), WorkOrder.closed_at.isnot(None)).all()
    
    machine_stats = {}
    for wo in closed_wos:
        if wo.machine_id not in machine_stats:
            machine_stats[wo.machine_id] = {'name': wo.machine.name, 'total_hours': 0.0, 'count': 0}
        
        diff = wo.closed_at - wo.opened_at
        hours = diff.total_seconds() / 3600.0
        machine_stats[wo.machine_id]['total_hours'] += hours
        machine_stats[wo.machine_id]['count'] += 1

    mttr_by_machine = []
    for mid, data in machine_stats.items():
        if data['count'] > 0:
            mttr = data['total_hours'] / data['count']
            mttr_by_machine.append({
                'machine_id': mid,
                'machine_name': data['name'],
                'mttr_hours': round(mttr, 2),
                'repair_count': data['count']
            })

    mttr_by_machine.sort(key=lambda x: x['machine_id'])
    worst_5 = sorted(mttr_by_machine, key=lambda x: x['mttr_hours'], reverse=True)[:5]

    return {
        'open_work_orders': open_count,
        'total_work_orders': total_count,
        'mttr_by_machine': mttr_by_machine,
        'worst_5_machines': worst_5
    }
