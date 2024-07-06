import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users

@pytest.fixture(scope="module")
def setup_database():
    """Фикстура для настройки базы данных перед тестами и её очистки после."""
    # Функция create_db() создает базу данных users.db и инициализирует схему
    create_db()
    yield
    # Очистка после выполнения тестов
    os.remove('users.db')

def test_create_db(setup_database):
    """Тест создания базы данных и таблицы пользователей."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Проверяем, существует ли таблица users
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "Таблица 'users' должна существовать в базе данных."

def test_add_new_user(setup_database):
    """Тест добавления нового пользователя."""
    add_user('testuser', 'testuser@example.com', 'password123')
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Пользователь должен быть добавлен в базу данных."

def test_add_existing_user(setup_database):
    """Тест добавления пользователя с существующим логином."""
    added_first_time = add_user('admin', 'cooladmin@example.com', 'password123123')
    added_second_time = add_user('admin', 'cooladmin1@example.com', 'anotherpassword123')
    assert added_first_time is True, "Пользователь должен быть добавлен при первом добавлении."
    assert added_second_time is False, "Добавление пользователя с существующим логином должно вернуть False."

def test_add_existing_user(setup_database):
    added_first_time = add_user('admin', 'cooladmin@example.com', 'password123123')
    added_second_time = add_user('admin', 'cooladmin1@example.com', 'anotherpassword123')
    assert added_first_time is True, "Пользователь должен быть добавлен при первом добавлении."
    assert added_second_time is False, "Добавление пользователя с существующим логином должно вернуть False."

def test_authenticate_user(setup_database):
    add_user('adminn', 'user@example.com', 'password123')
    authenticated = authenticate_user('adminn', 'password123')
    assert authenticated is True, "Должна быть успешная аутентификация с правильными логином и паролем."

def test_authenticate_nonexistent_user(setup_database):
    authenticated = authenticate_user('nonexistent', 'password123')
    assert authenticated is False, "Аутентификация несуществующего пользователя должна быть неуспешной."

def test_wrong_password(setup_database):
    add_user('exampleuser', 'testmail@example.com', '12345')
    authenticated = authenticate_user('exampleuser', 'wrong')
    assert authenticated is False, "Аутентификация с неправильным паролем должна быть неуспешной."

def test_display_users(setup_database, capsys):
    add_user('testuser1', 'testuser1@example.com', 'password123')
    add_user('testuser2', 'testuser2@example.com', 'password456')

    display_users()

    captured = capsys.readouterr()
    assert "Логин: testuser1, Электронная почта: testuser1@example.com" in captured.out
    assert "Логин: testuser2, Электронная почта: testuser2@example.com" in captured.out

