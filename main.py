from flask import render_template
import connexion
import random
from config import connex_app, app
from valid import gen_token
# Создадим экземпляр приложения
#people're telling that two instances causes stupid crashes
#app = connexion.App(__name__, specification_dir='./')

# Прочитаем файл swagger.yml для настройки конечных точек
connex_app.add_api('swagger2.yml')

random.seed()
# Создадим маршрут URL в нашем приложении для "/"
@connex_app.route('/')
def home():
    """
    Эта функция просто отвечает на URL "localhost:5000/" в браузера

    :return:        подствляет шаблон 'home.html'
    """
    return render_template('home.html')


# Если мы работаем в автономном режиме, запускаем приложение
if __name__ == '__main__':
    app.logger.info(str(gen_token()))

    connex_app.run(host='0.0.0.0', port=8080, debug=True)