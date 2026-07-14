import customtkinter as ctk
import psutil

from collections import deque

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from predictor import predict_resources
from allocator import adjust_priority


# ============================================================
# APPLICATION CONFIGURATION
# ============================================================

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


# ============================================================
# COLOR CONFIGURATION
# ============================================================

APP_BG = "#07111D"
SIDEBAR_BG = "#0B1726"
CARD_BG = "#0B1623"
CARD_BORDER = "#1D3548"

TEXT_PRIMARY = "#E8EEF5"
TEXT_SECONDARY = "#8291A5"

GREEN = "#20D98B"
BLUE = "#2EA8FF"
PURPLE = "#8B5CF6"
YELLOW = "#FFB800"
RED = "#FF5C5C"

GRAPH_BG = CARD_BG


# ============================================================
# MAIN GUI CLASS
# ============================================================

class ResourceGUI:

    def __init__(self, root):

        self.root = root

        self.root.title("Predictive OS Resource Allocator")
        self.root.geometry("1400x850")
        self.root.minsize(1200, 750)

        self.root.configure(fg_color=APP_BG)

        # ----------------------------------------------------
        # GRAPH DATA
        # ----------------------------------------------------

        self.max_points = 60

        self.time_data = deque(
            range(self.max_points),
            maxlen=self.max_points
        )

        self.cpu_history = deque(
            [0] * self.max_points,
            maxlen=self.max_points
        )

        self.predicted_cpu_history = deque(
            [0] * self.max_points,
            maxlen=self.max_points
        )

        # ----------------------------------------------------
        # ROOT GRID
        # ----------------------------------------------------

        self.root.grid_rowconfigure(0, weight=1)

        self.root.grid_columnconfigure(
            0,
            weight=0
        )

        self.root.grid_columnconfigure(
            1,
            weight=1
        )

        # ----------------------------------------------------
        # CREATE INTERFACE
        # ----------------------------------------------------

        self.create_sidebar()

        self.create_dashboard()

        # Start updating data

        self.update_stats()


    # ========================================================
    # SIDEBAR
    # ========================================================

    def create_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self.root,
            width=230,
            corner_radius=0,
            fg_color=SIDEBAR_BG,
            border_width=1,
            border_color=CARD_BORDER
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.sidebar.grid_propagate(False)

        # ----------------------------------------------------
        # APPLICATION TITLE
        # ----------------------------------------------------

        logo = ctk.CTkLabel(
            self.sidebar,
            text="Predictive OS",
            font=("Arial", 24, "bold"),
            text_color=TEXT_PRIMARY
        )

        logo.pack(
            pady=(30, 35)
        )

        # ----------------------------------------------------
        # NAVIGATION BUTTONS
        # ----------------------------------------------------

        self.create_nav_button(
            "⌂   Dashboard",
            active=True
        )

        self.create_nav_button(
            "▦   Processes"
        )

        self.create_nav_button(
            "◉   CPU"
        )

        self.create_nav_button(
            "▤   Memory"
        )

        self.create_nav_button(
            "⚙   Scheduler"
        )

        self.create_nav_button(
            "⚙   Settings"
        )

        self.create_nav_button(
            "ⓘ   About"
        )


    def create_nav_button(
        self,
        text,
        active=False
    ):

        button = ctk.CTkButton(
            self.sidebar,

            text=text,

            height=50,

            corner_radius=8,

            anchor="w",

            font=(
                "Arial",
                16,
                "bold" if active else "normal"
            ),

            fg_color=(
                "#10293A"
                if active
                else "transparent"
            ),

            hover_color="#153246",

            text_color=(
                GREEN
                if active
                else TEXT_PRIMARY
            )
        )

        button.pack(
            fill="x",
            padx=15,
            pady=5
        )


    # ========================================================
    # DASHBOARD
    # ========================================================

    def create_dashboard(self):

        self.dashboard = ctk.CTkFrame(
            self.root,
            fg_color=APP_BG,
            corner_radius=0
        )

        self.dashboard.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=18,
            pady=18
        )

        # ----------------------------------------------------
        # GRID CONFIGURATION
        # ----------------------------------------------------

        self.dashboard.grid_columnconfigure(
            0,
            weight=1
        )

        self.dashboard.grid_columnconfigure(
            1,
            weight=1
        )

        self.dashboard.grid_rowconfigure(
            0,
            weight=1
        )

        self.dashboard.grid_rowconfigure(
            1,
            weight=1
        )

        self.dashboard.grid_rowconfigure(
            2,
            weight=0
        )

        # ----------------------------------------------------
        # CREATE CARDS
        # ----------------------------------------------------

        self.create_process_card()

        self.create_cpu_card()

        self.create_memory_card()

        self.create_prediction_card()

        self.create_scheduler_card()


    # ========================================================
    # GENERIC CARD
    # ========================================================

    def create_card(
        self,
        row,
        column,
        title,
        columnspan=1
    ):

        frame = ctk.CTkFrame(

            self.dashboard,

            fg_color=CARD_BG,

            corner_radius=12,

            border_width=1,

            border_color=CARD_BORDER
        )

        frame.grid(

            row=row,

            column=column,

            columnspan=columnspan,

            sticky="nsew",

            padx=7,

            pady=7
        )

        title_label = ctk.CTkLabel(

            frame,

            text=title,

            font=(
                "Arial",
                16,
                "bold"
            ),

            text_color=TEXT_PRIMARY
        )

        title_label.pack(

            anchor="w",

            padx=20,

            pady=(15, 10)
        )

        return frame


    # ========================================================
    # PROCESS QUEUE CARD
    # ========================================================

    def create_process_card(self):

        self.process_frame = self.create_card(

            row=0,

            column=0,

            title="PROCESS QUEUE"
        )

        # ----------------------------------------------------
        # TABLE HEADER
        # ----------------------------------------------------

        header = ctk.CTkFrame(

            self.process_frame,

            fg_color="transparent"
        )

        header.pack(

            fill="x",

            padx=20,

            pady=5
        )

        headers = [

            "PID",

            "Process",

            "State",

            "CPU",

            "Memory"
        ]

        widths = [

            60,

            140,

            90,

            80,

            100
        ]

        for text, width in zip(
            headers,
            widths
        ):

            label = ctk.CTkLabel(

                header,

                text=text,

                width=width,

                anchor="w",

                font=(
                    "Arial",
                    13,
                    "bold"
                ),

                text_color=TEXT_SECONDARY
            )

            label.pack(
                side="left"
            )

        # ----------------------------------------------------
        # PROCESS TABLE BODY
        # ----------------------------------------------------

        self.process_container = ctk.CTkFrame(

            self.process_frame,

            fg_color="transparent"
        )

        self.process_container.pack(

            fill="both",

            expand=True,

            padx=20,

            pady=(0, 10)
        )


    # ========================================================
    # CPU CARD
    # ========================================================

    def create_cpu_card(self):

        self.cpu_frame = self.create_card(

            row=0,

            column=1,

            title="CPU USAGE"
        )

        # ----------------------------------------------------
        # CPU VALUE
        # ----------------------------------------------------

        self.cpu_value = ctk.CTkLabel(

            self.cpu_frame,

            text="0%",

            font=(
                "Arial",
                38,
                "bold"
            ),

            text_color=TEXT_PRIMARY
        )

        self.cpu_value.pack(
            pady=(0, 5)
        )

        self.cpu_text = ctk.CTkLabel(

            self.cpu_frame,

            text="Utilization",

            font=(
                "Arial",
                13
            ),

            text_color=TEXT_SECONDARY
        )

        self.cpu_text.pack()


        # ----------------------------------------------------
        # CPU PROGRESS BAR
        # ----------------------------------------------------

        self.cpu_progress = ctk.CTkProgressBar(

            self.cpu_frame,

            height=12,

            progress_color=GREEN,

            fg_color="#1C2937"
        )

        self.cpu_progress.pack(

            fill="x",

            padx=50,

            pady=15
        )

        self.cpu_progress.set(0)


        # ----------------------------------------------------
        # CPU GRAPH
        # ----------------------------------------------------

        self.cpu_figure = Figure(

            figsize=(5, 2),

            dpi=100,

            facecolor=GRAPH_BG
        )

        self.cpu_axis = self.cpu_figure.add_subplot(111)

        self.configure_graph(
            self.cpu_axis
        )

        self.cpu_line, = self.cpu_axis.plot(

            list(self.time_data),

            list(self.cpu_history),

            color=GREEN,

            linewidth=2
        )

        self.cpu_canvas = FigureCanvasTkAgg(

            self.cpu_figure,

            master=self.cpu_frame
        )

        self.cpu_canvas.get_tk_widget().pack(

            fill="both",

            expand=True,

            padx=10,

            pady=(0, 10)
        )


    # ========================================================
    # MEMORY CARD
    # ========================================================

    def create_memory_card(self):

        self.memory_frame = self.create_card(

            row=1,

            column=0,

            title="MEMORY DISTRIBUTION"
        )

        # ----------------------------------------------------
        # MEMORY FIGURE
        # ----------------------------------------------------

        self.memory_figure = Figure(

            figsize=(5, 3),

            dpi=100,

            facecolor=GRAPH_BG
        )

        self.memory_axis = self.memory_figure.add_subplot(111)

        self.memory_canvas = FigureCanvasTkAgg(

            self.memory_figure,

            master=self.memory_frame
        )

        self.memory_canvas.get_tk_widget().pack(

            fill="both",

            expand=True,

            padx=10,

            pady=10
        )


    # ========================================================
    # PREDICTION CARD
    # ========================================================

    def create_prediction_card(self):

        self.prediction_frame = self.create_card(

            row=1,

            column=1,

            title="PREDICTED VS ACTUAL USAGE"
        )

        # ----------------------------------------------------
        # PREDICTION GRAPH
        # ----------------------------------------------------

        self.prediction_figure = Figure(

            figsize=(5, 3),

            dpi=100,

            facecolor=GRAPH_BG
        )

        self.prediction_axis = (
            self.prediction_figure.add_subplot(111)
        )

        self.configure_graph(
            self.prediction_axis
        )

        self.actual_line, = (
            self.prediction_axis.plot(

                list(self.time_data),

                list(self.cpu_history),

                color=GREEN,

                linewidth=2,

                label="Actual CPU"
            )
        )

        self.predicted_line, = (
            self.prediction_axis.plot(

                list(self.time_data),

                list(self.predicted_cpu_history),

                color=BLUE,

                linestyle="--",

                linewidth=2,

                label="Predicted CPU"
            )
        )

        legend = self.prediction_axis.legend(

            facecolor=CARD_BG,

            edgecolor=CARD_BORDER,

            labelcolor=TEXT_PRIMARY
        )

        self.prediction_canvas = FigureCanvasTkAgg(

            self.prediction_figure,

            master=self.prediction_frame
        )

        self.prediction_canvas.get_tk_widget().pack(

            fill="both",

            expand=True,

            padx=10,

            pady=10
        )


    # ========================================================
    # SCHEDULER CARD
    # ========================================================

    def create_scheduler_card(self):

        self.scheduler_frame = self.create_card(

            row=2,

            column=0,

            columnspan=2,

            title="SCHEDULER STATUS"
        )

        content = ctk.CTkFrame(

            self.scheduler_frame,

            fg_color="transparent"
        )

        content.pack(

            fill="x",

            padx=30,

            pady=(5, 20)
        )


        # ----------------------------------------------------
        # AI DECISION
        # ----------------------------------------------------

        decision_frame = ctk.CTkFrame(

            content,

            fg_color="transparent"
        )

        decision_frame.pack(

            side="left",

            expand=True,

            fill="x"
        )

        self.status_label = ctk.CTkLabel(

            decision_frame,

            text="● Optimal Allocation",

            font=(
                "Arial",
                18,
                "bold"
            ),

            text_color=GREEN
        )

        self.status_label.pack(
            anchor="w"
        )

        self.status_description = ctk.CTkLabel(

            decision_frame,

            text="AI scheduler analyzing system resources.",

            font=(
                "Arial",
                13
            ),

            text_color=TEXT_SECONDARY
        )

        self.status_description.pack(
            anchor="w"
        )


        # ----------------------------------------------------
        # PROCESS COUNT
        # ----------------------------------------------------

        self.process_metric = self.create_metric(

            content,

            "Processes"
        )


        # ----------------------------------------------------
        # PREDICTED MEMORY
        # ----------------------------------------------------

        self.memory_metric = self.create_metric(

            content,

            "Predicted Memory"
        )


        # ----------------------------------------------------
        # PREDICTED DISK
        # ----------------------------------------------------

        self.disk_metric = self.create_metric(

            content,

            "Predicted Disk"
        )


    # ========================================================
    # CREATE METRIC
    # ========================================================

    def create_metric(
        self,
        parent,
        title
    ):

        frame = ctk.CTkFrame(

            parent,

            fg_color="transparent"
        )

        frame.pack(

            side="left",

            padx=30
        )

        title_label = ctk.CTkLabel(

            frame,

            text=title,

            font=(
                "Arial",
                12
            ),

            text_color=TEXT_SECONDARY
        )

        title_label.pack()

        value_label = ctk.CTkLabel(

            frame,

            text="--",

            font=(
                "Arial",
                24,
                "bold"
            ),

            text_color=TEXT_PRIMARY
        )

        value_label.pack()

        return value_label


    # ========================================================
    # GRAPH CONFIGURATION
    # ========================================================

    def configure_graph(
        self,
        axis
    ):

        axis.set_facecolor(GRAPH_BG)

        axis.set_ylim(
            0,
            100
        )

        axis.set_xlim(
            0,
            self.max_points - 1
        )

        axis.tick_params(

            colors=TEXT_SECONDARY,

            labelsize=8
        )

        axis.grid(

            True,

            alpha=0.08
        )

        for spine in axis.spines.values():

            spine.set_visible(False)


    # ========================================================
    # PROCESS TABLE UPDATE
    # ========================================================

    def update_process_table(self):

        # Remove previous rows

        for widget in (
            self.process_container.winfo_children()
        ):

            widget.destroy()


        # ----------------------------------------------------
        # GET PROCESSES
        # ----------------------------------------------------

        process_list = []

        for process in psutil.process_iter(

            [
                "pid",
                "name",
                "status",
                "cpu_percent",
                "memory_info"
            ]
        ):

            try:

                info = process.info

                process_list.append(info)

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied
            ):

                continue


        # Sort by CPU usage

        process_list = sorted(

            process_list,

            key=lambda x: x["cpu_percent"] or 0,

            reverse=True

        )[:5]


        # ----------------------------------------------------
        # CREATE ROWS
        # ----------------------------------------------------

        widths = [

            60,

            140,

            90,

            80,

            100
        ]

        for info in process_list:

            row = ctk.CTkFrame(

                self.process_container,

                fg_color="transparent"
            )

            row.pack(

                fill="x",

                pady=4
            )


            pid = info["pid"]

            name = info["name"] or "Unknown"

            status = info["status"] or "Unknown"

            cpu = info["cpu_percent"] or 0

            memory_mb = (
                info["memory_info"].rss
                / (1024 ** 2)
            )


            values = [

                str(pid),

                name[:16],

                status.title(),

                f"{cpu:.1f}%",

                f"{memory_mb:.0f} MB"
            ]


            for index, (
                value,
                width
            ) in enumerate(

                zip(values, widths)

            ):

                color = TEXT_PRIMARY

                if index == 2:

                    if status == "running":

                        color = GREEN

                    elif status == "sleeping":

                        color = BLUE

                    else:

                        color = YELLOW


                label = ctk.CTkLabel(

                    row,

                    text=value,

                    width=width,

                    anchor="w",

                    font=(
                        "Arial",
                        12
                    ),

                    text_color=color
                )

                label.pack(
                    side="left"
                )


    # ========================================================
    # MEMORY CHART UPDATE
    # ========================================================

    def update_memory_chart(
        self,
        memory
    ):

        self.memory_axis.clear()

        used = memory.used

        available = memory.available

        cached = getattr(
            memory,
            "cached",
            0
        )

        total = memory.total


        free = max(

            total
            - used
            - cached,

            0
        )


        values = [

            used,

            cached,

            available
        ]


        colors = [

            GREEN,

            BLUE,

            PURPLE
        ]


        self.memory_axis.pie(

            values,

            colors=colors,

            startangle=90,

            wedgeprops={

                "width": 0.35,

                "edgecolor": CARD_BG
            }
        )


        total_gb = (
            total
            / (1024 ** 3)
        )

        used_gb = (
            used
            / (1024 ** 3)
        )


        self.memory_axis.text(

            0,

            0.08,

            f"{used_gb:.1f} GB",

            ha="center",

            va="center",

            fontsize=16,

            color=TEXT_PRIMARY,

            fontweight="bold"
        )


        self.memory_axis.text(

            0,

            -0.13,

            f"/ {total_gb:.0f} GB",

            ha="center",

            va="center",

            fontsize=10,

            color=TEXT_SECONDARY
        )


        self.memory_axis.set_facecolor(
            GRAPH_BG
        )


        self.memory_canvas.draw_idle()


    # ========================================================
    # MAIN UPDATE LOOP
    # ========================================================

    def update_stats(self):

        try:

            # ------------------------------------------------
            # SYSTEM METRICS
            # ------------------------------------------------

            cpu = psutil.cpu_percent()

            memory = psutil.virtual_memory()

            swap = psutil.swap_memory()

            disk = psutil.disk_usage("/")

            disk_io = psutil.disk_io_counters()

            network = psutil.net_io_counters()

            process_count = len(
                psutil.pids()
            )


            try:

                load1, load5, load15 = (
                    psutil.getloadavg()
                )

            except (
                AttributeError,
                OSError
            ):

                load1 = 0

                load5 = 0

                load15 = 0


            # ------------------------------------------------
            # MACHINE LEARNING FEATURES
            # ------------------------------------------------

            features = [

                memory.percent,

                memory.available
                / (1024 ** 2),

                swap.percent,

                disk.percent,

                disk_io.read_bytes
                / (1024 ** 2),

                disk_io.write_bytes
                / (1024 ** 2),

                network.bytes_sent
                / (1024 ** 2),

                network.bytes_recv
                / (1024 ** 2),

                process_count,

                load1,

                load5,

                load15
            ]


            # ------------------------------------------------
            # PREDICTION
            # ------------------------------------------------

            prediction = predict_resources(
                features
            )


            # ------------------------------------------------
            # AI SCHEDULER DECISION
            # ------------------------------------------------

            decision = adjust_priority(
                features
            )


            predicted_cpu = prediction[
                "Predicted CPU"
            ]


            predicted_memory = prediction[
                "Predicted Memory"
            ]


            predicted_disk = prediction[
                "Predicted Disk"
            ]


            # ------------------------------------------------
            # UPDATE CPU CARD
            # ------------------------------------------------

            self.cpu_value.configure(

                text=f"{cpu:.0f}%"
            )


            self.cpu_progress.set(

                cpu / 100
            )


            # ------------------------------------------------
            # UPDATE GRAPH HISTORY
            # ------------------------------------------------

            self.cpu_history.append(
                cpu
            )


            self.predicted_cpu_history.append(
                predicted_cpu
            )


            # ------------------------------------------------
            # UPDATE CPU GRAPH
            # ------------------------------------------------

            self.cpu_line.set_ydata(

                list(
                    self.cpu_history
                )
            )


            self.cpu_canvas.draw_idle()


            # ------------------------------------------------
            # UPDATE PREDICTION GRAPH
            # ------------------------------------------------

            self.actual_line.set_ydata(

                list(
                    self.cpu_history
                )
            )


            self.predicted_line.set_ydata(

                list(
                    self.predicted_cpu_history
                )
            )


            self.prediction_canvas.draw_idle()


            # ------------------------------------------------
            # UPDATE MEMORY CHART
            # ------------------------------------------------

            self.update_memory_chart(
                memory
            )


            # ------------------------------------------------
            # UPDATE PROCESS TABLE
            # ------------------------------------------------

            self.update_process_table()


            # ------------------------------------------------
            # UPDATE SCHEDULER
            # ------------------------------------------------

            action = decision.get(

                "action",

                "Analyzing"
            )


            self.status_label.configure(

                text=f"● {action}"
            )


            self.status_description.configure(

                text=(
                    "AI scheduler dynamically "
                    "analyzing system resources."
                )
            )


            # ------------------------------------------------
            # UPDATE METRICS
            # ------------------------------------------------

            self.process_metric.configure(

                text=str(process_count)
            )


            self.memory_metric.configure(

                text=f"{predicted_memory:.1f}%"
            )


            self.disk_metric.configure(

                text=f"{predicted_disk:.1f}%"
            )


        except Exception as error:

            print(
                "Dashboard update error:",
                error
            )


        # ----------------------------------------------------
        # UPDATE EVERY 2 SECONDS
        # ----------------------------------------------------

        self.root.after(

            2000,

            self.update_stats
        )