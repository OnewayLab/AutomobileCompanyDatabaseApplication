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
    dealer_country: Union[str, None] = None,
    dealer_city: Union[str, None] = None,
    is_sold: bool = False,
    select: list[db.Model] = None,
    group_by: list[db.Model] = None
):
    """Get vehicles according to the given conditions

    Args:
        bid: brand id
        mid: model id
        color: color
        engine: engine
        transmission: transmission
        dealer_country: dealer country
        dealer_city: dealer city
        is_sold: whether the vehicle is sold
        select: columns to select
        group_by: columns to group by
    """
    vehicles = (
        db.session.query(*select)
        .select_from(Vehicle)
        .join(Inventory, Dealer, Model, Brand, Option)
        .filter(Inventory.is_sold==is_sold)
    )
    record = QueryRecord.query.filter_by(date=date.today())
    if mid:
        vehicles = vehicles.filter(Model.mid==mid)
        record = record.filter_by(mid=mid)
    if color:
        vehicles = vehicles.filter(Option.color==color)
        record = record.filter_by(color=color)
    if engine:
        vehicles = vehicles.filter(Option.engine==engine)
        record = record.filter_by(engine=engine)
    if transmission:
        vehicles = vehicles.filter(Option.transmission==transmission)
        record = record.filter_by(transmission=transmission)
    if bid:
        vehicles = vehicles.filter(Brand.bid==bid)
        record = record.filter_by(bid=bid)
    if dealer_country:
        vehicles = vehicles.filter(Dealer.country==dealer_country)
    if dealer_city:
        vehicles = vehicles.filter(Dealer.city==dealer_city)
    if group_by:
        vehicles = vehicles.group_by(*group_by)

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
    result = vehicles.all()
    return result
