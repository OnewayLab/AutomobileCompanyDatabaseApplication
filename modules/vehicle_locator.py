from typing import Union
from datetime import date

from database import db
from database.models import *


def get_vehicles(
    bid: Union[int, None] = None,
    mid: Union[int, None] = None,
    color: Union[str, None] = None,
    engine: Union[str, None] = None,
    transmission: Union[str, None] = None,
):
    """Get vehicles according to the given conditions

    Args:
        bid: brand id
        mid: model id
        color: color
        engine: engine
        transmission: transmission
    """
    vehicles = Vehicle.query
    record = QueryRecord.query.filter_by(date=date.today())
    if mid:
        vehicles = vehicles.filter_by(mid=mid)
        record = record.filter_by(mid=mid)
    if color:
        vehicles = vehicles.filter_by(color=color)
        record = record.filter_by(color=color)
    if engine:
        vehicles = vehicles.filter_by(engine=engine)
        record = record.filter_by(engine=engine)
    if transmission:
        vehicles = vehicles.filter_by(transmission=transmission)
        record = record.filter_by(transmission=transmission)
    if bid:
        vehicles = vehicles.join(Model).join(Brand).filter_by(bid=bid)
        record = record.filter_by(bid=bid)

    record = record.first()
    if record:
        record.count += 1
    else:
        record = QueryRecord(
            date=date.today().isoformat(),
            bid=bid,
            mid=mid,
            color=color,
            engine=engine,
            transmission=transmission,
            count=1,
        )
    db.session.add(record)
    db.session.commit()
    print(vehicles)
    return vehicles.all()
