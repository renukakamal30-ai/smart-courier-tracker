from tracking import CourierTrackingSystem


def print_header(title):
    """Display a formatted section header."""

    print("\n" + "=" * 60)
    print(title.center(60))
    print("=" * 60)


def add_courier(system):
    """Handle adding a new courier."""

    print_header("ADD NEW COURIER")

    sender_name = input("Sender name: ").strip()
    sender_phone = input("Sender phone: ").strip()

    receiver_name = input("Receiver name: ").strip()
    receiver_phone = input("Receiver phone: ").strip()

    origin = input("Origin: ").strip()
    destination = input("Destination: ").strip()

    package_description = input(
        "Package description: "
    ).strip()

    while True:
        weight_input = input("Package weight (kg): ").strip()

        try:
            weight = float(weight_input)

            if weight <= 0:
                print("Weight must be greater than 0.")
                continue

            break

        except ValueError:
            print("Please enter a valid numeric weight.")

    try:
        tracking_id = system.add_courier(
            sender_name=sender_name,
            sender_phone=sender_phone,
            receiver_name=receiver_name,
            receiver_phone=receiver_phone,
            origin=origin,
            destination=destination,
            package_description=package_description,
            weight=weight,
        )

        print("\nCourier added successfully!")
        print(f"Tracking ID: {tracking_id}")

    except Exception as error:
        print(f"\nError adding courier: {error}")


def update_delivery_status(system):
    """Handle updating a courier's delivery status."""

    print_header("UPDATE DELIVERY STATUS")

    tracking_id = input("Enter tracking ID: ").strip().upper()

    courier = system.get_courier(tracking_id)

    if not courier:
        print("\nTracking ID not found.")
        return

    current_status = courier["current_status"]
    next_status = system.get_next_status(current_status)

    print(f"\nCurrent status: {current_status}")

    if next_status is None:
        print("This courier has already been delivered.")
        return

    print(f"Next delivery stage: {next_status}")

    location = input("Current location: ").strip()
    remarks = input("Remarks: ").strip()

    success, message = system.update_status(
        tracking_id=tracking_id,
        new_status=next_status,
        location=location,
        remarks=remarks,
    )

    print(f"\n{message}")


def display_tracking(courier, history, system):
    """Display courier details and tracking history."""

    print_header("COURIER TRACKING DETAILS")

    print(f"Tracking ID       : {courier['tracking_id']}")
    print(f"Sender            : {courier['sender_name']}")
    print(f"Sender Phone      : {courier['sender_phone'] or 'N/A'}")
    print(f"Receiver          : {courier['receiver_name']}")
    print(
        f"Receiver Phone    : "
        f"{courier['receiver_phone'] or 'N/A'}"
    )
    print(f"Origin            : {courier['origin']}")
    print(f"Destination       : {courier['destination']}")
    print(
        f"Package           : "
        f"{courier['package_description'] or 'N/A'}"
    )
    print(
        f"Weight            : "
        f"{courier['weight'] if courier['weight'] is not None else 'N/A'} kg"
    )
    print(f"Current Status    : {courier['current_status']}")
    print(f"Created At        : {courier['created_at']}")
    print(f"Last Updated      : {courier['updated_at']}")

    progress = system.get_status_progress(
        courier["current_status"]
    )

    print(f"Delivery Progress : {progress}%")

    print("\nDelivery Stages:")

    for index, stage in enumerate(system.STATUS_STAGES):
        if stage == courier["current_status"]:
            marker = "● CURRENT"
        else:
            current_index = system.STATUS_STAGES.index(
                courier["current_status"]
            )

            if index < current_index:
                marker = "✓ COMPLETED"
            else:
                marker = "○ PENDING"

        print(f"  {index + 1}. {stage:<20} {marker}")

    print("\nTracking History:")
    print("-" * 60)

    if not history:
        print("No tracking history available.")
        return

    for item in history:
        print(f"Status   : {item['status']}")
        print(f"Location : {item['location'] or 'N/A'}")
        print(f"Remarks  : {item['remarks'] or 'N/A'}")
        print(f"Updated  : {item['updated_at']}")
        print("-" * 60)


def track_courier(system):
    """Handle tracking a courier."""

    print_header("TRACK COURIER")

    tracking_id = input(
        "Enter tracking ID: "
    ).strip().upper()

    courier, history = system.track_courier(tracking_id)

    if not courier:
        print("\nTracking ID not found.")
        return

    display_tracking(
        courier,
        history,
        system,
    )


def list_all_couriers(system):
    """Display all courier records."""

    print_header("ALL COURIERS")

    couriers = system.get_all_couriers()

    if not couriers:
        print("No courier records found.")
        return

    print(
        f"{'Tracking ID':<15}"
        f"{'Sender':<18}"
        f"{'Receiver':<18}"
        f"{'Status':<20}"
    )

    print("-" * 71)

    for courier in couriers:
        print(
            f"{courier['tracking_id']:<15}"
            f"{courier['sender_name'][:17]:<18}"
            f"{courier['receiver_name'][:17]:<18}"
            f"{courier['current_status']:<20}"
        )


def show_delivery_stages(system):
    """Display all available delivery stages."""

    print_header("DELIVERY STAGES")

    for index, stage in enumerate(
        system.STATUS_STAGES,
        start=1,
    ):
        print(f"{index}. {stage}")


def show_menu():
    """Display the main menu."""

    print("\n" + "=" * 60)
    print("        COURIER TRACKING SYSTEM")
    print("=" * 60)

    print("1. Add Courier")
    print("2. Update Delivery Status")
    print("3. Track Courier")
    print("4. View All Couriers")
    print("5. View Delivery Stages")
    print("6. Exit")

    print("=" * 60)


def main():
    """Application entry point."""

    system = CourierTrackingSystem()

    print("\nWelcome to the Courier Tracking System!")

    while True:
        show_menu()

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            add_courier(system)

        elif choice == "2":
            update_delivery_status(system)

        elif choice == "3":
            track_courier(system)

        elif choice == "4":
            list_all_couriers(system)

        elif choice == "5":
            show_delivery_stages(system)

        elif choice == "6":
            print("\nThank you for using the Courier Tracking System.")
            print("Goodbye!")
            break

        else:
            print("\nInvalid choice. Please select 1-6.")


if __name__ == "__main__":
    main()