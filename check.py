import requests
import platform

def get_os_info():
    os_info = {
        'system': platform.system(),
        'node': platform.node(),
        'release': platform.release(),
        'version': platform.version(),
        'machine': platform.machine(),
        'processor': platform.processor()
    }
    return os_info

def get_location():
    try:
        response = requests.get('https://ipinfo.io')
        data = response.json()
        loc = data['loc'].split(',')
        return {'latitude': loc[0], 'longitude': loc[1]}
    except Exception as e:
        return {'error': str(e)}

if __name__ == "__main__":
    os_info = get_os_info()
    location = get_location()
    print("Operating System Information:", os_info)
    print("Location (Latitude and Longitude):", location)
