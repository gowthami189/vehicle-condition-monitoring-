import urllib.parse
import urllib.request
import time
import random

BOT_TOKEN = "8249557092:AAFku7pGV0UTJSvIMTanifrI4-nogsg-I9w"
CHAT_ID = "7247112467"

def get_vehicle_data():
    return {
        'oil_pressure': random.uniform(20, 80),        # psi
        'coolant_temp': random.uniform(60, 120),       # °C
        'vibration': random.uniform(0.5, 5.0),         # g-force
        'torque': random.uniform(50, 500),             # Nm
        'exhaust_voltage': random.uniform(0.05, 1.0),  # V
        'fuel_consumption': random.uniform(0.5, 30.0), # L/h
        'acoustic_level': random.uniform(50, 120)      # dB
    }

def is_abnormal(data):
    return not (
        30 <= data['oil_pressure'] <= 70 and
        70 <= data['coolant_temp'] <= 105 and
        data['vibration'] < 3.0 and
        100 <= data['torque'] <= 400 and
        0.1 <= data['exhaust_voltage'] <= 0.9 and
        data['fuel_consumption'] <= 25 and
        data['acoustic_level'] <= 90
    )

def format_alert(data):
    return (
        "🚨 *Abnormal Vehicle Condition Detected!*\n\n"
        f"• Oil Pressure: {data['oil_pressure']:.1f} psi\n"
        f"• Coolant Temp: {data['coolant_temp']:.1f} °C\n"
        f"• Vibration: {data['vibration']:.2f} g\n"
        f"• Torque: {data['torque']:.1f} Nm\n"
        f"• Exhaust Sensor: {data['exhaust_voltage']:.2f} V\n"
        f"• Fuel Consumption: {data['fuel_consumption']:.2f} L/h\n"
        f"• Acoustic Level: {data['acoustic_level']:.1f} dB"
    )

def send_alert(message):
    base_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    params = urllib.parse.urlencode({
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    })
    url = f"{base_url}?{params}"
    print("\nSending the following alert message to Telegram:")
    print(message)
    try:
        urllib.request.urlopen(url)
        print("✅ Alert successfully sent to Telegram.")
    except Exception as e:
        print(f"❌ Error sending Telegram message: {e}")

def monitor():
    last_status = "normal"
    for _ in range(5):

        data = get_vehicle_data()

        print("\nSensor Data:")
        for key, value in data.items():
            unit = {
                'oil_pressure': 'psi',
                'coolant_temp': '°C',
                'vibration': 'g',
                'torque': 'Nm',
                'exhaust_voltage': 'V',
                'fuel_consumption': 'L/h',
                'acoustic_level': 'dB'
            }.get(key, '')

            val_str = f"{value:.2f}" if key in ['vibration', 'exhaust_voltage'] else f"{value:.1f}"
            print(f" - {key.replace('_', ' ').title()}: {val_str} {unit}")

        abnormal = is_abnormal(data)
        if abnormal and last_status != "abnormal":
            print("\n❗ Abnormal values detected!")
            alert = format_alert(data)
            send_alert(alert)
            last_status = "abnormal"
        elif not abnormal:
            if last_status != "normal":
                print("✅ Vehicle returned to normal condition.")
            else:
                print("✅ Vehicle status normal.")
            last_status = "normal"

        time.sleep(5)

if __name__ == "__main__":
    print("🚗 Starting vehicle health monitoring...")
    monitor()
