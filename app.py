import streamlit as st
import json
import os
from datetime import datetime

# 1. Настройка файла для хранения данных
DB_FILE = 'data.json'
DAILY_GOAL = 2000  # Цель: 2 литра

# Функция для загрузки данных из файла
def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    return {"total": 0, "history": []}

# Функция для сохранения данных в файл
def save_data(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f)

# --- ИНТЕРФЕЙС ПРИЛОЖЕНИЯ ---
st.set_page_config(page_title="Water Tracker", page_icon="💧")
st.title("💧 Мой Трекер Воды")
st.write("Помогает следить за здоровьем в Атырау! 🇰🇿")

# Загружаем текущие данные
data = load_data()

# 2. Основной функционал (Ввод данных)
with st.container():
    st.subheader("Добавить воду")
    ml = st.number_input("Сколько мл выпили?", min_value=0, max_value=1000, value=250, step=50)
    
    if st.button("Добавить в журнал"):
        # Обновляем данные
        data["total"] += ml
        now = datetime.now().strftime("%H:%M:%S")
        data["history"].append(f"+{ml} мл в {now}")
        
        # Сохраняем в файл (Требование хакатона!)
        save_data(data)
        st.success(f"Записано: {ml} мл!")
        st.rerun()

# 3. Визуализация (Прогресс-бар)
st.divider()
progress = min(data["total"] / DAILY_GOAL, 1.0)
st.write(f"Выпито за сегодня: **{data['total']} / {DAILY_GOAL} мл**")
st.progress(progress)

# 4. Вторая функция (Просмотр истории/очистка)
with st.expander("Посмотреть историю за сегодня"):
    if data["history"]:
        for item in reversed(data["history"]):
            st.text(item)
    else:
        st.write("История пуста.")

if st.button("Сбросить прогресс"):
    data = {"total": 0, "history": []}
    save_data(data)
    st.rerun()V
