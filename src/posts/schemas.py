from common.schemas import CreatedUpdatedSchema


class ImageSchema(CreatedUpdatedSchema):
    id: int
    post_id: int
    order: int


class CommentSchema(CreatedUpdatedSchema):
    id: int
    post_id: int
    user_id: int
    text: str


class PostSchema(CreatedUpdatedSchema):
    id: int
    user_id: int
    text: str
    allow_comments: bool
    is_blocked: bool
    images: list[ImageSchema] | None = None
    comments: list[CommentSchema] | None = None
