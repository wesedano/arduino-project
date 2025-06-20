#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('matplotlib', 'notebook')

import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import ipywidgets as widgets
from IPython.display import display


# In[2]:


# Serial settings
serial_port = 'COM6'  # Adjust if needed
baud_rate = 115200
ser = serial.Serial(serial_port, baud_rate, timeout=1)

# Buffers
max_points = 1000
target_data = deque([0]*max_points, maxlen=max_points)
current_data = deque([0]*max_points, maxlen=max_points)

# Plot setup
fig, ax = plt.subplots()
line1, = ax.plot([], [], label='Target Angle', color='tab:red', linewidth=2)
line2, = ax.plot([], [], label='Current Angle', color='tab:blue', linewidth=2)
setpoint_line = ax.axhline(y=0, color='gray', linestyle='--', label='Setpoint')

ax.set_xlim(0, max_points)
ax.set_ylim(-190, 190)
ax.legend()
ax.grid(True)
plt.title('SimpleFOC Real-Time Angle Tracking')
plt.xlabel('Time (frames)')
plt.ylabel('Angle (deg)')


# In[3]:


# Widgets
p_slider = widgets.FloatSlider(value=2.0, min=0, max=100, step=0.1, description='P')
i_slider = widgets.FloatSlider(value=360.0, min=0, max=1000, step=0.1, description='I')
d_slider = widgets.FloatSlider(value=0.0, min=0, max=100, step=0.1, description='D')
limit_slider = widgets.FloatSlider(value=3.0, min=0, max=20, step=0.1, description='Limit')
setpoint_slider = widgets.FloatSlider(value=0.0, min=-180, max=180, step=1.0, description='Setpoint')
info_label = widgets.Label()
pause_button = widgets.Button(description="Pause")


# In[4]:


# Pause toggle
pause = False
def toggle_pause(b):
    global pause
    pause = not pause
    b.description = "Resume" if pause else "Pause"
pause_button.on_click(toggle_pause)

# Send all values to Arduino
def update_all(change=None):
    try:
        p, i, d = p_slider.value, i_slider.value, d_slider.value
        lim, sp = limit_slider.value, setpoint_slider.value
        ser.write(f'P={p:.2f}\n'.encode())
        ser.write(f'I={i:.2f}\n'.encode())
        ser.write(f'D={d:.2f}\n'.encode())
        ser.write(f'L={lim:.2f}\n'.encode())
        ser.write(f'{sp:.2f}\n'.encode())
        info_label.value = f"P={p:.1f}, I={i:.1f}, D={d:.1f}, Limit={lim:.1f}, Setpoint={sp:.1f}°"
    except Exception as e:
        print("Serial error:", e)

# Update horizontal setpoint line
def update_setpoint_line(change):
    setpoint_line.set_ydata(change['new'])

# Attach
for s in [p_slider, i_slider, d_slider, limit_slider, setpoint_slider]:
    s.observe(update_all, names='value')
setpoint_slider.observe(update_setpoint_line, names='value')


# In[5]:


# Parse incoming data
def parse_line(line):
    try:
        parts = line.split(',')
        if len(parts) >= 2:
            return float(parts[0]), float(parts[1])
    except Exception as e:
        print("Parse error:", e)
    return None, None

# Plot update function
def update(frame):
    if pause:
        return line1, line2, setpoint_line

    while ser.in_waiting:
        try:
            raw = ser.readline().decode('utf-8').strip()
            target, current = parse_line(raw)
            if target is not None and current is not None:
                target_data.append(target)
                current_data.append(current)
        except Exception as e:
            print("Serial read error:", e)

    line1.set_data(range(len(target_data)), list(target_data))
    line2.set_data(range(len(current_data)), list(current_data))
    return line1, line2, setpoint_line

ani = animation.FuncAnimation(fig, update, interval=50, blit=True)


# In[6]:


# Rebuild vertical UI layout
ui = widgets.VBox([
    p_slider,
    i_slider,
    d_slider,
    limit_slider,
    setpoint_slider,
    info_label,
    pause_button
])
ui.layout = widgets.Layout(min_width='300px', max_width='400px')

# Resize plot again if needed
fig.set_size_inches(6, 4)  # Slightly wider to match layout

# Display plot + controls side by side
container = widgets.HBox([
    ui,
    widgets.HTML("<div style='width: 30px'></div>")
])

display(container)
display(fig)

