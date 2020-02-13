from django.db import models
from taggit.managers import TaggableManager
from django.conf import settings
from django.urls import reverse_lazy
from django.db import models


class Thread(models.Model):
    title = models.CharField('Título', max_length=100)
    slug = models.SlugField('Identificador', max_length=100, unique=True)
    body = models.TextField('Mensagem',)
    views = models.IntegerField('Visualizações', blank=True, default=0)
    answers = models.IntegerField('Respostas', blank=True, default=0)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               verbose_name='Autor', related_name='threads',
                               on_delete=models.CASCADE
                               )
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    modified = models.DateTimeField("Modificado em ", auto_now=True)
    tags = TaggableManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('thread', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Tópico'
        verbose_name_plural = 'Tópicos'
        ordering = ['-modified']


class Reply(models.Model):
    thread = models.ForeignKey(
        Thread, verbose_name='Tópico',
        related_name='replies',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    modified = models.DateTimeField("Modificado em ", auto_now=True)
    reply = models.TextField('Resposta')
    correct = models.BooleanField('Correta?', blank=True, default=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Autor', related_name='replies',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.reply[-100]

    class Meta:
        verbose_name = 'Resposta'
        verbose_name_plural = 'Respostas'
        ordering = ['-correct', 'created_at']


def post_save_reply(created, instance, **kwargs):
    instance.Thread.answers = instance.thread.replies.count()
    instance.thread.save()
    if instance.correct:
        instance.thread.replies.exclude(pk=instance.pk).update(
            correct=False
        )


def post_delete_reply(instance, **kwargs):
    instance.Thread.answers = instance.thread.replies.count()
    instance.thread.save()


models.signals.post_save.connect(
    post_save_reply, sender=Reply,
    dispatch_uid='post_save_reply'
)

models.signals.post_delete.connect(
    post_delete_reply, sender=Reply,
    dispatch_uid='post_delete_reply'
)
