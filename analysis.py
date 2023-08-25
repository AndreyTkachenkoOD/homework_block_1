import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind, ttest_rel

def load_data(file):
    if file is not None:
        try:
            data = pd.read_csv(file)
            st.success("Датасет успешно загружен")
            return data
        except FileNotFoundError:
            st.error("Файл не найден")
    else:
        st.warning("Файл не был выбран")

def display_data(data):
    st.write("Содержимое CSV файла:")
    st.dataframe(data)

def plot_distribution(data, variable, text_size, image_size):
    if data[variable].dtype == 'object':
        plt.figure(figsize=image_size)
        sns.countplot(data=data, x=variable)
        plt.title(f'Распределение переменной {variable}', fontsize=text_size)
        plt.xticks(rotation=45, fontsize=text_size)
        plt.yticks(fontsize=text_size)
        st.pyplot()
    else:
        plt.figure(figsize=image_size)
        sns.histplot(data=data, x=variable, kde=True)
        plt.title(f'Распределение переменной {variable}', fontsize=text_size)
        plt.xticks(fontsize=text_size)
        plt.yticks(fontsize=text_size)
        st.pyplot()

        plt.figure(figsize=image_size)
        plt.pie(data[variable].value_counts(), labels=data[variable].unique(), autopct='%1.1f%%')
        plt.title(f'Доля каждой категории в переменной {variable}', fontsize=text_size)
        st.pyplot()

def hypothesis_test(data, variable1, variable2, test):
    st.write(f"Проводим тест гипотезы: {test}")

    if test == "t-тест для независимых выборок":
        result = ttest_ind(data[variable1], data[variable2])
    elif test == "t-тест для зависимых выборок":
        result = ttest_rel(data[variable1], data[variable2])

    st.write("Результаты теста:")
    st.write("Статистика:", result.statistic)
    st.write("Уровень значимости:", result.pvalue)

def main():
    st.title("Проект по анализу данных")
    file = st.file_uploader("Выберите датасет (csv)", type=['csv'])
    data = load_data(file)

    if data is not None:
        display_data(data)

        variable1 = st.selectbox("Выберите первую переменную", options=data.columns)
        variable2 = st.selectbox("Выберите вторую переменную", options=data.columns)

        
        text_size = st.slider("Выберите размер текста", min_value=4, max_value=20, value=12)
        image_size = st.slider("Выберите размер изображения", min_value=5, max_value=35, value=13)
        plot_distribution(data, variable1, text_size, (image_size, image_size))
        plot_distribution(data, variable2, text_size, (image_size, image_size))

        
        test = st.selectbox("Выберите алгоритм теста гипотез", options=["t-тест для независимых выборок", "t-тест для зависимых выборок"])

        
        hypothesis_test(data, variable1, variable2, test)

if __name__ == "__main__":
    main()