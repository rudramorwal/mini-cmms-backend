import random
from datetime import timedelta, datetime, timezone
from app.database import SessionLocal, engine, Base
from app.models.machine import Machine
from app.models.technician import Technician
from app.models.work_order import WorkOrder
from app.models.comment import Comment

def utcnow():
    return datetime.now(timezone.utc)

def seed_data():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    machines_data = [
        ('CNC Lathe L001', 'Lathe', 'Floor 1'),
        ('Hydraulic Press H002', 'Press', 'Zone A'),
        ('Milling Machine M003', 'Mill', 'Floor 2'),
        ('Drill Press D004', 'Drill', 'Zone B'),
        ('Surface Grinder G005', 'Grinder', 'Floor 3'),
        ('Water Pump P006', 'Pump', 'Zone C'),
        ('AC Motor M007', 'Motor', 'Floor 1'),
        ('Belt Conveyor C008', 'Conveyor', 'Zone D'),
        ('Welding Robot W009', 'Welding Robot', 'Floor 2'),
        ('Air Compressor A010', 'Compressor', 'Zone A'),
        ('CNC Lathe L011', 'Lathe', 'Floor 1'),
        ('Hydraulic Press H012', 'Press', 'Zone B'),
        ('Milling Machine M013', 'Mill', 'Floor 3'),
        ('Centrifugal Pump P014', 'Pump', 'Zone C'),
        ('Roller Conveyor C015', 'Conveyor', 'Zone D'),
    ]
    
    machines = []
    for name, mtype, loc in machines_data:
        m = Machine(name=name, type=mtype, location=loc)
        db.add(m)
        machines.append(m)
    
    technicians_data = [
        ('Ramesh Kumar', 'Electrical'),
        ('Sunil Sharma', 'Mechanical'),
        ('Priya Patel', 'Hydraulic'),
        ('Amit Singh', 'Electrical'),
        ('Deepa Nair', 'Mechanical'),
        ('Vikram Rao', 'General')
    ]
    
    technicians = []
    for name, spec in technicians_data:
        t = Technician(name=name, specialization=spec, email=f"{name.split()[0].lower()}@example.com")
        db.add(t)
        technicians.append(t)
        
    db.commit()
    
    titles = [
        'Spindle motor overheating', 'Hydraulic pressure drop', 'Belt conveyor alignment issue',
        'Coolant leak detected', 'Bearing noise in drive shaft', 'Electrical panel short circuit',
        'Vibration during operation', 'Sensor failure', 'Pneumatic valve stuck', 'Routine maintenance'
    ]
    
    now = utcnow()
    
    # 3 open
    for _ in range(3):
        m = random.choice(machines)
        opened = now - timedelta(hours=random.randint(1, 24))
        wo = WorkOrder(
            machine_id=m.id,
            title=random.choice(titles),
            description="Needs immediate attention.",
            priority=random.choice(['critical', 'high', 'low']),
            status='open',
            opened_at=opened,
            created_at=opened,
            updated_at=opened
        )
        db.add(wo)
        
    # 4 assigned
    for _ in range(4):
        m = random.choice(machines)
        t = random.choice(technicians)
        opened = now - timedelta(days=random.randint(1, 5))
        assigned = opened + timedelta(hours=random.randint(1, 10))
        wo = WorkOrder(
            machine_id=m.id,
            technician_id=t.id,
            title=random.choice(titles),
            description="Assigned to tech.",
            priority=random.choice(['critical', 'high', 'low']),
            status='assigned',
            opened_at=opened,
            assigned_at=assigned,
            created_at=opened,
            updated_at=assigned
        )
        db.add(wo)
        
    # 3 in_progress
    for _ in range(3):
        m = random.choice(machines)
        t = random.choice(technicians)
        opened = now - timedelta(days=random.randint(3, 10))
        assigned = opened + timedelta(hours=random.randint(1, 5))
        inprog = assigned + timedelta(hours=random.randint(1, 5))
        wo = WorkOrder(
            machine_id=m.id,
            technician_id=t.id,
            title=random.choice(titles),
            description="Work is ongoing.",
            priority=random.choice(['critical', 'high', 'low']),
            status='in_progress',
            opened_at=opened,
            assigned_at=assigned,
            in_progress_at=inprog,
            created_at=opened,
            updated_at=inprog
        )
        db.add(wo)
        
    # 15 closed
    for _ in range(15):
        m = random.choice(machines)
        t = random.choice(technicians)
        opened = now - timedelta(days=random.randint(5, 30))
        assigned = opened + timedelta(hours=random.randint(1, 5))
        inprog = assigned + timedelta(hours=random.randint(1, 5))
        closed = opened + timedelta(hours=random.randint(1, 72))
        wo = WorkOrder(
            machine_id=m.id,
            technician_id=t.id,
            title=random.choice(titles),
            description="Issue resolved.",
            priority=random.choice(['critical', 'high', 'low']),
            status='closed',
            opened_at=opened,
            assigned_at=assigned,
            in_progress_at=inprog,
            closed_at=closed,
            created_at=opened,
            updated_at=closed
        )
        db.add(wo)
        
    db.commit()
    
    # comments
    wos = db.query(WorkOrder).all()
    for wo in wos:
        for _ in range(random.randint(2, 4)):
            c = Comment(
                work_order_id=wo.id,
                author=random.choice(["System", "Operator", wo.technician.name if wo.technician else "User"]),
                body="This is a test comment for the work order.",
                created_at=wo.opened_at + timedelta(minutes=random.randint(10, 60))
            )
            db.add(c)
            
    db.commit()
    print("Seeding complete: 15 machines, 6 technicians, 25 work orders seeded.")
    db.close()

if __name__ == "__main__":
    seed_data()
