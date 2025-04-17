Общая информация
1. Веб–сервис "Вишлист".
2. Стек: python>=3.13, django>=5.2, django-minio-storage>=0.5.7, postgres>=17, для фронта использую DTL и django-tailwind>=4.0.1.
2.1. Использую Tailwind CSS v4, поэтому: "The content section from Tailwind CSS v3 has been replaced with the @source directive in Tailwind CSS v4. The @source directive is a new way to specify the source files that Tailwind CSS should scan for class names. It’s placed in the style.css file."
3. Основные модели:
- User - базовая модель джанго;
- ProfileModel - one-to-one к User с доп. полями, пока не особо используется;
- FollowModel - подписка на чужие вишлисты (два поля user и following);
- WishItemModel - элементы вишлиста (поля title, description, link, picture, user (FK), is_private).
4. Регистрация/авторизация:
- регистрация по email (использую базовую модель User, но при регистрации создаю автоматически username=email);
- при авторизации пользователь вводит email, который равен username, пока так.
5. Страницы:
- register.html, login.html, logged_out.html;
- базовые - base.html, footer.html, header.html;
- главная страница (home.html) с общей информацией;
- авторизованному пользователю доступна страница wishlist.html с добавленными элементами;
- боковая панель (вишлист, подписки, настройки, выйти), боковая панель технически это общий side-bar, который для всех юзеров внизу содержит вкладку (контакты);
