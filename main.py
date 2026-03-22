from fastapi import FastAPI, Query, Response, status
from pydantic import BaseModel, Field

app = FastAPI()

# -----------------------------
# DATA (modified but same structure)
# -----------------------------

rooms = [
    {"id": 1, "room_number": "A101", "type": "Single", "price_per_night": 1300, "floor": 1, "is_available": True},
    {"id": 2, "room_number": "A102", "type": "Double", "price_per_night": 2200, "floor": 1, "is_available": True},
    {"id": 3, "room_number": "B201", "type": "Suite", "price_per_night": 4200, "floor": 2, "is_available": False},
    {"id": 4, "room_number": "B202", "type": "Deluxe", "price_per_night": 3100, "floor": 2, "is_available": True},
    {"id": 5, "room_number": "C301", "type": "Single", "price_per_night": 1600, "floor": 3, "is_available": True},
    {"id": 6, "room_number": "C302", "type": "Suite", "price_per_night": 5200, "floor": 3, "is_available": True},
]

bookings = []
booking_counter = 1


# -----------------------------
# MODELS
# -----------------------------

class BookingRequest(BaseModel):
    guest_name: str = Field(..., min_length=2)
    room_id: int = Field(..., gt=0)
    nights: int = Field(..., gt=0, le=30)
    phone: str = Field(..., min_length=10)
    meal_plan: str = "none"
    early_checkout: bool = False


class NewRoom(BaseModel):
    room_number: str = Field(..., min_length=1)
    type: str = Field(..., min_length=2)
    price_per_night: int = Field(..., gt=0)
    floor: int = Field(..., gt=0)
    is_available: bool = True


# -----------------------------
# HELPERS
# -----------------------------

def find_room(room_id: int):
    return next((r for r in rooms if r["id"] == room_id), None)


def calculate_stay_cost(price, nights, meal_plan, early_checkout):
    base = price * nights

    extra = 0
    if meal_plan == "breakfast":
        extra = 500 * nights
    elif meal_plan == "all-inclusive":
        extra = 1200 * nights

    total = base + extra

    discount = 0
    if early_checkout:
        discount = total * 0.10
        total -= discount

    return total, discount


def filter_rooms_logic(type=None, max_price=None, floor=None, is_available=None):
    result = rooms[:]

    if type is not None:
        result = [r for r in result if r["type"] == type]

    if max_price is not None:
        result = [r for r in result if r["price_per_night"] <= max_price]

    if floor is not None:
        result = [r for r in result if r["floor"] == floor]

    if is_available is not None:
        result = [r for r in result if r["is_available"] == is_available]

    return result


# -----------------------------
# DAY 1
# -----------------------------

@app.get("/")
def home():
    return {"message": "Welcome to Grand Stay Hotel"}


@app.get("/rooms")
def get_rooms():
    available_count = sum(1 for r in rooms if r["is_available"])
    return {
        "rooms": rooms,
        "total": len(rooms),
        "available_count": available_count
    }


@app.get("/rooms/summary")
def rooms_summary():
    available = sum(1 for r in rooms if r["is_available"])
    occupied = len(rooms) - available

    prices = [r["price_per_night"] for r in rooms]

    type_breakdown = {}
    for r in rooms:
        type_breakdown[r["type"]] = type_breakdown.get(r["type"], 0) + 1

    return {
        "total_rooms": len(rooms),
        "available": available,
        "occupied": occupied,
        "cheapest_price": min(prices),
        "highest_price": max(prices),
        "type_breakdown": type_breakdown
    }


@app.get("/rooms/filter")
def filter_rooms(
    type: str = Query(None),
    max_price: int = Query(None),
    floor: int = Query(None),
    is_available: bool = Query(None),
):
    result = filter_rooms_logic(type, max_price, floor, is_available)
    return {"rooms": result, "count": len(result)}


@app.get("/rooms/search")
def search_rooms(keyword: str = Query(...)):
    result = [
        r for r in rooms
        if keyword.lower() in r["room_number"].lower()
        or keyword.lower() in r["type"].lower()
    ]

    if not result:
        return {"message": "No rooms found", "results": []}

    return {"results": result, "total_found": len(result)}


@app.get("/rooms/sort")
def sort_rooms(
    sort_by: str = Query("price_per_night"),
    order: str = Query("asc"),
):
    if sort_by not in ["price_per_night", "floor", "type"]:
        return {"error": "Invalid sort field"}

    if order not in ["asc", "desc"]:
        return {"error": "Invalid order"}

    sorted_rooms = sorted(rooms, key=lambda r: r[sort_by], reverse=(order == "desc"))
    return {"rooms": sorted_rooms}


@app.get("/rooms/page")
def paginate_rooms(page: int = Query(1, ge=1), limit: int = Query(2, ge=1)):
    start = (page - 1) * limit
    end = start + limit

    return {
        "page": page,
        "limit": limit,
        "total": len(rooms),
        "total_pages": -(-len(rooms) // limit),
        "rooms": rooms[start:end],
    }


@app.get("/rooms/browse")
def browse_rooms(
    keyword: str = Query(None),
    sort_by: str = Query("price_per_night"),
    order: str = Query("asc"),
    page: int = Query(1),
    limit: int = Query(3),
):
    result = rooms[:]

    if keyword:
        result = [
            r for r in result
            if keyword.lower() in r["room_number"].lower()
            or keyword.lower() in r["type"].lower()
        ]

    result = sorted(result, key=lambda r: r[sort_by], reverse=(order == "desc"))

    start = (page - 1) * limit
    end = start + limit

    return {
        "total": len(result),
        "page": page,
        "rooms": result[start:end],
    }


@app.get("/rooms/{room_id}")
def get_room(room_id: int):
    room = find_room(room_id)
    if not room:
        return {"error": "Room not found"}
    return {"room": room}


@app.get("/bookings")
def get_bookings():
    return {"bookings": bookings, "total": len(bookings)}


# -----------------------------
# BOOKINGS
# -----------------------------

@app.post("/bookings")
def create_booking(data: BookingRequest):
    global booking_counter

    room = find_room(data.room_id)

    if not room:
        return {"error": "Room not found"}

    if not room["is_available"]:
        return {"error": "Room is already occupied"}

    total, discount = calculate_stay_cost(
        room["price_per_night"],
        data.nights,
        data.meal_plan,
        data.early_checkout
    )

    room["is_available"] = False

    booking = {
        "booking_id": booking_counter,
        "guest_name": data.guest_name,
        "room": room,
        "nights": data.nights,
        "meal_plan": data.meal_plan,
        "total_cost": total,
        "discount": discount,
        "status": "confirmed"
    }

    bookings.append(booking)
    booking_counter += 1

    return {"message": "Booking confirmed", "booking": booking}


# -----------------------------
# CRUD
# -----------------------------

@app.post("/rooms")
def add_room(new_room: NewRoom, response: Response):
    if any(r["room_number"] == new_room.room_number for r in rooms):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": "Room number already exists"}

    new_id = max(r["id"] for r in rooms) + 1

    room = new_room.dict()
    room["id"] = new_id

    rooms.append(room)
    response.status_code = status.HTTP_201_CREATED

    return {"room": room}


@app.put("/rooms/{room_id}")
def update_room(
    room_id: int,
    response: Response,
    price_per_night: int = Query(None),
    is_available: bool = Query(None),
):
    room = find_room(room_id)

    if not room:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Room not found"}

    if price_per_night is not None:
        room["price_per_night"] = price_per_night

    if is_available is not None:
        room["is_available"] = is_available

    return {"room": room}


@app.delete("/rooms/{room_id}")
def delete_room(room_id: int, response: Response):
    room = find_room(room_id)

    if not room:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Room not found"}

    if not room["is_available"]:
        return {"error": "Cannot delete occupied room"}

    rooms.remove(room)
    return {"message": "Room deleted"}


# -----------------------------
# CHECK-IN / CHECK-OUT
# -----------------------------

@app.post("/checkin/{booking_id}")
def checkin(booking_id: int):
    for b in bookings:
        if b["booking_id"] == booking_id:
            b["status"] = "checked_in"
            return {"booking": b}
    return {"error": "Booking not found"}


@app.post("/checkout/{booking_id}")
def checkout(booking_id: int):
    for b in bookings:
        if b["booking_id"] == booking_id:
            b["status"] = "checked_out"

            room = find_room(b["room"]["id"])
            if room:
                room["is_available"] = True

            return {"booking": b}
    return {"error": "Booking not found"}


@app.get("/bookings/active")
def active_bookings():
    active = [b for b in bookings if b["status"] in ["confirmed", "checked_in"]]
    return {"active": active}


@app.get("/bookings/search")
def search_bookings(keyword: str = Query(...)):
    result = [b for b in bookings if keyword.lower() in b["guest_name"].lower()]
    return {"results": result}


@app.get("/bookings/sort")
def sort_bookings(
    sort_by: str = Query("total_cost"),
    order: str = Query("asc"),
):
    sorted_b = sorted(bookings, key=lambda b: b[sort_by], reverse=(order == "desc"))
    return {"bookings": sorted_b}