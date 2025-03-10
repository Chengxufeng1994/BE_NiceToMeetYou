from app.entities.news import News as NewsEntity
from app.models.news import News


def news_entity_to_model(news_entity: NewsEntity) -> News:
    return News(
        id=news_entity.id,
        title=news_entity.title,
        link=news_entity.link,
        content=news_entity.content,
        published_at=news_entity.published_at,
    )


def news_model_to_entity(news_model: News) -> NewsEntity:
    return NewsEntity(
        id=news_model.id,
        title=news_model.title,
        link=news_model.link,
        summary=news_model.content,
        published_at=news_model.published_at,
    )
