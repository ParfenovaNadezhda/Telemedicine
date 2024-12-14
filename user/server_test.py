from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

# Хранилище для данных пользователей
users_data = {}

@app.route('/api/user', methods=['POST'])
def receive_user_data():
    """
    Обрабатывает POST-запрос с данными пользователя.
    """
    try:
        # Получаем данные из запроса
        user_data = request.json

        # Проверяем, что данные переданы
        if not user_data:
            return jsonify({"error": "No data provided"}), 400

        # Проверяем, что все необходимые поля присутствуют
        required_fields = ['ip', 'login', 'password', 'data', 'function']
        for field in required_fields:
            if field not in user_data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        # Генерируем уникальные user_id и task_id
        user_id = str(uuid.uuid4())
        task_id = str(uuid.uuid4())

        # Сохраняем данные пользователя
        users_data[user_id] = {
            "task_id": task_id,
            "data": user_data
        }

        # Возвращаем user_id и task_id
        return jsonify({
            "user_id": user_id,
            "task_id": task_id
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/user', methods=['GET'])
def get_user_data():
    """
    Обрабатывает GET-запрос для получения user_id и task_id.
    """
    try:
        # Возвращаем все данные пользователей (для тестирования)
        return jsonify(users_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/master', methods=['POST'])
def receive_master_data():
    """
    Обрабатывает POST-запрос с user_id и task_id от клиента.
    """
    try:
        # Получаем данные из запроса
        master_data = request.json

        # Проверяем, что данные переданы
        if not master_data:
            return jsonify({"error": "No data provided"}), 400

        # Проверяем, что все необходимые поля присутствуют
        required_fields = ['user_id', 'task_id']
        for field in required_fields:
            if field not in master_data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        # Возвращаем успешный статус
        return jsonify({"status": "success", "message": "Data received"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/master', methods=['GET'])
def get_master_status():
    """
    Обрабатывает GET-запрос для получения статуса выполнения задачи.
    """
    try:
        # Возвращаем фиктивный статус (для тестирования)
        return jsonify({
            "status": "completed",
            "task_id": "987e6543-21f0-98d6-c4e3-1234567890ab"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Запуск сервера на локальном хосте
    app.run(host='0.0.0.0', port=5000)
