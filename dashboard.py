import streamlit as st
import time
from client import Client


def start_injection(client: Client, inject_value_placeholder, wait):
    while True:
        inject_value = inject_value_placeholder()
        client.inject(inject_value, wait)
        st.write(f"Injected value: {inject_value} every {wait} seconds.")
        time.sleep(wait)


# Set up the title
st.title("hello")

# Input fields for IP address and port number
ip_address = st.text_input("Enter IP address (e.g., 192.168.1.1):")
port_number = st.number_input("Enter port number:", min_value=0, max_value=65535, value=502)

client = Client()

if ip_address:
    st.write("Client created with IP address:", ip_address, "and port number:", port_number)

    # Sliders for start_pos and num_chars
    start_pos = st.slider("Select start position:", min_value=0, max_value=100, value=0)
    num_chars = st.slider("Select number of characters:", min_value=1, max_value=50, value=14)

    # Display data read from server
    try:
        data_value = client.read_data(start_pos, num_chars)
    except:
        data_value = 'NULL'
    st.write("Data read from server:", data_value)

    # Slider for inject value
    inject_value_placeholder = st.empty()
    inject_value = inject_value_placeholder.slider("Select value to inject:", min_value=0, max_value=100, value=2)

    inject_interval = st.slider("Select interval for injection:", min_value=1, max_value=60, value=5)

    # Button to start injection
    if st.button("Start Injection"):
        thread = Thread(target=start_injection, args=(client, inject_value_placeholder.slider, inject_interval))
        thread.start()




###########
import streamlit as st
import time
from threading import Thread
from your_module import Client, Areas, get_string, set_real  # Replace with the actual module where these are defined


class CustomClient:
    def __init__(self, ip_address='127.0.0.1', port_num=24565):
        self.client = snap7.client.Client()
        self.client.connect(ip_address, 0, 1, port_num)

    def read_data(self, start_pos=0, num_chars=14):
        data_read = self.client.read_area(Areas.DB, 1, start_pos, num_chars)
        value = get_string(data_read, 0)
        return value

    def inject(self, value, wait=5):
        data_to_write = bytearray(4)
        set_real(data_to_write, 0, value)
        self.client.write_area(Areas.PE, 1, 0, data_to_write)
        time.sleep(wait)


def start_injection(client, inject_value_placeholder, wait):
    while True:
        inject_value = inject_value_placeholder()
        client.inject(inject_value, wait)
        st.write(f"Injected value: {inject_value} every {wait} seconds.")
        time.sleep(wait)


# Set up the title
st.title("hello")

# Input fields for IP address and port number
ip_address = st.text_input("Enter IP address (e.g., 192.168.1.1):")
port_number = st.number_input("Enter port number:", min_value=0, max_value=65535, value=502)

if ip_address and port_number:
    try:
        # Create client instance
        client = CustomClient(ip_address, port_number)
        st.write("Client created with IP address:", ip_address, "and port number:", port_number)

        # Sliders for start_pos and num_chars
        start_pos = st.slider("Select start position:", min_value=0, max_value=100, value=0)
        num_chars = st.slider("Select number of characters:", min_value=1, max_value=50, value=14)

        # Display data read from server
        data_value = client.read_data(start_pos, num_chars)
        st.write("Data read from server:", data_value)

        # Select box for number of injects
        num_injects = st.selectbox("Select number of injects:", [2, 3])

        inject_values = []
        inject_intervals = []

        # Create inject sliders dynamically
        for i in range(num_injects):
            inject_value_placeholder = st.empty()
            inject_value = inject_value_placeholder.slider(f"Select value to inject (Script {i + 1}):", min_value=0,
                                                           max_value=100, value=2)
            inject_values.append(inject_value_placeholder)

            inject_interval = st.slider(f"Select interval for injection (Script {i + 1}):", min_value=1, max_value=60,
                                        value=5)
            inject_intervals.append(inject_interval)

        # Button to start injection
        if st.button("Start Injections"):
            for i in range(num_injects):
                thread = Thread(target=start_injection, args=(client, inject_values[i].slider, inject_intervals[i]))
                thread.start()

    except Exception as e:
        st.error(f"Failed to connect to the client: {e}")

