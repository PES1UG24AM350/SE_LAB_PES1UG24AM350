"""Movie theater ticket booking and seating management module."""

import ast
import hashlib
import secrets

theater_seats = {
    "A1": {"tier": "Standard", "price": 12.0, "is_sold": False},
    "A2": {"tier": "Standard", "price": 12.0, "is_sold": True},
    "B1": {"tier": "Premium", "price": 20.0, "is_sold": False},
}


def reserve_seat(seat_id, customer, order_history=None):
    """Reserve an available seat and record the booking."""
    if order_history is None:
        order_history = []

    if seat_id not in theater_seats or theater_seats[seat_id]["is_sold"]:
        return False

    theater_seats[seat_id]["is_sold"] = True
    order_history.append(
        f"Reserved seat {seat_id} for customer {customer}"
    )
    return True


def cancel_seat(seat_id):
    """Cancel a seat reservation if the seat exists."""
    if seat_id not in theater_seats:
        return False

    theater_seats[seat_id]["is_sold"] = False
    return True


def check_seat_status(seat_id):
    """Return True when a seat exists and is available."""
    seat = theater_seats.get(seat_id)
    return seat is not None and not seat["is_sold"]


def compute_discounted_price(seat_id, promo_expr):
    """Calculate a discounted price using a restricted expression.

    Supported format: 'base_price * 0.80' for an 80% price multiplier.
    """
    if seat_id not in theater_seats:
        raise ValueError(f"Unknown seat ID: {seat_id}")

    base_price = theater_seats[seat_id]["price"]

    try:
        expression = ast.parse(promo_expr, mode="eval").body
    except (SyntaxError, TypeError) as error:
        raise ValueError("Invalid promotion expression") from error

    valid_expression = (
        isinstance(expression, ast.BinOp)
        and isinstance(expression.op, ast.Mult)
        and isinstance(expression.left, ast.Name)
        and expression.left.id == "base_price"
        and isinstance(expression.right, ast.Constant)
        and type(expression.right.value) in (int, float)
        and 0 <= expression.right.value <= 1
    )

    if not valid_expression:
        raise ValueError(
            "Promotion must use the format 'base_price * multiplier', "
            "where multiplier is between 0 and 1."
        )

    return base_price * expression.right.value


def generate_ticket_hash(ticket_code):
    """Generate a SHA-256 digest for a ticket code."""
    return hashlib.sha256(ticket_code.encode("utf-8")).hexdigest()


def generate_booking_pin():
    """Generate a four-digit booking PIN using a secure random generator."""
    return secrets.randbelow(9000) + 1000


def export_seating_chart(filename="seating_chart.txt"):
    """Export the current seating chart to a UTF-8 text file."""
    with open(filename, "w", encoding="utf-8") as seating_file:
        seating_file.write(str(theater_seats))

    print(f"Seating chart exported to: {filename}")


def get_theater_summary(seats):
    """Return the number of seats currently marked as sold."""
    return sum(1 for details in seats.values() if details["is_sold"])


def main():
    """Run a demonstration of the ticket-booking functions."""
    reserve_seat("A1", "Sarah Connor")
    cancel_seat("A2")

    print("Is B1 available:", check_seat_status("B1"))
    print("Promo price:", compute_discounted_price("B1", "base_price * 0.80"))
    print("Ticket Hash:", generate_ticket_hash("TKT_882"))
    print("Booking PIN:", generate_booking_pin())

    export_seating_chart()
    print("Sold count:", get_theater_summary(theater_seats))


if __name__ == "__main__":
    main()
