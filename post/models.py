from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    class Meta:
        db_table = "post"

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=250, null=False)
    postdate = models.DateTimeField(null=False)
    # 从post查作者，从post查内容
    author = models.ForeignKey(User,
                               on_delete=models.PROTECT)  # 迁移生成author_id字段 # self.content可以访问Content实例，其内容是self.content.content


    def __repr__(self):
        return "<Post {} {} {}>".format(
            self.id, self.title, self.author_id
        )


    __str__ = __repr__


class Content(models.Model):
    class Meta:
        db_table = "content"
    # 一对一，这边会有一个外键post_id引用post.id

    post = models.OneToOneField(Post, on_delete=models.PROTECT, primary_key=True)  # 如 果没有主键，会自动创建一个自增id主键
    content = models.TextField(null=False)

    def __repr__(self):
        return "<Content {} {}>".format(self.post_id, self.content[:20])

    __str__ = __repr__