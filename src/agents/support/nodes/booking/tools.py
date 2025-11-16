"""booking/tools.py"""
import random
from datetime import datetime, timedelta

from langchain_core.tools import tool

@tool("book_appointment", description="Book a medical appointment for a given date, time, doctor and pacient.")
def book_appointment(date: str, time: str, doctor: str, patient: str):
    """Book a medical appointment for a given date, time, doctor and pacient.
    
    Args:
        date (str): The date of the appointment.
        time (str): The time of the appointment.
        doctor (str): The doctor of the appointment.
        patient (str): The patient of the appointment.
    
    Returns:
        str: A message indicating the result of the appointment booking.
    """

    # Validar formato de fecha y hora
    try:
        appointment_dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    except ValueError:
        return "❌ Invalid date or time format. Please use YYYY-MM-DD and HH:MM."

    # Revisar si la cita está en el pasado
    if appointment_dt < datetime.now():
        return "⚠️ Cannot book an appointment in the past."

    # Revisar disponibilidad del doctor
    if doctor not in ["Dr. Smith", "Dr. Johnson", "Dr. Williams"]:
        return "You can't book an appointment with a doctor that is not available."

    # Simular probabilidad de error de sistema (para probar respuestas del agente)
    if random.random() < 0.05:
        return "⚠️ System temporarily unavailable. Please try again later."

    # Guardar la cita
    confirmation_id = f"""
        {doctor[:3].upper()}-{patient[:3].upper()}-{appointment_dt.strftime('%Y%m%d%H%M')}
    """

    return (
        f"✅ Appointment booked successfully!\n"
        f"Doctor: {doctor}\n"
        f"Patient: {patient}\n"
        f"Date: {date}\n"
        f"Time: {time}\n"
        f"Confirmation ID: {confirmation_id}"
    )

@tool("get_appointment_availability", description="Get the availability of a medical appointment.")
def get_appointment_availability(date: str, time: str, doctor: str):
    """Get the availability of a medical appointment.
    
    Args:
        date (str): The date of the appointment.
        time (str): The time of the appointment.
        doctor (str): The doctor of the appointment.
    
    Returns:
        str: A message indicating the availability of the appointment.
    """

    # Validar fecha
    try:
        appointment_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        return "❌ Invalid date format. Please use YYYY-MM-DD."

    if appointment_date < datetime.now().date():
        return "⚠️ Cannot check availability for a past date."

    # Validar doctor
    if not doctor:
        return "❌ Please specify a doctor's name."

    # Simular disponibilidad basada en un hash determinístico
    random.seed(f"{doctor.lower()}_{date}")
    occupied_slots = random.sample(range(16), k=random.randint(3, 7))  # 3–7 citas ya ocupadas

    # Generar horario base (8:00–17:00 cada 30 min)
    start_time = datetime.combine(appointment_date, datetime.strptime("08:00", "%H:%M").time())
    slots = [start_time + timedelta(minutes=30 * i) for i in range(16)]  # 8:00–16:30

    # Marcar slots ocupados
    available_slots = [
        slot.strftime("%H:%M") for i, slot in enumerate(slots) if i not in occupied_slots
    ]

    # Si el usuario consulta una hora específica
    if time:
        try:
            target_time = datetime.strptime(time, "%H:%M").time()
        except ValueError:
            return "❌ Invalid time format. Please use HH:MM."

        # Revisar si ese slot está ocupado
        time_str = target_time.strftime("%H:%M")
        if time_str in available_slots:
            return f"✅ Dr. {doctor} is available at {time} on {date}."
        else:
            return f"❌ Dr. {doctor} is not available at {time} on {date}."

    # Si no se especifica hora → listar todo el horario disponible
    if not available_slots:
        return f"❌ Dr. {doctor} has no available slots on {date}."

    return (
        f"✅ Available slots for Dr. {doctor} on {date}:\n"
        + ", ".join(available_slots)
    )

tools = [
    book_appointment,
    get_appointment_availability,
]
