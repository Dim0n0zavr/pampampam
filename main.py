import sqlite3
import customtkinter as ctk
from tkinter import messagebox
import math
import random

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
# c - cursor 
# Список интересных фактов
INTERESTING_FACTS = [
    "Яблоки помогают проснуться лучше, чем кофе.",
    "Банан — это ягода, а клубника — нет.",
    "Вода составляет около 60% веса тела взрослого человека.",
    "Орехи богаты полезными жирами и белками.",
    "Шпинат содержит больше железа, чем мясо.",
    "Авокадо — это фрукт, а не овощ.",
    "Мед никогда не портится.",
    "Чеснок помогает укрепить иммунитет.",
    "Морковь улучшает зрение благодаря витамину А.",
    "Зеленый чай богат антиоксидантами.",
    "Каждые 60 секунд в Африке проходит минута!",
    'You were rickrolled'
]

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Расчет калорий питания")
        self.geometry("600x700")
        self.current_user = None
        self.show_main_menu()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    # проверка зареганых пользователей
    def has_registered_users(self):
        conn = sqlite3.connect('nutrition.db')
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM users")
        count = c.fetchone()[0]
        conn.close()
        return count > 0 # True False


    #==========Основное Меню========== 

    def show_main_menu(self):
        self.clear_window()

        # Проверяем, есть ли зарегистрированные пользователи
        if not self.has_registered_users():
            login_btn_state = "disabled"
        else:
            login_btn_state = "normal"

        
        # Логотип
        self.logo_label = ctk.CTkLabel(self, text="🍎", font=("Arial", 50))
        self.logo_label.pack(pady=10)

        # Приветствие
        self.welcome_label = ctk.CTkLabel(self, text="Добро пожаловать!", font=("Arial", 20, "bold"))
        self.welcome_label.pack(pady=10)

        # Выбор пользователя
        conn = sqlite3.connect('nutrition.db')
        c = conn.cursor()
        c.execute("SELECT username FROM users")
        users = c.fetchall()
        conn.close()

        self.user_label = ctk.CTkLabel(self, text="Выберите пользователя:")
        self.user_label.pack(pady=5)

        self.user_var = ctk.StringVar(value=users[0][0] if users else "")
        self.user_menu = ctk.CTkOptionMenu(self, variable=self.user_var, values=[user[0] for user in users])
        self.user_menu.pack(pady=5)

        self.login_btn = ctk.CTkButton(self, text="Войти", command=self.perform_login, state=login_btn_state)
        self.login_btn.pack(pady=10)

        self.register_btn = ctk.CTkButton(self, text="Регистрация", command=self.show_registration)
        self.register_btn.pack(pady=10)

        # Интересный факт
        self.fact_label = ctk.CTkLabel(self, text=random.choice(INTERESTING_FACTS), wraplength=500, justify="center")
        self.fact_label.pack(pady=20)

    def perform_login(self):
        self.current_user = self.user_var.get()
        self.show_user_menu()

    #==========Меню регестрации==========

    def show_registration(self):
        self.clear_window()

        # Логотип
        self.logo_label = ctk.CTkLabel(self, text="🍎", font=("Arial", 50))
        self.logo_label.pack(pady=10)
        
        # 1 строчка
        self.name_age_frame = ctk.CTkFrame(self)
        self.name_age_frame.pack(pady=5)
        self.name_entry = ctk.CTkEntry(self.name_age_frame, placeholder_text="Имя", width=200)
        self.name_entry.pack(side="left", padx=5)
        self.age_entry = ctk.CTkEntry(self.name_age_frame, placeholder_text="Возраст", width=100)
        self.age_entry.pack(side="left", padx=5)

        # 2 строчка
        self.weight_height_frame = ctk.CTkFrame(self)
        self.weight_height_frame.pack(pady=5)
        self.weight_entry = ctk.CTkEntry(self.weight_height_frame, placeholder_text="Вес (кг)", width=150)
        self.weight_entry.pack(side="left", padx=5)
        self.height_entry = ctk.CTkEntry(self.weight_height_frame, placeholder_text="Рост (см)", width=150)
        self.height_entry.pack(side="left", padx=5)

        # Пол
        self.gender_frame = ctk.CTkFrame(self)
        self.gender_frame.pack(pady=5)
        self.gender_label = ctk.CTkLabel(self.gender_frame, text="Выберите пол:")
        self.gender_label.pack(side="left", padx=5)
        self.gender_var = ctk.StringVar(value="Мужской")
        self.gender_menu = ctk.CTkOptionMenu(self.gender_frame, variable=self.gender_var, values=["Мужской", "Женский", "Боевой вертолет"])
        self.gender_menu.pack(side="left", padx=5)

        # Активность
        self.activity_frame = ctk.CTkFrame(self)
        self.activity_frame.pack(pady=5)
        self.activity_label = ctk.CTkLabel(self.activity_frame, text="Выберите активность:")
        self.activity_label.pack(side="left", padx=5)
        self.activity_var = ctk.StringVar(value="Малоактивный")
        self.activity_menu = ctk.CTkOptionMenu(self.activity_frame, variable=self.activity_var, 
                                             values=["Малоактивный", "Среднеактивный", "Высокоактивный"])
        self.activity_menu.pack(side="left", padx=5)

        # Цель
        self.goal_frame = ctk.CTkFrame(self)
        self.goal_frame.pack(pady=5)
        self.goal_label = ctk.CTkLabel(self.goal_frame, text="Выберите цель:")
        self.goal_label.pack(side="left", padx=5)
        self.goal_var = ctk.StringVar(value="Поддержание веса")
        self.goal_menu = ctk.CTkOptionMenu(self.goal_frame, variable=self.goal_var, 
                                         values=["Похудение", "Набор массы", "Поддержание веса"])
        self.goal_menu.pack(side="left", padx=5)

        # Кнопки
        self.register_confirm_btn = ctk.CTkButton(self, text="Зарегистрироваться", command=self.perform_registration)
        self.register_confirm_btn.pack(pady=20)

        self.back_btn = ctk.CTkButton(self, text="Назад", command=self.show_main_menu)
        self.back_btn.pack(pady=10)

    #Расчет калорий и добавление в бд пользователя, выкидываем в юзер меню

    def perform_registration(self):
        try:
            # Расчет калорий
            activity_map = {
                "Малоактивный": 1.2,
                "Среднеактивный": 1.55,
                "Высокоактивный": 1.7
            }
            
            bmr = 0
            if self.gender_var.get() == "Мужской":
                bmr = (88.362 + (13.397 * float(self.weight_entry.get())) + 
                      (4.799 * float(self.height_entry.get())) - 
                      (5.677 * float(self.age_entry.get()))) * activity_map[self.activity_var.get()]
            elif self.gender_var.get() == "Боевой вертолет":
                bmr = (88.362 + (13.397 * float(self.weight_entry.get())) + 
                      (4.799 * float(self.height_entry.get())) - 
                      (5.677 * float(self.age_entry.get()))) * activity_map[self.activity_var.get()]
            else:
                bmr = (447.593 + (9.247 * float(self.weight_entry.get())) + 
                      (3.098 * float(self.height_entry.get())) - 
                      (4.330 * float(self.age_entry.get()))) * activity_map[self.activity_var.get()]

            if self.goal_var.get() == "Похудение":
                bmr *= 0.8
            elif self.goal_var.get() == "Набор массы":
                bmr *= 1.2

            conn = sqlite3.connect('nutrition.db')
            c = conn.cursor()
            c.execute('''INSERT INTO users (username, age, gender, weight, height, activity, goal, calories_norm)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                      (self.name_entry.get().strip(),
                       int(self.age_entry.get()),
                       self.gender_var.get(),
                       float(self.weight_entry.get()),
                       float(self.height_entry.get()),
                       activity_map[self.activity_var.get()],
                       self.goal_var.get(),
                       math.floor(bmr)))
            conn.commit()
            conn.close()
            
            self.current_user = self.name_entry.get().strip()
            self.show_user_menu() # Показ юзер мен
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Некорректные данные: {str(e)}")

    #==========Юзер меню==========

    def show_user_menu(self):
        self.clear_window()
        
        conn = sqlite3.connect('nutrition.db')
        c = conn.cursor()
        c.execute("SELECT calories_norm FROM users WHERE username = ?", (self.current_user,))
        calories_norm = c.fetchone()[0]
        conn.close()

        # Логотип
        self.logo_label = ctk.CTkLabel(self, text="🍎", font=("Arial", 50))
        self.logo_label.pack(pady=10)

        # hello user 
        self.greeting_label = ctk.CTkLabel(self, text=f"Добро пожаловать, {self.current_user}!", font=("Arial", 20, "bold"))
        self.greeting_label.pack(pady=20)

        self.calories_label = ctk.CTkLabel(self, text=f"Дневная норма калорий: {calories_norm}")
        self.calories_label.pack(pady=10)

        self.plan_btn = ctk.CTkButton(self, text="План на сегодня", command=self.create_meal_plan)
        self.plan_btn.pack(pady=10)

        self.logout_btn = ctk.CTkButton(self, text="Выйти", command=self.show_main_menu)
        self.logout_btn.pack(pady=10)

        # Интересный факт
        self.fact_label = ctk.CTkLabel(self, text=random.choice(INTERESTING_FACTS), wraplength=500, justify="center")
        self.fact_label.pack(pady=20)

    #==========еда план делать==========

    def create_meal_plan(self):
        self.clear_window()
        
        conn = sqlite3.connect('nutrition.db')
        c = conn.cursor()
        
        # Получаем дневную норму калорий
        c.execute("SELECT calories_norm FROM users WHERE username = ?", (self.current_user,))
        target_calories = c.fetchone()[0]
        
        # Получаем блюда по категориям
        meals = {'Завтрак': [], 'Обед': [], 'Ужин': []}
        for category in meals.keys():
            c.execute('''SELECT dishes.id, dishes.name, SUM((products.calories * dish_composition.grams)/100) as total_calories
                         FROM dishes
                         JOIN dish_composition ON dishes.id = dish_composition.dish_id
                         JOIN products ON dish_composition.product_id = products.id
                         WHERE dishes.category = ?
                         GROUP BY dishes.id''', (category,))
            meals[category] = c.fetchall()
        
        # Подбор блюда
        selected_meals = []
        total_calories = 0

        for category in ['Завтрак', 'Обед', 'Ужин']:
            if meals[category]:
                random.shuffle(meals[category])  # Перемешиваем блюда
                for meal in meals[category]:
                    if total_calories + meal[2] <= target_calories:
                        selected_meals.append((category, meal[1], meal[2]))
                        total_calories += meal[2]
                        if category == 'Обед' and len([m for m in selected_meals if m[0] == 'Обед']) < 2:
                            continue  # 2 штуки на обед
                        break

        remaining_calories = target_calories - total_calories
        if remaining_calories > 0:   
            all_meals = []
            for category in meals.keys():
                all_meals.extend(meals[category])

            available_meals = [meal for meal in all_meals if meal[2] <= remaining_calories]

            print('1', available_meals)
        
            while remaining_calories > 0 and available_meals:

                random.shuffle(available_meals)
                meal = available_meals.pop() # meal = (id, name, calories)

                if meal[2] <= remaining_calories:
                    selected_meals.append(('Распределите сами', meal[1], meal[2]))
                    total_calories += meal[2]
                    remaining_calories -= meal[2]                 




        # Отображение результатов

        if total_calories == 0:
            self.plan_label = ctk.CTkLabel(self, text="Нет данных для составления плана")
            self.plan_label.pack(pady=20)
        else:
            self.plan_label = ctk.CTkLabel(self, text=f"Примерный план (всего калорий: {total_calories:.0f} из {target_calories})", font=("Arial", 16, "bold"))
            self.plan_label.pack(pady=20)
            
            for category in ['Завтрак', 'Обед', 'Ужин', 'Распределите сами']:
                category_meals = [m for m in selected_meals if m[0] == category]
                if category_meals:
                    # Создаем фрейм для категории с обводкой
                    category_frame = ctk.CTkFrame(
                        self, 
                        border_width=2,  # Толщина обводки
                        border_color="#2CC985",  # Цвет обводки
                        corner_radius=10  # Закругление углов
                    )
                    category_frame.pack(pady=10, padx=20, fill="x")

                    # Заголовок категории
                    category_label = ctk.CTkLabel(
                        category_frame, 
                        text=f"{category}:", 
                        font=("Arial", 14, "bold")
                    )
                    category_label.pack(pady=5, padx=10, anchor="w")

                    # Список блюд
                    for meal in category_meals:
                        meal_label = ctk.CTkLabel(
                            category_frame, 
                            text=f"- {meal[1]} ({meal[2]:.0f} ккал)", 
                            font=("Arial", 12)
                        )
                        meal_label.pack(pady=2, padx=20, anchor="w")
        
        # Кнопка "Назад"
        self.back_btn = ctk.CTkButton(
            self, 
            text="Назад", 
            command=self.show_user_menu,
            fg_color="#2CC985",  # Цвет кнопки
            hover_color="#1E7D5B"  # Цвет кнопки при наведении
        )
        self.back_btn.pack(pady=20)
        
        conn.close()


if __name__ == "__main__":
    app = App()
    app.mainloop()