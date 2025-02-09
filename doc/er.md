``` mermaid
---
title: ER Диаграмма 
---
erDiagram

    Content-Wall {
        int wall_id "Идентификатор стены"
        int user_id "Идентификатор пользователя"
        int last_post_id "Идентификатор последнего поста"
    }

    Content-Post {
        int post_id "Идентификатор поста"
        int user_id "Идентификатор пользователя"
        int prev_id "Идентификатор предыдущего поста (если есть)"
        int parent_id "Идентификатор родительского поста (если есть)"
        int topic_id "Идентификатор топика с комментариями"
        string content "Текст поста"
    }

    Content-Comment-Topic {
        int topic_id "Идентификатор топика"
        int last_comment_id "Идентификатор последнего комментария"
    }

    Content-Comment {
        int comment_id "Идентификатор комментария"
        int post_id "Идентификатор поста"
        int user_id "Идентификатор автора"
        int prev_id "Идентификатор предыдущего комментария (если есть)"
        int parent_id "Идентификатор родительского комментария (если есть)"
        string content "Текст комментария"
    }

    Content-Like {
        int post_id "Идентификатор поста"
        int user_id "Идентификатор пользователя"
    }

    Content-Wall ||--|| Content-Post : "Один к одному"
    Content-Post ||--|| Content-Comment-Topic : "Один к одному"
    Content-Comment-Topic ||--|| Content-Comment : "Один к одному"
    Content-Post ||--o{ Content-Like : "Один пост к нескольким лайкам"

    Statistics-Like {
        int post_id "Идентификатор поста"
        int count "Количество лайков"
    }

    Statistics-Comment {
        int post_id "Идентификатор поста"
        int count "Количество комментариев"
    }

    Statistics-View {
        int post_id "Идентификатор поста"
        int count "Количество просмотров"
    }

    Statistics-Like ||--|| Content-Post : "Один к одному"
    Statistics-Comment ||--|| Content-Post : "Один к одному"
    Statistics-View ||--|| Content-Post : "Один к одному"

    User-User {
        int user_id "Идентификатор пользователя"
        int roles "Роли пользователя (битовая маска)"
    }

    User-Role {
        int role_id "Идентификатор роли"
        string name "Название роли"
        int role_mask "Битовая маска роли"
    }

    User-Info {
        int user_id "Идентификатор пользователя"
        string name "Имя пользователя"
        string surname "Фамилия пользователя"
        string email "Почта пользователя"
        string password "Пароль пользователя"
    }

    User-User ||--o{ Content-Post : "Один юзер к нескольким постам"
    User-User ||--o{ Content-Comment : "Один юзер к нескольким комментариям"
    User-User ||--o{ Content-Like : "Один юзер к нескольким лайкам"
    User-User |o--o{ User-Role : "Один юзер к нескольким ролям"
    User-User |o--|| User-Info : "Один юзер к одной информации"

```