from utils.schemas import CreatedUpdatedSchema


class PostSchema(CreatedUpdatedSchema):
    id: int
    user_id: int
    text: str
    allow_comments: bool
    is_blocked: bool


class ImageSchema(CreatedUpdatedSchema):
    id: int
    post_id: int
    order: int

class CommentSchema(CreatedUpdatedSchema):
    id: int
    post_id: int
    user_id: int
    text: str
