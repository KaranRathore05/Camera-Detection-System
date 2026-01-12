import time

person_timer = {}
LOITER_TIME = 10  # seconds

def check_loitering(person_id):
    current_time = time.time()

    if person_id not in person_timer:
        person_timer[person_id] = current_time
        return False

    time_spent = current_time - person_timer[person_id]

    if time_spent > LOITER_TIME:
        return True

    return False
